# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/samba/Projects/Personal/briesemeister.me/virtenv/lib/python2.7/site-packages/tackle/__init__.py
# Compiled at: 2016-02-11 18:13:10
from util import cached_property
from wsgi import WSGIService, WSGIApplication, WSGIRequestHandler as RequestHandler, sendfile
from middleware import Middleware, RedirectionMiddleware, StaticFileMiddleware, Shortener
__version__ = '0.0.1'
__author__ = [
 'Sam Briesemeister <sam.briesemeister@gmail.com>']
__license__ = 'Copyright Sam Briesemeister, 2015'