# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.6/site-packages/PyPlotter/canvasGfx.py
# Compiled at: 2017-09-02 15:42:18
# Size of source mod 2**32: 6490 bytes
"""Implements Gfx.Driver using Canvas. 

Requires the transcrypt Python -> Javascript transpiler (http://transcrypt.org/)
"""
import Gfx
document = window = Math = Date = 0
driverName = 'canvasGfx'

class Driver(Gfx.Driver):
    __doc__ = 'A graphics driver for  Tkinter.\n    For an explanation of the inherited methods see Gfx.py.\n    '

    def __init__(self, canvas):
        """Initialize Driver for a Tkinter Canvas Object."""
        self.canvas = canvas
        self.context = canvas.getContext('2d')
        self.resizedGfx()
        self.reset()
        self.clear()

    def colorStr(self, rgbTuple):
        """rgbTuple -> string (eg. '#A0A0F3')"""

        def hex(c):
            ci = max(0, min(255, int(round(c * 255))))
            hdigits = '0123456789ABCDEF'
            return hdigits[(ci // 16)] + hdigits[(ci % 16)]

        return '#' + hex(rgbTuple[0]) + hex(rgbTuple[1]) + hex(rgbTuple[2])

    def resizedGfx(self):
        """Take notice if the undelying device has been resized."""
        self.w = int(self.canvas.clientWidth)
        self.h = int(self.canvas.clientHeight)

    def getSize(self):
        return (
         self.w, self.h)

    def setColor(self, rgbTuple):
        self.color = rgbTuple
        self.fg = self.colorStr(rgbTuple)
        self.context.strokeStyle = self.fg
        self.context.fillStyle = self.fg

    def setLineWidth(self, width):
        self.lineWidth = width
        if width == Gfx.THIN:
            self.context.lineWidth = 1
        else:
            if width == Gfx.MEDIUM:
                self.context.lineWidth = 2
            else:
                if width == Gfx.THICK:
                    self.context.lineWidth = 3
                else:
                    raise ValueError("'thickness' must be THIN, MEDIUM or THICK !")

    def setLinePattern(self, pattern):
        """Set line pattern (CONTINOUS, DASHED or DOTTED)."""
        self.linePattern = pattern
        if pattern == Gfx.CONTINUOUS:
            self.context.setLineDash([])
        else:
            if pattern == Gfx.DASHED:
                self.context.setLineDash([5, 5])
            else:
                if pattern == Gfx.DOTTED:
                    self.context.setLineDash([2, 4])
                else:
                    raise ValueError("'pattern' must be CONTINUOUS, DASHED or DOTTED !")

    def setFillPattern(self, pattern):
        """Not yet implemented for HTML Canvas! 
        Set pattern for filled areas (SOLID or PATTERNED)."""
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
            family = 'sans-serif'
        else:
            if ftype == Gfx.SERIF:
                family = 'serif'
            else:
                if ftype == Gfx.FIXED:
                    family = 'monospace'
                else:
                    raise ValueError("'type' must be SANS, SERIF or FIXED !")
                if size == Gfx.SMALL:
                    size = '8px'
                else:
                    if size == Gfx.NORMAL:
                        size = '12px'
                    else:
                        if size == Gfx.LARGE:
                            size = '16px'
                        else:
                            raise ValueError("'size' must be SMALL or NORMAL or LARGE !")
                if 'i' in weight:
                    slant = 'italic'
                else:
                    slant = ''
            if 'b' in weight:
                weight = 'bold'
            else:
                weight = ''
        self.context.font = ' '.join([slant, weight, size, family])

    def getTextSize(self, text):
        return (
         len(text) * int(self.size) * 2 / 3, int(self.size))

    def drawLine(self, x1, y1, x2, y2):
        self.context.beginPath()
        self.context.moveTo(x1, self.h - y1 - 1)
        self.context.lineTo(x2, self.h - y2 - 1)
        self.context.stroke()

    def drawRect(self, x, y, w, h):
        """Draws a rectangle"""
        self.context.strokeRect(x, self.h - y - h, w, h)

    def drawPoly(self, array):
        if array:
            self.context.beginPath()
            for x, y in array:
                self.context.lineTo(x, self.h - y - 1)

            self.context.stroke()

    def fillRect(self, x, y, w, h):
        """Draws a filled rectangle"""
        self.context.fillRect(x, self.h - y - h, w, h)

    def fillPoly(self, array):
        if array:
            self.context.beginPath()
            for x, y in array:
                self.context.lineTo(x, self.h - y - 1)

            self.context.fill()

    def writeStr(self, x, y, text, rotationAngle=0.0):
        if abs(rotationAngle) < 0.01:
            self.context.fillText(text, x, self.h - y - 1)
        else:
            self.context.save()
            self.context.translate(x, self.h - y - 1)
            self.context.rotate(-rotationAngle * 3.1415926 / 180)
            self.context.translate(-x, -(self.h - y - 1))
            self.context.fillText(text, x, self.h - y - 1)
            self.context.restore()