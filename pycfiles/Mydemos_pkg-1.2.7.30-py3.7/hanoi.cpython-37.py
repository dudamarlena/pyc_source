# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Mydemos_pkg\hanoi.py
# Compiled at: 2020-04-30 10:20:44
# Size of source mod 2**32: 2120 bytes
"""       turtle-example-suite:

         tdemo_minimal_hanoi.py

A minimal 'Towers of Hanoi' animation:
A tower of 6 discs is transferred from the
left to the right peg.

An imho quite elegant and concise
implementation using a tower class, which
is derived from the built-in type list.

Discs are turtles with shape "square", but
stretched to rectangles by shapesize()
 ---------------------------------------
       To exit press STOP button
 ---------------------------------------
"""
from turtle import *

class Disc(Turtle):

    def __init__(self, n):
        Turtle.__init__(self, shape='square', visible=False)
        self.pu()
        self.shapesize(1.5, n * 1.5, 2)
        self.fillcolor(n / 6.0, 0, 1 - n / 6.0)
        self.st()


class Tower(list):
    __doc__ = 'Hanoi tower, a subclass of built-in type list'

    def __init__(self, x):
        """create an empty tower. x is x-position of peg"""
        self.x = x

    def push(self, d):
        d.setx(self.x)
        d.sety(-150 + 34 * len(self))
        self.append(d)

    def pop(self):
        d = list.pop(self)
        d.sety(150)
        return d


def hanoi(n, from_, with_, to_):
    if n > 0:
        hanoi(n - 1, from_, to_, with_)
        to_.push(from_.pop())
        hanoi(n - 1, with_, from_, to_)


def play():
    onkey(None, 'space')
    clear()
    try:
        hanoi(6, t1, t2, t3)
        write('press STOP button to exit', align='center',
          font=('Courier', 16, 'bold'))
    except Terminator:
        pass


def main():
    global t1
    global t2
    global t3
    ht()
    penup()
    goto(0, -225)
    t1 = Tower(-250)
    t2 = Tower(0)
    t3 = Tower(250)
    for i in range(6, 0, -1):
        t1.push(Disc(i))

    write('press spacebar to start game', align='center',
      font=('Courier', 16, 'bold'))
    onkey(play, 'space')
    listen()
    return 'EVENTLOOP'


def hanoi():
    msg = main()
    print(msg)
    mainloop()