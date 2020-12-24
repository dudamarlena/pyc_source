# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flask_template/templates/mongo/proj/proxy.py
# Compiled at: 2020-04-01 02:43:02
# Size of source mod 2**32: 1115 bytes
import time
from werkzeug.local import LocalProxy
from flask import g, current_app, abort
from proj.extensions import hamlet
from proj.models import HamletUser

def get_flask_app():
    """返回真实的 Flask 对象，在使用 signal 时作为 sender"""
    return current_app._get_current_object()


def set_current_user(remote_user):
    if remote_user:
        remote_user = HamletUser(remote_user)
    else:
        remote_user = None
    g.current_user = remote_user
    return g.current_user


def _find_current_user():
    if 'current_user' in g:
        return g.current_user
    time_begin = time.time()
    remote_user = hamlet.current_user()
    g._timeit_hamlet = (time.time() - time_begin) * 1000
    set_current_user(remote_user)
    return g.current_user


def find_current_user():
    """返回当前用户，g.current_user 在 login_required 装饰器中设置"""
    return _find_current_user()


current_user = LocalProxy(find_current_user)