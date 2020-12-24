# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/lib/authentication.py
# Compiled at: 2011-02-18 19:15:09
"""
Nicked from http://sarafsaurabh.wordpress.com/2010/08/10/pylons-authentication-and-authorization-using-repoze-what/
"""
from pylons import request
from repoze.what.plugins.quickstart import setup_sql_auth
from repoze.what.predicates import not_anonymous, has_permission
from argonaut.model.meta import Session
from argonaut.model.auth import User, Group, Permission

def add_auth(app, config):
    """
    Add authentication and authorization middleware to the ``app``.

    We're going to define post-login and post-logout pages
    to do some cool things.

    """
    return setup_sql_auth(app, User, Group, Permission, Session, login_url='/account/login', post_logout_url='/', login_handler='/account/login_handler', logout_handler='/account/logout', cookie_secret=config.get('cookie_secret'), translations={'user_name': 'username', 
       'group_name': 'name', 
       'permission_name': 'name'})


def get_logged_user():
    identity = request.environ.get('repoze.who.identity')
    if identity is None:
        return
    else:
        return identity['repoze.who.userid']
        return


def get_logged_identity():
    return request.environ.get('repoze.who.identity')