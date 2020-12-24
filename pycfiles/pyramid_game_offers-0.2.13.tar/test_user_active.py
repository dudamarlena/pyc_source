# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/test_user_active.py
# Compiled at: 2017-02-24 16:57:38
__doc__ = 'User active method tests.'
import pytest
from pyramid_fullauth.models import User

def test_is_active_error():
    """is_active can only be modified on object in session."""
    with pytest.raises(AttributeError):
        user = User()
        user.is_active = True


def test_is_active(db_session, user):
    """
    Test is_active attribute.

    Setting is_active to True, should result in change of activated_at date being set
    Setting to false, should set deactivated_at.
    """
    user = db_session.merge(user)
    assert not user.is_active
    assert not user.activated_at
    user.is_active = True
    assert user.is_active
    assert user.activated_at
    assert not user.deactivated_at
    user.is_active = False
    assert not user.is_active
    assert user.deactivated_at