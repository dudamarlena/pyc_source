# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyqart/qr/args/mask.py
# Compiled at: 2016-08-02 06:06:42
# Size of source mod 2**32: 1354 bytes
__all__ = [
 'QrMask']
_FUNCTION_LIST = [
 lambda y, x: (x + y) % 2 == 0,
 lambda y, x: y % 2 == 0,
 lambda y, x: x % 3 == 0,
 lambda y, x: (x + y) % 3 == 0,
 lambda y, x: (y // 2 + x // 3) % 2 == 0,
 lambda y, x: x * y % 2 + x * y % 3 == 0,
 lambda y, x: (x * y % 2 + x * y % 3) % 2 == 0,
 lambda y, x: ((x + y) % 2 + x * y % 3) % 2 == 0]

class QrMask(object):

    def __init__(self, mask_index):
        assert 0 <= mask_index <= 7, 'Mask must between 0 and 7'
        self._index = mask_index

    @property
    def index(self):
        """
        :return: Mask index, from 0 to 7, specific the mask pattern.
        :rtype: int
        """
        return self._index

    @property
    def should_invert(self):
        """
        :return: A function accept (y, x) to decide if point should invert.
        :rtype: callable
        """
        return _FUNCTION_LIST[self.index]