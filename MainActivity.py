import kivy
import GameSence
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder 
from kivy.uix.image import Image, AsyncImage
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

class ImageButton(ButtonBehavior, Image):
    def __init__(self, imgpath, **kwargs):
        super().__init__(**kwargs)
        self.source = imgpath

level2 = 1
homeButton = ImageButton(imgpath = 'homeButton.png', size_hint = (.1, .1), pos_hint = { 'x' : .83, 'y' : .87 })
#pauseButton = ImageButton(imgpath = 'puimg.jpg', size_hint = (.1, .1), pos_hint = { 'x' : .73, 'y' : .87 })

class HomeLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        bt1 = ImageButton(imgpath = 'menuButton.png', size_hint = (.20, .08), pos_hint = { 'x' : .1, 'y' : .2 })
        bt1.bind(on_press = self.moreGame)
        bt2 = ImageButton(imgpath = 'playButton.png', size_hint = (.20, .08), pos_hint = { 'x' : .4, 'y' : .2 })
        bt2.bind(on_press = self.startGame)
        bt3 = ImageButton(imgpath = 'storeButton.png', size_hint = (.20, .08), pos_hint = { 'x' : .7, 'y' : .2 })
        bt3.bind(on_press = self.openStore)
        homeButton.bind(on_press = self.backHome)
        self.bgimg = AsyncImage(source = 'bgGif.gif', anim_delay = 1.0/24)
        self.add_widget(self.bgimg)
        self.add_widget(bt1)
        self.add_widget(bt2)
        self.add_widget(bt3)

    def startGame(self, instance):
        self.clear_widgets()
        #gm = GameSence.Game(level = level)
        self.add_widget(GameSence.Game())
        self.add_widget(homeButton)


    def moreGame(self, instance):
        self.clear_widgets()
        self.add_widget(MoreLayout())

    def openStore(self, instance):
        self.clear_widgets()
        self.add_widget(self.bgimg)
        self.add_widget(StoreLayout())

    def backHome(self, instance):
        self.clear_widgets()
        self.add_widget(HomeLayout())

class MoreLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        bt1 = Button(text = 'MirrorMode', font_size=14, size_hint = (.4, .08), pos_hint = { 'x' : .3, 'y' : .2 })
        bt1.bind(on_press = self.mirrorGame)
        bt2 = Button(text = 'InfinityMode', font_size=14, size_hint = (.4, .08), pos_hint = { 'x' : .3, 'y' : .4 })
        bt2.bind(on_press = self.infinityGame)
        bt3 = Button(text = 'DoublePlayer', font_size=14, size_hint = (.4, .08), pos_hint = { 'x' : .3, 'y' : .6 })
        bt3.bind(on_press = self.doublePlayer)
        homeButton.bind(on_press = self.backHome)
        self.add_widget(bt1)
        self.add_widget(bt2)
        self.add_widget(bt3)
        self.add_widget(homeButton)

    def backHome(self, instance):
        self.clear_widgets()
        self.add_widget(HomeLayout())
    
    def mirrorGame(self, instance):
        self.clear_widgets()
        self.add_widget(homeButton)
        self.add_widget(GameSence.Game(mode = 3))
    
    def infinityGame(self, instance):
        self.clear_widgets()
        self.add_widget(homeButton)
        self.add_widget(GameSence.Game(mode = 4))

    def doublePlayer(self, instance):
        self.clear_widgets()
        self.add_widget(homeButton)
        self.add_widget(GameSence.Game(mode = 2))

class StoreLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        homeButton.bind(on_press = self.backHome)
        self.add_widget(Label(text = 'Coming soon'))
        self.add_widget(homeButton)

    def backHome(self, instance):
        self.clear_widgets()
        self.add_widget(HomeLayout())

class PingPongApp(App):
    def build(self):
        self.root = root = HomeLayout()
        root.bind(size=self._update_rect, pos=self._update_rect)
        with root.canvas.before:
            Color(.745, .875, 1)
            self.rect = Rectangle(size=root.size, pos=root.pos)
            #Clock.schedule_interval(game.update, 1.0 / 60.0)
        return root
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    PingPongApp().run()