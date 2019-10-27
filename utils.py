from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.units import mm, inch
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from models import Ssid, Bssid, Measure, Security, Channel, Point

def log(application, log_level, msg):
    print("[{}] - [{}] - {}".format(application, log_level, msg))

def pdf_generator(session):
    # This should be the results of the measures - Hardcoded temporarily.
    ssid_list = ['UTN BA']

    pdf_buffer = []
    my_pdf = SimpleDocTemplate('heatmap_report.pdf')

    pdf_style_sheet = getSampleStyleSheet()

    paragraph_1 = Paragraph('Reporte de medición WiFi<br /><br /><br />', pdf_style_sheet['Heading1'])
    paragraph_2 = Paragraph('Proyecto de Base de Datos 2019 - Heatmap<br /><br />', pdf_style_sheet['Heading3'])
    paragraph_3 = Paragraph('Alumno: Juan Ignacio Battaglino - juanibattaglino@gmail.com<br /><br />', pdf_style_sheet['Heading3'])
    paragraph_4 = Paragraph('Profesores: Sergio Kaszczyszyn - Roberto Gomez<br /><br />', pdf_style_sheet['Heading3'])
    
    pdf_buffer.append(paragraph_1)
    pdf_buffer.append(paragraph_2)
    pdf_buffer.append(paragraph_3)
    pdf_buffer.append(paragraph_4)
    pdf_buffer.append(PageBreak())

    # This would be inside a for loop.


    for ssid in session.query(Ssid).filter(Ssid.id == Measure.ssid_id).all():
        paragraph_measure = Paragraph('SSID: {}'.format(ssid), pdf_style_sheet['Heading2'])
        pdf_buffer.append(paragraph_measure)
        # I would insert here the image.
        # pdf_buffer.append(ssid + '.png')
        pdf_buffer.append(PageBreak())
    # Loop would end here.

    my_pdf.build(pdf_buffer, onFirstPage=add_page_number, onLaterPages=add_page_number)

def add_page_number(canvas, doc):
     canvas.saveState()
     canvas.setFont('Times-Roman', 10)
     page_number_text = "%d" % (doc.page)
     canvas.drawCentredString(0.75 * inch, 0.75 * inch, page_number_text)
     canvas.restoreState()

if __name__ == "__main__":
    pdf_generator()