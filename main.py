from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Ellipse, Line, Color
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.behaviors import DragBehavior
from kivy.uix.vkeyboard import VKeyboard
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils import log, pdf_generator
from measure import get_measure
from db_functions import save_measure_in_db, save_draw_point_in_db
from models import Base, Point, Bssid, Channel, Measure, Ssid, Security
from kivy.core.window import Window
from kivy.config import Config

# relative path with triple dash, full path with cuadruple dash
#db_path = 'sqlite:///heatmap.db'
db_path = 'sqlite:///'

class myApplication(Widget):
    def __init__(self, **kwargs):
        super(myApplication, self).__init__(**kwargs)
        #Window.fullscreen = True

        self.engine = create_engine(db_path, echo=True)
        self.engine.execute('PRAGMA foreign_keys = ON')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        #self.my_vkeyboard = VKeyboard()
        self.point_list_figure = []
        self.mode = 'first_step'
        log('heatmap','INFO',"First step: draw area.")

    def on_touch_down(self, touch):
        if self.mode is 'second_step' and touch.x < self.width / 1.25 and touch.y > self.height / 4:
            print(self.point_list_figure) 
        
        elif self.mode == 'third_step' and touch.is_double_tap:
            with self.canvas:
                Color(1, 0, 1) 
                Ellipse(pos=(touch.x, touch.y), size=(15,15))
                log('heatmap','INFO',"New measure.")
                measure_list = get_measure(model='MacOS')
                save_measure_in_db(session=self.session, data=measure_list, point=touch)
        else:
            return super(myApplication, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        return super(myApplication, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.mode is 'first_step' and touch.x < self.width / 1.25:
            with self.canvas:
                Color(0,0,0)
                point_list = [touch.x, touch.y]
                print(point_list)
                self.point_list_figure.append(point_list)
                Line(points=self.point_list_figure, width = 5)
                save_draw_point_in_db(self.session, touch)
        else:
            return super(myApplication, self).on_touch_down(touch)

    def check_button(self):
        if self.mode is 'first_step':
            self.mode = 'second_step'
            log('heatmap','INFO',"Second step: Select scale.")
            #self.add_widget(self.my_vkeyboard)
            
        elif self.mode is 'second_step':
            self.mode = 'third_step'
            log('heatmap','INFO',"The scale is: {}.".format(self.scale))
            log('heatmap','INFO',"Third step: measure wifi signal.")
            #self.remove_widget(self.my_vkeyboard)
        elif self.mode is 'third_step':
            pdf_generator(session=self.session)
            self.mode = 'fourth_step'
            log('heatmap','INFO',"Fourth step: generating PDF report.")
        elif self.mode is 'fourth_step':
            log('heatmap','INFO',"Closing application - Bye!")
            self.session.close()
            App.get_running_app().stop()

    def search_location(self):
        self.scale = self.ids.input_scale.text

class heatmap(App):
    def build(self):
        log('heatmap','INFO', "Starting application!")
        return myApplication()

if __name__ == "__main__":
    #Config.set('graphics', 'fullscreen', 'auto')
    #Config.set('graphics', 'window_state', 'maximized')
    #Config.write()
    heatmap().run()
