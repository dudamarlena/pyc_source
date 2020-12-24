# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Mydemos_pkg\colormixer.py
# Compiled at: 2020-04-30 10:11:31
# Size of source mod 2**32: 1390 bytes
from turtle import Screen, Turtle, mainloop

class ColorTurtle(Turtle):

    def __init__(self, x, y):
        Turtle.__init__(self)
        self.shape('turtle')
        self.resizemode('user')
        self.shapesize(3, 3, 5)
        self.pensize(10)
        self._color = [0, 0, 0]
        self.x = x
        self._color[x] = y
        self.color(self._color)
        self.speed(0)
        self.left(90)
        self.pu()
        self.goto(x, 0)
        self.pd()
        self.sety(1)
        self.pu()
        self.sety(y)
        self.pencolor('gray25')
        self.ondrag(self.shift)

    def shift(self, x, y):
        self.sety(max(0, min(y, 1)))
        self._color[self.x] = self.ycor()
        self.fillcolor(self._color)
        setbgcolor()


def setbgcolor():
    screen.bgcolor(red.ycor(), green.ycor(), blue.ycor())


def main():
    global blue
    global green
    global red
    global screen
    screen = Screen()
    screen.delay(0)
    screen.setworldcoordinates(-1, -0.3, 3, 1.3)
    red = ColorTurtle(0, 0.5)
    green = ColorTurtle(1, 0.5)
    blue = ColorTurtle(2, 0.5)
    setbgcolor()
    writer = Turtle()
    writer.ht()
    writer.pu()
    writer.goto(1, 1.15)
    writer.write('DRAG!', align='center', font=('Arial', 30, ('bold', 'italic')))
    return 'EVENTLOOP'


def colormixer():
    msg = main()
    print(msg)
    mainloop()