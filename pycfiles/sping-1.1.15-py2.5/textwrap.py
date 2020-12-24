# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sping\textwrap.py
# Compiled at: 2002-06-27 14:43:17
"""chris lee 1999, based upon Andy Robinson's line breaking code
I use these classes to manage text in sping.  They aren't really polished yet--they don't
   handle hypthenation-breaks and you can't flow text from one box or column to the next--but
   they are useful.

classes:
   TextColumn -- defines a colmun of text with automatic word wrapping, allows for right, left,
                 and centered alignment
               
   TextBox --  allows you to define a rectangle on the page into which you can place
               text which is automatically word-wrapped.  Give the origin (x1,y1) of the
               upper-left corner of the box and the width and height of the box.  Allows for
               rotation of the box around it's x1,y1 origin, and alignment of the text
               within the box

Usage: create the object, set the text buffer for the object, then call the object's draw()
               method

"""
import string, math
TA_LEFT = -1
TA_RIGHT = 1
TA_CENTERED = 0

class TextColumn:
    """Provides a region on a canvas for placing justifed text of one tye of font.
    The upper left corner is defined by x1,y1 and the right side is defined by x2"""

    def __init__(self, sping_canvas, x1, y1, x2, input_text=None, font=None, align=TA_LEFT):
        self.canvas = sping_canvas
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.width = x2 - x1
        self.text = input_text
        self.font = font
        self.align = align
        self.linespacing = 1.0

    def _breakPara(self, text, maxwidth, font=None):
        """Returns a structure broken into lines.  Each line has two items.  Item one
        is the extra points of space available on that line; item two is the list of
        words themselves"""
        lines = []
        spacewidth = self.canvas.stringWidth(' ', font)
        words = string.split(text, ' ')
        currentline = []
        currentwidth = -spacewidth
        for word in words:
            wordwidth = self.canvas.stringWidth(word, font)
            space_available = maxwidth - (currentwidth + spacewidth + wordwidth)
            if space_available > 0:
                currentline.append(word)
                currentwidth = currentwidth + spacewidth + wordwidth
            else:
                lines.append((maxwidth - currentwidth, currentline))
                currentline = [word]
                currentwidth = wordwidth

        if currentline != []:
            lines.append((maxwidth - currentwidth, currentline))
        return lines

    def draw(self):
        """Crude paragraph-wrapper"""
        orig_self_font = self.font
        if not self.font:
            self.font = self.canvas.defaultFont
        lineheight = self.font.size * self.linespacing
        cur_y = self.y1 + lineheight
        wrapinfo = self._breakPara(self.text, self.width, self.font)
        for (extra_space, words) in wrapinfo:
            text = string.join(words, ' ')
            if self.align == TA_LEFT:
                self.canvas.drawString(text, self.x1, cur_y, self.font)
            elif self.align == TA_RIGHT:
                self.canvas.drawString(text, self.x1 + extra_space, cur_y, self.font)
            elif self.align == TA_CENTERED:
                self.canvas.drawString(text, self.x1 + 0.5 * extra_space, cur_y, self.font)
            cur_y = cur_y + lineheight

        self.font = orig_self_font
        return cur_y


