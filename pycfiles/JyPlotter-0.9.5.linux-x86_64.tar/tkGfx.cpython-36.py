# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.6/site-packages/PyPlotter/tkGfx.py
# Compiled at: 2017-09-02 11:04:34
# Size of source mod 2**32: 7225 bytes
"""Implements Gfx.Driver using tkInter. 

Has some flaws! Specifically rotated text is not yet implemented properly.
"""
import math
try:
    from tkinter import *
    import tkinter.font as tkFont
except ImportError:
    from Tkinter import *
    import tkFont

try:
    import Gfx
except ImportError:
    from . import Gfx

try:
    from Compatibility import *
except ImportError:
    from .Compatibility import *

driverName = 'tkGfx'

class Driver(Gfx.Driver):
    __doc__ = 'A graphics driver for  Tkinter.\n    For an explanation of the inherited methods see Gfx.py.\n    '

    def __init__(self, tkCanvas):
        """Initialize Driver for a Tkinter Canvas Object."""
        self.canvas = tkCanvas
        self.resizedGfx()
        self.reset()
        self.clear()

    def colorStr(self, rgbTuple):
        """rgbTuple -> string (eg. '#A0A0F3')"""

        def hex2str(c):
            h = hex(int(round(c * 255)))[2:]
            if len(h) == 1:
                return '0' + h
            else:
                return h

        s = '#' + hex2str(rgbTuple[0]) + hex2str(rgbTuple[1]) + hex2str(rgbTuple[2])
        return s

    def resizedGfx(self):
        """Take notice if the undelying device has been resized."""
        self.w = int(self.canvas.cget('width'))
        self.h = int(self.canvas.cget('height'))

    def getSize(self):
        return (
         self.w, self.h)

    def setColor(self, rgbTuple):
        self.color = rgbTuple
        self.fg = self.colorStr(rgbTuple)

    def setLineWidth(self, width):
        self.lineWidth = width
        if width == Gfx.THIN:
            self.width = '1.0'
        else:
            if width == Gfx.MEDIUM:
                self.width = '2.0'
            else:
                if width == Gfx.THICK:
                    self.width = '3.0'
                else:
                    raise ValueError("'thickness' must be THIN, MEDIUM or THICK !")

    def setLinePattern(self, pattern):
        """Set line pattern (CONTINOUS, DASHED or DOTTED)."""
        self.linePattern = pattern
        if pattern == Gfx.CONTINUOUS:
            self.dash = ''
        else:
            if pattern == Gfx.DASHED:
                self.dash = '- '
            else:
                if pattern == Gfx.DOTTED:
                    self.dash = '. '
                else:
                    raise ValueError("'pattern' must be CONTINUOUS, DASHED or DOTTED !")

    def setFillPattern(self, pattern):
        """Set pattern for filled areas (SOLID or PATTERNED)."""
        self.fillPattern = pattern
        if pattern == Gfx.SOLID:
            self.stipple = ''
        else:
            if pattern == Gfx.PATTERN_A:
                self.stipple = ''
            else:
                if pattern == Gfx.PATTERN_B:
                    self.stipple = ''
                else:
                    if pattern == Gfx.PATTERN_C:
                        self.stipple = ''
                    else:
                        raise ValueError("'pattern' must be SOLID or PATTERNED !")

    def setFont(self, ftype, size, weight):
        self.fontType = ftype
        self.fontSize = size
        self.fontWeight = weight
        if ftype == Gfx.SANS:
            self.family = 'Helvetica'
        else:
            if ftype == Gfx.SERIF:
                self.family = 'Times'
            else:
                if ftype == Gfx.FIXED:
                    self.family = 'Courier'
                else:
                    raise ValueError("'type' must be SANS, SERIF or FIXED !")
                if size == Gfx.SMALL:
                    self.size = '8'
                else:
                    if size == Gfx.NORMAL:
                        self.size = '12'
                    else:
                        if size == Gfx.LARGE:
                            self.size = '16'
                        else:
                            raise ValueError("'size' must be SMALL or NORMAL or LARGE !")
                if 'i' in weight:
                    self.slant = 'italic'
                else:
                    self.slant = 'roman'
            if 'b' in weight:
                self.weight = 'bold'
            else:
                self.weight = 'bold'
        self.font = tkFont.Font(family=(self.family), size=(self.size), weight=(self.weight),
          slant=(self.slant))

    def getTextSize(self, text):
        return (
         len(text) * int(self.size) * 2 / 3, int(self.size))

    def clear(self, rgbTuple=(1.0, 1.0, 1.0)):
        self.canvas.delete('all')
        self.canvas.config(bg=(self.colorStr(rgbTuple)))

    def drawPoint(self, x, y):
        self.canvas.create_line((x + 1), (self.h - y), (x + 2), (self.h - y), width=(self.width),
          fill=(self.fg))

    def drawLine(self, x1, y1, x2, y2):
        self.canvas.create_line((x1 + 1), (self.h - y1), (x2 + 1), (self.h - y2), width=(self.width),
          dash=(self.dash),
          fill=(self.fg))

    def fillPoly(self, array):
        if array:
            coords = ()
            for point in array:
                coords += (point[0] + 1, self.h - point[1])

            self.canvas.create_polygon(coords, fill=(self.fg), stipple=(self.stipple))

    def writeStr(self, x, y, str, rotationAngle=0.0):
        if rotationAngle != 0.0:
            for i in range(len(str)):
                w, h = self.getTextSize(str[0:i])
                w *= 1.4
                xx = x + int(w * math.cos(math.pi * rotationAngle / 180.0) - 0.5)
                yy = y + int(w * math.sin(math.pi * rotationAngle / 180.0) - 0.5)
                if rotationAngle >= 315.0:
                    an = 'w'
                else:
                    if rotationAngle >= 270.0:
                        an = 'nw'
                    else:
                        if rotationAngle >= 225.0:
                            an = 'n'
                        else:
                            if rotationAngle >= 180.0:
                                an = 'ne'
                            else:
                                if rotationAngle >= 135.0:
                                    an = 'e'
                                else:
                                    if rotationAngle >= 90.0:
                                        an = 'se'
                                    else:
                                        if rotationAngle >= 45.0:
                                            an = 's'
                                        else:
                                            an = 'sw'
                self.canvas.create_text(xx, (self.h - yy), text=(str[i]), anchor=an, font=(self.font),
                  fill=(self.fg))

        else:
            self.canvas.create_text((x + 1), (self.h - y), text=str, anchor='sw', font=(self.font),
              fill=(self.fg))


class Window(Driver, Gfx.Window):

    def __init__(self, size=(640, 480), title='tkGraph'):
        self.root = Tk()
        self.root.title(title)
        self.root.protocol = ('WM_DELETE_WINDOW', self.quit)
        self.graph = Canvas((self.root), width=(size[0]), height=(size[1]))
        self.graph.pack()
        self.root.update()
        Driver.__init__(self, self.graph)

    def refresh(self):
        self.root.update()

    def quit(self):
        self.root.destroy()

    def waitUntilClosed(self):
        self.root.mainloop()

    def dumpPS(self, fileName):
        f = open(fileName, 'w')
        f.write(self.graph.postscript())
        f.close()


if __name__ == '__main__':
    import systemTest
    systemTest.Test_tkGfx()