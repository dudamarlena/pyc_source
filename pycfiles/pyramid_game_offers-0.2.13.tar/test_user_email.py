# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/test_user_email.py
# Compiled at: 2017-02-24 16:57:38
__doc__ = 'Test email related User methods.'
from pyramid.compat import text_type
from pyramid_fullauth.models import User
NEW_EMAIL = text_type('new@example.com')

def test_set_new_email():
    """
    Test User.set_new_email method.

    setting new email should result in setting new_email field,
    and key used to activate the change.
    """
    user = User()
    assert user.email_change_key is None
    assert user.new_email is None
    user.set_new_email(NEW_EMAIL)
    assert user.new_email == NEW_EMAIL
    assert user.email_change_key
    return


def test_change_email():
    """
    Test User.change_email method.

    Calling it should copy new email set by set_new_email method
    into regular email field.
    """
    user = User()
    assert not user.email
    user.set_new_email(NEW_EMAIL)
    user.change_email()
    assert not user.email_change_key
    assert user.email == NEW_EMAIL