class TextBox:
    """Provides a region on a canvas for placing justifed text of one type of font"""

    def __init__(self, sping_canvas, x1, y1, width, height, angle=0, input_text=None, font=None, align=TA_LEFT):
        self.canvas = sping_canvas
        self.x1 = x1
        self.x2 = x1 + width
        self.y1 = y1
        self.y2 = y1 + height
        self.width = width
        self.height = height
        self.angle = angle
        self.sinA = math.sin(angle / 180.0 * math.pi)
        self.cosA = math.cos(angle / 180.0 * math.pi)
        self.text = input_text
        self.font = font
        self.align = align
        self.linespacing = 1.0

    def _breakPara(self, text, maxwidth, font=None):
        """Returns a structure broken into lines.  Each line has two items.  Item one
        is the extra points of space available on that line; item two is the list of
        words themselves"""
        lines = []
        spacewidth = self.canvas.stringWidth(' ', font)
        words = string.split(text, ' ')
        currentline = []
        currentwidth = -spacewidth
        for word in words:
            wordwidth = self.canvas.stringWidth(word, font)
            space_available = maxwidth - (currentwidth + spacewidth + wordwidth)
            if space_available > 0:
                currentline.append(word)
                currentwidth = currentwidth + spacewidth + wordwidth
            else:
                lines.append((maxwidth - currentwidth, currentline))
                currentline = [word]
                currentwidth = wordwidth

        if currentline != []:
            lines.append((maxwidth - currentwidth, currentline))
        return lines

    def MatRotate(self, vx, vy):
        wx, wy = self.cosA * vx + self.sinA * vy, -self.sinA * vx + self.cosA * vy
        return (wx, wy)

    def drawBoxBorder(self):
        """Useful for debugging, shows box in which text should go."""
        (wx1, wy1) = self.MatRotate(self.width, 0)
        (wx2, wy2) = self.MatRotate(self.width, self.height)
        (wx3, wy3) = self.MatRotate(0, self.height)
        self.canvas.drawLine(self.x1, self.y1, self.x1 + wx1, self.y1 + wy1)
        self.canvas.drawLine(self.x1 + wx1, self.y1 + wy1, self.x1 + wx2, self.y1 + wy2)
        self.canvas.drawLine(self.x1 + wx2, self.y1 + wy2, self.x1 + wx3, self.y1 + wy3)
        self.canvas.drawLine(self.x1 + wx3, self.y1 + wy3, self.x1, self.y1)

    def draw(self):
        """Crude paragraph-wrapper"""
        orig_self_font = self.font
        if not self.font:
            self.font = self.canvas.defaultFont
        lineheight = self.font.size * self.linespacing
        cur_y = lineheight
        wrapinfo = self._breakPara(self.text, self.width, self.font)
        for (extra_space, words) in wrapinfo:
            text = string.join(words, ' ')
            if self.align == TA_LEFT:
                if self.angle != 0:
                    (wx, wy) = self.MatRotate(0, cur_y)
                    wx, wy = wx + self.x1, wy + self.y1
                else:
                    wx, wy = self.x1, self.y1 + cur_y
                self.canvas.drawString(text, wx, wy, self.font, angle=self.angle)
            elif self.align == TA_RIGHT:
                if self.angle != 0:
                    (wx, wy) = self.MatRotate(extra_space, cur_y)
                    wx, wy = wx + self.x1, wy + self.y1
                else:
                    wx, wy = self.x1 + extra_space, self.y1 + cur_y
                self.canvas.drawString(text, wx, wy, self.font, angle=self.angle)
            elif self.align == TA_CENTERED:
                if self.angle != 0:
                    (wx, wy) = self.MatRotate(0.5 * extra_space, cur_y)
                    wx, wy = wx + self.x1, wy + self.y1
                else:
                    wx, wy = self.x1 + 0.5 * extra_space, self.y1 + cur_y
                self.canvas.drawString(text, wx, wy, self.font, angle=self.angle)
            cur_y = cur_y + lineheight
            if cur_y > self.height:
                print 'Warning!! text is too long for box height'
                break

        self.font = orig_self_font
        return cur_y


if __name__ == '__main__':
    import sping.pid, sping.PDF
    canvas = sping.PDF.PDFCanvas((300, 300), name='TextClasses.pdf')
    print 'Will save output to TextClasses.pdf'
    textcol1 = TextColumn(canvas, 10, 10, 145, font=sping.pid.Font(face='serif', size=12), align=TA_RIGHT)
    textcol1.text = 'These text classes are examples of how to define columns of left, right, ' + 'and center-aligned text with automatic word wrapping.'
    textcol1.draw()
    textcol2 = TextColumn(canvas, 190, 190, 290, align=TA_RIGHT)
    textcol2.text = 'The sea is calm to-night. The tide is full, the moon lies fair upon ' + 'the straits; - on the French coast the light gleams and is gone...'
    textcol2.draw()
    textcol3 = TextColumn(canvas, 155, 10, 290, font=sping.pid.Font(face='serif', size=12), align=TA_LEFT)
    textcol3.text = 'A box of text may also be rotated ' + 'with the text contents clipped to a rectangle'
    textcol3.draw()
    textbox4 = TextBox(canvas, 10, 290, 100, 50, angle=90)
    textbox4.text = 'A box of text may also be rotated with the text contents clipped' + ' to a rectangle'
    textbox4.draw()
    textbox5 = TextBox(canvas, 40, 170, 100, 50, angle=50, align=TA_LEFT)
    textbox5.text = textcol3.text
    textbox5.draw()
    textbox6 = TextBox(canvas, 160, 100, 100, 50, angle=-25, align=TA_LEFT)
    textbox6.text = textcol3.text
    textbox6.draw()
    canvas.flush()
    canvas.save()