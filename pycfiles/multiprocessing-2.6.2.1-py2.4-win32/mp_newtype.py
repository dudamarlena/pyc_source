# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\multiprocessing\examples\mp_newtype.py
# Compiled at: 2009-07-30 09:32:52
from multiprocessing import freeze_support
from multiprocessing.managers import BaseManager, BaseProxy
import operator

class Foo(object):
    __module__ = __name__

    def f(self):
        print 'you called Foo.f()'

    def g(self):
        print 'you called Foo.g()'

    def _h(self):
        print 'you called Foo._h()'


def baz():
    for i in xrange(10):
        yield i * i


class GeneratorProxy(BaseProxy):
    __module__ = __name__
    _exposed_ = ('next', '__next__')

    def __iter__(self):
        return self

    def next(self):
        return self._callmethod('next')

    def __next__(self):
        return self._callmethod('__next__')


def get_operator_module():
    return operator


class MyManager(BaseManager):
    __module__ = __name__


MyManager.register('Foo1', Foo)
MyManager.register('Foo2', Foo, exposed=('g', '_h'))
MyManager.register('baz', baz, proxytype=GeneratorProxy)
MyManager.register('operator', get_operator_module)

def test():
    manager = MyManager()
    manager.start()
    print '-' * 20
    f1 = manager.Foo1()
    f1.f()
    f1.g()
    assert not hasattr(f1, '_h')
    assert sorted(f1._exposed_) == sorted(['f', 'g'])
    print '-' * 20
    f2 = manager.Foo2()
    f2.g()
    f2._h()
    assert not hasattr(f2, 'f')
    assert sorted(f2._exposed_) == sorted(['g', '_h'])
    print '-' * 20
    it = manager.baz()
    for i in it:
        print '<%d>' % i,

    print
    print '-' * 20
    op = manager.operator()
    print 'op.add(23, 45) =', op.add(23, 45)
    print 'op.pow(2, 94) =', op.pow(2, 94)
    print 'op.getslice(range(10), 2, 6) =', op.getslice(range(10), 2, 6)
    print 'op.repeat(range(5), 3) =', op.repeat(range(5), 3)
    print 'op._exposed_ =', op._exposed_


if __name__ == '__main__':
    freeze_support()
    test()