# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/gwill/changes/DrawGossip.py
# Compiled at: 2019-03-25 05:37:00
# Size of source mod 2**32: 2237 bytes
from turtle import Screen, Turtle, TK
import time

class DrawGossip(object):

    def __init__(self, pen):
        self.pen = pen.clone()
        self.pen.showturtle()
        self.pen.speed(1)
        self.pen.begin_fill()

    def drawGossip(self, yo1, yo2, yo3, yo4, yo5, yo6):
        self.drawYo(yo1)
        self.pen.penup()
        self.pen.goto(x=0, y=(-10))
        self.drawYo(yo2)
        self.pen.penup()
        self.pen.goto(x=0, y=(-20))
        self.drawYo(yo3)
        self.pen.penup()
        self.pen.goto(x=0, y=(-30))
        self.drawYo(yo4)
        self.pen.penup()
        self.pen.goto(x=0, y=(-40))
        self.drawYo(yo5)
        self.pen.penup()
        self.pen.goto(x=0, y=(-50))
        self.drawYo(yo6)
        self.pen.end_fill()
        self.pen.hideturtle()

    def drawYo(self, yo):
        self.pen.pensize(5)
        if yo == 1:
            self.pen.color('yellow', 'red')
            self.pen.pendown()
            self.pen.forward(200)
        else:
            self.pen.color('black', 'red')
            self.pen.pendown()
            self.pen.forward(90)
            self.pen.penup()
            self.pen.setx(x=110)
            self.pen.pendown()
            self.pen.forward(90)

    def drawOctagonalLine(self, long, linesCount):
        self.pen.pensize(1)
        degree = 360 / linesCount
        for i in range(int(linesCount)):
            self.pen.forward(long)
            self.pen.right(degree)

        self.pen.hideturtle()
        screen = self.pen.getscreen()
        screen.onkey(self.closeWindow, 'space')
        screen.listen()

    def getScreen(self):
        screen = self.pen.getscreen()
        return screen

    def closeWindow(self):
        TK._exit(0)


def main():
    main = DrawGossip(Turtle())
    long = main.getScreen().numinput('边长', '请输入边长（像素值）：', 0, 1, 500)
    linesCount = main.getScreen().numinput('边数', '多边形边的数量：', 3, 3, 100)
    main.drawOctagonalLine(long, linesCount)
    return 'EVENTLOOP'