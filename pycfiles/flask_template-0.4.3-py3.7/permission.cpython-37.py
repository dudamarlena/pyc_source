# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flask_template/templates/mongo/proj/permission.py
# Compiled at: 2020-04-01 02:43:02
# Size of source mod 2**32: 1094 bytes
import functools
from flask import abort, request, redirect
from proj.proxy import current_user

def login_required_check_token(view_func):

    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user:
            abort(401)
        return view_func(*args, **kwargs)

    return wrapper


def login_required(view_func):

    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user:
            abort(401)
        return view_func(*args, **kwargs)

    return wrapper


def authorize(roles=[
 'admin']):

    def wrapper(view_func):

        @functools.wraps(view_func)
        def inner_func(*args, **kwargs):
            if not current_user:
                abort(401)
            role = current_user.role
            if role not in roles:
                abort(403)
            return view_func(*args, **kwargs)

        return inner_func

    return wrapper