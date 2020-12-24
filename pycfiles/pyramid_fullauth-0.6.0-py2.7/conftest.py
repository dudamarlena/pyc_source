# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/views/conftest.py
# Compiled at: 2017-02-24 16:57:38
"""General view fixtures."""
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