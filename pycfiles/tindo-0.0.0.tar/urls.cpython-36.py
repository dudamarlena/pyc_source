# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gaufung/WorkSpace/SimpleWebFramework/example/urls.py
# Compiled at: 2017-09-14 21:49:37
# Size of source mod 2**32: 692 bytes
import sys
sys.path.insert(0, '../')
import importlib
importlib.reload(sys)
from tindo import get, view, post, ctx

@view('index.html')
@get('/')
def index():
    return dict()


@view('register.html')
@get('/register')
def register():
    return dict()


@view('registered.html')
@post('/registered')
def registered():
    i = ctx.request.input(firstname='', lastname='')
    return dict(firstname=(i.get('firstname', '')), lastname=(i.get('lastname', '')))


@view('name.html')
@get('/user/<username>')
def user(name):
    return dict(name=name)


@view('comment.html')
@get('/user/<name>/<group>')
def comment(name, group):
    return dict(name=name, group=group)