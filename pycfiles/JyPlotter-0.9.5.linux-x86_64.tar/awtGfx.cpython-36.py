# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.6/site-packages/PyPlotter/awtGfx.py
# Compiled at: 2015-02-27 13:11:06
# Size of source mod 2**32: 10930 bytes
"""Implementes Gfx.Driver for the java awt.
"""
import math, java, pawt
from java import awt, applet
import Gfx
from Compatibility import *
driverName = 'awtGfx'
white = java.awt.Color.WHITE
black = java.awt.Color.BLACK

class Driver(Gfx.Driver):
    __doc__ = 'A simple graphics layer on top of teh java awt.\n    See GfxInterface.py\n    '

    def __init__(self, awtObject):
        """Initialize canvas on an awt component or image.
        """
        Gfx.Driver.__init__(self)
        self.stroke_width = 1.0
        self.stroke_dash = [1.0]
        self.stroke = None
        self.paint = None
        self.w, self.h = (640, 480)
        self.fsize = 12
        self.awtObject = None
        self.graphics = None
        self.pattern = awt.image.BufferedImage(16, 16, awt.image.BufferedImage.TYPE_INT_RGB)
        self.changeGfx(awtObject)
        self.setAntialias(True)

    def setAntialias(self, onOff):
        if onOff:
            rh = awt.RenderingHints(awt.RenderingHints.KEY_ANTIALIASING, awt.RenderingHints.VALUE_ANTIALIAS_ON)
            rh.put(awt.RenderingHints.KEY_TEXT_ANTIALIASING, awt.RenderingHints.VALUE_TEXT_ANTIALIAS_ON)
        else:
            rh = awt.RenderingHints(awt.RenderingHints.KEY_ANTIALIASING, awt.RenderingHints.VALUE_ANTIALIAS_OFF)
            rh.put(awt.RenderingHints.KEY_TEXT_ANTIALIASING, awt.RenderingHints.VALUE_TEXT_ANTIALIAS_OFF)
        self.graphics.setRenderingHints(rh)

    def _updateStroke(self):
        if len(self.stroke_dash) > 1:
            self.stroke = awt.BasicStroke(self.stroke_width, awt.BasicStroke.CAP_BUTT, awt.BasicStroke.JOIN_BEVEL, 10.0, self.stroke_dash, 0.0)
        else:
            self.stroke = awt.BasicStroke(self.stroke_width, awt.BasicStroke.CAP_BUTT, awt.BasicStroke.JOIN_BEVEL, 10.0)
        self.graphics.setStroke(self.stroke)

    def _updatePaint(self):
        awtColor = awt.Color(self.color[0], self.color[1], self.color[2])
        if self.fillPattern == Gfx.SOLID:
            self.graphics.setColor(awtColor)
            self.graphics.setPaint(awtColor)
            self.paint = awtColor
            return
        else:
            gr = self.pattern.createGraphics()
            gr.setColor(awt.Color(255, 255, 255))
            gr.fillRect(0, 0, 16, 16)
            gr.setColor(awtColor)
            if self.fillPattern == Gfx.PATTERN_A:
                for x in range(0, 16, 4):
                    gr.drawLine(x, 0, x + 16, 16)
                    gr.drawLine(x + 1, 0, x + 17, 16)
                    gr.drawLine(x - 16, 0, x, 16)
                    gr.drawLine(x - 15, 0, x + 1, 16)

            else:
                if self.fillPattern == Gfx.PATTERN_B:
                    for x in range(0, 16, 4):
                        gr.drawLine(x, 0, x - 16, 16)
                        gr.drawLine(x + 1, 0, x - 15, 16)
                        gr.drawLine(x + 16, 0, x, 16)
                        gr.drawLine(x + 17, 0, x + 1, 16)

                else:
                    if self.fillPattern == Gfx.PATTERN_C:
                        for x in range(0, 16, 4):
                            for y in range(0, 16, 4):
                                gr.fillRect(x, y, 2, 2)

                    else:
                        raise ValueError("'pattern' must be 'solid' or 'patternA', " + "'patternB', 'patternC' !")
        self.paint = awt.TexturePaint(self.pattern, awt.Rectangle(16, 16))

    def changeGfx(self, awtObject):
        """Change the awt object (either image or awt component)"""
        self.awtObject = awtObject
        self.graphics = self.awtObject.getGraphics()
        self._updateStroke()
        self.resizedGfx()
        self.reset()

    def resizedGfx(self):
        self.w = self.awtObject.getWidth()
        self.h = self.awtObject.getHeight()

    def getSize(self):
        return (
         self.w, self.h)

    def getResolution(self):
        return 100

    def setColor(self, rgbTuple):
        self.color = rgbTuple
        awtColor = awt.Color(rgbTuple[0], rgbTuple[1], rgbTuple[2])
        self.graphics.setPaint(awtColor)
        self.graphics.setColor(awtColor)
        self._updatePaint()

    def setLineWidth(self, width):
        self.lineWidth = width
        if width == Gfx.THIN:
            self.stroke_width = 1.0
        else:
            if width == Gfx.MEDIUM:
                self.stroke_width = 2.0
            else:
                if width == Gfx.THICK:
                    self.stroke_width = 3.0
                else:
                    raise ValueError("'thickness' must be 'thin', 'medium' or 'thick' !")
        self._updateStroke()

    def setLinePattern(self, pattern):
        self.linePattern = pattern
        if pattern == Gfx.CONTINUOUS:
            self.stroke_dash = [
             1.0]
        else:
            if pattern == Gfx.DASHED:
                self.stroke_dash = [
                 5.0, 5.0]
            else:
                if pattern == Gfx.DOTTED:
                    self.stroke_dash = [
                     2.0, 2.0]
                else:
                    raise ValueError("'pattern' must be 'continuous', " + "'dashed' or 'dotted' !")
        self._updateStroke()

    def setFillPattern(self, pattern):
        self.fillPattern = pattern
        self._updatePaint()

    def setFont(self, ftype, size, weight):
        self.fontType = ftype
        self.fontSize = size
        self.fontWeight = weight
        if ftype == Gfx.SANS:
            ff = 'SansSerif'
        else:
            if ftype == Gfx.SERIF:
                ff = 'Serif'
            else:
                if ftype == Gfx.FIXED:
                    ff = 'Monospaced'
                else:
                    raise ValueError("'type' must be 'sans', 'serif' or 'fixed' !")
                if size == Gfx.SMALL:
                    fsize = 10
                else:
                    if size == Gfx.NORMAL:
                        fsize = 14
                    else:
                        if size == Gfx.LARGE:
                            fsize = 18
                        else:
                            raise ValueError("'size' must be 'small', 'normal' or 'large' !")
                self.fsize = fsize
                fst = 0
                if 'i' in weight:
                    fst |= awt.Font.ITALIC
                elif 'b' in weight:
                    fst |= awt.Font.BOLD
        self.graphics.setFont(awt.Font(ff, fst, fsize))

    def getTextSize(self, text):
        return (
         len(text) * self.fsize * 2 / 3, self.fsize)

    def drawLine(self, x1, y1, x2, y2):
        self.graphics.drawLine(x1, self.h - y1 - 1, x2, self.h - y2 - 1)

    def drawPoly(self, array):
        xpoints = [x for x, y in array]
        ypoints = [self.h - y - 1 for x, y in array]
        self.graphics.drawPolyline(xpoints, ypoints, len(array))

    def drawRect(self, x, y, w, h):
        self.graphics.drawRect(x, self.h - y - h, w - 1, h - 1)

    def fillRect(self, x, y, w, h):
        self.graphics.setPaint(self.paint)
        self.graphics.fillRect(x, self.h - y - h, w, h)
        self.graphics.setPaint(awt.Color(self.color[0], self.color[1], self.color[2]))

    def fillPoly(self, array):
        if len(array) == 0:
            return
        xpoints = [x for x, y in array]
        ypoints = [self.h - y - 1 for x, y in array]
        self.graphics.setPaint(self.paint)
        self.graphics.fillPolygon(xpoints, ypoints, len(array))
        self.graphics.setPaint(self.paint)

    def writeStr(self, x, y, str, rotationAngle=0.0):
        w, h = self.getTextSize(str)
        if rotationAngle == 0.0:
            self.graphics.drawString(str, x, self.h - y)
        else:
            af = awt.geom.AffineTransform()
            theta = (360.0 - rotationAngle) * math.pi / 180.0
            af.rotate(theta, x, self.h - y)
            saveAT = self.graphics.getTransform()
            self.graphics.setTransform(af)
            self.graphics.drawString(str, x, self.h - y)
            self.graphics.setTransform(saveAT)


