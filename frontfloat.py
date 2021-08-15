from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from curvelayout import FrontLayout
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import dp
from label import MyLabel #NOQA
import numpy as np
from bezier import Bezier as Bz

Builder.load_string(
    """
<FrontFloat>
    title_label:title_label

    canvas:
        Color:
            rgba: [255/255,0/255,85/255,1]
        Mesh:
            mode: "triangle_fan"
            vertices: root.vertices
            indices: root.indices

        Color:
            rgba: 1,1,1,1
        Rectangle:
            pos: root.taxi_x - dp(150) , dp(150)
            size: dp(300), dp(300)
            source: "assets/taxi.png"

    MyLabel:
        text: "What is Lorem Ipsum?"
        id: title_label
        font_type: "bold"
        y: dp(100)
        x: dp(100)
        size_hint_x: None
        width: dp(300)
        font_size: dp(20)
        opacity: 0


    """
)


class FrontFloat(FrontLayout):
    vertices = ListProperty()
    indices = ListProperty()
    curve_pos = ListProperty()
    start_pos = ListProperty([0, 0])
    end_pos = ListProperty([0, 0])
    title_label = ObjectProperty()
    taxi_x = NumericProperty("-500dp")

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self._update)

    def on_curve_pos(self, *args):
        self.update_mesh(self.start_pos, self.end_pos, self.curve_pos)

    def _update(self, *args):
        self.update_mesh([0, 0], [0, 200], [0, self.height])

    def show_curve(self):
        self.curve_pos = [0, self.height / 2]
        anim = Animation(
            start_pos=[dp(2000), 0],
            end_pos=[dp(1000), self.height],
            curve_pos=[self.width / 2, self.height / 2],
            t="out_quad",
            d=0.4,
        )
        anim.start(self)

    def hide_curve(self):
        anim = Animation(
            start_pos=[dp(-200), 0],
            end_pos=[dp(-200), self.height],
            curve_pos=[dp(200), self.height / 2],
            t="out_quad",
            d=0.3,
        )
        anim += Animation(curve_pos=[0, self.height / 2], t="out_quad", d=0.2)
        anim.start(self)

    def update_mesh(self, start, end, pos):
        res = []
        points_1 = [[-dp(1000), -dp(1000)], start, [pos[0] / 2, pos[1] / 2], pos]
        points_2 = [
            pos,
            [pos[0] / 2, (end[1] + pos[1]) / 2],
            end,
            [-dp(1000), end[1] + dp(1000)],
        ]
        res.extend(points_1)
        res.extend(points_2)

        t_points = np.arange(0, 1, 0.02)
        points1 = np.array(res)
        curve = Bz.Curve(t_points, points1)

        # curve = sigmoid(res)

        vertices = []
        indices = []
        _i = 0
        for x, y in curve:
            vertices.extend([x, y, 0, 0])
            indices.append(_i)
            _i += 1
        self.indices = indices
        self.vertices = vertices

    def show_title(self):
        anim = Animation(opacity=1, t="out_quad", d=0.3, center_x=self.width / 2)
        anim.start(self.title_label)

    def hide_title(self):
        anim = Animation(opacity=0, t="out_quad", d=0.3, right=0)
        anim.start(self.title_label)

    def show_taxi(self):
        anim = Animation(
            taxi_x=self.width / 2,
            t="out_quad",
            d=0.3,
        )
        anim.start(self)

    def hide_taxi(self):
        anim = Animation(
            taxi_x=dp(-500),
            t="out_quad",
            d=0.3,
        )
        anim.start(self)
