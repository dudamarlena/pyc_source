# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bilbo/Projects/playground/redis_cache/tests/test_keygen.py
# Compiled at: 2012-12-22 13:12:45
from unittest import TestCase
from redcache.cache_manager import CacheManager

class KeygenTestCase(TestCase):

    def test_no_args(self):
        cache_manager = CacheManager()

        def testfunc():
            pass

        assert cache_manager.key(testfunc, None) == 'cache:testfunc'
        return

    def test_functions(self):
        cache_manager = CacheManager()

        def testfunc(a, b, c=None):
            pass

        args = [
         1, 2]
        assert cache_manager.key(testfunc, args) == 'cache:testfunc:1:2'
        args = [
         'a', 'b']
        assert cache_manager.key(testfunc, args) == 'cache:testfunc:a:b'

        def testfunc2(self, a, b, c=None):
            pass

        args = [
         None, 1, 2]
        assert cache_manager.key(testfunc2, args) == 'cache:testfunc2:1:2'

        def testfunc3(cls, a, b, c=None):
            pass

        args = [
         None, 1, 2]
        assert cache_manager.key(testfunc3, args) == 'cache:testfunc3:1:2'
        return

    def test_methods(self):
        cache_manager = CacheManager()

        class MyClass(object):

            def my_imethod(self):
                return "I'm an instance method!"

            @classmethod
            def my_cmethod(cls):
                return "I'm a class method!"

            @staticmethod
            def my_smethod():
                return "I'm a static method!"

        my_obj = MyClass()
        assert cache_manager.key(my_obj.my_imethod, None) == 'cache:MyClass.my_imethod'
        assert cache_manager.key(MyClass.my_cmethod, None) == 'cache:MyClass.my_cmethod'
        assert cache_manager.key(MyClass.my_smethod, None) == 'cache:my_smethod'
        return