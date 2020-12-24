# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/ImageEnhance.py
# Compiled at: 2007-09-25 20:00:35
import Image, ImageFilter

class _Enhance:

    def enhance(self, factor):
        return Image.blend(self.degenerate, self.image, factor)


class Color(_Enhance):
    """Adjust image colour balance"""

    def __init__(self, image):
        self.image = image
        self.degenerate = image.convert('L').convert(image.mode)


class Contrast(_Enhance):
    """Adjust image contrast"""

    def __init__(self, image):
        self.image = image
        mean = reduce(lambda a, b: a + b, image.convert('L').histogram()) / 256.0
        self.degenerate = Image.new('L', image.size, mean).convert(image.mode)


class Brightness(_Enhance):
    """Adjust image brightness"""

    def __init__(self, image):
        self.image = image
        self.degenerate = Image.new(image.mode, image.size, 0)


class Sharpness(_Enhance):
    """Adjust image sharpness"""

    def __init__(self, image):
        self.image = image
        self.degenerate = image.filter(ImageFilter.SMOOTH)