myCanvas = None
myApplet = None

class Canvas(awt.Canvas):

    def __init__(self):
        self.win = None

    def setWin(self, win):
        self.win = win

    def paint(self, g):
        if self.win != None:
            self.win.refresh()


class Applet(applet.Applet):

    def init(self):
        self.setLayout(awt.BorderLayout())
        self.panel = awt.Panel()
        self.panel.setLayout(awt.BorderLayout())
        self.canvas = Canvas()
        self.panel.add(self.canvas)
        self.add(self.panel)


class Window(Driver, Gfx.Window):

    def __init__(self, size=(640, 480), title='awtGraph'):
        global myApplet
        global myCanvas
        if myCanvas == None:
            if myApplet == None:
                myApplet = Applet()
                pawt.test(myApplet, name=title, size=(size[0] + 8, size[1] + 30))
            myCanvas = myApplet.canvas
        dcfg = myCanvas.getGraphics().getDeviceConfiguration()
        self.image = dcfg.createCompatibleImage(size[0], size[1])
        Driver.__init__(self, self.image)
        if isinstance(myCanvas, Canvas):
            myCanvas.setWin(self)

    def refresh(self):
        myCanvas.getGraphics().drawImage(self.image, None, 0, 0)

    def quit(self):
        pass

    def waitUntilClosed(self):
        self.refresh()


if __name__ == '__main__':
    import systemTest
    systemTest.Test_awtGfx()