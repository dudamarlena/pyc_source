# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vaitk/core/VSize.py
# Compiled at: 2015-05-02 14:14:14
# Size of source mod 2**32: 542 bytes


class VSize(object):

    def __init__(self, width, height):
        self._size = (width, height)

    def __iter__(self):
        return iter(self._size)

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

    def __str__(self):
        return 'VSize(width=%d, height=%d)' % self._size

    class tuple:

        @staticmethod
        def width(size):
            return size[0]

        @staticmethod
        def height(size):
            return size[1]