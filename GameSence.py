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
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.gender = 'boy'

    def p1hitl(self, instacne):
        if(self.game.ball.canhit == 3):
            self.game.ball.poskey = randint(1,2)
            self.game.getball = 1
        print('HitL')

    def p1hitr(self, instance):
        if(self.game.ball.canhit == 4):
            self.game.ball.poskey = randint(1,2)
            self.game.getball = 1
        print('HitR')
            
    def p2hitl(self, instance):
        if(self.game.ball.canhit == 2):
            self.game.ball.poskey = randint(3, 4)
            self.game.getball = 1

    def p2hitr(self, instance):
        if(self.game.ball.canhit == 1):
            self.game.ball.poskey = randint(3, 4)
            self.game.getball = 1

    def aihit(self, instance):
        if(self.game.ball.canhit == 1 or self.game.ball.canhit == 2):
            if(randint(1, 4) != 5):
                self.game.ball.poskey = randint(3, 4)
                self.game.getball = 1
            print('aihit')


class PingpongBall(Widget):
    def __init__(self, game, ballcolor = 'white', **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.canhit = 0
        self.timeWait = 1
        self.spd = 60
        self.t = 1 / self.spd
        self.poskey = 4
        self.stpos = [1, 1]
        self.dst = [1, 1]
        self.pos = [1, 1]
        self.ballcolor = ballcolor

    def move(self, table):
        if(self.game.getball == 1):         #击球后的动作
            self.game.getball = 0
            self.ballPos(self.poskey)
            self.canhit = 0
        elif(self.game.getball == -1):      #小球初始运动
            self.game.getball = 0
            self.ballPos(0)
            self.canhit = 0
        if(self.t <= 1):                    #贝塞尔曲线绘制乒乓球轨迹
            t = self.t
            v1 = Vector(self.stpos)
            v2 = Vector([self.dst[0], self.stpos[1]])
            v3 = Vector(self.dst)
            v4 = ((v2 + (v3 - v2) * t) - (v1 + (v2 - v1) * t)) * t + (v1 + (v2 - v1) * t)
            self.t += 1.0/self.spd
            self.pos = [round(v4.x, 1), round(v4.y, 1)]
        elif(self.poskey == 3 or self.poskey == 4):     #小球在p1弹起
            if(True):
                self.canhit = self.poskey
                self.timeWait += 1
            else:
                self.canhit = 0
            if(self.poskey == 3):
                self.pos[0] -= 2
                self.pos[1] -= 2
            else:
                self.pos[0] += 2
                self.pos[1] -= 2
            if(self.game.getball == 1):
                self.timeWait = 1
        elif(self.poskey == 1 or self.poskey == 2):         #小球在p2弹起
            if(self.timeWait < 400):
                self.canhit = self.poskey
                self.timeWait += 1
            else:
                self.canhit = 0
            if(self.poskey == 1):
                self.pos[0] -= 2
                self.pos[1] += 2
            else:
                self.pos[0] += 2
                self.pos[1] += 2
            if(self.game.getball == 1):
                self.timeWait = 1      
        self.canvas.clear()
        self.drawBall()

    def ballPos(self, poskey):
        if(poskey == 0):
            self.stpos[0] = self.pos[0] = self.game.width * 0.35
            self.stpos[1] = self.pos[1] = self.game.height * 0.58
            self.dst = [self.game.width * 0.6, self.game.height * 0.38]
        else:
            self.t = 1 / self.spd
            self.stpos[0] = self.pos[0]
            self.stpos[1] = self.pos[1]
            if(poskey == 1):
                self.dst = [self.game.width * 0.35, self.game.height * 0.58]
            if(poskey == 2):
                self.dst = [self.game.width * 0.6, self.game.height * 0.58]
            if(poskey == 3):
                self.dst = [self.game.width * 0.35, self.game.height * 0.38]
            if(poskey == 4):
                self.dst = [self.game.width * 0.6, self.game.height * 0.38]

    def drawBall(self):
        self.switch = 0
        with self.canvas:
            Color(1, 1, 1)
            Ellipse(pos = self.pos, size = (20, 20) )

class Game(FloatLayout):
    def __init__(self, mode = 1, level = 1, bgcolor = 'default', ballcolor = 'white', **kwargs):
        super().__init__(**kwargs)
        self.lbutton = HitButton(text = 'Hit L', pos_hint = { 'x' : .2, 'y' : .05 })
        self.rbutton = HitButton(text = 'Hit R', pos_hint = { 'x' : .6, 'y' : .05 })
        self.level = level
        self.mode = mode
        self.table = Table()
        self.getball = -1
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
        p1 = Player(self)
        ai = Player(self)
        self.lbutton.bind(on_press = p1.p1hitl)
        self.rbutton.bind(on_press = p1.p1hitr)
        Clock.schedule_interval(ai.aihit, 1.0/60.0)
        Clock.schedule_interval(self.update, 1.0/60.0)

    def mirrorGame(self):
        self.lbutton.pos_hint = { 'x' : .6, 'y' : .05 }
        self.rbutton.pos_hint = { 'x' : .2, 'y' : .05 }

    def infinityGame(self):
        pass

    def doublePlayer(self):
        p1 = Player(self)
        p2 = Player(self)
        self.lbutton.bind(on_press = p1.p1hitl)
        self.rbutton.bind(on_press = p1.p1hitr)
        p2lbutton = HitButton(text = 'Hit L', pos_hint = { 'x' : .6, 'y' : .85 })
        p2rbutton = HitButton(text = 'Hit R', pos_hint = { 'x' : .2, 'y' : .85 })
        p2lbutton.bind(on_press = p1.p2hitl)
        p2rbutton.bind(on_press = p1.p2hitr)
        self.add_widget(p2lbutton)
        self.add_widget(p2rbutton)
        Clock.schedule_interval(self.update, 1.0/60.0)

    def update(self, dt):
        self.ball.move(self)
        #self.ball.move2Right()

    def gamePause(self):
        pass