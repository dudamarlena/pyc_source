# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fastpy/pretty_printer.py
# Compiled at: 2016-07-10 22:45:16
import pprint, ast

def ast2tree(node, include_attrs=True):

    def _transform(node):
        if isinstance(node, ast.AST):
            fields = ((a, _transform(b)) for a, b in ast.iter_fields(node))
            if include_attrs:
                attrs = ((a, _transform(getattr(node, a))) for a in node._attributes if hasattr(node, a))
                return (
                 node.__class__.__name__, dict(fields), dict(attrs))
            return (node.__class__.__name__, dict(fields))
        if isinstance(node, list):
            return [ _transform(x) for x in node ]
        if isinstance(node, str):
            return repr(node)
        return node

    if not isinstance(node, ast.AST):
        raise TypeError('expected AST, got %r' % node.__class__.__name__)
    return _transform(node)


def pformat_ast(node, include_attrs=False, **kws):
    return pprint.pformat(ast2tree(node, include_attrs), **kws)


def dump(node):
    return pformat_ast(node)