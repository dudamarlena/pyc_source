# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyqart/art/target.py
# Compiled at: 2016-08-04 13:24:56
# Size of source mod 2**32: 930 bytes
__all__ = [
 'Target']

class Target(object):

    def __init__(self, y, x, fill, contrast, point):
        self._y = y
        self._x = x
        self._fill = fill
        self._contrast = contrast
        self._point = point
        self._hard_zero = False

    @property
    def fill(self):
        return self._fill

    @property
    def contrast(self):
        return self._contrast

    @property
    def y(self):
        return self._y

    @property
    def x(self):
        return self._x

    @property
    def point(self):
        return self._point

    def set_hard_zero(self):
        self._hard_zero = True

    def is_hard_zero(self):
        return self._hard_zero

    def __str__(self):
        return 'Target({fill}, {contrast:.3f})'.format(fill=self.fill, contrast=self.contrast)