# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ducktype/tests/test_doc_examples.py
# Compiled at: 2013-12-03 19:39:03
from unittest import TestCase

class DocExamplesTest(TestCase):

    def test_example1_comparing_functions(self):
        from ducktype import isducktype
        func_a = lambda a1, a2, a3=None: None
        func_b = lambda *b1: None
        func_c = lambda **c2: None
        func_d = lambda d1, d2: None
        func_e = lambda e1: None
        func_f = lambda f1, f2, f3, f4: None
        assert isducktype(func_b, func_a)
        assert isducktype(func_c, func_a)
        assert isducktype(func_d, func_a)
        assert isducktype(func_a, func_e) is False
        assert isducktype(func_e, func_a) is False
        assert isducktype(func_f, func_a) is False
        assert isducktype(func_e, (func_a, func_b))
        assert isducktype(func_e, (func_a, func_d)) is False
        return

    def test_example2_comparing_objects(self):
        from ducktype import isducktype

        class A(object):
            _protected = 'hidden'
            __private = 'hidden'
            attr1 = None

            def method1(self, arg, kwargs=True):
                return kwargs

            def method2(self, arg):
                return arg

        class B(object):
            attr1 = None

            def method1(self, **kwargs):
                return kwargs

            def method2(self, arg1, arg2=None):
                return

        class C(object):
            attr1 = False

            def method1(self, arg, kwarg):
                return arg

        class D(object):
            attr1 = False
            method1 = None
            method2 = None

        class E(object):

            def method1(self, **kwargs):
                return kwargs

            def method2(self, arg1, arg2=None):
                return

        assert isducktype(A, B)
        assert isducktype(A(), B)
        assert isducktype(A, B())
        assert isducktype(A(), B())
        assert isducktype(A, C)
        assert isducktype(C, A) is False
        assert isducktype(A, D) is False
        assert isducktype(D, A) is False
        assert isducktype(A, E)
        assert isducktype(E, A) is False

    def test_example3_overriding_default(self):
        from ducktype import isducktype

        class A(object):
            attr1 = None

        class B(object):
            attr1 = None
            attr2 = None

        class C(B):

            @classmethod
            def __ducktypecheck__(cls, maybe_duck):
                return hasattr(maybe_duck, 'attr1')

        class D(B):

            def __ducktypecheck__(self, maybe_duck):
                return hasattr(maybe_duck, 'attr1')

        assert isducktype(A, B) is False
        assert isducktype(A, C)
        assert isducktype(A, D) is False
        assert isducktype(A, D())