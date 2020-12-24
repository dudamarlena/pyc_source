# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cinje/inline/require.py
# Compiled at: 2019-03-06 14:25:23
# Size of source mod 2**32: 1153 bytes
from importlib import import_module

class Require(object):
    __doc__ = 'Include reusable components from other modules.\n\t\n\tDoes what is nessicary to discover template functions and construct complete imports template-side.\n\t\n\tSyntax:\n\t\n\t\t: require package.subpackage.module\n\t\n\tAll template functions in the target namespace will be imported.\n\t'
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