# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cinje/inline/use.py
# Compiled at: 2019-03-06 14:26:52
# Size of source mod 2**32: 1554 bytes
from ..util import py, pypy, ensure_buffer
PREFIX = '_buffer.extend(' if pypy else '__w('

class Use(object):
    __doc__ = 'Consume the result of calling another template function, extending the local buffer.\n\t\n\tThis is meant to consume non-wrapping template functions.  For wrapping functions see ": using" instead.\n\t\n\tSyntax:\n\t\n\t\t: use <name-constant> [<arguments>]\n\t\n\tThe name constant must resolve to a generator function that participates in the cinje "yielded buffer" protocol.\n\t\n\t'
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