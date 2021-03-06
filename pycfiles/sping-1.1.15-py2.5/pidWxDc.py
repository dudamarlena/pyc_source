# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sping\WX\pidWxDc.py
# Compiled at: 2008-04-09 15:29:55
"""a Sping  wrapper for wxPython DeviceContexts
spingWxDc.py

By Paul and Kevin Jacobs

History -

    1.0  Many fixes and the rest of required piddle functionality added.
    0.5  Much work done by Jeffrey Kunce on image support and code factoring.

SpingWxDc adds Sping -compatible methods to any wxPython DeviceContext.
It can be used any where a wxDC is used (onPaint, onDraw, etc).

Code factoring and pil image support by Jeffrey Kunce

see also sping.examples.wxDcDemo.py
"""
import wx, sping.pid

class SpingWxDc(sping.pid.Canvas):

    def __init__(self, aWxDc, size=(300, 300), name='spingWX'):
        sping.pid.Canvas.__init__(self, size, name)
        self.dc = aWxDc
        self.dc.BeginDrawing()

    def __del__(self):
        self.dc.EndDrawing()

    def _getWXcolor(self, color, default=None):
        """Converts Sping colors to wx colors"""
        if color is not None:
            if color == sping.pid.transparent:
                return
            elif color.red >= 0 and color.green >= 0 and color.blue >= 0:
                return wx.Color(color.red * 255, color.green * 255, color.blue * 255)
        if default is not None:
            return self._getWXcolor(default)
        else:
            return
        return

    def _getWXbrush(self, color, default_color=None):
        """Converts Sping colors to a wx brush"""
        if color == sping.pid.transparent:
            return wx.TRANSPARENT_BRUSH
        wxcolor = self._getWXcolor(color)
        if wxcolor is None:
            if default_color is not None:
                return self._getWXbrush(default_color)
            else:
                raise 'WXcanvas error:  Cannot create brush.'
        return wx.Brush(wxcolor)

    def _getWXpen(self, width, color, default_color=None):
        """Converts Sping colors to a wx pen"""
        if width is None or width < 0:
            width = self.defaultLineWidth
        if color == sping.pid.transparent:
            return wx.TRANSPARENT_PEN
        wxcolor = self._getWXcolor(color)
        if wxcolor is None:
            if default_color is not None:
                return self._getWXpen(width, default_color)
            else:
                raise 'WXcanvas error:  Cannot create pen.'
        return wx.Pen(wxcolor, width)

    def _getWXfont(self, font):
        """Returns a wxFont roughly equivalent to the requested Sping font"""
        if font is None:
            font = self.defaultFont
        if font.face is None or font.face == 'times':
            family = wx.DEFAULT
        elif font.face == 'courier' or font.face == 'monospaced':
            family = wx.MODERN
        elif font.face == 'helvetica' or font.face == 'sansserif':
            family = wx.SWISS
        elif font.face == 'serif' or font.face == 'symbol':
            family = wx.DEFAULT
        else:
            family = wx.DEFAULT
        weight = wx.NORMAL
        style = wx.NORMAL
        underline = 0
        if font.bold == 1:
            weight = wx.BOLD
        if font.underline == 1:
            underline = 1
        if font.italic == 1:
            style = wx.ITALIC
        return wx.Font(font.size, family, style, weight, underline)

    def _setWXfont(self, font=None):
        """set/return the current font for the dc
        jjk  10/28/99"""
        wx_font = self._getWXfont(font)
        self.dc.SetFont(wx_font)
        return wx_font

    def isInteractive(self):
        return 0

    def canUpdate(self):
        return 1

    def clear(self):
        self.dc.Clear()

    def stringWidth(self, s, font=None):
        """Return the logical width of the string if it were drawn         in the current font (defaults to self.font)."""
        wx_font = self._setWXfont(font)
        return self.dc.GetTextExtent(s)[0]

    def fontHeight(self, font=None):
        """Find the total height (ascent + descent) of the given font."""
        return self.fontAscent(font) + self.fontDescent(font)

    def fontAscent(self, font=None):
        """Find the ascent (height above base) of the given font."""
        wx_font = self._setWXfont(font)
        return self.dc.GetCharHeight() - self.fontDescent(font)

    def fontDescent(self, font=None):
        """Find the descent (extent below base) of the given font."""
        wx_font = self._setWXfont(font)
        extents = self.dc.GetFullTextExtent(' ', wx_font)
        return extents[2]

    def drawLine(self, x1, y1, x2, y2, color=None, width=None):
        """Draw a straight line between x1,y1 and x2,y2."""
        if width is None or width < 0:
            width = self.defaultLineWidth
        self.dc.SetPen(self._getWXpen(width, color, self.defaultLineColor))
        self.dc.DrawLine(x1, y1, x2, y2)
        return

    def drawString(self, s, x, y, font=None, color=None, angle=None):
        """Draw a string starting at location x,y.
        NOTE: the baseline goes on y; drawing covers (y-ascent,y+descent)
        Text rotation (angle%360 != 0) is not supported."""
        self._setWXfont(font)
        if color == sping.pid.transparent:
            return
        wx_color = self._getWXcolor(color, self.defaultLineColor)
        if wx_color is None:
            wx_color = wx.BLACK
        self.dc.SetTextForeground(wx_color)
        if '\n' in s or '\r' in s:
            s = s.replace('\r\n', '\n')
            s = s.replace('\n\r', '\n')
            lines = s.split('\n')
        else:
            lines = [
             s]
        if angle is not None:
            self._drawRotatedString(lines, x, y, font, wx_color, angle)
        line_height = self.fontHeight(font)
        for l in range(0, len(lines)):
            self.dc.DrawText(lines[l], x, y - self.fontAscent(font) + l * line_height)

        return

    def _drawRotatedString(self, lines, x, y, font=None, color=None, angle=0):
        import math
        if font is None:
            font = sping.pid.Font(face='helvetica')
            self._setWXfont(font)
        ascent = self.fontAscent(font)
        height = self.fontHeight(font)
        rad = angle * math.pi / 180.0
        s = math.sin(rad)
        c = math.cos(rad)
        dx = s * height
        dy = c * height
        lx = x - dx
        ly = y - c * ascent
        for i in range(0, len(lines)):
            self.dc.DrawRotatedText(lines[i], lx + i * dx, ly + i * dy, angle)

        return

    def drawPolygon(self, pointlist, edgeColor=None, edgeWidth=None, fillColor=None, closed=0):
        """
        drawPolygon(pointlist) -- draws a polygon 
        pointlist: a list of (x,y) tuples defining vertices
        closed:    if 1, adds an extra segment connecting the last point 
            to the first
        """
        self.dc.SetPen(wx.TRANSPARENT_PEN)
        self.dc.SetBrush(self._getWXbrush(fillColor, self.defaultFillColor))
        pointlist = map(lambda i: tuple(i), pointlist)
        if closed == 1:
            pointlist.append(pointlist[0])
        self.dc.DrawPolygon(pointlist)
        linelist = []
        if len(pointlist) > 1:
            for i in range(1, len(pointlist)):
                linelist.append((pointlist[(i - 1)][0],
                 pointlist[(i - 1)][1],
                 pointlist[i][0],
                 pointlist[i][1]))
            else:
                linelist.append((pointlist[0][0],
                 pointlist[0][1],
                 pointlist[0][0],
                 pointlist[0][1]))
        self.drawLines(linelist, edgeColor, edgeWidth)

    def drawImage(self, image, x1, y1, x2=None, y2=None):
        """Draw a PIL Image into the specified rectangle.  If x2 and y2 are
        omitted, they are calculated from the image size.
        jjk  11/03/99"""
        try:
            from PIL import Image
        except ImportError:
            print 'PIL not installed as package'
            try:
                import Image
            except ImportError:
                raise 'PIL not available!'

        if x2 and y2 and x2 > x1 and y2 > y1:
            imgPil = image.resize((x2 - x1, y2 - y1))
        else:
            imgPil = image
        if imgPil.mode != 'RGB':
            imgPil = imgPil.convert('RGB')
        imgData = imgPil.tostring('raw', 'RGB')
        imgWx = wx.EmptyImage(imgPil.size[0], imgPil.size[1])
        imgWx.SetData(imgData)
        self.dc.DrawBitmap(imgWx.ConvertToBitmap(), x1, y1)