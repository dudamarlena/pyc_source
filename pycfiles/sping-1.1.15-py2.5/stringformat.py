# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sping\stringformat.py
# Compiled at: 2002-09-29 01:37:44
"""
Module StringFormat
The StringFormat module allows for character-by-character formatting of
strings. It imitates the SPING string drawing and string metrics
interface. The string formatting is done with specialized XML syntax
within the string. Therefore, the interface for the StringFormat module
consists of wrapper functions for the SPING string interface and
various XML tags and characters.

StringFormat functions 

       drawString(canvas, s, x, y, [font], [color], [angle]) 
       stringWidth(canvas, s, [font]) 
       fontHeight(canvas, [font]) 
       fontAscent(canvas, [font]) 
       fontDescent(canvas, [font]) 
StringFormat XML tags 

       <b> </b> - bold 
       <i> </i> - italics 
       <u> </u> - underline 
       <super> </super> - superscript 
       <sub> </sub> - subscript 

StringFormat XML characters 

       Greek Letter Symbols as specified in MathML 
"""
from sping.pid import Font
import xmllib, math
sizedelta = 2
subFraction = 0.5
superFraction = 0.5
greekchars = {'alpha': 'a', 
   'beta': 'b', 
   'chi': 'c', 
   'Delta': 'D', 
   'delta': 'd', 
   'epsiv': 'e', 
   'eta': 'h', 
   'Gamma': 'G', 
   'gamma': 'g', 
   'iota': 'i', 
   'kappa': 'k', 
   'Lambda': 'L', 
   'lambda': 'l', 
   'mu': 'm', 
   'nu': 'n', 
   'Omega': 'W', 
   'omega': 'w', 
   'omicron': 'x', 
   'Phi': 'F', 
   'phi': 'f', 
   'phiv': 'j', 
   'Pi': 'P', 
   'pi': 'p', 
   'piv': 'v', 
   'Psi': 'Y', 
   'psi': 'y', 
   'rho': 'r', 
   'Sigma': 'S', 
   'sigma': 's', 
   'sigmav': 'V', 
   'tau': 't', 
   'Theta': 'Q', 
   'theta': 'q', 
   'thetav': 'j', 
   'Xi': 'X', 
   'xi': 'x', 
   'zeta': 'z'}

class StringSegment:
    """class StringSegment contains the intermediate representation of string
        segments as they are being parsed by the XMLParser. 
        """

    def __init__(self):
        self.super = 0
        self.sub = 0
        self.bold = 0
        self.italic = 0
        self.underline = 0
        self.s = ''
        self.width = 0
        self.greek = 0

    def calcNewFont(self, font):
        """Given a font (does not accept font==None), creates a            new font based on the format of this text segment."""
        if self.greek:
            face = 'symbol'
        else:
            face = font.face
        return Font(face=face, size=font.size - self.super * sizedelta - self.sub * sizedelta, underline=self.underline or font.underline, bold=self.bold or font.bold, italic=self.italic or font.italic)

    def calcNewY(self, font, y):
        """Returns a new y coordinate depending on its             whether the string is a sub and super script."""
        if self.sub == 1:
            return y + font.size * subFraction
        elif self.super == 1:
            return y - font.size * superFraction
        else:
            return y

    def dump(self):
        print 'StringSegment: ]%s[' % self.s
        print '\tsuper = ', self.super
        print '\tsub = ', self.sub
        print '\tbold = ', self.bold
        print '\titalic = ', self.italic
        print '\tunderline = ', self.underline
        print '\twidth = ', self.width
        print '\tgreek = ', self.greek


class StringFormatter(xmllib.XMLParser):

    def start_b(self, attributes):
        self.bold = 1

    def end_b(self):
        self.bold = 0

    def start_i(self, attributes):
        self.italic = 1

    def end_i(self):
        self.italic = 0

    def start_u(self, attributes):
        self.underline = 1

    def end_u(self):
        self.underline = 0

    def start_super(self, attributes):
        self.super = 1

    def end_super(self):
        self.super = 0

    def start_sub(self, attributes):
        self.sub = 1

    def end_sub(self):
        self.sub = 0

    def start_greek(self, attributes, letter):
        self.greek = 1
        self.handle_data(letter)

    def end_greek(self):
        self.greek = 0

    def __init__(self):
        xmllib.XMLParser.__init__(self)
        self.segmentlist = []
        self.sub = 0
        self.super = 0
        self.bold = 0
        self.italic = 0
        self.underline = 0
        self.elements = {'b': (self.start_b, self.end_b), 'u': (
               self.start_u, self.end_u), 
           'i': (
               self.start_i, self.end_i), 
           'super': (
                   self.start_super, self.end_super), 
           'sub': (
                 self.start_sub, self.end_sub)}
        for item in greekchars.keys():
            self.elements[item] = (
             lambda attr, self=self, letter=greekchars[item]: self.start_greek(attr, letter), self.end_greek)

        self.greek = 0
        for item in greekchars.keys():
            self.entitydefs[item] = '<%s/>' % item

    def handle_data(self, data):
        """Creates an intermediate representation of string segments."""
        segment = StringSegment()
        segment.s = data
        if self.sub == 1 and self.super == 1:
            segment.sub = 0
            segment.super = 0
        else:
            segment.sub = self.sub
            segment.super = self.super
        segment.bold = self.bold
        segment.italic = self.italic
        segment.underline = self.underline
        segment.greek = self.greek
        self.segmentlist.append(segment)

    def parseSegments(self, s):
        """Given a formatted string will return a list of          StringSegment objects with their calculated widths."""
        self.feed('<formattedstring>' + s + '</formattedstring>')
        self.close()
        self.reset()
        segmentlist = self.segmentlist
        self.segmentlist = []
        return segmentlist


