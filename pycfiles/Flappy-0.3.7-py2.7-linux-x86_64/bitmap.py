# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flappy/display/bitmap.py
# Compiled at: 2014-03-13 10:09:15
from flappy.display import BitmapData, DisplayObject

class PixelSnapping(object):
    NEVER = 0
    AUTO = 1
    ALWAYS = 2


class Bitmap(DisplayObject):

    def __init__(self, bitmap_data=None, pixel_snapping=PixelSnapping.AUTO, smoothing=False):
        DisplayObject.__init__(self, 'Bitmap')
        self.pixelSnapping = pixel_snapping
        self._smoothing = smoothing
        self._bitmapData = bitmap_data
        self._rebuild()

    def _rebuild(self):
        if self._bitmapData:
            g = self.graphics
            g.clear()
            g.beginBitmapFill(self._bitmapData, repeat=False, smooth=True)
            g.drawRect(0.0, 0.0, self._bitmapData.width, self._bitmapData.height)
            g.endFill()

    @property
    def smoothing(self):
        return self._smoothing

    @smoothing.setter
    def smoothing(self, value):
        self._smoothing = value
        self._rebuild()

    @property
    def bitmapData(self):
        return self._bitmapData

    @bitmapData.setter
    def bitmapData(self, value):
        self._bitmapData = value
        self._rebuild()