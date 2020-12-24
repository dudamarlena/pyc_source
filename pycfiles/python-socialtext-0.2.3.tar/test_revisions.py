# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/justin/Projects/python-socialtext/tests/test_pages/test_revisions.py
# Compiled at: 2011-12-23 09:02:47
from nose.tools import assert_equal, raises
from tests.fakeserver import FakeServer
from tests.utils import assert_isinstance
from socialtext.resources.pages import PageRevision, PageRevisionManager
st = FakeServer()
page = st.pages.list('marketing')[0]

@raises(NotImplementedError)
def test_create():
    page.revision_set.create()


@raises(NotImplementedError)
def test_delete():
    page.revision_set.delete(123)


def test_get():
    rev = page.revision_set.get(1234567890)
    st.assert_called('GET', '/data/workspaces/marketing/pages/test_1/revisions/1234567890')
    assert_isinstance(rev, PageRevision)
    rev.get()
    st.assert_called('GET', '/data/workspaces/marketing/pages/test_1/revisions/1234567890')
    assert_isinstance(rev, PageRevision)
    rev = page.revision_set.get(rev)
    st.assert_called('GET', '/data/workspaces/marketing/pages/test_1/revisions/1234567890')
    assert_isinstance(rev, PageRevision)


def test_get_wikitext():
    rev = page.revision_set.list()[0]
    wiki = rev.get_wikitext()
    assert '[Hello world]' in wiki
    st.assert_called('GET', '/data/workspaces/marketing/pages/test_1/revisions/1234567890')


def test_get_html():
    rev = page.revision_set.list()[0]
    html = rev.get_html()
    assert '</div>' in html
    st.assert_called('GET', '/data/workspaces/marketing/pages/test_1/revisions/1234567890')


def test_list():
    revs = page.revision_set.list()
    st.assert_called('GET', '/data/workspaces/marketing/pages/test_1/revisions')
    [ assert_isinstance(r, PageRevision) for r in revs ]