# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tornado_extensions/sessions/middlewares.py
# Compiled at: 2013-09-03 05:36:04
from tornado import gen
from importlib import import_module
from game_commons.patterns import Singleton

class SessionMiddleware(object):
    __metaclass__ = Singleton

    def __init__(self, settings):
        self.settings = settings
        self.session_cookie_name = settings['django_session']['cookie_name']
        self.session_engine = settings['django_session']['engine']
        self.engine = import_module(self.session_engine)
        self.cookie_secret = settings.get('cookie_secret', None)
        return

    @gen.engine
    def on_open_async(self, conn, request, callback=None):
        cookie = request.get_cookie(self.session_cookie_name)
        session_key = cookie and cookie.value or None
        session = self.engine.SessionStore(session_key, secret=self.cookie_secret)
        conn.session.django_session = session
        yield gen.Task(session.load)
        callback(session)
        return