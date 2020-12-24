# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/IOU.py
# Compiled at: 2018-08-04 12:32:06


def IOU(Reframe=[], GTframe=[]):
    u"""
    计算两矩形 IOU，传入为均为矩形每条对角线，（x,y）  坐标。
    """
    x1 = Reframe[0]
    y1 = Reframe[1]
    width1 = Reframe[2] - Reframe[0]
    height1 = Reframe[3] - Reframe[1]
    x2 = GTframe[0]
    y2 = GTframe[1]
    width2 = GTframe[2] - GTframe[0]
    height2 = GTframe[3] - GTframe[1]
    endx = max(x1 + width1, x2 + width2)
    startx = min(x1, x2)
    width = width1 + width2 - (endx - startx)
    endy = max(y1 + height1, y2 + height2)
    starty = min(y1, y2)
    height = height1 + height2 - (endy - starty)
    if width <= 0 or height <= 0:
        ratio = 0
    else:
        Area = width * height
        Area1 = width1 * height1
        Area2 = width2 * height2
        ratio = Area * 1.0 / (Area1 + Area2 - Area)
    print 'IOU=%f' % ratio
    print Reframe
    print GTframe
    return ratio