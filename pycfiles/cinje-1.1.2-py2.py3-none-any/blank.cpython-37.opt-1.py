# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cinje/inline/blank.py
# Compiled at: 2019-03-06 14:23:07
# Size of source mod 2**32: 283 bytes


class Blank(object):
    __doc__ = 'Blank line handler.  This eats leading blank lines.'
    priority = -90

    def match(self, context, line):
        return not line.stripped

    def __call__(self, context):
        try:
            yield context.input.next()
        except StopIteration:
            return