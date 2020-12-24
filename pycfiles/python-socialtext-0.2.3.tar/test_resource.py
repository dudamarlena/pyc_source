# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/justin/Projects/python-socialtext/tests/test_users/test_resource.py
# Compiled at: 2011-12-23 09:02:47
from nose.tools import assert_equal, raises
from tests.fakeserver import FakeServer
from tests.utils import assert_isinstance
from socialtext.resources.users import User
st = FakeServer()

def test_is_member_of_account():
    accounts = [{'account_id': '123'}, {'account_id': '987'}]
    user = st.users.load({'accounts': accounts})
    assert_equal(True, user.is_member_of_account('123'))
    assert_equal(True, user.is_member_of_account('987'))
    assert_equal(False, user.is_member_of_account('1000'))


def test_is_member_of_group():
    groups = [{'group_id': '123'}, {'group_id': '987'}]
    user = st.users.load({'groups': groups})
    assert_equal(True, user.is_member_of_group('123'))
    assert_equal(True, user.is_member_of_group('987'))
    assert_equal(False, user.is_member_of_group('1000'))