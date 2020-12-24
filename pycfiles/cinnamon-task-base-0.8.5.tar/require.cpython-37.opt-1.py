# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /cinje/inline/require.py
# Compiled at: 2019-03-06 14:25:23
# Size of source mod 2**32: 1153 bytes
from importlib import import_module

class Require(object):
    """Require"""
    priority = 25

    def match(self, context, line):
        """Match code lines prefixed with a "require" keyword."""
        return line.kind == 'code' and line.partitioned[0] == 'require'

    def __call__(self, context):
        """Identify template functions in the target namespace, and construct the import line for them."""
        input = context.input
        try:
            declaration = input.next()
        except StopIteration:
            return
        else:
            namespace = declaration.partitioned[1]
            module = import_module(namespace)
            if not hasattr(module, '__tmpl__'):
                raise ImportError('Attempted to require ' + namespace + ', which contains no template functions.')
            yield declaration.clone(line=('from ' + namespace + ' import ' + ', '.join(module.__tmpl__)))