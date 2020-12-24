# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sping\PS\pidPS.py
# Compiled at: 2002-01-21 21:51:42
"""
pidPS - formerly piddlePS - a PostScript backend for the PIDDLE drawing module

   Magnus Lie Hetland
   
   1999
"""
from sping.pid import *
import string, cStringIO, psmetrics, math
linesep = '\n'
PiddleLegalFonts = {'helvetica': 'helvetica', 'times': 'times', 
   'courier': 'courier', 
   'serif': 'times', 
   'sansserif': 'helvetica', 
   'monospaced': 'courier', 
   'symbol': 'symbol'}
Roman = 'Roman'
Bold = 'Bold'
Italic = 'Italic'
PSFontMapStdEnc = {('helvetica', Roman): 'Helvetica-Roman', ('helvetica', Bold): 'Helvetica-Bold', 
   ('helvetica', Italic): 'Helvetica-Oblique', 
   ('times', Roman): 'Times-Roman', 
   ('times', Bold): 'Times-Bold', 
   ('times', Italic): 'Times-Italic', 
   ('courier', Roman): 'Courier-Roman', 
   ('courier', Bold): 'Courier-Bold', 
   ('courier', Italic): 'Courier-Oblique', 
   ('symbol', Roman): 'Symbol', 
   ('symbol', Bold): 'Symbol', 
   ('symbol', Italic): 'Symbol', 
   'EncodingName': 'StandardEncoding'}
PSFontMapLatin1Enc = {('helvetica', Roman): 'Helvetica-Roman-ISOLatin1', ('helvetica', Bold): 'Helvetica-Bold-ISOLatin1', 
   ('helvetica', Italic): 'Helvetica-Oblique-ISOLatin1', 
   ('times', Roman): 'Times-Roman-ISOLatin1', 
   ('times', Bold): 'Times-Bold-ISOLatin1', 
   ('times', Italic): 'Times-Italic-ISOLatin1', 
   ('courier', Roman): 'Courier-Roman-ISOLatin1', 
   ('courier', Bold): 'Courier-Bold-ISOLatin1', 
   ('courier', Italic): 'Courier-Oblique-ISOLatin1', 
   ('symbol', Roman): 'Symbol', 
   ('symbol', Bold): 'Symbol', 
   ('symbol', Italic): 'Symbol', 
   'EncodingName': 'Latin1Encoding'}

def latin1FontEncoding(fontname):
    """use this to generating PS code for re-encoding a font as ISOLatin1
    from font with name 'fontname' defines reencoded font, 'fontname-ISOLatin1'"""
    latin1FontTemplate = '/%s findfont\ndup length dict begin\n  {1 index /FID ne\n        {def}\n        {pop pop}\n      ifelse\n   } forall\n   /Encoding ISOLatin1Encoding  def\n   currentdict\nend\n/%s-ISOLatin1 exch definefont pop\n'
    return latin1FontTemplate % (fontname, fontname)


class PsDSC():

    def __init__(self):
        pass

    def documentHeader(self):
        return '%!PS-Adobe-3.0'

    def boundingBoxStr(self, x0, y0, x1, y1):
        """coordinates of bbox in default PS coordinates"""
        return '%%BoundingBox: ' + '%s %s %s %s' % (x0, y0, x1, y1)

    def BeginPageStr(self, pageSetupStr, pageName=None):
        """Use this at the beginning of each page, feed it your setup code
        in the form of a string of postscript.  pageName is the "number" of the
        page.  By default it will be 0."""
        self.inPageFlag = 1
        if not pageName:
            pageDeclaration = '%%Page: ' + '0'
        else:
            pageDeclaration = '%%Page: ' + pageName
        ret = pageDeclaration + '\n' + '%%BeginPageSetup\n/pgsave save def\n'
        return ret + pageSetupStr + '\n%%EndPageSetup'

    def EndPageStr(self):
        self.inPageFlag = 0
        return ''


class EpsDSC(PsDSC):

    def __init__(self):
        PsDSC.__init__(self)

    def documentHeader(self):
        return '%!PS-Adobe-3.0 EPSF-3.0'


