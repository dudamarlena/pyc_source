# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/views/conftest.py
# Compiled at: 2017-02-24 16:57:38
__doc__ = 'General view fixtures.'
import pytest, transaction
from pyramid_fullauth.models import AuthenticationProvider

def mock_translate(msg, *args, **kwargs):
    """Mock translate function (simply returns message)."""
    return msg


@pytest.fixture
def facebook_user(active_user, db_session):
    """Facebook user."""
    active_user = db_session.merge(active_user)
    active_user.providers.append(AuthenticationProvider(provider='facebook', provider_id='1234'))
    transaction.commit()
    return db_session.merge(active_user)