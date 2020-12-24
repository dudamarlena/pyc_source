# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/NEMbox/scrollstring.py
# Compiled at: 2020-03-16 06:22:03
# Size of source mod 2**32: 1457 bytes
from __future__ import print_function, unicode_literals, division, absolute_import
from time import time
from future.builtins import int, chr

class scrollstring(object):

    def __init__(self, content, START):
        self.content = content
        self.display = content
        self.START = START // 1
        self.update()

    def update(self):
        self.display = self.content
        curTime = time() // 1
        offset = max(int((curTime - self.START) % len(self.content)) - 1, 0)
        while offset > 0:
            if self.display[0] > chr(127):
                offset -= 1
                self.display = self.display[3:] + self.display[:3]
            else:
                offset -= 1
                self.display = self.display[1:] + self.display[:1]

    def __repr__(self):
        return self.display


def truelen(string):
    """
    It appears one Asian character takes two spots, but __len__
    counts it as three, so this function counts the dispalyed
    length of the string.

    >>> truelen('abc')
    3
    >>> truelen('你好')
    4
    >>> truelen('1二3')
    4
    >>> truelen('')
    0
    """
    return len(string) + sum((1 for c in string if c > chr(127)))