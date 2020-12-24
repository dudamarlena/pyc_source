# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/python-storymarket/tests/test_base.py
# Compiled at: 2010-07-12 11:34:05
from __future__ import absolute_import
from storymarket import Text
from storymarket.base import Resource
from .fakeserver import FakeStorymarket
from nose.tools import assert_equal, assert_not_equal, assert_raises
sm = FakeStorymarket()

def test_resource_repr():
    r = Resource(None, dict(foo='bar', baz='spam'))
    assert_equal(repr(r), '<Resource baz=spam, foo=bar>')
    return


def test_resource_lazy_getattr():
    t = Text(sm.text, {'id': 1})
    assert_equal(t.title, 'Text')
    sm.assert_called('GET', 'content/text/1/')
    assert_raises(AttributeError, getattr, t, 'blahblah')
    sm.assert_called('GET', 'content/text/1/')


def test_eq():
    r1 = Resource(None, {'id': 1, 'name': 'hi'})
    r2 = Resource(None, {'id': 1, 'name': 'hello'})
    assert_equal(r1, r2)
    r1 = Resource(None, {'id': 1})
    r2 = Text(None, {'id': 1})
    assert_not_equal(r1, r2)
    r1 = Resource(None, {'name': 'joe', 'age': 12})
    r2 = Resource(None, {'name': 'joe', 'age': 12})
    assert_equal(r1, r2)
    return