def fontHeight(canvas, font=None):
    """Find the total height (ascent + descent) of the given font."""
    return canvas.fontHeight(font)


def fontAscent(canvas, font=None):
    """Find the ascent (height above base) of the given font."""
    return canvas.fontAscent(font)


def fontDescent(canvas, font=None):
    """Find the descent (extent below base) of the given font."""
    return canvas.fontDescent(font)


def stringWidth(canvas, s, font=None):
    """Return the logical width of the string if it were drawn         in the current font (defaults to canvas.font)."""
    sformatter = StringFormatter()
    segmentlist = sformatter.parseSegments(s)
    if not font:
        font = canvas.defaultFont
    sum = 0
    for seg in segmentlist:
        sum = sum + canvas.stringWidth(seg.s, seg.calcNewFont(font))

    return sum


def rotateXY(x, y, theta):
    """Rotate (x,y) by theta degrees.  Got tranformation       from page 299 in linear algebra book."""
    radians = theta * math.pi / 180.0
    return (
     math.cos(radians) * x + math.sin(radians) * y,
     -(math.sin(radians) * x - math.cos(radians) * y))


def drawString(canvas, s, x, y, font=None, color=None, angle=0):
    """Draw a formatted string starting at location x,y in canvas."""
    sformatter = StringFormatter()
    segmentlist = sformatter.parseSegments(s)
    if not font:
        font = canvas.defaultFont
    startpos = x
    for seg in segmentlist:
        (delta_x, delta_y) = rotateXY(startpos - x, seg.calcNewY(font, y) - y, angle)
        canvas.drawString(seg.s, x + delta_x, y + delta_y, seg.calcNewFont(font), color, angle)
        startpos = startpos + canvas.stringWidth(seg.s, seg.calcNewFont(font))


