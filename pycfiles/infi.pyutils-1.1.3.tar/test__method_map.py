# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Infinidat/infi.pyutils/tests/test__method_map.py
# Compiled at: 2016-09-14 06:55:36
import platform
from .test_utils import TestCase
from infi.pyutils.method_map import MethodMap

class MethodMapTest(TestCase):

    def test__method_map(self):

        class MyObj(object):
            METHODS = MethodMap()

            @METHODS.registering('a')
            def func_a(self):
                return 'a'

            @METHODS.registering('b')
            def func_b(self):
                return 'b'

            @METHODS.registering('c')
            @classmethod
            def func_c(cls):
                return 'c'

            @METHODS.registering('d')
            @staticmethod
            def func_d():
                return 'd'

        m = MyObj()
        self.assertEquals(m.METHODS.get('a')(), 'a')
        self.assertEquals(m.METHODS['a'](), 'a')
        self.assertEquals(m.METHODS.get('b')(), 'b')
        self.assertEquals(m.METHODS.get('bla', 2), 2)
        self.assertIsNone(m.METHODS.get('bfd', None))
        self.assertIsNone(m.METHODS.get('bfd'))
        self.assertEquals(m.METHODS['c'](), 'c')
        self.assertEquals(m.METHODS['d'](), 'd')
        with self.assertRaises(LookupError):
            m.METHODS['bbb']
        return

    def test__method_map_old_style_class(self):

        class MyObj:
            METHODS = MethodMap()

            @METHODS.registering('a')
            def func_a(self):
                return 'a'

        m = MyObj()
        if platform.python_version() < '3':
            self.assertNotEquals(type(m), MyObj)
        self.assertEquals(m.METHODS.get('a')(), 'a')
        self.assertEquals(m.METHODS['a'](), 'a')

    def test__method_map_with_decoration(self):

        class MyObj(object):
            METHODS = MethodMap(decorator=lambda func: lambda self: 666)

            @METHODS.registering('key')
            def func(self):
                raise Exception("Shouldn't  be called!!!")

        self.assertEquals(MyObj().METHODS.get('key')(), 666)