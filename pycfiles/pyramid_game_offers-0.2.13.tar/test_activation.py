# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/views/test_activation.py
# Compiled at: 2017-02-24 16:57:38
__doc__ = 'Account activation related tests.'
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

import transaction
from pyramid_fullauth.models import User
from tests.tools import authenticate, is_user_logged

def test_account_activation(user, db_session, default_app):
    """Activate user."""
    user = db_session.merge(user)
    default_app.get('/register/activate/' + user.activate_key)
    transaction.commit()
    user = db_session.query(User).filter(User.email == user.email).one()
    assert not user.activate_key
    assert user.is_active
    assert user.activated_at
    authenticate(default_app)
    assert is_user_logged(default_app) is True


def test_account_activation_wrong_key(user, db_session, default_app):
    """Activate user with wrong key."""
    user = db_session.merge(user)
    activate_key = user.activate_key
    res = default_app.get('/register/activate/' + activate_key[:-5], status=200)
    transaction.commit()
    assert 'Invalid activation code' in res.body.decode('unicode_escape')
    user = db_session.query(User).filter(User.email == user.email).one()
    assert user.activate_key == activate_key
    assert user.activate_key is not None
    assert not user.activated_at
    assert not user.is_active
    return


def test_account_activation_key_with_trash_chars(user, db_session, default_app):
    """Strange characters in activation key."""
    user = db_session.merge(user)
    activate_key = user.activate_key
    res = default_app.get('/register/activate/' + quote('ąśðłĸęł¶→łęóħó³→←śðđ[]}³½ĸżćŋðń→↓ŧ¶ħ→ĸł¼²³↓←ħ@ĸđśðĸ@ł¼ęłśħđó[³²½łðśđħ'), status=200)
    transaction.commit()
    assert 'Invalid activation code' in res.body.decode('unicode_escape')
    user = db_session.query(User).filter(User.email == user.email).one()
    assert user.activate_key == activate_key
    assert user.activate_key is not None
    assert not user.activated_at
    assert not user.is_active
    return


def test_account_activation_twice(user, db_session, default_app):
    """Click activation link twice."""
    user = db_session.merge(user)
    activate_key = user.activate_key
    res = default_app.get('/register/activate/' + activate_key)
    transaction.commit()
    user = db_session.query(User).filter(User.email == user.email).one()
    assert not user.activate_key
    assert user.is_active
    assert user.activated_at
    res = default_app.get('/register/activate/' + activate_key, status=200)
    assert 'Invalid activation code' in res.body.decode('unicode_escape')