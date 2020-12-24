# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/cloudservers/tests/test_base.py
# Compiled at: 2010-08-16 13:11:53
import mock, cloudservers.base
from cloudservers import Flavor
from cloudservers.exceptions import NotFound
from cloudservers.base import Resource
from nose.tools import assert_equal, assert_not_equal, assert_raises
from fakeserver import FakeServer
cs = FakeServer()

def test_resource_repr():
    r = Resource(None, dict(foo='bar', baz='spam'))
    assert_equal(repr(r), '<Resource baz=spam, foo=bar>')
    return


def test_getid():
    assert_equal(cloudservers.base.getid(4), 4)

    class O(object):
        id = 4

    assert_equal(cloudservers.base.getid(O), 4)


def test_resource_lazy_getattr():
    f = Flavor(cs.flavors, {'id': 1})
    assert_equal(f.name, '256 MB Server')
    cs.assert_called('GET', '/flavors/1')
    assert_raises(AttributeError, getattr, f, 'blahblah')
    cs.assert_called('GET', '/flavors/1')


def test_eq():
    r1 = Resource(None, {'id': 1, 'name': 'hi'})
    r2 = Resource(None, {'id': 1, 'name': 'hello'})
    assert_equal(r1, r2)
    r1 = Resource(None, {'id': 1})
    r2 = Flavor(None, {'id': 1})
    assert_not_equal(r1, r2)
    r1 = Resource(None, {'name': 'joe', 'age': 12})
    r2 = Resource(None, {'name': 'joe', 'age': 12})
    assert_equal(r1, r2)
    return


def test_findall_invalid_attribute():
    cs.flavors.findall(vegetable='carrot')
    assert_raises(NotFound, cs.flavors.find, vegetable='carrot')