# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\language\base\digits_base.py
# Compiled at: 2009-01-22 11:33:57
"""
This file implements base classes for structured number grammar
elements.

"""
from dragonfly.grammar.elements import Alternative, Repetition, Compound

class DigitsBase(Repetition):
    _digits = None
    _digit_name = '_digit'

    def __init__(self, name=None, min=1, max=12, as_int=False):
        self._as_int = as_int
        if self._as_int:
            self._base = len(self._digits) - 1
        pairs = []
        for (value, word) in enumerate(self._digits):
            if isinstance(word, str):
                pairs.append((word, value))
            elif isinstance(word, (tuple, list)):
                pairs.extend([ (w, value) for w in word ])
            else:
                raise ValueError('Invalid type in digit list: %r' % word)

        alternatives = [ Compound(w, value=v, name=self._digit_name) for (w, v) in pairs ]
        child = Alternative(alternatives)
        Repetition.__init__(self, child, min, max, name=name)

    def __str__(self):
        arguments = '%d-%d' % (self._min, self._max)
        if self.name is not None:
            arguments = "'%s', %s" % (self.name, arguments)
        return '%s(%s)' % (self.__class__.__name__, arguments)

    def value(self, node):
        children = node.get_children_by_name(self._digit_name)
        digits = [ c.value() for c in children ]
        if self._as_int:
            value = 0
            for d in digits:
                value *= self._base
                value += d

            return d
        else:
            return digits