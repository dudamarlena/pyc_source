# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyqart/qr/args/rotation.py
# Compiled at: 2016-08-02 13:38:18
# Size of source mod 2**32: 664 bytes
__all__ = [
 'QrRotation']
_ROTATE_FUNC_LIST = [
 None,
 lambda y, x, s: (
  x, s - y - 1),
 lambda y, x, s: (
  s - y - 1, s - x - 1),
 lambda y, x, s: (
  s - x - 1, y)]

class QrRotation(object):

    def __init__(self, rotate_index):
        assert 0 <= rotate_index <= 3, 'Rotation must between 0 and 3.'
        self._index = rotate_index

    @property
    def index(self):
        return self._index

    @property
    def rotate_func(self):
        return _ROTATE_FUNC_LIST[self.index]