class PSCanvas(Canvas):
    """This canvas is meant for generating encapsulated PostScript files
    (EPS) used for inclusion in other documents; thus really only
    single-page documents are supported.  For historical reasons and
    because they can be printed (a showpage is included), the files are
    given a .ps extension by default, and a primitive sort of multipage
    document can be generated using nextPage() or clear().  Use at your own
    risk!  Future versions of piddlePS will include an EPSCanvas and a
    PSCanvas which will clearly delineate between single and multipage
    documents.

    Note: All font encodings must be taken care in __init__, you can't add
          more after this"""

    def __init__(self, size=(300, 300), name='spingPS', PostScriptLevel=2, fontMapEncoding=PSFontMapLatin1Enc):
        Canvas.__init__(self, size, name)
        (width, height) = self.size = size
        self.filename = name
        if len(name) < 3 or string.lower(name[-3:]) != '.ps':
            self.filename = name + '.ps'
        if PostScriptLevel == 1:
            self.drawImage = self._drawImageLevel1
        elif PostScriptLevel == 2:
            self.drawImage = self._drawImageLevel2
        else:
            raise 'PostScriptLevelException'
        try:
            import _psAccelerators
            self._AsciiHexEncode = _psAccelerators._AsciiHexEncode
        except ImportError:
            pass

        self.code = []
        self.dsc = PsDSC()
        c = self._currentColor = self.defaultLineColor
        r, g, b = c.red, c.green, c.blue
        w = self._currentWidth = self.defaultLineWidth
        self.defaultFont = Font(face='serif')
        self.fontMapEncoding = fontMapEncoding
        self._currentFont = self.defaultFont
        f = self._findFont(self._currentFont)
        s = self._currentFont.size
        self._inDocumentFlag = 0
        self._inPageFlag = 0
        self.pageNum = 1
        self.psBeginDocument()
        self.psBeginPage()

    def psBeginDocument(self):
        self.code.append(self.dsc.documentHeader())
        self.code.append(self.dsc.boundingBoxStr(0, 0, self.size[0], self.size[1]))
        self.code.append('%%Pages: (atend)')
        self._inDocumentFlag = 1
        shapes = {'Helvetica': ['Roman', 'Bold', 'Oblique'], 'Times': [
                   'Roman', 'Bold', 'Italic'], 
           'Courier': [
                     'Roman', 'Bold', 'Oblique']}
        fntnames = []
        for basename in ['Helvetica', 'Times', 'Courier']:
            for mys in shapes[basename]:
                fntnames.append(basename + '-' + mys)

        for fontname in fntnames:
            self.code.append(latin1FontEncoding(fontname))

    def psEndDocument(self):
        if self._inDocumentFlag:
            self.code.append('%%Trailer')
            self.code.append('%%%%Pages: %d' % self.pageNum)
            self.code.append('%%EOF')

    def psBeginPage(self, pageName=None):
        if not pageName:
            pageName = '%s' % self.pageNum
        pagesetup = self._psPageSetupStr(self.size[1], self.defaultLineColor, self._findFont(self.defaultFont), self.defaultFont.size, self.defaultLineWidth)
        self.code.append(self.dsc.BeginPageStr(pageSetupStr=pagesetup, pageName=pageName))
        self._inPageFlag = 1

    def _psPageSetupStr(self, pageheight, initialColor, font_family, font_size, line_width):
        """ps code for settin up coordinate system for page in accords w/ piddle standards"""
        r, g, b = initialColor.red, initialColor.green, initialColor.blue
        return '\n%% initialize\n\n2 setlinecap\n\n0 %d\ntranslate\n\n%s %s %s setrgbcolor\n(%s) findfont %s scalefont setfont\n%s setlinewidth' % (pageheight, r, g, b, font_family, font_size, line_width)

    def psEndPage(self):
        self.code.append('pgsave restore')
        self.code.append('showpage')
        self._inPageFlag = 0

    def _findFont(self, font):
        requested = font.face or 'Serif'
        if type(requested) == StringType:
            requested = [
             requested]
        face = string.lower(PiddleLegalFonts['serif'])
        for reqFace in requested:
            if PiddleLegalFonts.has_key(string.lower(reqFace)):
                face = string.lower(PiddleLegalFonts[string.lower(reqFace)])
                break

        if font.bold:
            shape = Bold
        elif font.italic:
            shape = Italic
        else:
            shape = Roman
        return self.fontMapEncoding[(face, shape)]

    def _findExternalFontName(self, font):
        """Attempts to return proper font name.
        PDF uses a standard 14 fonts referred to
        by name. Default to self.defaultFont('Helvetica').
        The dictionary allows a layer of indirection to
        support a standard set of PIDDLE font names."""
        piddle_font_map = {'Times': 'Times', 
           'times': 'Times', 
           'Courier': 'Courier', 
           'courier': 'Courier', 
           'helvetica': 'Helvetica', 
           'Helvetica': 'Helvetica', 
           'symbol': 'Symbol', 
           'Symbol': 'Symbol', 
           'monospaced': 'Courier', 
           'serif': 'Times', 
           'sansserif': 'Helvetica', 
           'ZapfDingbats': 'ZapfDingbats', 
           'zapfdingbats': 'ZapfDingbats', 
           'arial': 'Helvetica'}
        try:
            face = piddle_font_map[string.lower(font.face)]
        except:
            return 'Helvetica'

        name = face + '-'
        if font.bold and face in ('Courier', 'Helvetica', 'Times'):
            name = name + 'Bold'
        if font.italic and face in ('Courier', 'Helvetica'):
            name = name + 'Oblique'
        elif font.italic and face == 'Times':
            name = name + 'Italic'
        if name == 'Times-':
            name = name + 'Roman'
        if name[(-1)] == '-':
            name = name[0:-1]
        return name

    def _psNextPage(self):
        """advance to next page of document.  """
        self.psEndPage()
        self.pageNum = self.pageNum + 1
        self.psBeginPage()

    def nextPage(self):
        self.clear()

    def clear(self):
        """clear resets the canvas to it's default state.  Though this
        canvas is really only meant to be an EPS canvas, i.e., single page,
        for historical reasons we will allow multipage documents.  Thus
        clear will end the page, clear the canvas state back to default,
        and start a new page.  In the future, this PSCanvas will become
        EPSCanvas and will not support multipage documents.  In that case,
        the canvas will be reset to its default state and the file will be
        emptied of all previous drawing commands"""
        self.resetToDefaults()
        self._psNextPage()

    def resetToDefaults(self):
        self._currentColor = self.defaultLineColor
        self._currentWidth = self.defaultLineWidth
        self._currentFont = self.defaultFont

    def flush(self):
        pass

    def save(self, file=None, format=None):
        """Write the current document to a file or stream and close the file
        Computes any final trailers, etc. that need to be done in order to
        produce a well formed postscript file.  At least for now though,
        it still allows you to add to the file after a save by not actually
        inserting the finalization code into self.code

        the format argument is not used"""
        file = file or self.filename
        fileobj = getFileObject(file)
        fileobj.write(string.join(self.code, linesep))
        preserveCode = self.code
        self.code = finalizationCode = ['']
        preserve_inPageFlag = self._inPageFlag
        preserve_inDocumentFlag = self._inDocumentFlag
        if self._inPageFlag:
            self.psEndPage()
        self.psEndDocument()
        fileobj.write(string.join(finalizationCode, linesep))
        self.code = preserveCode
        self._inPageFlag = preserve_inPageFlag
        self._inDocumentFlag = preserve_inDocumentFlag

    def stringWidth(self, s, font=None):
        """Return the logical width of the string if it were drawn         in the current font (defaults to self.font)."""
        if not font:
            font = self.defaultFont
        fontname = self._findExternalFontName(font)
        return psmetrics.stringwidth(s, fontname, self.fontMapEncoding['EncodingName']) * font.size * 0.001

    def fontAscent(self, font=None):
        if not font:
            font = self.defaultFont
        fontname = self._findExternalFontName(font)
        return psmetrics.ascent_descent[fontname][0] * 0.001 * font.size

    def fontDescent(self, font=None):
        if not font:
            font = self.defaultFont
        fontname = self._findExternalFontName(font)
        return -psmetrics.ascent_descent[fontname][1] * 0.001 * font.size

    def _updateLineColor(self, color):
        color = color or self.defaultLineColor
        if color != self._currentColor:
            self._currentColor = color
            r, g, b = color.red, color.green, color.blue
            self.code.append('%s %s %s setrgbcolor' % (r, g, b))

    def _updateFillColor(self, color):
        color = color or self.defaultFillColor
        if color != self._currentColor:
            self._currentColor = color
            r, g, b = color.red, color.green, color.blue
            self.code.append('%s %s %s setrgbcolor' % (r, g, b))

    def _updateLineWidth(self, width):
        if width == None:
            width = self.defaultLineWidth
        if width != self._currentWidth:
            self._currentWidth = width
            self.code.append('%s setlinewidth' % width)
        return

    def _updateFont(self, font):
        font = font or self.defaultFont
        if font != self._currentFont:
            self._currentFont = font
            f = self._findFont(font)
            s = font.size
            self.code.append('(%s) findfont %s scalefont setfont' % (f, s))

    def drawLine(self, x1, y1, x2, y2, color=None, width=None):
        self._updateLineColor(color)
        self._updateLineWidth(width)
        if self._currentColor != transparent:
            self.code.append('%s %s neg moveto %s %s neg lineto stroke' % (
             x1, y1, x2, y2))

    def drawLines(self, lineList, color=None, width=None):
        self._updateLineColor(color)
        self._updateLineWidth(width)
        codeline = '%s %s neg moveto %s %s neg lineto stroke'
        if self._currentColor != transparent:
            for line in lineList:
                self.code.append(codeline % line)

    def _escape(self, s):
        str = string.replace(s, chr(92), '\\\\')
        str = string.replace(str, '(', '\\(')
        str = string.replace(str, ')', '\\)')
        return str

    def _drawStringOneLineNoRot(self, s, x, y, font=None):
        text = self._escape(s)
        self.code.append('%s %s neg moveto (%s) show' % (x, y, text))
        if self._currentFont.underline:
            swidth = self.stringWidth(s, self._currentFont)
            ypos = 0.5 * self.fontDescent(self._currentFont)
            thickness = 0.08 * self._currentFont.size
            self.code.extend(['%s setlinewidth' % thickness,
             '0 %s neg rmoveto' % ypos,
             '%s 0 rlineto stroke' % -swidth])

    def _drawStringOneLine(self, s, x, y, font=None, color=None, angle=0):
        text = self._escape(s)
        self.code.extend(['%f %f neg moveto (%s) show' % (x, y, text)])
        if self._currentFont.underline:
            swidth = self.stringWidth(s, self._currentFont)
            dy = 0.5 * self.fontDescent(self._currentFont)
            thickness = 0.08 * self._currentFont.size
            self.code.extend(['%s setlinewidth' % thickness,
             '%f %f neg moveto' % (x, dy + y),
             '%f 0 rlineto stroke' % swidth])

    def drawString(self, s, x, y, font=None, color=None, angle=0):
        """drawString(self, s, x, y, font=None, color=None, angle=0)
        draw a string s at position x,y"""
        self._updateLineColor(color)
        self._updateFont(font)
        if self._currentColor != transparent:
            lines = string.split(s, '\n')
            lineHeight = self.fontHeight(font)
            if angle == 0:
                for line in lines:
                    self._drawStringOneLineNoRot(line, x, y, font=font)

            else:
                self.code.extend([
                 'gsave',
                 '%s %s neg translate' % (x, y),
                 `angle` + ' rotate'])
                down = 0
                for line in lines:
                    self._drawStringOneLine(line, 0, 0 + down, font, color, angle)
                    down = down + lineHeight

                self.code.extend(['grestore'])

    def drawCurve(self, x1, y1, x2, y2, x3, y3, x4, y4, edgeColor=None, edgeWidth=None, fillColor=None, closed=0):
        codeline = '%s %s neg moveto %s %s neg %s %s neg %s %s neg curveto'
        data = (x1, y1, x2, y2, x3, y3, x4, y4)
        self._updateFillColor(fillColor)
        if self._currentColor != transparent:
            self.code.append(codeline % data + ' eofill')
        self._updateLineWidth(edgeWidth)
        self._updateLineColor(edgeColor)
        if self._currentColor != transparent:
            self.code.append(codeline % data + (closed and ' closepath' or '') + ' stroke')

    def drawRoundRect(self, x1, y1, x2, y2, rx=8, ry=8, edgeColor=None, edgeWidth=None, fillColor=None):
        """Draw a rounded rectangle between x1,y1, and x2,y2,         with corners inset as ellipses with x radius rx and y radius ry.         These should have x1<x2, y1<y2, rx>0, and ry>0."""
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        ellipsePath = 'matrix currentmatrix %s %s neg translate %s %s scale 0 0 1 %s %s arc setmatrix'
        rrcode = [
         'newpath']
        rrcode.append(ellipsePath % (x1 + rx, y1 + ry, rx, ry, 90, 180))
        rrcode.append(ellipsePath % (x1 + rx, y2 - ry, rx, ry, 180, 270))
        rrcode.append(ellipsePath % (x2 - rx, y2 - ry, rx, ry, 270, 360))
        rrcode.append(ellipsePath % (x2 - rx, y1 + ry, rx, ry, 0, 90))
        rrcode.append('closepath')
        self._updateFillColor(fillColor)
        if self._currentColor != transparent:
            self.code.extend(rrcode)
            self.code.append('eofill')
        self._updateLineWidth(edgeWidth)
        self._updateLineColor(edgeColor)
        if self._currentColor != transparent:
            self.code.extend(rrcode)
            self.code.append('stroke')

    def drawEllipse(self, x1, y1, x2, y2, edgeColor=None, edgeWidth=None, fillColor=None):
        """Draw an orthogonal ellipse inscribed within the rectangle x1,y1,x2,y2.         These should have x1<x2 and y1<y2."""
        self.drawArc(x1, y1, x2, y2, edgeColor=edgeColor, edgeWidth=edgeWidth, fillColor=fillColor)

    def drawArc(self, x1, y1, x2, y2, startAng=0, extent=360, edgeColor=None, edgeWidth=None, fillColor=None):
        """Draw a partial ellipse inscribed within the rectangle x1,y1,x2,y2,         starting at startAng degrees and covering extent degrees.   Angles         start with 0 to the right (+x) and increase counter-clockwise.         These should have x1<x2 and y1<y2."""
        cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        rx, ry = (x2 - x1) / 2.0, (y2 - y1) / 2.0
        codeline = self._genArcCode(x1, y1, x2, y2, startAng, extent)
        self._updateFillColor(fillColor)
        if self._currentColor != transparent:
            self.code.append('%s %s neg moveto' % (cx, cy))
            self.code.append(codeline + ' eofill')
        self._updateLineWidth(edgeWidth)
        self._updateLineColor(edgeColor)
        if self._currentColor != transparent:
            self.code.append('%s %s neg moveto' % (cx + rx * math.cos(-startAng),
             cy + ry * math.sin(-startAng)))
            self.code.append(codeline + ' stroke')

    def _genArcCode(self, x1, y1, x2, y2, startAng, extent):
        """Calculate the path for an arc inscribed in rectangle defined by (x1,y1),(x2,y2)"""
        xScale = abs((x2 - x1) / 2.0)
        yScale = abs((y2 - y1) / 2.0)
        x, y = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        codeline = 'matrix currentmatrix ' + '%s %s neg translate %s %s scale 0 0 1 %s %s %s ' + 'setmatrix'
        if extent >= 0:
            arc = 'arc'
        else:
            arc = 'arcn'
        data = (
         x, y, xScale, yScale, startAng, startAng + extent, arc)
        return codeline % data

    def drawPolygon(self, pointlist, edgeColor=None, edgeWidth=None, fillColor=None, closed=0):
        start = pointlist[0]
        pointlist = pointlist[1:]
        polyCode = []
        polyCode.append('%s %s neg moveto' % start)
        for point in pointlist:
            polyCode.append('%s %s neg lineto' % point)

        if closed:
            polyCode.append('closepath')
        self._updateFillColor(fillColor)
        if self._currentColor != transparent:
            self.code.extend(polyCode)
            self.code.append('eofill')
        self._updateLineWidth(edgeWidth)
        self._updateLineColor(edgeColor)
        if self._currentColor != transparent:
            self.code.extend(polyCode)
            self.code.append('stroke')

    def drawFigure(self, partList, edgeColor=None, edgeWidth=None, fillColor=None, closed=0):
        figureCode = []
        first = 1
        for part in partList:
            op = part[0]
            args = list(part[1:])
            if op == figureLine:
                if first:
                    first = 0
                    figureCode.append('%s %s neg moveto' % tuple(args[:2]))
                else:
                    figureCode.append('%s %s neg lineto' % tuple(args[:2]))
                figureCode.append('%s %s neg lineto' % tuple(args[2:]))
            elif op == figureArc:
                first = 0
                (x1, y1, x2, y2, startAngle, extent) = args[:6]
                figureCode.append(self._genArcCode(x1, y1, x2, y2, startAngle, extent))
            elif op == figureCurve:
                if first:
                    first = 0
                    figureCode.append('%s %s neg moveto' % tuple(args[:2]))
                else:
                    figureCode.append('%s %s neg lineto' % tuple(args[:2]))
                figureCode.append('%s %s neg %s %s neg %s %s neg curveto' % tuple(args[2:]))
            else:
                raise TypeError, 'unknown figure operator: ' + op

        if closed:
            figureCode.append('closepath')
        self._updateFillColor(fillColor)
        if self._currentColor != transparent:
            self.code.extend(figureCode)
            self.code.append('eofill')
        self._updateLineWidth(edgeWidth)
        self._updateLineColor(edgeColor)
        if self._currentColor != transparent:
            self.code.extend(figureCode)
            self.code.append('stroke')

    def _drawImageLevel1(self, image, x1, y1, x2=None, y2=None):
        """drawImage(self,image,x1,y1,x2=None,y2=None) : If x2 and y2 are ommitted, they are
       calculated from image size.  (x1,y1) is upper left of image, (x2,y2) is lower right of
       image in piddle coordinates."""
        try:
            from PIL import Image
        except ImportError:
            print 'Python Imaging Library not available'
            return

        print 'Trying to drawImage in piddlePS'
        component_depth = 8
        myimage = image.convert('RGB')
        (imgwidth, imgheight) = myimage.size
        if not x2:
            x2 = imgwidth + x1
        if not y2:
            y2 = y1 + imgheight
        drawwidth = x2 - x1
        drawheight = y2 - y1
        print 'Image size (%d, %d); Draw size (%d, %d)' % (imgwidth, imgheight, drawwidth, drawheight)
        self.code.extend([
         'gsave',
         '%s %s translate' % (x1, -y1 - drawheight),
         '%s %s scale' % (drawwidth, drawheight),
         '/scanline %d 3 mul string def' % imgwidth])
        self.code.extend([
         '%s %s %s' % (imgwidth, imgheight, component_depth),
         '[%s %s %s %s %s %s]' % (imgwidth, 0, 0, -imgheight, 0, imgheight),
         '{ currentfile scanline readhexstring pop } false 3',
         'colorimage '])
        rawimage = myimage.tostring()
        assert (len(rawimage) == imgwidth * imgheight, 'Wrong amount of data for image')
        hex_encoded = self._AsciiHexEncode(rawimage)
        outstream = cStringIO.StringIO(hex_encoded)
        dataline = outstream.read(78)
        while dataline != '':
            self.code.append(dataline)
            dataline = outstream.read(78)

        self.code.append('% end of image data')
        self.code.append('grestore')

    def _AsciiHexEncode(self, input):
        """Helper function used by images"""
        output = cStringIO.StringIO()
        for char in input:
            output.write('%02x' % ord(char))

        output.reset()
        return output.read()

    def _drawImageLevel2(self, image, x1, y1, x2=None, y2=None):
        try:
            from PIL import Image
        except ImportError:
            print 'Python Imaging Library not available'
            return

        if image.mode == 'L':
            print 'found image.mode= L'
            imBitsPerComponent = 8
            imNumComponents = 1
            myimage = image
        elif image.mode == '1':
            print 'found image.mode= 1'
            myimage = image.convert('L')
            imNumComponents = 1
            myimage = image
        else:
            myimage = image.convert('RGB')
            imNumComponents = 3
            imBitsPerComponent = 8
        (imwidth, imheight) = myimage.size
        if not x2:
            x2 = imwidth + x1
        if not y2:
            y2 = y1 + imheight
        drawwidth = x2 - x1
        drawheight = y2 - y1
        self.code.extend([
         'gsave',
         '%s %s translate' % (x1, -y1 - drawheight),
         '%s %s scale' % (drawwidth, drawheight)])
        if imNumComponents == 3:
            self.code.append('/DeviceRGB setcolorspace')
        elif imNumComponents == 1:
            self.code.append('/DeviceGray setcolorspace')
            print 'setting colorspace gray'
        self.code.append('\n<<\n/ImageType 1\n/Width %d /Height %d  %% dimensions of source image\n/BitsPerComponent %d' % (imwidth, imheight, imBitsPerComponent))
        if imNumComponents == 1:
            self.code.append('/Decode [0 1]')
        if imNumComponents == 3:
            self.code.append('/Decode [0 1 0 1 0 1]  %% decode color values normally')
        self.code.extend(['/ImageMatrix [%s 0 0 %s 0 %s]' % (imwidth, -imheight, imheight),
         '/DataSource currentfile /ASCIIHexDecode filter',
         '>> % End image dictionary',
         'image'])
        rawimage = myimage.tostring()
        assert (len(rawimage) == imwidth * imheight, 'Wrong amount of data for image')
        hex_encoded = self._AsciiHexEncode(rawimage)
        outstream = cStringIO.StringIO(hex_encoded)
        dataline = outstream.read(78)
        while dataline != '':
            self.code.append(dataline)
            dataline = outstream.read(78)

        self.code.append('> % end of image data')
        self.code.append('grestore')


EPSCanvas = PSCanvas