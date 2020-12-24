# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/harold/tests/files_five/pypub.py
# Compiled at: 2006-08-02 05:57:50
"""

a - no args - def X()
b - kwd args - def X(x=1) 
c - extra args - def X(*v)
d - extra args kwd args - def X(x=1, *v)
e - pos args - def X(x)
f - pos args kwd args - def X(x, y=2)
g - pos args extra args - def X(x, *v)
h - pos args extra args kwd args - def X(x, *v, y=2)

"""

class a_base:
    __module__ = __name__
    expose = ['meth']

    def __init__(self):
        pass


class a_a(a_base):
    __module__ = __name__

    def meth(self):
        pass


class a_b(a_base):
    __module__ = __name__

    def meth(self, x=1):
        return x


class a_c(a_base):
    __module__ = __name__

    def meth(self, *v):
        return v


class a_d(a_base):
    __module__ = __name__

    def meth(self, x=1, *v):
        return (x, v)


class a_e(a_base):
    __module__ = __name__

    def meth(self, x, y):
        return (x, y)


class a_f(a_base):
    __module__ = __name__

    def meth(self, x, y=0):
        return (x, y)


class a_g(a_base):
    __module__ = __name__

    def meth(self, x, *v):
        return (x, v)


class a_h(a_base):
    __module__ = __name__

    def meth(self, x, y=0, *v):
        return (x, y, v)


class b_base:
    __module__ = __name__
    expose = ['meth']

    def __init__(self, p):
        self.p = p


class b_a(b_base):
    __module__ = __name__

    def meth(self):
        return self.p


class b_b(b_base):
    __module__ = __name__

    def meth(self, x=0):
        return (self.p, x)


class b_c(b_base):
    __module__ = __name__

    def meth(self, *v):
        return (self.p, v)


class b_d(b_base):
    __module__ = __name__

    def meth(self, x=1, *v):
        return (x, v)


class b_e(b_base):
    __module__ = __name__

    def meth(self, x, y):
        return (x, y)


class b_f(b_base):
    __module__ = __name__

    def meth(self, x, y=0):
        return (x, y)


class b_g(b_base):
    __module__ = __name__

    def meth(self, x, *v):
        return (x, v)


class b_h(b_base):
    __module__ = __name__

    def meth(self, x, y=0, *v):
        return (x, y, v)