# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Mydemos_pkg\peace.py
# Compiled at: 2020-04-30 10:26:21
# Size of source mod 2**32: 1115 bytes
"""       turtle-example-suite:

              tdemo_peace.py

A simple drawing suitable as a beginner's
programming example. Aside from the
peacecolors assignment and the for loop,
it only uses turtle commands.
"""
from turtle import *

def main():
    peacecolors = ('red3', 'orange', 'yellow', 'seagreen4', 'orchid4', 'royalblue1',
                   'dodgerblue4')
    reset()
    Screen()
    up()
    goto(-320, -195)
    width(70)
    for pcolor in peacecolors:
        color(pcolor)
        down()
        forward(640)
        up()
        backward(640)
        left(90)
        forward(66)
        right(90)

    width(25)
    color('white')
    goto(0, -170)
    down()
    circle(170)
    left(90)
    forward(340)
    up()
    left(180)
    forward(170)
    right(45)
    down()
    forward(170)
    up()
    backward(170)
    left(90)
    down()
    forward(170)
    up()
    goto(0, 300)
    return 'Done!'


def peace():
    main()
    mainloop()