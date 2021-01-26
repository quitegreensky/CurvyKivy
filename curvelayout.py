import numpy as np
from bezier import Bezier as Bz
from kivymd.theming import ThemableBehavior
from kivy.lang.builder import Builder
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation

Builder.load_string(
    """

<CurveLayout>:

    BoxLayout:
        id: backlayout

    BoxLayout:
        canvas:
            Color:
                rgba: root.color if root.color else root.theme_cls.primary_color
            Mesh:
                mode: "triangle_fan"
                vertices: root.vertices
                indices: root.indices

    BoxLayout:
        id: frontlayout

    """
)


class FrontLayout(BoxLayout):
    pass


class BackLayout(BoxLayout):
    pass


class CurveLayout(ThemableBehavior, FloatLayout, EventDispatcher):
    drag_distance = NumericProperty("100dp")
    curve_pos = ListProperty([0, 0])
    start_pos = ListProperty([0, 0])
    end_pos = ListProperty([0, 1000])
    color = ListProperty()

    indices = ListProperty()
    vertices = ListProperty()

    _state = "left"

    def __init__(self, **kw):
        super().__init__(**kw)
        self.register_event_type("on_right_finish")
        self.register_event_type("on_right_start")
        self.register_event_type("on_right_second_start")

        self.register_event_type("on_left_finish")
        self.register_event_type("on_left_start")
        self.register_event_type("on_left_second_start")

    def on_right_finish(self, *args):
        pass

    def on_right_start(self, *args):
        pass

    def on_right_second_start(self, *args):
        pass

    def on_left_finish(self, *args):
        pass

    def on_left_start(self, *args):
        pass

    def on_left_second_start(self, *args):
        pass

    def update_mesh(self, start, end, pos):
        res = []
        points_1 = [[-1000, -1000], start, [pos[0] / 2, pos[1] / 2], pos]
        points_2 = [
            pos,
            [pos[0] / 2, (end[1] + pos[1]) / 2],
            end,
            [-1000, end[1] + 1000],
        ]
        res.extend(points_1)
        res.extend(points_2)

        t_points = np.arange(0, 1, 0.01)
        points1 = np.array(res)
        curve = Bz.Curve(t_points, points1)

        vertices = []
        indices = []
        _i = 0
        for x, y in curve:
            vertices.extend([x, y, 0, 0])
            indices.append(_i)
            _i += 1
        self.indices = indices
        self.vertices = vertices

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        self.curve_pos = touch.pos

    def on_curve_pos(self, *args):
        self.update_mesh(self.start_pos[:], self.end_pos[:], self.curve_pos[:])

    def on_start_pos(self, *args):
        self.update_mesh(self.start_pos[:], self.end_pos[:], self.curve_pos[:])

    def on_touch_up(self, touch):
        distance = touch.x - touch.ox
        if abs(distance) > self.drag_distance:

            if distance > 0:
                start_pos = [self.width + 400, -400]
                end_pos = [self.width + 400, self.height + 400]
                curve_pos = [self.width + 400, self.curve_pos[1]]
                self.move_anim("right", curve_pos, start_pos, end_pos)
                self.dispatch("on_right_start")
            else:
                start_pos = [0, 0]
                end_pos = [0, self.height]
                curve_pos = [0, self.curve_pos[1]]
                self.move_anim("left", curve_pos, start_pos, end_pos)
                self.dispatch("on_left_start")
        else:
            if self._state == "right":
                self.reset_anim([self.width + 400, touch.y])
            elif self._state == "left":
                self.reset_anim([0, touch.y])

    def move_anim(self, state, curve_pos, start_pos, end_pos):
        anim = Animation(
            curve_pos=curve_pos,
            t="out_quad",
            d=0.3,
        )
        anim.bind(on_complete=lambda *args: self.dispatch(f"on_{state}_second_start"))

        anim2 = Animation(d=0.2) + Animation(
            start_pos=start_pos,
            end_pos=end_pos,
            t="in_quad",
            d=0.3,
        )
        anim2.bind(on_complete=lambda *args: self.dispatch(f"on_{state}_finish"))
        anim.start(self)
        anim2.start(self)
        self._state = state

    def reset_anim(self, curve_pos):
        anim = Animation(curve_pos=curve_pos, t="out_quad", d=0.2)
        anim.start(self)

    def add_widget(self, widget, **kw):
        if issubclass(widget.__class__, FrontLayout):
            self.ids.frontlayout.add_widget(widget)
            return True

        elif issubclass(widget.__class__, BackLayout):
            self.ids.backlayout.add_widget(widget)
            return True

        return super().add_widget(widget)