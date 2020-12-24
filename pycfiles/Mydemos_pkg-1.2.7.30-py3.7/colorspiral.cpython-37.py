# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Mydemos_pkg\colorspiral.py
# Compiled at: 2020-04-13 08:18:34
# Size of source mod 2**32: 456 bytes
import turtle
print('welcome to colorspiral!')

def colorspiral(sides, bg='black'):
    t = turtle.Pen()
    turtle.bgcolor('black')
    sides = 6
    colors = ['red', 'yellow', 'blue', 'orange', 'green', 'purple', 'white']
    for x in range(360):
        t.pencolor(colors[(x % sides)])
        t.forward(x * 3 / sides + x)
        t.left(360 / sides + 1)
        t.width(x * sides / 200)