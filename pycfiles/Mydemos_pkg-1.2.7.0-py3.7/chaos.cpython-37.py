# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Mydemos_pkg\chaos.py
# Compiled at: 2020-04-30 10:01:22
# Size of source mod 2**32: 998 bytes
from turtle import *
N = 80

def f(x):
    return 3.9 * x * (1 - x)


def g(x):
    return 3.9 * (x - x ** 2)


def h(x):
    return 3.9 * x - 3.9 * x * x


def jumpto(x, y):
    penup()
    goto(x, y)


def line(x1, y1, x2, y2):
    jumpto(x1, y1)
    pendown()
    goto(x2, y2)


def coosys():
    line(-1, 0, N + 1, 0)
    line(0, -0.1, 0, 1.1)


def plot(fun, start, color):
    pencolor(color)
    x = start
    jumpto(0, x)
    pendown()
    dot(5)
    for i in range(N):
        x = fun(x)
        goto(i + 1, x)
        dot(5)


def main():
    reset()
    setworldcoordinates(-1.0, -0.1, N + 1, 1.1)
    speed(0)
    hideturtle()
    coosys()
    plot(f, 0.35, 'blue')
    plot(g, 0.35, 'green')
    plot(h, 0.35, 'red')
    for s in range(100):
        setworldcoordinates(0.5 * s, -0.1, N + 1, 1.1)

    return 'Done!'


def chaos():
    main()
    mainloop()