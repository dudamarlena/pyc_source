# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sping\TK\pidTK.py
# Compiled at: 2008-08-12 13:58:40
""" 
A Tkinter based backend for sping. 
  
Perry A. Stoll 
  
Created: February 15, 1999 
  
Requires PIL for rotated string support.

Known Problems: 
     - Doesn't handle the interactive commands yet.
     - PIL based canvas inherits lack of underlining strings from pidPIL
     
You can find the latest version of this file:
    via http://sping.sourceforge.net
"""
import Tkinter, tkFont
tk = Tkinter
import sping.pid, string
__version__ = '0.3'
__date__ = 'April 8, 1999'
__author__ = 'Perry Stoll,  perry.stoll@mail.com '

class FontManager():
    __alt_faces = {'serif': 'Times', 'sansserif': 'Helvetica', 
       'monospaced': 'Courier'}

    def __init__(self, master):
        self.master = master
        self.font_cache = {}

    def stringWidth(self, s, font):
        tkfont = self.spingToTkFont(font)
        return tkfont.measure(s)

    def fontHeight(self, font):
        tkfont = self.spingToTkFont(font)
        return self._tkfontHeight(tkfont)

    def fontAscent(self, font):
        tkfont = self.spingToTkFont(font)
        return self._tkfontAscent(tkfont)

    def fontDescent(self, font):
        tkfont = self.spingToTkFont(font)
        return self._tkfontDescent(tkfont)

    def getTkFontString(self, font):
        """Return a string suitable to pass as the -font option to
        to a Tk widget based on the sping-style FONT"""
        tkfont = self.spingToTkFont(font)
        return '-family %(family)s -size %(size)s -weight %(weight)s -slant %(slant)s -underline %(underline)s' % tkfont.config()

    def getTkFontName(self, font):
        """Return a the name associated with the sping-style FONT"""
        tkfont = self.spingToTkFont(font)
        return str(tkfont)

    def spingToTkFont(self, font):
        """Return a tkFont instance based on the pid-style FONT"""
        if font is None:
            return ''
        size = 12
        family = 'Times'
        weight = 'normal'
        slant = 'roman'
        underline = 'false'
        if font.face:
            f = string.lower(font.face)
            if self.__alt_faces.has_key(f):
                family = self.__alt_faces[f]
            else:
                family = font.face
        size = font.size or 12
        if font.bold:
            weight = 'bold'
        if font.italic:
            slant = 'italic'
        if font.underline:
            underline = 'true'
        key = (
         family, size, weight, slant, underline)
        if self.font_cache.has_key(key):
            font = self.font_cache[key]
        else:
            font = tkFont.Font(self.master, family=family, size=size, weight=weight, slant=slant, underline=underline)
            self.font_cache[(family, size, weight, slant, underline)] = font
        return font

    def _tkfontAscent(self, tkfont):
        return tkfont.metrics('ascent')

    def _tkfontDescent(self, tkfont):
        return tkfont.metrics('descent')


