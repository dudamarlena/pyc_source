# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /cinje/inline/use.py
# Compiled at: 2019-03-06 14:26:52
# Size of source mod 2**32: 1554 bytes
from ..util import py, pypy, ensure_buffer
PREFIX = '_buffer.extend(' if pypy else '__w('

class Use(object):
    """Use"""
    priority = 25

    def match(self, context, line):
        """Match code lines prefixed with a "use" keyword."""
        return line.kind == 'code' and line.partitioned[0] == 'use'

    def __call__(self, context):
        """Wrap the expression in a `_buffer.extend()` call."""
        input = context.input
        try:
            declaration = input.next()
        except StopIteration:
            return
        else:
            parts = declaration.partitioned[1]
            name, _, args = parts.partition(' ')
            for i in ensure_buffer(context):
                yield i

            name = name.rstrip()
            args = args.lstrip()
            if 'buffer' in context.flag:
                yield declaration.clone(line=(PREFIX + name + '(' + args + '))'))
                context.flag.add('dirty')
                return
            if py == 3:
                yield declaration.clone(line=('yield from ' + name + '(' + args + ')'))
            else:
                yield declaration.clone(line=('for _chunk in ' + name + '(' + args + '):'))
                yield declaration.clone(line='yield _chunk', scope=(context.scope + 1))