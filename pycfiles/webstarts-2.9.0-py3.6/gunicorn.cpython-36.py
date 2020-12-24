# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/webstarts/gunicorn.py
# Compiled at: 2017-09-29 15:01:16
# Size of source mod 2**32: 1204 bytes
"""Applicable to webstarts"""
import logging
from gunicorn.app.wsgiapp import WSGIApplication
from gunicorn.glogging import Logger
__author__ = 'john'
from . import types

class WebstartsApp(WSGIApplication):
    __doc__ = 'Gunicorn wrapper'

    def __init__(self, program, is_dev=False):
        self.is_dev = is_dev
        super().__init__(program)

    def load_wsgiapp(self):
        app = super().load_wsgiapp()
        from . import log_id, wflask
        app = log_id.wrap_logid(app)
        app = wflask.wrap_sentry(app)
        return app

    def init(self, parser, opts, args):
        cfg = super().init(parser, opts, args) or {}
        cfg['logger_class'] = GunicornLogger
        if self.is_dev:
            cfg.update(reload=True, timeout=99999, accesslog='-')
        return cfg


class GunicornLogger(Logger):

    def setup(self, cfg):
        super().setup(cfg)
        self.error_log.propagate = True
        self._set_handler(self.error_log, None, None)
        self.access_log.propagate = True
        self._set_handler(self.access_log, None, None)

    @classmethod
    def install(cls):
        logging.setLoggerClass(types.WebstartsLogger)