class TKCanvas(tk.Canvas, sping.pid.Canvas):
    __TRANSPARENT = ''

    def __init__(self, size=(300, 300), name='sping.TK', master=None, scrollingViewPortSize=None, **kw):
        """This canvas allows you to add a tk.Canvas with a sping API for drawing.
        To add scrollbars, the simpliest method is to set the 'scrollingViewPortSize'
        equal to a tuple that describes the width and height of the visible porition
        of the canvas on screen.  This sets scrollregion=(0,0, size[0], size[1]).
        Then you can add scrollbars as you would any tk.Canvas.

        Note, because this is a subclass of tk.Canvas, you can use the normal keywords
        to specify a tk.Canvas with scrollbars, however, you should then be careful to
        set the "scrollregion" option to the same size as the 'size' passed to __init__.
        Tkinter's scrollregion option essentially makes 'size' ignored.  """
        sping.pid.Canvas.__init__(self, size=size, name=size)
        if scrollingViewPortSize:
            kw['scrollregion'] = (
             0, 0, size[0], size[1])
            kw['height'] = scrollingViewPortSize[0]
            kw['width'] = scrollingViewPortSize[1]
        else:
            kw['width'] = size[0]
            kw['height'] = size[1]
        apply(tk.Canvas.__init__, (self, master), kw)
        self.config(background='white')
        (self.width, self.height) = size
        self._font_manager = FontManager(self)
        self._configure()
        self._item_ids = []
        self._images = []

    def _configure(self, *a, **kw):
        pass

    def _display(self):
        self.flush()
        self.mainloop()

    def _quit(self):
        self.quit()

    def _to_ps_file(self, filename):
        self.postscript(file=filename)

    def isInteractive(self):
        return 0

    def onOver(self, event):
        pass

    def onClick(self, event):
        pass

    def onKey(self, event):
        pass

    def flush(self):
        tk.Canvas.update(self)

    def clear(self):
        map(self.delete, self._item_ids)
        self._item_ids = []

    def _colorToTkColor(self, c):
        return '#%02X%02X%02X' % (int(c.red * 255),
         int(c.green * 255),
         int(c.blue * 255))

    def _getTkColor(self, color, defaultColor):
        if color is None:
            color = defaultColor
        if color is sping.pid.transparent:
            color = self.__TRANSPARENT
        else:
            color = self._colorToTkColor(color)
        return color

    def drawLine(self, x1, y1, x2, y2, color=None, width=None):
        color = self._getTkColor(color, self.defaultLineColor)
        if width is None:
            width = self.defaultLineWidth
        new_item = self.create_line(x1, y1, x2, y2, fill=color, width=width)
        self._item_ids.append(new_item)
        return

    def stringWidth(self, s, font=None):
        return self._font_manager.stringWidth(s, font or self.defaultFont)

    def fontAscent(self, font=None):
        return self._font_manager.fontAscent(font or self.defaultFont)

    def fontDescent(self, font=None):
        return self._font_manager.fontDescent(font or self.defaultFont)

    def drawString(self, s, x, y, font=None, color=None, angle=None):
        if angle:
            try:
                self._drawRotatedString(s, x, y, font, color, angle)
                return
            except ImportError:
                print 'PIL not available. Using unrotated strings.'

        y = y - self.fontHeight(font) * 0.28
        color = self._getTkColor(color, self.defaultLineColor)
        font = self._font_manager.getTkFontString(font or self.defaultFont)
        new_item = self.create_text(x, y, text=s, font=font, fill=color, anchor=Tkinter.W)
        self._item_ids.append(new_item)

    def _drawRotatedString(self, s, x, y, font=None, color=None, angle=0):
        try:
            import sping.PIL.pidPIL
            try:
                import Image, ImageTk
            except ImportError:
                from PIL import Image, ImageTk

            pp = sping.PIL.pidPIL
        except ImportError:
            raise ImportError('Rotated strings only possible with PIL support')

        pilCan = pp.PILCanvas(size=(self.width, self.height))
        pilCan.defaultFont = self.defaultFont
        pilCan.defaultLineColor = self.defaultLineColor
        if '\n' in s or '\r' in s:
            self.drawMultiLineString(s, x, y, font, color, angle)
            return
        if not font:
            font = pilCan.defaultFont
        if not color:
            color = self.defaultLineColor
        if color == sping.pid.transparent:
            return
        tempsize = pilCan.stringWidth(s, font) * 1.2
        tempimg = Image.new('RGB', (tempsize, tempsize), (0, 0, 0))
        txtimg = Image.new('RGB', (tempsize, tempsize), (255, 255, 255))
        from PIL import ImageDraw
        temppen = ImageDraw.ImageDraw(tempimg)
        temppen.setink((255, 255, 255))
        pilfont = pp._pilFont(font)
        if not pilfont:
            raise 'bad font!', font
        temppen.setfont(pilfont)
        pos = [4, int(tempsize / 2 - pilCan.fontAscent(font)) - pilCan.fontDescent(font)]
        temppen.text(pos, s)
        pos[1] = int(tempsize / 2)
        if angle:
            from math import pi, sin, cos
            tempimg = tempimg.rotate(angle, Image.BILINEAR)
            temppen = ImageDraw.ImageDraw(tempimg)
            radians = -angle * pi / 180.0
            r = tempsize / 2 - pos[0]
            pos[0] = int(tempsize / 2 - r * cos(radians))
            pos[1] = int(pos[1] - r * sin(radians))
        mask = tempimg.convert('L').point(lambda c: c)
        temppen.setink((color.red * 255, color.green * 255, color.blue * 255))
        temppen.setfill(1)
        temppen.rectangle((0, 0, tempsize, tempsize))
        txtimg.paste(tempimg, (0, 0), mask)
        transp = txtimg.convert('RGBA')
        source = transp.split()
        (R, G, B, A) = (0, 1, 2, 3)
        mask = transp.point(lambda i: i < 255 and 255)
        source[A].paste(mask)
        transp = Image.merge(transp.mode, source)
        self.drawImage(transp, x - pos[0], y - pos[1])

    def drawRect(self, x1, y1, x2, y2, edgeColor=None, edgeWidth=None, fillColor=None):
        fillColor = self._getTkColor(fillColor, self.defaultFillColor)
        edgeColor = self._getTkColor(edgeColor, self.defaultLineColor)
        if edgeWidth is None:
            edgeWidth = self.defaultLineWidth
        new_item = self.create_rectangle(x1, y1, x2, y2, fill=fillColor, width=edgeWidth, outline=edgeColor)
        self._item_ids.append(new_item)
        return

    def drawEllipse(self, x1, y1, x2, y2, edgeColor=None, edgeWidth=None, fillColor=None):
        fillColor = self._getTkColor(fillColor, self.defaultFillColor)
        edgeColor = self._getTkColor(edgeColor, self.defaultLineColor)
        if edgeWidth is None:
            edgeWidth = self.defaultLineWidth
        new_item = self.create_oval(x1, y1, x2, y2, fill=fillColor, outline=edgeColor, width=edgeWidth)
        self._item_ids.append(new_item)
        return

    def drawArc(self, x1, y1, x2, y2, startAng=0, extent=360, edgeColor=None, edgeWidth=None, fillColor=None):
        fillColor = self._getTkColor(fillColor, self.defaultFillColor)
        edgeColor = self._getTkColor(edgeColor, self.defaultLineColor)
        if edgeWidth is None:
            edgeWidth = self.defaultLineWidth
        new_item = self.create_arc(x1, y1, x2, y2, start=startAng, extent=extent, fill=fillColor, width=edgeWidth, outline=edgeColor)
        self._item_ids.append(new_item)
        return

    def drawPolygon(self, pointlist, edgeColor=None, edgeWidth=None, fillColor=None, closed=0):
        fillColor = self._getTkColor(fillColor, self.defaultFillColor)
        edgeColor = self._getTkColor(edgeColor, self.defaultLineColor)
        if edgeWidth is None:
            edgeWidth = self.defaultLineWidth
        if closed:
            new_item = self.create_polygon(pointlist, fill=fillColor, width=edgeWidth, outline=edgeColor)
        elif fillColor == self.__TRANSPARENT:
            d = {'fill': edgeColor, 'width': edgeWidth}
            new_item = apply(self.create_line, pointlist, d)
        else:
            new_item = self.create_polygon(pointlist, fill=fillColor, outline=self.__TRANSPARENT)
            self._item_ids.append(new_item)
            d = {'fill': edgeColor, 'width': edgeWidth}
            new_item = apply(self.create_line, pointlist, d)
        self._item_ids.append(new_item)
        return

    def drawImage(self, image, x1, y1, x2=None, y2=None):
        try:
            from PIL import ImageTk
        except ImportError:
            raise NotImplementedError('drawImage - require the ImageTk module')

        (w, h) = image.size
        if not x2:
            x2 = w + x1
        if not y2:
            y2 = h + y1
        if w != x2 - x1 or h != y2 - y1:
            myimage = image.resize((x2 - x1, y2 - y1))
        else:
            myimage = image
        itk = ImageTk.PhotoImage(myimage, master=self)
        new_item = self.create_image(x1, y1, image=itk, anchor=Tkinter.NW)
        self._item_ids.append(new_item)
        self._images.append(itk)


try:
    import sping.PIL

    class TKCanvasPIL(sping.PIL.PILCanvas):
        """This canvas maintains a PILCanvas as its backbuffer.  Drawing calls
        are made to the backbuffer and flush() sends the image to the screen
        using TKCanvas.  
           You can also save what is displayed to a file in any of the formats
        supported by PIL"""

        def __init__(self, size=(300, 300), name='TKCanvas', master=None, **kw):
            sping.PIL.PILCanvas.__init__(self, size=size, name=name)
            self._tkcanvas = apply(TKCanvas, (size, name, master), kw)

        def flush(self):
            sping.PIL.PILCanvas.flush(self)
            self._tkcanvas.drawImage(self._image, 0, 0)
            self._tkcanvas.flush()

        def getTKCanvas(self):
            return self._tkcanvas


except ImportError:
    raise ImportError, 'TKCanvasPIL requires sping  PIL Canvas, PIL may not be installed'