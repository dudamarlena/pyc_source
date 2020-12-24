# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /cinje/inline/flush.py
# Compiled at: 2019-03-06 14:24:28
# Size of source mod 2**32: 1710 bytes
from ..util import Line, ensure_buffer

def flush_template(context, declaration=None, reconstruct=True):
    """Emit the code needed to flush the buffer.
                
        Will only emit the yield and clear if the buffer is known to be dirty.
        """
    if declaration is None:
        declaration = Line(0, '')
    if {'text', 'dirty'}.issubset(context.flag):
        yield declaration.clone(line='yield "".join(_buffer)')
        context.flag.remove('text')
        context.flag.remove('dirty')
        if reconstruct:
            for i in ensure_buffer(context):
                yield i

    if declaration.stripped == 'yield':
        yield declaration


class Flush(object):
    """Flush"""
    priority = 25

    def match(self, context, line):
        """Match exact "flush" command usage."""
        return line.kind == 'code' and line.stripped in ('flush', 'yield')

    def __call__(self, context):
        try:
            line = context.input.next()
        except StopIteration:
            return
        else:
            return flush_template(context, line)