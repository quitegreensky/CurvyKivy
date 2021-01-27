from kivy.lang.builder import Builder
from kivy.properties import StringProperty, NumericProperty, StringProperty
from kivymd.uix.label import MDLabel


Builder.load_string(
    """
<MyLabel>:
    adaptive_size: True
    text: "Text"
    halign: "center"
    theme_text_color: "Custom"
    text_color: 1,1,1,1
    font_name: "assets/regular.otf" if root.font_type=="regular" else "assets/light.otf"

    """
)

class MyLabel(MDLabel):
    font_type = StringProperty("regular")