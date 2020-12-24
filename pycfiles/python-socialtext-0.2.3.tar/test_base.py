# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/justin/Projects/python-socialtext/tests/test_base.py
# Compiled at: 2011-12-29 14:42:22
import mock
from nose.tools import assert_equal, assert_not_equal, assert_raises
from fakeserver import FakeServer
from socialtext.resources.base import BasicObject, Resource, get_id
from socialtext.resources.signals import Signal
cs = FakeServer()

def test_resource_repr():
    r = Resource(None, dict(foo='bar', baz='spam'))
    assert_equal(repr(r), '<Resource baz=spam, foo=bar>')
    return


def test_get_id():
    assert_equal(get_id(4), '4')

    class O(object):
        id = 4

        def get_id(self):
            return self.id

    o = O()
    assert_equal(get_id(o), 4)


def test_eq():
    r1 = Resource(None, {'id': 1})
    r2 = Signal(cs.signals, {'signal_id': 1})
    assert_not_equal(r1, r2)
    r1 = Resource(None, {'name': 'joe', 'age': 12})
    r2 = Resource(None, {'name': 'joe', 'age': 12})
    assert_equal(r1, r2)
    return