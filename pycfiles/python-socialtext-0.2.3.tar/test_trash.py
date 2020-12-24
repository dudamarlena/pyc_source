# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/justin/Projects/python-socialtext/tests/test_groups/test_trash.py
# Compiled at: 2011-12-29 15:54:18
from nose.tools import assert_equal, raises
from tests.fakeserver import FakeServer
from tests.utils import assert_isinstance
from socialtext.resources.groups import Group, GroupManager, GroupTrashManager
st = FakeServer()

def test_delete():
    group = st.groups.get(21)
    workspace = st.workspaces.get('marketing')
    user = st.users.get(123)
    expected = [{'user_id': 123}, {'workspace_id': '123'}]
    group.trash([user, workspace])
    st.assert_called('POST', '/data/groups/21/trash', data=expected)