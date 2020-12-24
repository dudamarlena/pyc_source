# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\language\base\number_base.py
# Compiled at: 2009-01-22 02:49:02
"""
This file implements the Number class.

"""
from dragonfly.grammar.elements import Alternative, Repetition, Sequence

class Number(Alternative):
    _element_type = None
    _int_max = 1000000
    _ser_len = 8

    def __init__(self, name=None, zero=False):
        name = str(name)
        int_name = '_Number_int_' + name
        if zero:
            int_min = 0
        else:
            int_min = 1
        single = self._element_type(None, int_min, self._int_max)
        ser_name = '_Number_ser_' + name
        item = self._element_type(None, 0, 100)
        if zero:
            series = Repetition(item, 1, self._ser_len)
        else:
            first = self._element_type(None, 1, 100)
            repetition = Repetition(item, 0, self._ser_len - 1)
            series = Sequence([first, repetition])
        children = [single, series]
        Alternative.__init__(self, children, name=name)
        return

    def value(self, node):
        value = Alternative.value(self, node)
        if isinstance(value, list):
            items = []
            for item in value:
                if isinstance(item, list):
                    items.extend(item)
                else:
                    items.append(item)

            value = 0
            for item in items:
                if item < 10:
                    factor = 10
                else:
                    factor = 100
                value *= factor
                value += item

        return value