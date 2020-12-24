# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/uli/WorkShop/devel/zope/zope.pytest/tags/0.1/src/zope/pytest/tests/sample_fixtures/zcml/mypkg2/tests/test_foo.py
# Compiled at: 2011-03-05 10:41:26
import mypkg2
from zope.component import queryUtility
from mypkg2.interfaces import IFoo
from zope.pytest import configure

def pytest_funcarg__config_mypkg2(request):
    return configure(request, mypkg2, 'ftesting.zcml')


def test_get_utility(config_mypkg2):
    util = queryUtility(IFoo, name='foo utility', default=None)
    assert util is not None
    return


def test_dofoo_utility(config_mypkg2):
    util = queryUtility(IFoo, name='foo utility', default=None)
    assert util().do_foo() == 'Foo!'
    return