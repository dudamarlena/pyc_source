# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sping\PIL\pidPIL.py
# Compiled at: 2008-04-09 20:33:23
"""pidPIL

This module implements a Python Imaging Library SPING canvas.
In other words, this is a SPING backend that renders into a
PIL Image object.  From there, you can save as GIF, plot into
another SPING canvas, etc.
                
Joe Strout (joe@strout.net), 10/26/99
modified for use with sping.
"""
from sping.pid import *
import string, os
try:
    import Image, ImageFont, ImageDraw
except ImportError:
    try:
        from PIL import Image, ImageFont, ImageDraw
    except ImportError:
        raise ImportError("Couldn't find Image or PIL.Image")

if __name__ == '__main__':
    _fontprefix = os.path.join(os.curdir, 'pilfonts')
else:
    _fontprefix = os.path.join(os.path.split(__file__)[0], 'pilfonts')
try:
    try:
        f = open(os.path.join(_fontprefix, 'metrics.dat'), 'rb')
        import cPickle
        _widthmaps = cPickle.load(f)
        _ascents = cPickle.load(f)
        _descents = cPickle.load(f)
        f.close()
    except:
        print 'Warning: unable to load font metrics!'
        _widthmaps = {}
        _ascents = {}
        _descents = {}

finally:
    pass

def _closestSize(size):
    supported = [
     8, 10, 12, 14, 18, 24]
    if size in supported:
        return size
    best = supported[0]
    bestdist = abs(size - best)
    for trial in supported[1:]:
        dist = abs(size - trial)
        if dist < bestdist:
            best = trial
            bestdist = dist

    return best


def _pilFontPath(face, size, bold=0):
    if face == 'monospaced':
        face = 'courier'
    elif face == 'serif':
        face = 'times'
    elif face == 'sansserif' or face == 'system':
        face = 'helvetica'
    if bold and face != 'symbol':
        fname = '%s-bold-%d.pil' % (face, size)
    else:
        fname = '%s-%d.pil' % (face, size)
    path = os.path.join(_fontprefix, fname)
    return path


def _matchingFontPath(font):
    if font.face:
        face = font.face
    else:
        face = 'times'
    size = _closestSize(font.size)
    if type(face) == StringType:
        path = _pilFontPath(face, size, font.bold)
        path = string.split(path, os.sep)[(-1)]
        if path in _widthmaps.keys():
            return path
    for item in font.face:
        path = _pilFontPath(item, size, font.bold)
        path = string.split(path, os.sep)[(-1)]
        if path in _widthmaps.keys():
            return path

    path = _pilFontPath('courier', size, font.bold)
    return string.split(path, os.sep)[(-1)]


def _pilFont(font):
    if font.face:
        face = font.face
    else:
        face = 'times'
    size = _closestSize(font.size)
    if type(face) == StringType:
        try:
            pilfont = ImageFont.load_path(_pilFontPath(face, size, font.bold))
        except:
            return 0

    else:
        for item in font.face:
            pilfont = None
            try:
                pilfont = ImageFont.load_path(_pilFontPath(item, size, font.bold))
                break
            except:
                pass

        if pilfont == None:
            return 0
    return pilfont


def _pilColor(spingColor, defaultIfNoneColor):
    color = spingColor or defaultIfNoneColor
    if color == transparent:
        return
    else:
        return (
         int(color.red * 255), int(color.green * 255), int(color.blue * 255))
    return


