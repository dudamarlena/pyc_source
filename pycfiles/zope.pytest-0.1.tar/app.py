# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/uli/WorkShop/devel/zope/zope.pytest/tags/0.1/src/zope/pytest/tests/sample_fixtures/zcml/mypkg2/app.py
# Compiled at: 2011-03-05 10:41:26
from zope.interface import implements
from mypkg2.interfaces import ISampleApp, IFoo

class SampleApp(object):
    implements(ISampleApp)


class FooUtility(object):
    implements(IFoo)

    def do_foo(self):
        return 'Foo!'