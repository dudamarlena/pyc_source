# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Captcha/Visual/Text.py
# Compiled at: 2006-02-05 00:25:47
""" Captcha.Visual.Text

Text generation for visual CAPTCHAs.
"""
import random, os
from Captcha import Visual, File
import ImageFont, ImageDraw

class FontFactory(File.RandomFileFactory):
    """Picks random fonts and/or sizes from a given list.
       'sizes' can be a single size or a (min,max) tuple.
       If any of the given files are directories, all *.ttf found
       in that directory will be added.
       """
    __module__ = __name__
    extensions = [
     '.ttf']
    basePath = 'fonts'

    def __init__(self, sizes, *fileNames):
        File.RandomFileFactory.__init__(self, *fileNames)
        if type(sizes) is tuple:
            self.minSize = sizes[0]
            self.maxSize = sizes[1]
        else:
            self.minSize = sizes
            self.maxSize = sizes

    def pick(self):
        """Returns a (fileName, size) tuple that can be passed to ImageFont.truetype()"""
        fileName = File.RandomFileFactory.pick(self)
        size = int(random.uniform(self.minSize, self.maxSize) + 0.5)
        return (fileName, size)


defaultFontFactory = FontFactory((30, 40), 'vera')

class TextLayer(Visual.Layer):
    """Represents a piece of text rendered within the image.
       Alignment is given such that (0,0) places the text in the
       top-left corner and (1,1) places it in the bottom-left.

       The font and alignment are optional, if not specified one is
       chosen randomly. If no font factory is specified, the default is used.
       """
    __module__ = __name__

    def __init__(self, text, alignment=None, font=None, fontFactory=None, textColor='black', borderSize=0, borderColor='white'):
        global defaultFontFactory
        if fontFactory is None:
            fontFactory = defaultFontFactory
        if font is None:
            font = fontFactory.pick()
        if alignment is None:
            alignment = (
             random.uniform(0, 1), random.uniform(0, 1))
        self.text = text
        self.alignment = alignment
        self.font = font
        self.textColor = textColor
        self.borderSize = borderSize
        self.borderColor = borderColor
        return

    def render(self, img):
        font = ImageFont.truetype(*self.font)
        textSize = font.getsize(self.text)
        draw = ImageDraw.Draw(img)
        x = int((img.size[0] - textSize[0] - self.borderSize * 2) * self.alignment[0] + 0.5)
        y = int((img.size[1] - textSize[1] - self.borderSize * 2) * self.alignment[1] + 0.5)
        if self.borderSize > 0:
            for bx in (-1, 0, 1):
                for by in (-1, 0, 1):
                    if bx and by:
                        draw.text((x + bx * self.borderSize, y + by * self.borderSize), self.text, font=font, fill=self.borderColor)

        draw.text((x, y), self.text, font=font, fill=self.textColor)