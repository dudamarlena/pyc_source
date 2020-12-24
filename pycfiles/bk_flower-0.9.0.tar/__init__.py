# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: tests/__init__.py
# Compiled at: 2016-01-12 02:26:02
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import tornado.testing, tornado.options, celery
from flower.app import Flower
from flower.urls import handlers
from flower.events import Events
from flower.urls import settings
from flower import command

class AsyncHTTPTestCase(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        capp = celery.Celery()
        events = Events(capp)
        app = Flower(capp=capp, events=events, options=tornado.options.options, handlers=handlers, **settings)
        app.delay = lambda method, *args, **kwargs: method(*args, **kwargs)
        return app

    def get(self, url, **kwargs):
        return self.fetch(url, **kwargs)

    def post(self, url, **kwargs):
        if 'body' in kwargs and isinstance(kwargs['body'], dict):
            kwargs['body'] = urlencode(kwargs['body'])
        return self.fetch(url, method='POST', **kwargs)