class PILCanvas(Canvas):

    def __init__(self, size=(300, 300), name='spingPIL'):
        self._image = Image.new('RGB', size, (255, 255, 255))
        self._pen = ImageDraw.ImageDraw(self._image)
        Canvas.__init__(self, size, name)

    def getImage(self):
        return self._image

    def save(self, file=None, format=None):
        """format may be a string specifying a file extension corresponding to
        an image file format. Ex: 'png', 'jpeg', 'gif', 'tif' etc.
        These are defined by PIL, not by us so you need to check the docs.
        In general, I just specify an extension and let format default to None"""
        file = file or self.name
        if hasattr(file, 'write'):
            self._image.save(file, format)
            return
        if format == None:
            if '.' not in file:
                filename = file + '.png'
            else:
                filename = file
        else:
            filename = file + '.' + format
        self._image.save(filename, format=format)
        return

    def clear(self):
        self.drawRect(0, 0, self.size[0], self.size[1], edgeColor=yellow, fillColor=white)

    def stringWidth(self, s, font=None):
        """Return the logical width of the string if it were drawn         in the current font (defaults to self.defaultFont)."""
        if not font:
            font = self.defaultFont
        if not _widthmaps:
            return font.size * len(s)
        path = _matchingFontPath(font)
        map = _widthmaps[path]
        out = 0
        for c in s:
            out = out + map[c]

        return out

    def fontAscent(self, font=None):
        """Find the ascent (height above base) of the given font."""
        if not font:
            font = self.defaultFont
        if not _ascents:
            return font.size
        path = _matchingFontPath(font)
        return _ascents[path]

    def fontDescent(self, font=None):
        """Find the descent (extent below base) of the given font."""
        if not font:
            font = self.defaultFont
        if not _descents:
            return font.size / 2
        path = _matchingFontPath(font)
        return _descents[path]

    def drawLine(self, x1, y1, x2, y2, color=None, width=None):
        """Draw a straight line between x1,y1 and x2,y2."""
        pilColor = _pilColor(color, self.defaultLineColor)
        w = width or self.defaultLineWidth
        if w > 1:
            hw = int((w - 1) / 2)
            pts = []
            if x1 <= x2 and y1 <= y2:
                pts.append((x1 - hw + w, y1 - hw))
                pts.append((x1 - hw, y1 - hw))
                pts.append((x1 - hw, y1 - hw + w))
                pts.append((x2 - hw, y2 - hw + w))
                pts.append((x2 - hw + w, y2 - hw + w))
                pts.append((x2 - hw + w, y2 - hw))
            elif x1 <= x2:
                pts.append((x1 - hw, y1 - hw))
                pts.append((x1 - hw, y1 - hw + w))
                pts.append((x1 - hw + w, y1 - hw + w))
                pts.append((x2 - hw + w, y2 - hw + w))
                pts.append((x2 - hw + w, y2 - hw))
                pts.append((x2 - hw, y2 - hw))
            elif y1 <= y2:
                pts.append((x1 - hw + w, y1 - hw + w))
                pts.append((x1 - hw + w, y1 - hw))
                pts.append((x1 - hw, y1 - hw))
                pts.append((x2 - hw, y2 - hw))
                pts.append((x2 - hw, y2 - hw + w))
                pts.append((x2 - hw + w, y2 - hw + w))
            else:
                pts.append((x1 - hw, y1 - hw + w))
                pts.append((x1 - hw + w, y1 - hw + w))
                pts.append((x1 - hw + w, y1 - hw))
                pts.append((x2 - hw + w, y2 - hw))
                pts.append((x2 - hw, y2 - hw))
                pts.append((x2 - hw, y2 - hw + w))
            self._pen.polygon(pts, fill=pilColor, outline=None)
        else:
            self._pen.line((x1, y1, x2, y2), fill=pilColor)
        return

    def drawPolygon(self, pointlist, edgeColor=None, edgeWidth=None, fillColor=None, closed=0):
        """drawPolygon(pointlist) -- draws a polygon
        pointlist: a list of (x,y) tuples defining vertices
        """
        pts = list(pointlist)
        for i in range(len(pts)):
            pts[i] = tuple(pts[i])

        pilFill = _pilColor(fillColor, self.defaultFillColor)
        pilEdge = _pilColor(edgeColor, self.defaultLineColor)
        if pilFill:
            self._pen.polygon(pts, fill=pilFill, outline=pilEdge)
        width = edgeWidth if edgeWidth != None else self.defaultLineWidth
        customEdge = width > 1 or closed or pts[0][0] == pts[(-1)][0] and pts[0][1] == pts[(-1)][1]
        if pilEdge and customEdge:
            oldp = pts[0]
            if closed:
                pts.append(oldp)
            for p in pts[1:]:
                self.drawLine(oldp[0], oldp[1], p[0], p[1], edgeColor, width)
                oldp = p

        return

    def drawString(self, s, x, y, font=None, color=None, angle=0):
        """Draw a string starting at location x,y."""
        if '\n' in s or '\r' in s:
            self.drawMultiLineString(s, x, y, font, color, angle)
            return
        if not font:
            font = self.defaultFont
        if not color:
            color = self.defaultLineColor
        if color == transparent:
            return
        sHeight = self.fontAscent(font) + self.fontDescent(font)
        sWidth = self.stringWidth(s, font)
        tempsize = max(sWidth * 1.2, sHeight * 2.0)
        tempimg = Image.new('RGB', (int(tempsize), int(tempsize)), (0, 0, 0))
        temppen = ImageDraw.ImageDraw(tempimg)
        pilfont = _pilFont(font)
        if not pilfont:
            raise 'bad font!', font
        pos = [
         4, int(tempsize / 2 - self.fontAscent(font)) - self.fontDescent(font)]
        temppen.text(pos, s, font=pilfont, fill=(255, 255, 255))
        pos[1] = int(tempsize / 2)
        if font.underline:
            ydown = 0.5 * self.fontDescent(font)
            temppen.line([(pos[0], pos[1] + ydown), (pos[0] + sWidth, pos[1] + ydown)])
        if angle:
            from math import pi, sin, cos
            tempimg = tempimg.rotate(angle, Image.BILINEAR)
            temppen = ImageDraw.ImageDraw(tempimg)
            radians = -angle * pi / 180.0
            r = tempsize / 2 - pos[0]
            pos[0] = int(tempsize / 2 - r * cos(radians))
            pos[1] = int(pos[1] - r * sin(radians))
        mask = tempimg.convert('L').point(lambda c: c)
        temppen.rectangle((0, 0, tempsize, tempsize), fill=_pilColor(color, None))
        self._image.paste(tempimg, (int(x) - pos[0], int(y) - pos[1]), mask)
        return

    def drawImage(self, image, x1, y1, x2=None, y2=None):
        """Draw a PIL Image into the specified rectangle.  If x2 and y2 are
        omitted, they are calculated from the image size."""
        if x2 and y2:
            bbox = image.getbbox()
            if x2 - x1 != bbox[2] - bbox[0] or y2 - y1 != bbox[3] - bbox[1]:
                image = image.resize((x2 - x1, y2 - y1))
        self._image.paste(image, (x1, y1))


