# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Captcha/Visual/Backgrounds.py
# Compiled at: 2006-02-05 00:25:47
__doc__ = ' Captcha.Visual.Backgrounds\n\nBackground layers for visual CAPTCHAs\n'
from Captcha.Visual import Layer, Pictures
import random, os, ImageDraw, Image

class SolidColor(Layer):
    """A solid color background. Very weak on its own, but good
       to combine with other backgrounds.
       """
    __module__ = __name__

    def __init__(self, color='white'):
        self.color = color

    def render(self, image):
        image.paste(self.color)


class Grid(Layer):
    """A grid of lines, with a given foreground color.
       The size is given in pixels. The background is transparent,
       so another layer (like SolidColor) should be put behind it.
       """
    __module__ = __name__

    def __init__(self, size=16, foreground='black'):
        self.size = size
        self.foreground = foreground
        self.offset = (random.uniform(0, self.size), random.uniform(0, self.size))

    def render(self, image):
        draw = ImageDraw.Draw(image)
        for i in xrange(image.size[0] / self.size + 1):
            draw.line((i * self.size + self.offset[0], 0, i * self.size + self.offset[0], image.size[1]), fill=self.foreground)

        for i in xrange(image.size[0] / self.size + 1):
            draw.line((0, i * self.size + self.offset[1], image.size[0], i * self.size + self.offset[1]), fill=self.foreground)


class TiledImage(Layer):
    """Pick a random image and a random offset, and tile the rendered image with it"""
    __module__ = __name__

    def __init__(self, imageFactory=Pictures.abstract):
        self.tileName = imageFactory.pick()
        self.offset = (random.uniform(0, 1), random.uniform(0, 1))

    def render(self, image):
        tile = Image.open(self.tileName)
        for j in xrange(-1, int(image.size[1] / tile.size[1]) + 1):
            for i in xrange(-1, int(image.size[0] / tile.size[0]) + 1):
                dest = (
                 int((self.offset[0] + i) * tile.size[0]), int((self.offset[1] + j) * tile.size[1]))
                image.paste(tile, dest)


class CroppedImage(Layer):
    """Pick a random image, cropped randomly. Source images should be larger than the CAPTCHA."""
    __module__ = __name__

    def __init__(self, imageFactory=Pictures.nature):
        self.imageName = imageFactory.pick()
        self.align = (random.uniform(0, 1), random.uniform(0, 1))

    def render(self, image):
        i = Image.open(self.imageName)
        image.paste(i, (int(self.align[0] * (image.size[0] - i.size[0])), int(self.align[1] * (image.size[1] - i.size[1]))))


class RandomDots(Layer):
    """Draw random colored dots"""
    __module__ = __name__

    def __init__(self, colors=(
 'white', 'black'), dotSize=4, numDots=400):
        self.colors = colors
        self.dotSize = dotSize
        self.numDots = numDots
        self.seed = random.random()

    def render(self, image):
        r = random.Random(self.seed)
        for i in xrange(self.numDots):
            bx = int(r.uniform(0, image.size[0] - self.dotSize))
            by = int(r.uniform(0, image.size[1] - self.dotSize))
            image.paste(r.choice(self.colors), (bx, by, bx + self.dotSize - 1, by + self.dotSize - 1))