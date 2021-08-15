from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from curvelayout import BackLayout
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import dp
from label import MyLabel  # NOQA
from background import BackGround  # NOQA

Builder.load_string(
    """
<BackFloat>
    title_label:title_label
    description_label:description_label

    BackGround:

        canvas:
            Color:
                rgba: 1, 1, 1, 1
            PushMatrix
            Rotate:
                origin: [root.car_pos[0] + dp(125), root.car_pos[1] + 60]
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
        pos_hint: {"center_x": .5}
        text: "What is Lorem Ipsum?"
        font_size: dp(30)
        y: self.height
        opacity: 0
        font_type: "bold"

    MyLabel:
        id: description_label
        pos_hint: {"center_x": .5}
        text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry"
        font_size: dp(20)
        top: 0
        opacity: 0

    """
)


class BackFloat(BackLayout):
    car_pos = ListProperty([2000, 0])
    car_angle = NumericProperty(0)
    description_label = ObjectProperty()
    title_label = ObjectProperty()
    chevron_pos = ListProperty()
    _root = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self._update, 2)
        self.shake_car()

    def _update(self, *args):
        self.show_title()
        self.show_description()
        self.show_car()

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        if self._root._state == "left":
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