if __name__ == '__main__':
    from sping.colors import *
    from sping.PDF import PDFCanvas

    def test1():
        canvas = PDFCanvas(name='stringformat_test1.pdf')
        drawString(canvas, '<u><b>hello there</b></u><super>hi</super>', 10, 20)
        drawString(canvas, 'hello!', 10, 40)
        print "'hello!' width = ", stringWidth(canvas, 'hello!')
        print "'hello!' SPING width = ", canvas.stringWidth('hello!')
        drawString(canvas, '<b>hello!</b> goodbye', 10, 60)
        print "'<b>hello!</b> goodbye' width = ", stringWidth(canvas, '<b>hello!</b> goodbye')
        drawString(canvas, 'hello!', 10, 80, Font(bold=1))
        print "'hello!' Font(bold=1) SPING width = ", canvas.stringWidth('hello!', Font(bold=1))
        drawString(canvas, ' goodbye', 10, 100)
        print "' goodbye' SPING width = ", canvas.stringWidth(' goodbye')
        canvas.flush()
        canvas.save()


    def test2():
        canvas = PDFCanvas(name='stringformat_test2.pdf')
        drawString(canvas, '<alpha/>', 10, 10)
        drawString(canvas, '&alpha;', 10, 30)
        canvas.flush()
        canvas.save()


    def allTagCombos(canvas, x, y, font=None, color=None, angle=0):
        r"""Try out all tags and various combinations of them. \ 
                Starts at given x,y and returns possible next (x,y)."""
        oldDefault = canvas.defaultFont
        if font:
            canvas.defaultFont = font
        oldx = x
        dx = stringWidth(canvas, ' ')
        dy = canvas.defaultFont.size * 1.5
        drawString(canvas, '<b>bold</b>', x, y, color=color, angle=angle)
        x = x + stringWidth(canvas, '<b>bold</b>') + dx
        drawString(canvas, '<i>italic</i>', x, y, color=color, angle=angle)
        x = x + stringWidth(canvas, '<i>italic</i>') + dx
        drawString(canvas, '<u>underline</u>', x, y, color=color, angle=angle)
        x = x + stringWidth(canvas, '<u>underline</u>') + dx
        drawString(canvas, '<super>super</super>', x, y, color=color, angle=angle)
        x = x + stringWidth(canvas, '<super>super</super>') + dx
        drawString(canvas, '<sub>sub</sub>', x, y, color=color, angle=angle)
        y = y + dy
        drawString(canvas, '<b><u>bold+underline</u></b>', oldx, y, color=color, angle=angle)
        x = oldx + stringWidth(canvas, '<b><u>bold+underline</u></b>') + dx
        drawString(canvas, '<super><i>super+italic</i></super>', x, y, color=color, angle=angle)
        x = x + stringWidth(canvas, '<super><i>super+italic</i></super>') + dx
        drawString(canvas, '<b><sub>bold+sub</sub></b>', x, y, color=color, angle=angle)
        y = y + dy
        canvas.defaultFont = oldDefault
        return (oldx, y)


    def stringformatTest():
        canvas = PDFCanvas(name='stringformat_bigtest1.pdf')
        x = 10
        y = canvas.defaultFont.size * 1.5
        (x, y) = allTagCombos(canvas, x, y)
        (x, y) = allTagCombos(canvas, x, y + 30, Font(face='serif'))
        (x, y) = allTagCombos(canvas, x, y + 30, Font(face='monospaced'))
        (x, y) = allTagCombos(canvas, x, y + 30, Font(face='serif'), angle=-30)
        (x, y) = allTagCombos(canvas, x, y + 30, Font(size=16))
        (x, y) = allTagCombos(canvas, x, y + 30, Font(size=9))
        (x, y) = allTagCombos(canvas, x, y + 30, Font(underline=1))
        (x, y) = allTagCombos(canvas, x, y + 30, color=red)
        sfwidth = stringWidth(canvas, '<b><sub>bold+sub</sub></b> hello <u><super>underline+super</super></u>')
        print 'sw("<b><sub>bold+sub</sub></b>") = ', stringWidth(canvas, '<b><sub>bold+sub</sub></b>')
        print 'sw(" hello ") = ', stringWidth(canvas, ' hello ')
        print 'sw("<u><super>underline+super</super></u>") = ',
        print stringWidth(canvas, '<u><super>underline+super</super></u>')
        pwidth1 = canvas.stringWidth('bold+sub', Font(size=canvas.defaultFont.size - sizedelta, bold=1))
        print 'pwidth1 = ', pwidth1
        pwidth2 = canvas.stringWidth(' hello ')
        print 'pwidth2 = ', pwidth2
        pwidth3 = canvas.stringWidth('underline+super', Font(size=canvas.defaultFont.size - sizedelta, underline=1))
        print 'pwidth3 = ', pwidth3
        print 'sfwidth = ', sfwidth, ' pwidth = ', pwidth1 + pwidth2 + pwidth3
        canvas = PDFCanvas(name='bigtest2.pdf')
        x = 10
        y = canvas.defaultFont.size * 1.5
        drawString(canvas, '&alpha; &beta; <chi/> &Delta; <delta/>', x, y, Font(size=16), color=blue)
        print 'line starting with alpha should be font size 16'
        y = y + 30
        drawString(canvas, '&epsiv; &eta; &Gamma; <gamma/>', x, y, color=green)
        y = y + 30
        drawString(canvas, '&iota; &kappa; &Lambda; <lambda/>', x, y, color=blue)
        y = y + 30
        drawString(canvas, '<u>&mu;</u> &nu; <b>&Omega;</b> <omega/>', x, y, color=green)
        print 'mu should be underlined, Omega should be big and bold'
        y = y + 30
        drawString(canvas, '&omicron; &Phi; &phi; <phiv/>', x, y, color=blue)
        y = y + 30
        drawString(canvas, '&Pi; &pi; &piv; <Psi/> &psi; &rho;', x, y, color=green)
        y = y + 30
        drawString(canvas, '<u>&Sigma; &sigma; &sigmav; <tau/></u>', x, y, color=blue)
        print 'line starting with sigma should be completely underlined'
        y = y + 30
        drawString(canvas, '&Theta; &theta; &thetav; <Xi/> &xi; &zeta;', x, y, color=green)
        y = y + 30
        drawString(canvas, "That's &alpha;ll <u>folks</u><super>&omega;</super>", x, y)
        canvas.flush()
        canvas.save()


    test1()
    test2()
    stringformatTest()