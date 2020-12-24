# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/auth/handlers/modwsgi.py
# Compiled at: 2018-07-11 18:15:30
from django.contrib import auth
from django import db
from django.utils.encoding import force_bytes

def check_password(environ, username, password):
    """
    Authenticates against Django's auth database

    mod_wsgi docs specify None, True, False as return value depending
    on whether the user exists and authenticates.
    """
    UserModel = auth.get_user_model()
    db.reset_queries()
    try:
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            return

        if not user.is_active:
            return
        return user.check_password(password)
    finally:
        db.close_connection()

    return


def groups_for_user(environ, username):
    """
    Authorizes a user based on groups
    """
    UserModel = auth.get_user_model()
    db.reset_queries()
    try:
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            return []

        if not user.is_active:
            return []
        return [ force_bytes(group.name) for group in user.groups.all() ]
    finally:
        db.close_connection()