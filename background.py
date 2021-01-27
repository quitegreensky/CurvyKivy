from kivy.lang.builder import Builder
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty


Builder.load_string(
    """
<BackGround>:
    canvas:
        Color:
            rgba: root.darkColor
        Rectangle:
            pos: 0, root.height - root.height*root.ratio
            size: root.width, root.height*root.ratio

        Color:
            rgba: root.barColor
        Rectangle:
            pos: 0, root.height - root.height*root.ratio - root.bar_height
            size: root.width , root.bar_height

        Color:
            rgba: root.lightColor
        Rectangle:
            pos: 0, 0
            size: root.width , root.height - root.bar_height - root.height*root.ratio
    """
)
class BackGround(Widget):
    darkColor = ListProperty([222/255 ,10/255,74/255,1])
    barColor = ListProperty([201/255,9/255,67/255,1])
    lightColor= ListProperty([255/255,0/255,85/255,1])
    ratio = NumericProperty(0.6)
    bar_height = NumericProperty("8dp")