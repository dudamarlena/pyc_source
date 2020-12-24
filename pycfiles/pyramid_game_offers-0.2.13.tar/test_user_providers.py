# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/test_user_providers.py
# Compiled at: 2017-02-24 16:57:38
__doc__ = 'Test provider related user methods.'
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