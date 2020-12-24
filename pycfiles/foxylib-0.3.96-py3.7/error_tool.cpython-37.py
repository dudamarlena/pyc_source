# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/error/error_tool.py
# Compiled at: 2020-01-06 01:07:42
# Size of source mod 2**32: 1493 bytes
from functools import wraps
from foxylib.tools.log.foxylib_logger import FoxylibLogger

class ErrorTool:

    @classmethod
    def log_when_error(cls, func=None, logger=None, err2msg=None):
        if err2msg is None:
            err2msg = lambda e: e

        def wrapper(f):

            @wraps(f)
            def wrapped(*_, **__):
                _logger = logger if logger else FoxylibLogger.func2logger(f)
                try:
                    return f(*_, **__)
                except Exception as e:
                    try:
                        _logger.exception(err2msg(e))
                        raise
                    finally:
                        e = None
                        del e

            return wrapped

        if func:
            return wrapper(func)
        return wrapper

    @classmethod
    def default_if_error(cls, func=None, default=None, exception_tuple=(Exception,)):

        def wrapper(f):

            @wraps(f)
            def wrapped(*args, **kwargs):
                try:
                    return f(*args, **kwargs)
                except exception_tuple:
                    return default

            return wrapped

        if func:
            return wrapper(func)
        return wrapper

    @classmethod
    def f_if_error(cls, func=None, f_error=None):

        def wrapper(f):

            @wraps(f)
            def wrapped(*_, **__):
                try:
                    return f(*_, **__)
                except:
                    f_error(*_, **__)
                    raise

            return wrapped

        if func:
            return wrapper(func)
        return wrapper