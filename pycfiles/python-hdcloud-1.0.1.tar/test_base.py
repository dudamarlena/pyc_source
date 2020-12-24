# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/python-hdcloud/tests/test_base.py
# Compiled at: 2010-04-14 14:12:59
from __future__ import absolute_import
import hdcloud.base
from .fakeserver import FakeHDCloud
from hdcloud import Store
from hdcloud.base import Resource
from nose.tools import assert_equal, assert_not_equal, assert_raises
hdcloud = FakeHDCloud()

def test_resource_repr():
    r = Resource(None, dict(foo='bar', baz='spam'))
    assert_equal(repr(r), '<Resource baz=spam, foo=bar>')
    return


def test_resource_lazy_getattr():
    s = Store(hdcloud.stores, {'id': 1})
    assert_equal(s.name, 'Example Store')
    hdcloud.assert_called('GET', '/stores/1.json')
    assert_raises(AttributeError, getattr, s, 'blahblah')
    hdcloud.assert_called('GET', '/stores/1.json')


def test_eq():
    r1 = Resource(None, {'id': 1, 'name': 'hi'})
    r2 = Resource(None, {'id': 1, 'name': 'hello'})
    assert_equal(r1, r2)
    r1 = Resource(None, {'id': 1})
    r2 = Store(None, {'id': 1})
    assert_not_equal(r1, r2)
    r1 = Resource(None, {'name': 'joe', 'age': 12})
    r2 = Resource(None, {'name': 'joe', 'age': 12})
    assert_equal(r1, r2)
    return