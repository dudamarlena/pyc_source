# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cinje/block/generic.py
# Compiled at: 2019-03-06 14:21:14
# Size of source mod 2**32: 1805 bytes


class Generic(object):
    __doc__ = 'Block-level passthrough.  Blocks must be terminated by ": end" markers.\n\t\n\tSupport is included for chains of blocks of the expected types, without requiring ": end" markers between them.\n\t\n\tThis block-level transformer handles: "if", "elif", and "else" conditional scopes; "while" and "for" loops,\n\tincluding the optional "else" clause to "for"; "with" context managers; and the exception management machinery of\n\t"try", "except", "finally", and "else".  (Any given intermediary component is optional, of course.)\n\t\n\tSyntax::\n\t\n\t\t: if ...\n\t\t: elif ...\n\t\t: else\n\t\t: end\n\t\t\n\t\t: while ...\n\t\t: end\n\t\t\n\t\t: for ...\n\t\t: else\n\t\t: end\n\t\t\n\t\t: with ...\n\t\t: end\n\t\t\n\t\t: try\n\t\t: except ...\n\t\t: finally\n\t\t: else\n\t\t: end\n\t\n\tSingle-line conditionals and loops are not allowed, and the declaration should not include a trailing colon.\n\t'
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