from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Ellipse, Line, Color
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.behaviors import DragBehavior
from kivy.uix.vkeyboard import VKeyboard
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from utils import log, pdf_generator
from measure import get_measure
from db_functions import save_measure
from db_class import Base, Point, Bssid, Channel, Measure, Ssid, Security

# relative path with triple dash, full path with cuadruple dash
db_path = 'sqlite:///heatmap.db'

class myApplication(Widget):
    def __init__(self, **kwargs):
        super(myApplication, self).__init__(**kwargs)

        self.engine = create_engine(db_path, echo=True)
        self.engine.execute('PRAGMA foreign_keys = ON')
        Base.metadata.create_all(self.engine)

        self.my_vkeyboard = VKeyboard()
        self.point_list_figure = []
        self.mode = 'first_step'
        log('heatmap','INFO',"First step: draw area.")

    def on_touch_down(self, touch):
        if self.mode is 'second_step' and touch.x < self.width / 1.25 and touch.y > self.height / 4:
            print(self.point_list_figure) 
            # I should select one line from the draw and get its initial and final point to set scale
        elif self.mode == 'third_step' and touch.is_double_tap:
            with self.canvas:
                Color(1, 0, 1) 
                Ellipse(pos=(touch.x, touch.y), size=(15,15))
                log('heatmap','INFO',"New measure.")
                measure_list = get_measure(model='MacOS')
                save_measure(db=self.engine, data=measure_list)
        else:
            return super(myApplication, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        return super(myApplication, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.mode is 'first_step' and touch.x < self.width / 1.25:
            with self.canvas:
                Color(0,0,0)
                point_list = [touch.x, touch.y]
                self.point_list_figure.append(point_list)
                Line(points=self.point_list_figure, width = 5)
        else:
            return super(myApplication, self).on_touch_down(touch)

    def check_button(self):
        if self.mode is 'first_step':
            self.mode = 'second_step'
            log('heatmap','INFO',"Second step: Select scale.")
            self.add_widget(self.my_vkeyboard)
            
        elif self.mode is 'second_step':
            self.mode = 'third_step'
            log('heatmap','INFO',"The scale is: {}.".format(self.scale))
            log('heatmap','INFO',"Third step: measure wifi signal.")
            self.remove_widget(self.my_vkeyboard)
        elif self.mode is 'third_step':
            pdf_generator()
            self.mode = 'fourth_step'
            log('heatmap','INFO',"Fourth step: generating PDF report.")
        elif self.mode is 'fourth_step':
            log('heatmap','INFO',"Closing application - Bye!")
            App.get_running_app().stop()

    def search_location(self):
        self.scale = self.ids.input_scale.text

class heatmap(App):
    def build(self):
        log('heatmap','INFO', "Starting application!")
        return myApplication()

if __name__ == "__main__":
    heatmap().run()