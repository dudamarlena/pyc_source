# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/justin/Projects/python-socialtext/tests/test_signals/test_likes.py
# Compiled at: 2011-12-29 14:42:22
from nose.tools import assert_equal, raises
from tests.fakeserver import FakeServer
from tests.utils import assert_isinstance
from socialtext.resources.signals import SignalLike, SignalLikeManager
st = FakeServer()
signal = st.signals.get(123)

def test_create():
    signal.like_set.create()
    st.assert_called('PUT', '/data/signals/123/likes/%s' % st.config.username)
    signal.like()
    st.assert_called('PUT', '/data/signals/123/likes/%s' % st.config.username)


def test_delete():
    signal.like_set.delete()
    st.assert_called('DELETE', '/data/signals/123/likes/%s' % st.config.username)
    signal.unlike()
    st.assert_called('DELETE', '/data/signals/123/likes/%s' % st.config.username)


def test_list():
    signal.like_set.list()
    st.assert_called('GET', '/data/signals/123/likes')