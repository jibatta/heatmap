from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.input.shape import ShapeRect
from kivy.graphics import Ellipse, Line, Color
from utils import log

class MyButton(Button):
    def on_touch_up(self, touch):
        super(MyButton, self).on_touch_up(touch)
        if self.collide_point(*touch.pos):
            self._do_release()
            self.dispatch('on_release')

class myApplication(Widget):
    def __init__(self, **kwargs):
        super(myApplication, self).__init__(**kwargs)
        self.point_list_figure = []
        self.mode = 'first_step'
        log('heatmap','INFO',"First step.")

            
    def on_touch_down(self, touch):
        if self.mode is 'first_step'  and touch.x < self.width / 1.25:
            self.line_start_point_x, self.line_start_point_y = touch.pos
        elif self.mode is 'second_step':
            print("Second step.")
        elif self.mode == 'third_step' and touch.is_double_tap:
            with self.canvas:
                Color(1, 0, 1) 
                Ellipse(pos=(touch.x, touch.y), size=(15,15))
                log('heatmap','INFO',"New measure.")
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

    def btn_clk(self):
        if self.mode is 'first_step':
            self.mode = 'second_step'
            log('heatmap','INFO',"Second step.")
        elif self.mode is 'second_step':
            self.mode = 'third_step'
            log('heatmap','INFO',"Third step.")
        elif self.mode is 'third_step':
            self.mode = 'fourth_step'
            log('heatmap','INFO',"Fourth step.")
        elif self.mode is 'fourth_step':
            log('heatmap','INFO',"Application finished!")

class heatmap(App):
    def build(self):
        log('heatmap','INFO', "Starting application!")
        return myApplication()

if __name__ == "__main__":
    heatmap().run()