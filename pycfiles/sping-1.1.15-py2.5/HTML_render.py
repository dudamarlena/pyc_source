# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sping\util\HTML_render.py
# Compiled at: 2002-01-21 21:45:02
"""rendering HTML text with sping
HTML_render.py
jjk  02/02/00  001  first working version
jjk  02/03/00  002  some enhancements, renamed from piddleTaggedText.py
jjk  02/04/00  003  more enhancements, renamed from piddleHtmlWriter.py
cwl  01/01/02  004  renamed 

Purpose:
    The HTMLPiddler class accepts an HTML string and a few layout constraints,
    and renders the HTML on a piddle canvas. This code is mainly a demonstration
    and proof-of-concept, and is not really intended for real work.
    
Usage:
    piddler = HTMLPiddler(html=aHtmlString, 
                              start=(startX, startY), 
                              xLimits=(leftMarginX, rightMarginX), 
                              font=aPiddleFontForDefault, 
                              color=aPiddleColorForDefault)
    piddler.renderOn(aPiddleCanvas)
    
    see also demo() functions at end of this file
    
Example:
    Just run this module as a python script (must have piddle installed)
    
Limitations:
    -only renders a subset of HTML (mostly text-related tags)
    -content between unsupported tags may not be rendered at all
    
Implementation:
    -derived largely on "demo07.py" from Jim Ahlstrom's WPY distribution (see credits)
    -uses the parser-formatter-writer model from the python standard library
    
Credits:
    PIDDLE
        author: Joe Strout <joe@strout.net>, et al
        download: http://www.strout.net/python/piddle/
        disclaimers: see __copyrite_jim__ below
    WPY
        author: Jim Ahlstrom <jim@interet.com>
        download: http://www.python.org/ftp/python/wpy/
        disclaimers: see __copyrite_jim__ below
    HTMLPiddler.py
        author: Jeff Kunce <kuncej@mail.conservation.state.mo.us>
        download: http://starship.python.net/crew/jjkunce/
        disclaimers: * NO WARRANTIES * USE AT YOUR OWN RISK *    
    
"""
import htmllib, formatter, string
from types import *
import piddle
TRACE = 0

class HTMLPiddler:
    """jjk  02/01/00"""

    def __init__(self, html='', start=(0, 0), xLimits=(0, 800), font=None, color=None):
        """instance initializer
        jjk  02/01/00"""
        self.html = html
        self.start = start
        self.xLimits = xLimits
        if not font:
            font = piddle.Font()
        self.font = font
        self.color = color

    def renderOn(self, aPiddleCanvas):
        """draw the text with aPiddleCanvas
        jjk  02/01/00"""
        writer = _HtmlPiddleWriter(self, aPiddleCanvas)
        fmt = formatter.AbstractFormatter(writer)
        parser = _HtmlParser(fmt)
        parser.feed(self.html)
        parser.close()


class _HtmlParser(htmllib.HTMLParser):

    def anchor_bgn(self, href, name, type):
        htmllib.HTMLParser.anchor_bgn(self, href, name, type)
        self.formatter.writer.anchor_bgn(href, name, type)

    def anchor_end(self):
        htmllib.HTMLParser.anchor_end(self)
        self.formatter.writer.anchor_end()


