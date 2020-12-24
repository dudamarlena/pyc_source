# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/test/examples/decorators.py
# Compiled at: 2009-05-07 08:05:55


def foo(arg):
    return foo


def bar(*args):
    return bar


class C(object):
    __module__ = __name__

    def meth(self, arg):
        return arg


class FooBar(object):
    __module__ = __name__

    @foo
    def foo(self):
        return 'foo'


c = C()

@c.meth
@foo
@bar(1, 2)
def foobar(arg):
    return 'bar'