# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/turtleart/draw.py
# Compiled at: 2016-11-07 14:42:45


def drawline(turt, a, b, c, d):
    turt.pu()
    turt.goto(a, b)
    turt.pendown()
    turt.goto(c, d)


def makegraph(turt):
    drawline(turt, -1000, 0, 1000, 0)
    drawline(turt, 0, -1000, 0, 1000)


def get_quad_values(quad_num, size, count):
    if quad_num == 1:
        return (size, size * count)
    if quad_num == 2:
        return (-size, size * count)
    if quad_num == 3:
        return (-size, -(size * count))
    if quad_num == 4:
        return (size, -(size * count))


def draw_quad(turt, quad_num, size, count=10):
    x, y = get_quad_values(quad_num, size, count)
    for _ in range(count):
        drawline(turt, x, 0, 0, y)
        if x < 0:
            x -= size
        else:
            x += size
        if y < 0:
            y += size
        else:
            y -= size


def draw_all_quads(turt, size, count=10):
    for i in range(1, 5):
        draw_quad(turt, i, size, count)