from kivymd.app import MDApp
from kivy.lang.builder import Builder
from curvelayout import CurveLayout, FrontLayout, BackLayout
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from background import BackGround
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.graphics import Rectangle
from backfloat import BackFloat
from frontfloat import FrontFloat

kv = """


MainLayout:
    front:front
    back: back
    color: app.theme_cls.primary_color

    FrontFloat:
        id: front

    BackFloat:
        id: back
        _root: root


"""


class MainLayout(CurveLayout):
    front = ObjectProperty()
    back = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_left_start(self, *args):
        self.back.reset_chevron()
        self.front.hide_curve()
        self.front.hide_title()
        self.front.hide_taxi()

    def on_left_second_start(self, *args):
        self.back.show_car()
        self.back.show_title()
        self.back.show_description()

    def on_right_start(self, *args):
        self.back.run_chevron()
        self.front.show_curve()
        self.front.show_taxi()

    def on_right_second_start(self, *args):
        self.back.hide_car()
        self.back.hide_title()
        self.back.hide_description()
        self.front.show_title()

    def on_right_finish(self, *args):
        self.back.reset_chevron()

    # def on_left_second_start(self, *args):

    def on_reset_left(self, *args):
        self.back.reset_chevron()


class MeshTestApp(MDApp):
    def build(self):
        return Builder.load_string(kv)


if __name__ == "__main__":
    MeshTestApp().run()