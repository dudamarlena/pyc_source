# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /cinje/block/generic.py
# Compiled at: 2019-03-06 14:21:14
# Size of source mod 2**32: 1805 bytes


class Generic(object):
    """Generic"""
    priority = 50
    _keywords = ('if', 'while', 'for', 'with', 'try')
    _continuation = ('elif', 'else', 'except', 'finally')
    _both = _keywords + _continuation

    def match(self, context, line):
        """Match code lines prefixed with a variety of keywords."""
        return line.kind == 'code' and line.partitioned[0] in self._both

    def __call__(self, context):
        """Process conditional declarations."""
        input = context.input
        try:
            declaration = input.next()
        except StopIteration:
            return
        else:
            stripped = declaration.stripped
            prefix, _ = declaration.partitioned
            if prefix in self._continuation:
                yield declaration.clone(line=(stripped + ':'), scope=(context.scope - 1))
                return
            yield declaration.clone(line=(stripped + ':'))
            context.scope += 1
            for i in context.stream:
                yield i

            context.scope -= 1