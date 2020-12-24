# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/justin/Projects/python-socialtext/tests/test_pages/test_comments.py
# Compiled at: 2011-12-23 09:02:47
from nose.tools import assert_equal, raises
from tests.fakeserver import FakeServer
from socialtext.resources.pages import PageCommentManager
st = FakeServer()
page = st.pages.list('marketing')[0]

def test_create():
    comment = 'This is a *comment* using _wikitext_!'
    page.comment_set.create(comment)
    st.assert_called('POST', '/data/workspaces/marketing/pages/test_1/comments')


@raises(NotImplementedError)
def test_delete():
    page.comment_set.delete()


@raises(NotImplementedError)
def test_get():
    page.comment_set.get()


@raises(NotImplementedError)
def test_list():
    page.comment_set.list()