from kivymd.app import MDApp
from kivy.lang.builder import Builder
from curvelayout import CurveLayout, FrontLayout, BackLayout
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from background import BackGround
from label import MyLabel
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.graphics.fbo import Fbo
from kivy.graphics import Rectangle


kv = """
<BackFloat>
    title_label:title_label
    description_label:description_label

    BackGround:

        canvas:
            Color:
                rgba: 1,1,1,1
            PushMatrix
            Rotate:
                origin: [root.car_pos[0]+dp(125), root.car_pos[1]+60]
                angle: root.car_angle

            Rectangle:
                pos: root.car_pos
                size: dp(250), dp(125)
                source: "assets/car.png"
            PopMatrix

            Rectangle:
                pos: root.pos
                size: dp(150), dp(300)
                source: "assets/man.png"

            Color:
                rgba: app.theme_cls.primary_color
            Rectangle:
                pos: root.chevron_pos if root.chevron_pos else [dp(5), root.height/2]
                size: dp(25), dp(50)
                source: "assets/chevron.png"
    MyLabel:
        id: title_label
        pos_hint: {"center_x" :.5}
        text: "What is Lorem Ipsum?"
        font_size: dp(30)
        y: self.height
        opacity: 0

    MyLabel:
        id: description_label
        pos_hint: {"center_x" :.5}
        text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry"
        font_size: dp(20)
        top: 0
        opacity: 0


<FrontFloat>


MainLayout:
    front:front
    back: back 

    FrontFloat:
        id: front

    BackFloat:
        id: back


"""


class FrontFloat(FrontLayout):
    pass


class MainLayout(CurveLayout):
    front = ObjectProperty()
    back = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_left_second_start(self, *args):
        self.back.show_car()
        self.back.show_title()
        self.back.show_description()

    def on_right_start(self, *args):
        self.back.run_chevron()

    def on_left_start(self, *args):
        self.back.reset_chevron()

    def on_reset_left(self, *args):
        self.back.reset_chevron()

    def on_right_second_start(self, *args):
        self.back.hide_car()
        self.back.hide_title()
        self.back.hide_description()


class BackFloat(BackLayout):
    car_pos = ListProperty([2000, 0])
    car_angle = NumericProperty(0)
    description_label = ObjectProperty()
    title_label = ObjectProperty()
    chevron_pos = ListProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self._update)
        self.shake_car()

    def _update(self, *args):
        self.show_title()
        self.show_description()

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        self.chevron_pos = [touch.x, touch.y - dp(25)]

    def reset_chevron(self):
        anim = Animation(chevron_pos=[dp(5), self.height / 2], t="out_quad", d=0.5)
        anim.start(self)

    def run_chevron(self):
        anim = Animation(chevron_pos=[self.width, self.height / 2], t="out_quad", d=0.5)
        anim.start(self)

    def show_car(self, *args):
        anim = Animation(car_pos=[self.width - dp(300), dp(150)], t="out_quad")
        anim.start(self)

    def hide_car(self, *args):
        anim = Animation(car_pos=[self.width, 0], t="out_quad")
        anim.start(self)

    def shake_car(self, *args):
        anim = Animation(car_angle=2, d=0.1, t="out_quad")
        anim += Animation(car_angle=-2, d=0.1, t="out_quad")
        anim.repeat = True
        anim.start(self)

    def show_title(self, *args):
        anim = Animation(y=dp(200), d=0.5, t="out_quad", opacity=1)
        anim.start(self.title_label)

    def hide_title(self, *args):
        anim = Animation(y=self.height, d=0.5, t="out_quad", opacity=0)
        anim.start(self.title_label)

    def show_description(self, *args):
        anim = Animation(y=dp(150), d=0.5, t="out_quad", opacity=1)
        anim.start(self.description_label)

    def hide_description(self, *args):
        anim = Animation(top=0, d=0.5, t="out_quad", opacity=0)
        anim.start(self.description_label)


class MeshTestApp(MDApp):
    def build(self):
        return Builder.load_string(kv)


if __name__ == "__main__":
    MeshTestApp().run()