class _HtmlPiddleWriter:
    FontSizeDict = {'h1': 36, 'h2': 24, 'h3': 18, 'h4': 12, 'h5': 10, 'h6': 8}
    DefaultFontSize = 12

    def __init__(self, aHTMLPiddler, aPiddleCanvas):
        self.piddler = aHTMLPiddler
        self.pc = aPiddleCanvas
        self.anchor = None
        self.lineHeight = 0
        self.atbreak = 0
        self.color = self.piddler.color
        self.defaultFont = self.font = self.piddler.font
        s = 'WWWWWWWWWWWWWWWWWWWW'
        x = self.pc.stringWidth(s, self.font)
        y = self.pc.fontHeight(self.font)
        x = (x + 19) / 20
        self.fsizex = x
        self.fsizey = self.oldLineHeight = y
        self.indentSize = x * 3
        (self.lmargin, self.rmargin) = self.piddler.xLimits
        (self.x, self.y) = self.piddler.start
        self.indent = self.lmargin + x / 3
        return

    def anchor_bgn(self, href, name, type):
        if href:
            self.oldcolor = self.color
            self.color = piddle.Color(0.0, 0.0, 200 / 255.0)
            self.anchor = (href, name, type)

    def anchor_end(self):
        if self.anchor:
            self.color = self.oldcolor
            self.anchor = None
        return

    def new_font(self, fontParams):
        if TRACE:
            print 'nf', fontParams
        if not fontParams:
            fontParams = (None, None, None, None)
        size = fontParams[0]
        try:
            points = self.FontSizeDict[size]
        except KeyError:
            points = self.DefaultFontSize

        if fontParams[3]:
            face = 'courier'
        elif type(size) is StringType and size[0] == 'h':
            face = 'helvetica'
        else:
            face = 'times'
        italic = fontParams[1]
        if italic == None:
            italic = 0
        bold = fontParams[2]
        if bold == None:
            bold = 0
        self.font = piddle.Font(points, bold, italic, face=face)
        x = self.pc.stringWidth('WWWWWWWWWWWWWWWWWWWW', self.font)
        self.fsizex = (x + 19) / 20
        self.fsizey = self.pc.fontHeight(self.font)
        return

    def new_margin(self, margin, level):
        self.send_line_break()
        self.indent = self.x = self.lmargin + self.indentSize * level

    def new_spacing(self, spacing):
        self.send_line_break()
        t = 'new_spacing(%s)' % `spacing`
        self.OutputLine(t, 1)

    def new_styles(self, styles):
        self.send_line_break()
        t = 'new_styles(%s)' % `styles`
        self.OutputLine(t, 1)

    def send_label_data(self, data):
        if data == '*':
            w = self.pc.stringWidth(data, self.font) / 3
            h = self.pc.fontHeight(self.font) / 3
            x = self.indent - w
            y = self.y - w
            self.pc.drawRect(x, y, x - w, y - w)
        else:
            w = self.pc.stringWidth(data, self.font)
            h = self.pc.fontHeight(self.font)
            x = self.indent - w - self.fsizex / 3
            if x < 0:
                x = 0
            self.pc.drawString(data, x, self.y, self.font, self.color)

    def send_paragraph(self, blankline):
        self.send_line_break()
        self.y = self.y + self.oldLineHeight * blankline

    def send_line_break(self):
        if self.lineHeight:
            self.y = self.y + self.lineHeight
            self.oldLineHeight = self.lineHeight
            self.lineHeight = 0
        self.x = self.indent
        self.atbreak = 0
        if TRACE:
            raw_input('lb')

    def send_hor_rule(self):
        self.send_line_break()
        self.y = self.y + self.oldLineHeight
        border = self.fsizex
        self.pc.drawLine(border, self.y, self.rmargin - border, self.y, piddle.Color(0.0, 0.0, 200 / 255.0))
        self.y = self.y + self.oldLineHeight

    def send_literal_data(self, data):
        if not data:
            return
        lines = string.splitfields(data, '\n')
        text = string.expandtabs(lines[0])
        for l in lines[1:]:
            self.OutputLine(text, 1)
            text = string.expandtabs(l)

        self.OutputLine(text, 0)
        self.atbreak = 0

    def send_flowing_data(self, data):
        if not data:
            return
        atbreak = self.atbreak or data[0] in string.whitespace
        text = ''
        pixels = chars = 0
        for word in string.split(data):
            bword = ' ' + word
            length = len(bword)
            if not atbreak:
                text = word
                chars = chars + length - 1
            elif self.x + pixels + (chars + length) * self.fsizex < self.rmargin:
                text = text + bword
                chars = chars + length
            else:
                w = self.pc.stringWidth(text + bword, self.font)
                h = self.pc.fontHeight(self.font)
                if TRACE:
                    print 'sfd T:', text + bword
                if TRACE:
                    print 'sfd', self.x, w, self.x + w, self.rmargin
                if self.x + w < self.rmargin:
                    text = text + bword
                    pixels = w
                    chars = 0
                else:
                    self.OutputLine(text, 1)
                    text = word
                    chars = length - 1
                    pixels = 0
            atbreak = 1

        self.OutputLine(text, 0)
        self.atbreak = data[(-1)] in string.whitespace

    def OutputLine(self, text, linebreak=0):
        if text:
            if TRACE:
                print 'olt:', text
            if TRACE:
                print 'olf:', self.font.size, self.font.bold, self.font.italic, self.font.underline, self.font.face
            self.pc.drawString(text, self.x, self.y, self.font, self.color)
            self.lineHeight = max(self.lineHeight, self.pc.fontHeight(self.font))
            self.x = self.x + self.pc.stringWidth(text, self.font)
        if linebreak:
            self.send_line_break()


