# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twapi_authn.py
# Compiled at: 2016-09-01 06:24:38
# Size of source mod 2**32: 1590 bytes
from twapi_connection.exc import NotFoundError

class AccessTokenError(NotFoundError):
    pass


def claim_access_token(connection, access_token):
    """
    Claim the session identified by access_token and return the associated
    user’s Id (integer).

    """
    path_info = '/sessions/{}/'.format(access_token)
    try:
        response = connection.send_post_request(path_info)
    except NotFoundError:
        raise AccessTokenError()
    else:
        user_id = response.json()
    return user_id


def is_session_active(connection, access_token):
    """Check whether the session identified by access_token is still active."""
    path_info = '/sessions/{}/'.format(access_token)
    try:
        connection.send_head_request(path_info)
    except NotFoundError:
        is_active = False
    else:
        is_active = True
    return is_active