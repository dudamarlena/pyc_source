# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /cinje/inline/comment.py
# Compiled at: 2019-03-06 14:23:56
# Size of source mod 2**32: 722 bytes


class Comment(object):
    """Comment"""
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