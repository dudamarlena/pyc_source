# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Mydemos_pkg\yinyang.py
# Compiled at: 2020-04-30 10:38:43
# Size of source mod 2**32: 860 bytes
"""       turtle-example-suite:

            tdemo_yinyang.py

Another drawing suitable as a beginner's
programming example.

The small circles are drawn by the circle
command.

"""
from turtle import *

def yin(radius, color1, color2):
    width(3)
    color('black', color1)
    begin_fill()
    circle(radius / 2.0, 180)
    circle(radius, 180)
    left(180)
    circle(-radius / 2.0, 180)
    end_fill()
    left(90)
    up()
    forward(radius * 0.35)
    right(90)
    down()
    color(color1, color2)
    begin_fill()
    circle(radius * 0.15)
    end_fill()
    left(90)
    up()
    backward(radius * 0.35)
    down()
    left(90)


def main():
    reset()
    yin(200, 'black', 'white')
    yin(200, 'white', 'black')
    ht()
    return 'Done!'


def yinyang():
    main()
    mainloop()