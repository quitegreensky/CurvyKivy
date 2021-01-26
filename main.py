from kivymd.app import MDApp
from kivy.lang.builder import Builder
from curvelayout import CurveLayout


class MeshTestApp(MDApp):
    def build(self):
        return CurveLayout()


if __name__ == "__main__":
    MeshTestApp().run()