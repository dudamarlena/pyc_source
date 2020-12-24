# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\jobspider\baseclass\utils\setcolor.py
# Compiled at: 2016-03-20 20:41:25
__author__ = 'whb'

def setcolor(color):

    def inner(msg, bold=False):
        color = '1;%d' % color if bold else str(color)
        return '\x1b[%sm%s\x1b[0m' % (color, msg)

    return inner


black = setcolor(30)
red = setcolor(31)
green = setcolor(32)
yellow = setcolor(33)
blue = setcolor(34)
cyanine = setcolor(36)
white = setcolor(37)