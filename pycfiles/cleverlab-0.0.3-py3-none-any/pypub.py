# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/tests/files_five/pypub.py
# Compiled at: 2006-08-02 05:57:50
__doc__ = '\n\na - no args - def X()\nb - kwd args - def X(x=1) \nc - extra args - def X(*v)\nd - extra args kwd args - def X(x=1, *v)\ne - pos args - def X(x)\nf - pos args kwd args - def X(x, y=2)\ng - pos args extra args - def X(x, *v)\nh - pos args extra args kwd args - def X(x, *v, y=2)\n\n'

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
        return (
         x, v)


class a_e(a_base):
    __module__ = __name__

    def meth(self, x, y):
        return (
         x, y)


class a_f(a_base):
    __module__ = __name__

    def meth(self, x, y=0):
        return (
         x, y)


class a_g(a_base):
    __module__ = __name__

    def meth(self, x, *v):
        return (
         x, v)


class a_h(a_base):
    __module__ = __name__

    def meth(self, x, y=0, *v):
        return (
         x, y, v)


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
        return (
         self.p, x)


class b_c(b_base):
    __module__ = __name__

    def meth(self, *v):
        return (
         self.p, v)


class b_d(b_base):
    __module__ = __name__

    def meth(self, x=1, *v):
        return (
         x, v)


class b_e(b_base):
    __module__ = __name__

    def meth(self, x, y):
        return (
         x, y)


class b_f(b_base):
    __module__ = __name__

    def meth(self, x, y=0):
        return (
         x, y)


class b_g(b_base):
    __module__ = __name__

    def meth(self, x, *v):
        return (
         x, v)


class b_h(b_base):
    __module__ = __name__

    def meth(self, x, y=0, *v):
        return (
         x, y, v)