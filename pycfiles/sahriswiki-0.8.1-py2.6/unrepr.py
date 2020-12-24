# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sahriswiki/unrepr.py
# Compiled at: 2010-07-19 18:24:16
"""unrepr

unrepr(...) function and support borrowed from the CherryPy3 library
with fixes and improvements.
"""
import sys, operator as _operator

class _Builder:

    def build(self, o):
        m = getattr(self, 'build_' + o.__class__.__name__, None)
        if m is None:
            raise TypeError('unrepr does not recognize %s' % repr(o.__class__.__name__))
        return m(o)

    def build_Subscript(self, o):
        return self.build(o.value)[self.build(o.slice)]

    def build_Index(self, o):
        return self.build(o.value)

    def build_Call(self, o):
        callee = self.build(o.func)
        if o.args is None:
            args = ()
        else:
            args = tuple([ self.build(a) for a in o.args ])
        if o.starargs is None:
            starargs = ()
        else:
            starargs = self.build(o.starargs)
        if o.kwargs is None:
            kwargs = {}
        else:
            kwargs = self.build(o.kwargs)
        return callee(*(args + starargs), **kwargs)

    def build_List(self, o):
        return list(map(self.build, o.elts))

    def build_Str(self, o):
        return o.s

    def build_Num(self, o):
        return o.n

    def build_Dict(self, o):
        return dict([ (self.build(k), self.build(v)) for (k, v) in zip(o.keys, o.values)
                    ])

    def build_Tuple(self, o):
        return tuple(self.build_List(o))

    def build_Name(self, o):
        name = o.id
        if name == 'None':
            return
        else:
            if name == 'True':
                return True
            if name == 'False':
                return False
            try:
                return modules(name)
            except ImportError:
                pass

            try:
                return getattr(__builtins__, name)
            except AttributeError:
                pass

            raise TypeError('unrepr could not resolve the name %s' % repr(name))
            return

    def build_BinOp(self, o):
        (left, op, right) = map(self.build, [o.left, o.op, o.right])
        return op(left, right)

    def build_Add(self, o):
        return _operator.add

    def build_Attribute(self, o):
        parent = self.build(o.value)
        return getattr(parent, o.attr)

    def build_NoneType(self, o):
        return


def _astnode(s):
    """Return a Python ast Node compiled from a string."""
    try:
        import ast
    except ImportError:
        return eval(s)

    p = ast.parse('__tempvalue__ = ' + s)
    return p.body[0].value


def unrepr(s):
    """Return a Python object compiled from a string."""
    if not s:
        return s
    obj = _astnode(s)
    return _Builder().build(obj)


def modules(modulePath):
    """Load a module and retrieve a reference to that module."""
    try:
        mod = sys.modules[modulePath]
        if mod is None:
            raise KeyError()
    except KeyError:
        mod = __import__(modulePath, globals(), locals(), [''])

    return mod