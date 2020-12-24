# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/justin/Projects/python-socialtext/tests/test_workspaces/test_tags.py
# Compiled at: 2011-12-23 09:02:47
from nose.tools import assert_equal, raises
from tests.fakeserver import FakeServer
from tests.utils import assert_isinstance
from socialtext.resources.workspaces import WorkspaceTag, WorkspaceTagManager
st = FakeServer()
workspace = st.workspaces.get('marketing')

def test_create():
    t = workspace.tag_set.create('Test')
    st.assert_called('GET', '/data/workspaces/marketing/tags/Test')
    st.assert_called('PUT', '/data/workspaces/marketing/tags/Test')
    assert_isinstance(t, WorkspaceTag)


def test_delete():
    workspace.tag_set.delete('Test')
    st.assert_called('DELETE', '/data/workspaces/marketing/tags/Test')
    t = workspace.tag_set.list()[0]
    t.delete()
    st.assert_called('DELETE', '/data/workspaces/marketing/tags/Test')
    workspace.tag_set.delete(t)
    st.assert_called('DELETE', '/data/workspaces/marketing/tags/Test')


def test_get():
    t = workspace.tag_set.get('Test')
    st.assert_called('GET', '/data/workspaces/marketing/tags/Test')
    assert_isinstance(t, WorkspaceTag)
    t.get()
    st.assert_called('GET', '/data/workspaces/marketing/tags/Test')
    assert_isinstance(t, WorkspaceTag)
    t = workspace.tag_set.get(t)
    st.assert_called('GET', '/data/workspaces/marketing/tags/Test')
    assert_isinstance(t, WorkspaceTag)


def test_list():
    tags = workspace.tag_set.list()
    st.assert_called('GET', '/data/workspaces/marketing/tags')
    [ assert_isinstance(t, WorkspaceTag) for t in tags ]