# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tests/output/AuthXpProjectName/authxpprojectname/lib/auth.py
# Compiled at: 2007-09-06 07:54:22
from pylons import request, session
from pylons.helpers import redirect_to
from authxpprojectname import model
_login_url = '/login'
_auth_user_environ_key = 'AUTH_USER'
_auth_user_session_key = 'AUTH_USER_ID'

def get_user():
    if _auth_user_environ_key not in request.environ:
        user_id = session.get(_auth_user_session_key)
        if user_id:
            user = model.User.get_by(id=user_id, active=True)
            request.environ[_auth_user_environ_key] = user
        else:
            request.environ[_auth_user_environ_key] = None
    return request.environ[_auth_user_environ_key]


def login(user):
    session[_auth_user_session_key] = str(user.id)
    session.save()


def logout():
    session.pop(_auth_user_session_key, None)
    session.save()
    return


def redirect_to_login():
    redirect_to(controller=_login_url)