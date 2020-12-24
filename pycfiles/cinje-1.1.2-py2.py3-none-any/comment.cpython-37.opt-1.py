# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cinje/inline/comment.py
# Compiled at: 2019-03-06 14:23:56
# Size of source mod 2**32: 722 bytes


class Comment(object):
    __doc__ = 'Line comment handler.\n\t\n\tThis handles not emitting double-hash comments and has a high priority to prevent other processing of\n\tcommented-out lines.\n\t\n\tSyntax:\n\t\n\t\t# <comment>\n\t\t## <hidden comment>\n\t'
    priority = -90

    def match(self, context, line):
        """Match lines prefixed with a hash ("#") mark that don't look like text."""
        stripped = line.stripped
        return stripped.startswith('#') and not stripped.startswith('#{')

    def __call__(self, context):
        """Emit comments into the final code that aren't marked as hidden/private."""
        try:
            line = context.input.next()
        except StopIteration:
            return
        else:
            if not line.stripped.startswith('##'):
                yield line