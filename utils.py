import pyscreenshot as ImageGrab
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import csv
import os
import shutil
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Image
from reportlab.lib.units import mm, inch
from reportlab.lib.styles import getSampleStyleSheet
from sqlalchemy import distinct
from models import Ssid, Bssid, Measure, Security, Channel, Point, Draw_Point
from PIL import Image as Img


def log(application, log_level, msg):
    print("[{}] - [{}] - {}".format(application, log_level, msg))


def pdf_generator(session):
    
    if os.path.exists('./res'):
        shutil.rmtree('./res', ignore_errors=True)
    os.makedirs('./res')
    
    pdf_buffer = []
    my_pdf = SimpleDocTemplate('heatmap_report.pdf')
    pdf_style_sheet = getSampleStyleSheet()

    paragraph = Paragraph('Reporte de medición WiFi<br /><br /><br />', pdf_style_sheet['Heading1'])
    pdf_buffer.append(paragraph)
    paragraph = Paragraph('Proyecto de Base de Datos 2019 - Heatmap<br /><br />', pdf_style_sheet['Heading3'])
    pdf_buffer.append(paragraph)
    paragraph = Paragraph('Alumno: Juan Ignacio Battaglino - juanibattaglino@gmail.com<br /><br />', pdf_style_sheet['Heading3'])
    pdf_buffer.append(paragraph)
    paragraph = Paragraph('Profesores: Sergio Kaszczyszyn - Roberto Gomez<br /><br />', pdf_style_sheet['Heading3'])
    pdf_buffer.append(paragraph)
    pdf_buffer.append(PageBreak())

    take_screenshot(session)
    paragraph = Paragraph('Site analysis for floor plan draw:<br /><br /><br />', pdf_style_sheet['Heading1'])
    pdf_buffer.append(paragraph)
    pdf_buffer.append(Image('./res/my_floor_diagram.png', width=4*200, height=2*200, kind='proportional'))
    pdf_buffer.append(PageBreak())

    for ssid in session.query(Ssid).filter(Ssid.id==Measure.ssid_id).order_by(Ssid.ssid_value).all():
        paragraph_measure = Paragraph('SSID: {}'.format(ssid), pdf_style_sheet['Heading2'])
        pdf_buffer.append(paragraph_measure)

        #Security types:
        #SELECT DISTINCT ssid_value, security_type FROM measure INNER JOIN ssid ON measure.ssid_id = ssid.id INNER JOIN security ON measure.security_id = security.id ORDER BY ssid_value ASC;
        query = session.query(Security, Measure, Ssid).join(Ssid, Ssid.id==Measure.ssid_id).filter(Ssid.ssid_value==str(ssid)).join(Security, Security.id==Measure.security_id).first()
        paragraph_sec = Paragraph('Security type: {}'.format(query[0]), pdf_style_sheet['Heading2'])
        
        #Bssids:
        #SELECT DISTINCT ssid_value, bssid_value FROM measure INNER JOIN ssid ON measure.ssid_id = ssid.id INNER JOIN bssid ON measure.bssid_id = bssid.id ORDER BY ssid_value ASC;
        query = session.query(Bssid, Measure, Ssid).join(Ssid, Ssid.id==Measure.ssid_id).filter(Ssid.ssid_value==str(ssid)).join(Bssid, Bssid.id==Measure.bssid_id).all()
        bssid_list = remove_repeated_values(query)
        paragraph_bssid = Paragraph('Bssids detected: {}'.format(bssid_list), pdf_style_sheet['Heading2'])
        
        #Channels:
        #SELECT DISTINCT ssid_value, channel_number FROM measure INNER JOIN ssid ON measure.ssid_id = ssid.id INNER JOIN channel ON measure.channel_id = channel.id ORDER BY ssid_value ASC;
        query = session.query(Channel, Measure, Ssid).join(Ssid, Ssid.id==Measure.ssid_id).filter(Ssid.ssid_value==str(ssid)).join(Channel, Channel.id==Measure.channel_id).all()
        channel_list = remove_repeated_values(query)
        paragraph_channel = Paragraph('Channels detected: {}<br /><br /><br /><br />'.format(channel_list), pdf_style_sheet['Heading2'])
        
        pdf_buffer.append(paragraph_sec)
        pdf_buffer.append(paragraph_bssid)
        pdf_buffer.append(paragraph_channel)

        #rssi:
        #SELECT DISTINCT ssid_value, x_location, y_location, rssi FROM measure INNER JOIN ssid ON measure.ssid_id = ssid.id INNER JOIN point ON measure.point_id = point.id ORDER BY ssid_value ASC;
        query = session.query(Point.id, Point.x_location, Point.y_location, Measure, Ssid).join(Ssid, Ssid.id==Measure.ssid_id).filter(Ssid.ssid_value==str(ssid)).join(Point, Point.id==Measure.point_id).all()
        query.insert(0, ['id','x_position', 'y_position', 'rssi', 'ssid'])
        plot_heatmap(query)

        plt.tight_layout()
        plt.savefig('./res/{}-measure.png'.format(ssid))
        pdf_buffer.append(Image('./res/{}-measure.png'.format(ssid),width=3*200, height=1.5*200, kind='proportional'))
        pdf_buffer.append(PageBreak())

    my_pdf.build(pdf_buffer, onFirstPage=add_page_number, onLaterPages=add_page_number)


def add_page_number(canvas, doc):
     canvas.saveState()
     canvas.setFont('Times-Roman', 10)
     page_number_text = "%d" % (doc.page)
     canvas.drawCentredString(0.75 * inch, 0.75 * inch, page_number_text)
     canvas.restoreState()


def remove_repeated_values(query_list):
    my_list = []
    for my_query in query_list:
        my_list.append(my_query[0])
        my_set = set(my_list)
        my_set.union(my_set)
    return list(my_set)


def define_screen_window_size(session):
    query = session.query(Draw_Point.x_location).order_by(Draw_Point.x_location).all()
    x_min, x_max = int(query[0][0]), int(query[-1][0])
    query = session.query(Draw_Point.y_location).order_by(Draw_Point.y_location).all()
    y_min, y_max = int(query[0][0]), int(query[-1][0])
    #return (x_min, 1800-y_max, x_max-1130, 1800-y_min)
    return (x_min-120, y_min-400, x_max-1000, 800)


def take_screenshot(session):
    #im = ImageGrab.grab()
    my_screen = define_screen_window_size(session)
    #print(my_screen)
    im = ImageGrab.grab(bbox=my_screen) # X1,Y1,X2,Y2
    im.save('./res/my_floor_diagram.png')
    #im_resized = Img.open('./res/my_floor_diagram.png')
    #im_resized.save(im_resized.resize(500,420))
    #im.show()


def plot_heatmap(query):
    query_list = []
    for elem in query:
        query_list.append(list(elem))
    
    plt.figure()
    outfile = open('./res/mycsv.csv', 'w')
    outcsv = csv.writer(outfile)
    outcsv.writerows(query_list)
    outfile.close()
    df1 = pd.read_csv('./res/mycsv.csv', index_col=0)
    #df2 = df1[['x_position','y_position','rssi']]
    heatmap_data = pd.pivot_table(df1, values='rssi', columns='x_position', index=['y_position'])
    sns.heatmap(heatmap_data, cmap="RdYlBu_r", annot=True, vmin=-90, vmax=-30)