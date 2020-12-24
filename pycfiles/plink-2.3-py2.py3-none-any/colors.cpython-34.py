# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /build/plink/build/lib/plink/colors.py
# Compiled at: 2019-07-15 20:56:41
# Size of source mod 2**32: 2457 bytes
"""
Tools for dealing with colors, including the class Palette.
"""
from colorsys import hls_to_rgb

class Palette:
    __doc__ = '\n    Dispenses colors.\n    '

    def __init__(self):
        self.colorizer = Colorizer()
        self.reset()

    def reset(self):
        self.free_colors = [self.colorizer(n) for n in range(6)]
        self.active_colors = []

    def new(self):
        if len(self.free_colors) == 0:
            for n in range(10):
                color = self.colorizer(len(self.active_colors))
                if color not in self.free_colors + self.active_colors:
                    self.free_colors.append(color)
                    continue

        try:
            color = self.free_colors.pop(0)
            self.active_colors.append(color)
            return color
        except IndexError:
            self.active_colors.append('black')
            return 'black'

    def recycle(self, color):
        self.active_colors.remove(color)
        self.free_colors.append(color)


class Colorizer:
    __doc__ = '\n    Callable class which returns an RGB color string when passed an\n    index.  Uses the same algorithm as the SnapPea kernel.\n    '

    def __init__(self, lightness=0.5, saturation=0.7):
        self.base_hue = [0, 4, 2, 3, 5, 1]
        self.lightness = lightness
        self.saturation = saturation

    def __call__(self, index):
        hue = (self.base_hue[(index % 6)] + self.index_to_hue(index // 6)) / 6.0
        rgb = hls_to_rgb(hue, self.lightness, self.saturation)
        return '#%.2x%.2x%.2x' % tuple(int(x * 255) for x in rgb)

    def index_to_hue(self, index):
        num, den = (0, 1)
        while index:
            num = num << 1
            den = den << 1
            if index & 1:
                num += 1
            index = index >> 1

        return float(num) / float(den)