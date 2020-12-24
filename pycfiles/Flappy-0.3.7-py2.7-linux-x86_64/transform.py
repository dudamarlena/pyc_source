# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flappy/geom/transform.py
# Compiled at: 2014-03-13 10:09:15


class Transform(object):

    def __init__(self, parent):
        self.obj = parent

    @property
    def colorTransform(self):
        return self.obj._getColorTransform()

    @colorTransform.setter
    def colorTransform(self, ct):
        self.obj._setColorTransform(ct)
        return ct

    @property
    def concatenatedColorTransform(self):
        return self.obj._getColorTransform(True)

    @property
    def concatenatedMatrix(self):
        return self.obj._getMatrix(True)

    @property
    def matrix(self):
        return self.obj._getMatrix()

    @matrix.setter
    def matrix(self, m):
        self.obj._setMatrix(m)
        return m

    @property
    def pixelBounds(self):
        return self.obj._getPixelBounds()