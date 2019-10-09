from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Ellipse, Line, Color
from utils import log


class myApplication(Widget):
    def __init__(self, **kwargs):
        super(myApplication, self).__init__(**kwargs)
        self.point_list_figure = []
        self.mode = 'first_step'
        log('heatmap','INFO',"First step: draw area.")

    def on_touch_down(self, touch):
        if self.mode is 'first_step'  and touch.x < self.width / 1.25:
            self.line_start_point_x, self.line_start_point_y = touch.pos
        # elif self.mode is 'second_step':
            # I should select one line from the draw and get its initial and final point to set scale
            # if inputlabel opened:
            # I should open virtual keyboard here.
        elif self.mode == 'third_step' and touch.is_double_tap:
            with self.canvas:
                Color(1, 0, 1) 
                Ellipse(pos=(touch.x, touch.y), size=(15,15))
                log('heatmap','INFO',"New measure.")
                # Measure wifi signal here and store in database.
        else:
            return super(myApplication, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        return super(myApplication, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.mode is 'first_step' and touch.x < self.width / 1.25:
            with self.canvas:
                Color(0,0,0)
                point_list = [self.line_start_point_x, self.line_start_point_y, touch.x, touch.y]
                self.point_list_figure.append(point_list)
                Line(points=self.point_list_figure, width = 5)
        else:
            return super(myApplication, self).on_touch_down(touch)

    def check_button(self):
        if self.mode is 'first_step':
            self.mode = 'second_step'
            log('heatmap','INFO',"Second step: Select scale.")
        elif self.mode is 'second_step':
            self.mode = 'third_step'
            self.scale = self.ids.input_scale.text
            log('heatmap','INFO',"The scale is: {}.".format(self.scale))
            log('heatmap','INFO',"Third step: measure wifi signal.")
        elif self.mode is 'third_step':
            self.mode = 'fourth_step'
            # Get measures from database here and load heatmap results.
            log('heatmap','INFO',"Fourth step: printing results.")
        elif self.mode is 'fourth_step':
            log('heatmap','INFO',"Closing application - Bye!")
            App.get_running_app().stop()

class heatmap(App):
    def build(self):
        log('heatmap','INFO', "Starting application!")
        return myApplication()

if __name__ == "__main__":
    heatmap().run()