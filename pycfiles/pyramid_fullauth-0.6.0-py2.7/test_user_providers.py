# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/test_user_providers.py
# Compiled at: 2017-02-24 16:57:38
"""Test provider related user methods."""
from pyramid.compat import text_type
import transaction
from pyramid_fullauth.models import User
from pyramid_fullauth.models import AuthenticationProvider

def test_user_provider_id(db_session, user):
    """User provider_id returns proper provider identification."""
    user = db_session.merge(user)
    email = user.email
    assert not user.provider_id('email')
    provider = AuthenticationProvider()
    provider.provider = text_type('email')
    provider.provider_id = email
    user.providers.append(provider)
    transaction.commit()
    user = db_session.query(User).filter(User.email == email).one()
    assert user.provider_id('email') == email