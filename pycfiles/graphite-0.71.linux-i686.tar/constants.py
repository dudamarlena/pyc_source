# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/graphite/constants.py
# Compiled at: 2007-10-25 11:25:30


class AlignChar(object):

    def __init__(self, c='.'):
        self.c = c

    def align(self, text):
        if len(text) == 0:
            return 0.5
        try:
            idx = text.index(self.c)
        except ValueError:
            return 1.0

        return (0.5 + idx) / len(text)


DECIMAL = AlignChar('.')
LEFT = 'LEFT'
RIGHT = 'RIGHT'
CENTER = 'CENTER'
TOP = 'TOP'
BOTTOM = 'BOTTOM'
(X, Y, Z) = (0, 1, 2)
AUTO = 'AUTO'
UNSPECIFIED = -1
MIN = 0
MAX = 1
LINEAR = 1
SOLID = 'SOLID'
DASHED = 'DASHED'