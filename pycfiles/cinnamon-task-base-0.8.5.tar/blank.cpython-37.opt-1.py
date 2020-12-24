# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /cinje/inline/blank.py
# Compiled at: 2019-03-06 14:23:07
# Size of source mod 2**32: 283 bytes


class Blank(object):
    """Blank"""
    priority = -90

    def match(self, context, line):
        return not line.stripped

    def __call__(self, context):
        try:
            yield context.input.next()
        except StopIteration:
            return