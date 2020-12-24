# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/harambe/harambe/contrib/views/error_page.py
# Compiled at: 2017-02-26 06:59:25
"""
Error Page

This plugin to display customize error page

Can be called as standalone
"""
from __future__ import division
import logging
from harambe import Harambe, page_meta, register_package, abort
from harambe import exceptions
from sqlalchemy.exc import SQLAlchemyError
__version__ = '1.0.0'
__options__ = {}
renderer = None

class Main(Harambe):

    @classmethod
    def _register(cls, app, **kwargs):
        template_page = __options__.get('template', 'error_page/Main/index.jade')
        super(cls, cls)._register(app, **kwargs)

        @app.errorhandler(400)
        @app.errorhandler(401)
        @app.errorhandler(403)
        @app.errorhandler(404)
        @app.errorhandler(405)
        @app.errorhandler(406)
        @app.errorhandler(408)
        @app.errorhandler(409)
        @app.errorhandler(410)
        @app.errorhandler(413)
        @app.errorhandler(414)
        @app.errorhandler(429)
        @app.errorhandler(500)
        @app.errorhandler(501)
        @app.errorhandler(502)
        @app.errorhandler(503)
        @app.errorhandler(504)
        @app.errorhandler(505)
        def index(error):
            if int(error.code // 100) != 4:
                _error = str(error)
                _error += ' - HTTException Code: %s' % error.code
                _error += ' - HTTException Description: %s' % error.description
                logging.error(_error)
            if renderer:
                return renderer(error)
            else:
                return (
                 cls.render(error=error), error.code)