def test():
    canvas = PILCanvas()
    canvas.defaultLineColor = Color(0.7, 0.7, 1.0)
    canvas.drawLines(map(lambda i: (i * 10, 0, i * 10, 300), range(30)))
    canvas.drawLines(map(lambda i: (0, i * 10, 300, i * 10), range(30)))
    canvas.defaultLineColor = black
    canvas.drawLine(10, 200, 20, 190, color=red)
    canvas.drawEllipse(130, 30, 200, 100, fillColor=yellow, edgeWidth=4)
    canvas.drawArc(130, 30, 200, 100, 45, 50, fillColor=blue, edgeColor=navy, edgeWidth=4)
    canvas.defaultLineWidth = 4
    canvas.drawRoundRect(30, 30, 100, 100, fillColor=blue, edgeColor=maroon)
    canvas.drawCurve(20, 20, 100, 50, 50, 100, 160, 160)
    canvas.drawString('This is a test!', 30, 130, Font(face='times', size=16, bold=1), color=green, angle=-45)
    canvas.drawString('This is a test!', 30, 130, color=red, angle=-45)
    polypoints = [
     (160, 120), (130, 190), (210, 145), (110, 145), (190, 190)]
    canvas.drawPolygon(polypoints, fillColor=lime, edgeColor=red, edgeWidth=3, closed=1)
    canvas.drawRect(200, 200, 260, 260, edgeColor=yellow, edgeWidth=5)
    canvas.drawLine(200, 260, 260, 260, color=green, width=5)
    canvas.drawLine(260, 200, 260, 260, color=red, width=5)
    canvas.flush()
    canvas.getImage().save('test.png')
    return canvas


def testit(canvas, s, x, y, font=None):
    canvas.defaultLineColor = black
    canvas.drawString(s, x, y, font=font)
    canvas.defaultLineColor = blue
    w = canvas.stringWidth(s, font=font)
    canvas.drawLine(x, y, x + w, y)
    canvas.drawLine(x, y - canvas.fontAscent(font=font), x + w, y - canvas.fontAscent(font=font))
    canvas.drawLine(x, y + canvas.fontDescent(font=font), x + w, y + canvas.fontDescent(font=font))


def test2():
    global dammit
    global qdcanvas
    canvas = PILCanvas()
    testit(canvas, 'Foogar', 20, 30)
    testit(canvas, 'Foogar', 20, 90, font=Font(size=24))
    dammit = _pilFont(Font(size=24))
    testit(canvas, 'Foogar', 20, 150, font=Font(face='courier', size=24))
    testit(canvas, 'Foogar', 20, 240, font=Font(face='courier'))
    import spingQD
    try:
        qdcanvas.close()
    except:
        pass

    qdcanvas = spingQD.QDCanvas()
    qdcanvas.drawImage(canvas.getImage(), 0, 0)


if __name__ == '__main__':
    test()