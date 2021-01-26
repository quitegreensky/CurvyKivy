from kivymd.app import MDApp
from kivy.lang.builder import Builder
from curvelayout import CurveLayout, FrontLayout, BackLayout


kv= """
CurveLayout:
    
    FrontLayout:

    BackLayout:

"""


class MeshTestApp(MDApp):
    def build(self):
        return Builder.load_string(kv)


if __name__ == "__main__":
    MeshTestApp().run()