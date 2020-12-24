# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/webstarts/log_id.py
# Compiled at: 2017-09-29 15:01:16
# Size of source mod 2**32: 979 bytes
"""Applicable to webstarts"""
import uuid
from structlog import get_logger
from . import defaults
__author__ = 'john'
logger = get_logger(__name__)

def err(v):
    ass = 1 + v
    return ass


def make():
    return str(uuid.uuid4())[:12].replace('-', '')


def ctx():
    return dict(logger._context._dict)


def find():
    return ctx().get(defaults.LOG_KEY) or ''


def wrap_logid(app):

    def wrap_logid_(environ, start_response):
        logid = environ.get(defaults.LOG_KEY)
        if not logid:
            from webstarts.util import clear_cache
            clear_cache()
            logid = make()
        environ[defaults.LOG_KEY] = logid
        logger.new(logid=logid)

        def wrap_logid_header(status, headers, exc_info=None):
            headers.append((defaults.LOG_KEY, logid))
            start_response(status, headers, exc_info)

        return app(environ, wrap_logid_header)

    return wrap_logid_