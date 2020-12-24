# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/test_user_admin.py
# Compiled at: 2017-02-24 16:57:38
__doc__ = 'Test admin related behaviour on user model.'
import pytest, transaction
from pyramid.compat import text_type
from pyramid_fullauth.models import User
from pyramid_fullauth.exceptions import DeleteException

def test_regular_user_not_admin(db_session, user):
    """Regular user is_admin flag test."""
    user = db_session.merge(user)
    assert not user.is_admin


def test_remove_last_admin(db_session, user):
    """
    Admin user is_admin flag test.

    At least one admin needed.
    """
    user = db_session.merge(user)
    user.is_admin = True
    transaction.commit()
    user = db_session.merge(user)
    with pytest.raises(AttributeError):
        user.is_admin = False


def test_delete_admin(db_session, user):
    """Admin user soft delete behaviour - more than one admins present."""
    user = db_session.merge(user)
    user2 = User(email=text_type('test2@example.com'), address_ip='127.0.0.1', password='pass', is_admin=True)
    db_session.add(user2)
    user.is_admin = True
    transaction.commit()
    user = db_session.merge(user)
    user.delete()
    assert user.deleted_at


def test_delete_last_admin(db_session, user):
    """Admin user soft delete - only one admin, no deleting possible."""
    user = db_session.merge(user)
    user.is_admin = True
    transaction.commit()
    user = db_session.merge(user)
    with pytest.raises(DeleteException):
        user.delete()