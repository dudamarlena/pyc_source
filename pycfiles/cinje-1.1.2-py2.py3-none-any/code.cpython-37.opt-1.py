# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cinje/inline/code.py
# Compiled at: 2019-03-06 14:23:26
# Size of source mod 2**32: 443 bytes


class Code(object):
    __doc__ = 'General code handler.\n\t\n\tThis captures all code segments not otherwise handled.  It has a very low priority to ensure other "code" handlers\n\tget a chance to run first.\n\t\n\tSyntax:\n\t\n\t\t: <code>\n\t'
    priority = 100

    def match(self, context, line):
        return line.kind == 'code'

    def __call__(self, context):
        try:
            yield context.input.next()
        except StopIteration:
            return