__copyrite_jim__ = 'Copyright 1994, 1995 by James C. Ahlstrom, Stirling NJ, USA.\nComments and complaints to jim@interet.com\n\n                        All Rights Reserved\n\nPermission to use, copy, modify, and distribute this software and its \ndocumentation for any purpose and without fee is hereby granted, \nprovided that the above copyright notice appear in all copies and that\nboth that copyright notice and this permission notice appear in \nsupporting documentation.\n\nJAMES C. AHLSTROM DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS\nSOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND\nFITNESS, IN NO EVENT SHALL HE BE LIABLE FOR ANY SPECIAL, INDIRECT\nOR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM\nLOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,\nNEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION\nWITH THE USE OR PERFORMANCE OF THIS SOFTWARE.\n\n'
DEMO_HTML = 'Here\'s some starting text - should be rendered in\ndefault font and color, and should start at specified start coordinates.\n<BR><BR>\n<H2>HTMLPiddler.py</H2>\n<H3>Rendering HTML with Piddle</H3>\n\n<P>The <b>HTMLPiddler</b> class accepts an HTML string and a few layout constraints,\nand renders the HTML on a piddle canvas\n<P>An Example:\n<PRE>\n    piddler = HTMLPiddler(html=aHtmlString, \n                              start=(startX, startY), \n                              xLimits=(leftMarginX, rightMarginX), \n                              font=aPiddleFontForDefault, \n                              color=aPiddleColorForDefault)\n    piddler.renderOn(aPiddleCanvas)\n</PRE>\n\n<P>Limitations\n<UL>\n    <LI>only renders a subset of HTML (mostly text-related tags)\n    <LI>content between unsupported tags may not be rendered at all\n</UL>\n    \n<P><b>HTMLPiddler</b> is derived largely on "demo07.py" from the \n<A HREF="http://www.python.org/ftp/python/wpy/">WPY distribution</A>\nby <A HREF="mailto:jim@interet.com">Jim Ahlstrom</A>\n\n<P><i><b>HTMLPiddler.py</b> is mainly a demonstration/proof-of-concept, and\nis not really intended for real work.</i>\n<BR>\n<BR><A HREF="mailto:kuncej@mail.conservation.state.mo.us">Jeff Kunce</A>\n<BR><A HREF="http://starship.python.net/crew/jjkunce/">\n    http://starship.python.net/crew/jjkunce/</A>\n'

def demoPDF(html):
    import piddlePDF
    pc = piddlePDF.PDFCanvas((750, 1000), 'HTMLPiddler.pdf')
    pc.drawLine(100, 100, 250, 150, color=piddle.green)
    pc.drawRect(100, 100, 650, 900, edgeColor=piddle.pink)
    ptt = HTMLPiddler(html, (250, 150), (100, 650))
    ptt.renderOn(pc)
    pc.save()


def demoPIL(html):
    print 'be patient, this is a little slow...'
    import piddlePIL
    pc = piddlePIL.PILCanvas((800, 600), 'HTMLPiddler')
    pc.drawLine(0, 0, 100, 80, color=piddle.green)
    pc.drawRect(50, 50, 750, 550, edgeColor=piddle.pink)
    ptt = HTMLPiddler(html, (100, 80), (50, 750))
    ptt.renderOn(pc)
    pc.save(format='tif')


def demoTK(html):
    import piddleTK
    pc = piddleTK.TKCanvas((800, 600))
    pc.drawLine(0, 0, 50, 50, color=piddle.green)
    pc.drawRect(10, 10, 590, 790, edgeColor=piddle.pink)
    ptt = HTMLPiddler(html, (50, 50), (10, 790))
    pc.flush()
    ptt.renderOn(pc)


def demoWX(html):
    import piddleWX
    pc = piddleWX.WXCanvas((800, 600))
    pc.drawLine(0, 0, 50, 50, color=piddle.green)
    pc.drawRect(10, 10, 590, 790, edgeColor=piddle.pink)
    ptt = HTMLPiddler(html, (50, 50), (10, 790))
    pc.flush()
    ptt.renderOn(pc)


def demo(html=DEMO_HTML):
    while 1:
        print 'Demo of HTMLPiddler.py'
        print '   1. piddlePDF'
        print '   2. piddlePIL'
        print '   0. EXIT'
        sel = raw_input('Enter Selection Number: ')
        try:
            sel = string.atoi(string.strip(sel))
        except:
            sel = -1

        if sel == 0:
            break
        elif sel == 1:
            demoPDF(html)
        elif sel == 2:
            demoPIL(html)
        elif sel == 3:
            demoTK(html)
        elif sel == 4:
            demoWX(html)


if __name__ == '__main__':
    import pdb
    demo()