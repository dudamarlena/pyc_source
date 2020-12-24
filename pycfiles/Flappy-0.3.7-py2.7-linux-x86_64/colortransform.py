# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flappy/geom/colortransform.py
# Compiled at: 2014-03-13 10:09:15


class ColorTransform(object):

    def __init__(self, redMultiplier=1.0, greenMultiplier=1.0, blueMultiplier=1.0, alphaMultiplier=1.0, redOffset=0.0, greenOffset=0.0, blueOffset=0.0, alphaOffset=0.0):
        self.redMultiplier = redMultiplier
        self.greenMultiplier = greenMultiplier
        self.blueMultiplier = blueMultiplier
        self.alphaMultiplier = alphaMultiplier
        self.redOffset = redOffset
        self.greenOffset = greenOffset
        self.blueOffset = blueOffset
        self.alphaOffset = alphaOffset

    def concat(self, second):
        self.redMultiplier += second.redMultiplier
        self.greenMultiplier += second.greenMultiplier
        self.blueMultiplier += second.blueMultiplier
        self.alphaMultiplier += second.alphaMultiplier

    @property
    def color(self):
        col = int(self.redOffset) << 16
        col |= int(self.greenOffset) << 8
        col |= int(self.blueOffset)
        return col

    @color.setter
    def color(self, value):
        self.redOffset = value >> 16 & 255
        self.greenOffset = value >> 8 & 255
        self.blueOffset = value & 255
        self.redMultiplier = 0
        self.greenMultiplier = 0
        self.blueMultiplier = 0
        return self.color