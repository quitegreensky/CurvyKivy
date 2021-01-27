from kivymd.app import MDApp
from kivy.lang.builder import Builder
from curvelayout import CurveLayout, FrontLayout, BackLayout
from kivy.properties import ListProperty

kv= """
<BackFloat>
    canvas:
        Rectangle:
            pos: root.car_pos
            size: dp(100), dp(80)
            source: "assets/car.png"

CurveLayout:
    
    FrontLayout:

    BackFloat:


        MDLabel:
            text: "Did You Know..."
            adaptive_size: True
            pos_hint: {"center_x": .5, "center_y":.7}


"""


class BackFloat(BackLayout):
    car_pos = ListProperty([100,100])

class MeshTestApp(MDApp):
    def build(self):
        return Builder.load_string(kv)


if __name__ == "__main__":
    MeshTestApp().run()