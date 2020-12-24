# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/justin/Projects/python-socialtext/tests/test_pages/test_backlinks.py
# Compiled at: 2011-12-23 09:02:47
from nose.tools import assert_equal, raises
from tests.fakeserver import FakeServer
from tests.utils import assert_isinstance
from socialtext.resources.pages import Page, PageBacklinkManager
st = FakeServer()
page = st.pages.list('marketing')[0]

@raises(NotImplementedError)
def test_create():
    page.backlink_set.create()


@raises(NotImplementedError)
def test_delete():
    page.backlink_set.delete()


@raises(NotImplementedError)
def test_get():
    page.backlink_set.get()


def test_list():
    bl = page.backlink_set.list()
    st.assert_called('GET', '/data/workspaces/marketing/pages/test_1/backlinks')
    [ assert_isinstance(b, Page) for b in bl ]