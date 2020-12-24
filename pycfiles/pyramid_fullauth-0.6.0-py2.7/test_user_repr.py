# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/test_user_repr.py
# Compiled at: 2017-02-24 16:57:38
"""Test user representation."""
from pyramid.compat import text_type
from pyramid_fullauth.models import User

def test_introduce_email():
    """User gets introduced by e-mail only."""
    user = User()
    user.email = text_type('test@test.pl')
    assert str(user) == 'test@...'


def test_introduce_username():
    """User gets introduced by username."""
    user = User()
    assert str(user) == 'None'
    user.id = 1
    assert str(user) == '1'
    user.email = text_type('test@test.pl')
    user.username = text_type('testowy')
    assert str(user) == 'testowy'
    assert user.__repr__() == "<User ('1')>"