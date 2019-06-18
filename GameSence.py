import kivy
import time
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder 
from kivy.vector import Vector
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from random import randint

class ScoreBoard(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.maxscore = 65535
        self.p1score = 0
        self.p2score = 0

class HitButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self. size_hint = (.2, .1)

class Table(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tablecolor = (1, 1, 1, 1)
        self.size_hint = (.6, .6)
        self.pos_hint = { 'x' : .2, 'y' : .2 }
        self.source = 'table.png'

class Player(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gender = 'boy'

    def hitLeft(self):
        pass

    def hitRight(self):
        pass

class PingpongBall(Widget):
    def __init__(self, game, ballcolor = 'white', **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1)
        with self.canvas:
            Color(1, 1, 1)
            Ellipse(pos_hint = { 'x' : .5, 'y' : .5 }, size = (20, 20))
        self.ballcolor = ballcolor

    def move2Left(self, table):
        self.pos = Vector(*self.velocity) + self.pos

    def move2Right(self):
        self.pos = Vector(*self.velocity) + self.pos

class Game(FloatLayout):
    def __init__(self, mode = 1, level = 1, bgcolor = 'default', ballcolor = 'white', **kwargs):
        super().__init__(**kwargs)
        self.lbutton = HitButton(text = 'Hit L', pos_hint = { 'x' : .2, 'y' : .05 })
        self.rbutton = HitButton(text = 'Hit R', pos_hint = { 'x' : .6, 'y' : .05 })
        self.level = level
        self.mode = mode
        self.table = Table()
        self.ball = PingpongBall(self)
        self.add_widget(self.table)
        self.start()
        self.add_widget(self.ball)
        self.add_widget(self.lbutton)
        self.add_widget(self.rbutton)

    def start(self):
        if(self.mode == 1):
            self.singleGame()
        elif(self.mode == 2):
            self.doublePlayer()
        elif(self.mode == 3):
            self.mirrorGame()
        elif(self.mode == 4):
            self.infinityGame()

    def timeWait(self):
        time.sleep(3)

    def singleGame(self):
        pass
        #Clock.schedule_interval(self.update, 1.0 / 60.0)

    def mirrorGame(self):
        self.lbutton.pos_hint = { 'x' : .6, 'y' : .05 }
        self.rbutton.pos_hint = { 'x' : .2, 'y' : .05 }

    def infinityGame(self):
        pass

    def doublePlayer(self):
        p2lbutton = HitButton(text = 'Hit L', pos_hint = { 'x' : .6, 'y' : .85 })
        p2rbutton = HitButton(text = 'Hit R', pos_hint = { 'x' : .2, 'y' : .85 })
        self.add_widget(p2lbutton)
        self.add_widget(p2rbutton)

    def update(self):
        self.ball.move2Left(self.table)

    def gamePause(self):
        pass