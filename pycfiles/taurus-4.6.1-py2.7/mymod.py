# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/evaluation/test/res/mymod.py
# Compiled at: 2019-08-19 15:09:29
"""
This module is used for the tests of custom evaluation devices.
"""
from __future__ import print_function
from builtins import object
import os
from taurus.core.units import Quantity
modattr = 'hello world'

def myfunction():
    return 987


class MyClass(object):
    class_member = 1234

    def __init__(self, foomag=123):
        self._foo = Quantity(foomag, 'm')

    def get_foo(self):
        return self._foo

    def set_foo(self, value):
        self._foo = value

    def bar(self):
        return str(os.environ.get('__MYMOD_TEST_BAR', 'hi there'))

    def set_bar(self, value):
        os.environ['__MYMOD_TEST_BAR'] = str(value)

    foo = property(get_foo, set_foo)
    bar = property(bar, set_bar)
    baz = 'hello'

    @property
    def float_ro(self):
        return 1.234

    @classmethod
    def classmeth(cls):
        return cls.class_member

    @staticmethod
    def staticmeth():
        return 4321


if __name__ == '__main__':
    import taurus

    def test1():
        n = 'eval:@c=taurus.core.evaluation.test.res.mymod.MyClass(987)/c.foo'
        a = taurus.Attribute(n)
        print('READ 1:   ', a.read())
        print('WRITE+READ', a.write(Quantity(999, 'm')))
        print('READ 2:   ', a.read(cache=False))


    def test2(models):
        for m in models:
            print(m)
            a = taurus.Attribute(m)
            print('   -->', a.writable, a.read().rvalue)


    models = [
     'eval:@taurus.core.evaluation.test.res.mymod.MyClass()/self.foo',
     'eval:@taurus.core.evaluation.test.res.mymod.MyClass()/self.bar',
     'eval:@taurus.core.evaluation.test.res.mymod.MyClass()/self.baz',
     'eval:@taurus.core.evaluation.test.res.mymod.MyClass()/self.float_ro',
     'eval:@taurus.core.evaluation.test.res.mymod.MyClass()/self.class_member',
     'eval:@taurus.core.evaluation.test.res.mymod.MyClass()/self.classmeth()',
     'eval:@taurus.core.evaluation.test.res.mymod.MyClass()/self.staticmeth()',
     'eval:@taurus.core.evaluation.test.res.mymod.MyClass()/self.__class__.__name__',
     'eval:@c=taurus.core.evaluation.test.res.mymod.MyClass()/c.foo',
     'eval:@c=taurus.core.evaluation.test.res.mymod.MyClass(1)/c.foo',
     'eval:@c=taurus.core.evaluation.test.res.mymod.MyClass(2)/c.get_foo()',
     'eval:@c=taurus.core.evaluation.test.res.mymod.MyClass(foomag=2)/c.foo',
     'eval:@taurus.core.evaluation.test.res.mymod.*/modattr',
     'eval:@taurus.core.evaluation.test.res.mymod.*/myfunction()',
     'eval:@taurus.core.evaluation.test.res.mymod.*/MyClass().foo']
    test1()
    test2(models)