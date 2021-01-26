import pyximport; pyximport.install()
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Mesh
from kivy.properties import NumericProperty, ListProperty, AliasProperty
from kivy.animation import Animation
from kivy.event import EventDispatcher
from cal import Cal
from kivy.lang.builder import Builder


class MyBox(BoxLayout, EventDispatcher):
    drag_distance = NumericProperty("100dp")
    curve_pos = ListProperty([0, 0])
    start_pos = ListProperty([0,0])
    end_pos = ListProperty([0,0])

    _indices = ListProperty([0])
    def _get_indices(self):
        return self._indices
    
    def _set_indices(self, val):
        self._indices = val

    indices = AliasProperty(_get_indices, _set_indices)

    _state = "left"

    def __init__(self, **kw):
        super().__init__(**kw)
        with self.canvas:
            self.mesh = Mesh(mode="triangle_fan")
        self.cal = Cal(self.mesh)

    # def update_mesh(self, list start, list end, list pos):
    #     cpdef list res = []
    #     cpdef list points_1
    #     cpdef list points_2
    #     cpdef list vertices
    #     cpdef list indices
    #     cpdef int _i 
    #     cpdef int x
    #     cpdef int y

    #     points_1 = [[-1000, -1000], start, [pos[0] / 2, pos[1] / 2], pos]
    #     points_2 = [
    #         pos,
    #         [pos[0] / 2, (end[1] + pos[1]) / 2],
    #         end,
    #         [-1000, end[1] + 1000],
    #     ]
    #     res.extend(points_1)
    #     res.extend(points_2)

    #     t_points = np.arange(0, 1, 0.01)
    #     points1 = np.array(res)
    #     curve = Bz.Curve(t_points, points1)

    #     vertices = []
    #     indices = []
    #     _i = 0
    #     for x, y in curve:
    #         vertices.extend([x, y, 0, 0])
    #         indices.append(_i)
    #         _i += 1
    #     self.mesh.indices = indices
    #     self.mesh.vertices = vertices

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        self.curve_pos = touch.pos

    def on_curve_pos(self, *args):
        self.cal.update_mesh(self.start_pos[:], self.end_pos[:], self.curve_pos[:])

    def on_start_pos(self, *args):
        self.cal.update_mesh(self.start_pos[:], self.end_pos[:], self.curve_pos[:])

    def on_touch_up(self, touch):
        distance = touch.x - touch.ox
        if abs(distance) > self.drag_distance:

            if distance > 0:
                start_pos = [self.width+400, -400]
                end_pos = [self.width+400, self.height+400]
                curve_pos = [self.width+400, self.curve_pos[1]]             
                self.move_anim("right", curve_pos, start_pos, end_pos)
            else:
                start_pos = [0, 0]
                end_pos = [0, self.height]
                curve_pos = [0, self.curve_pos[1]]
                self.move_anim("left", curve_pos, start_pos, end_pos)
        else:
            if self._state == "right":
                self.reset_anim([self.width+400, touch.y])
            elif self._state == "left":
                self.reset_anim([0, touch.y])

    def move_anim(self, state, curve_pos, start_pos, end_pos):
        anim = Animation(
            curve_pos=curve_pos,
            t="out_quad",
            d=0.8,
        )
        anim2 = Animation(d=0.2)+Animation(
            start_pos=start_pos,
            end_pos=end_pos,
            t="out_quad",
            d=0.5,
        )
        anim.start(self)
        anim2.start(self)
        self._state = state

    def reset_anim(self, curve_pos):
        anim = Animation(curve_pos=curve_pos, t="out_quad", d=0.2)
        anim.start(self)





Builder.load_string(
    """
# MyBox:
#     canvas:
#         Mesh:
#             mode: "triangle_fan"
#             indices: root.indices 
#             vertices: [\
#                 [-1000, -1000]
#                 ]

    """
)

class MeshTestApp(App):
    def build(self):
        return MyBox()


if __name__ == "__main__":
    MeshTestApp().run()