# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Mydemos_pkg\paint.py
# Compiled at: 2020-04-30 10:25:26
# Size of source mod 2**32: 1333 bytes
"""       turtle-example-suite:

            tdemo_paint.py

A simple  event-driven paint program

- left mouse button moves turtle
- middle mouse button changes color
- right mouse button toogles betweem pen up
(no line drawn when the turtle moves) and
pen down (line is drawn). If pen up follows
at least two pen-down moves, the polygon that
includes the starting point is filled.
 -------------------------------------------
 Play around by clicking into the canvas
 using all three mouse buttons.
 -------------------------------------------
          To exit press STOP button
 -------------------------------------------
"""
from turtle import *

def switchupdown(x=0, y=0):
    if pen()['pendown']:
        end_fill()
        up()
    else:
        down()
        begin_fill()


def changecolor(x=0, y=0):
    global colors
    colors = colors[1:] + colors[:1]
    color(colors[0])


def main():
    global colors
    shape('circle')
    resizemode('user')
    shapesize(0.5)
    width(3)
    colors = ['red', 'green', 'blue', 'yellow']
    color(colors[0])
    switchupdown()
    onscreenclick(goto, 1)
    onscreenclick(changecolor, 2)
    onscreenclick(switchupdown, 3)
    return 'EVENTLOOP'


def paint():
    msg = main()
    print(msg)
    mainloop()