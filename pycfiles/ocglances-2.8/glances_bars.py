# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/outputs/glances_bars.py
# Compiled at: 2017-02-11 10:25:25
"""Manage bars for Glances output."""
from __future__ import division
from math import modf
curses_bars = [
 ' ', ' ', ' ', ' ', '|', '|', '|', '|', '|']

class Bar(object):
    r"""Manage bar (progression or status).

    import sys
    import time
    b = Bar(10)
    for p in range(0, 100):
        b.percent = p
        print("\r%s" % b),
        time.sleep(0.1)
        sys.stdout.flush()
    """

    def __init__(self, size, pre_char='[', post_char=']', empty_char=' ', with_text=True):
        self.__size = size
        self.__percent = 0
        self.min_value = 0
        self.max_value = 100
        self.__pre_char = pre_char
        self.__post_char = post_char
        self.__empty_char = empty_char
        self.__with_text = with_text

    @property
    def size(self, with_decoration=False):
        if with_decoration:
            return self.__size
        if self.__with_text:
            return self.__size - 6

    @property
    def percent(self):
        return self.__percent

    @percent.setter
    def percent(self, value):
        if value <= self.min_value:
            value = self.min_value
        if value >= self.max_value:
            value = self.max_value
        self.__percent = value

    @property
    def pre_char(self):
        return self.__pre_char

    @property
    def post_char(self):
        return self.__post_char

    def __str__(self):
        """Return the bars."""
        frac, whole = modf(self.size * self.percent / 100.0)
        ret = curses_bars[8] * int(whole)
        if frac > 0:
            ret += curses_bars[int(frac * 8)]
            whole += 1
        ret += self.__empty_char * int(self.size - whole)
        if self.__with_text:
            ret = ('{}{:>5}%').format(ret, self.percent)
        return ret