# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Infinidat/infi.pyutils/tests/test__mixin.py
# Compiled at: 2016-09-14 06:55:36
from infi.pyutils.mixin import *

def test_install_mixin__simple():

    class A(object):
        pass

    class B(object):

        def foo(self):
            self.a = 1

    a = A()
    install_mixin(a, B)
    a.foo()
    assert a.a == 1


def test_install_mixin__multiple_inheritence1():

    class A(object):
        pass

    class B(object):
        pass

    class C(object):
        pass

    class D(A, B, C):
        pass

    class E(object):

        def foo(self):
            self.a = 1

    d = D()
    install_mixin(d, E)
    d.foo()
    assert d.a == 1


def test_install_mixin__multiple_inheritence2():

    class A(object):
        pass

    class B(object):
        pass

    class C(object):
        pass

    class D(A, B, C):
        pass

    class E(object):

        def foo(self):
            self.a = 1

    d = D()
    install_mixin(d, E)
    assert issubclass(d.__class__, E)
    d.foo()
    assert d.a == 1


def test_install_mixin__multiple_inheritence3():

    class A(object):
        pass

    class B(object):
        pass

    class C(object):
        pass

    class E(object):

        def foo(self):
            self.a = 2

    class D(A, B, C):

        class D_E(E):

            def foo(self):
                self.a = 1

    d = D()
    install_mixin(d, E)
    assert issubclass(d.__class__, E)
    assert isinstance(d, E)
    assert isinstance(d, D)
    install_mixin(d, D.D_E)
    assert issubclass(d.__class__, D.D_E)
    assert isinstance(d, E)
    assert isinstance(d, D)
    assert isinstance(d, D.D_E)
    d.foo()
    assert d.a == 1