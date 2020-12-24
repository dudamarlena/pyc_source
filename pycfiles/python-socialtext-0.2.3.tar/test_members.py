# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/justin/Projects/python-socialtext/tests/test_accounts/test_members.py
# Compiled at: 2011-12-23 09:02:47
from nose.tools import assert_equal, raises
from tests.fakeserver import FakeServer
from tests.utils import assert_isinstance
from socialtext.resources.accounts import AccountMember, AccountMemberManager
st = FakeServer()
account = st.accounts.get(2)

def test_create():
    data = {'username': 'abc123'}
    member = account.member_set.create(data['username'])
    st.assert_called('POST', '/data/accounts/2/users', data=data)