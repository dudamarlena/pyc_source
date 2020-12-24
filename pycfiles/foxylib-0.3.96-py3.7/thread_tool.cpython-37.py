# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/thread/thread_tool.py
# Compiled at: 2020-01-06 01:07:42
# Size of source mod 2**32: 1369 bytes
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from foxylib.tools.log.logger_tool import LoggerTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
logger = logging.getLogger(__name__)

class ThreadTool:

    @classmethod
    def func2threaded(cls, func=None, max_workers=None):
        logger = FoxylibLogger.func2logger(cls.func2threaded)

        def wrapper(f):

            @wraps(f)
            def wrapped(*args, **kwargs):
                executor = ThreadPoolExecutor(max_workers=max_workers)

                def f_new(*args, **kwargs):
                    rv = f(*args, **kwargs)
                    logger.info({'message':'func2thread',  'value':rv})
                    LoggerTool.logger2flush_handlers(logger)
                    return rv

                future = (executor.submit)(f_new, *args, **kwargs)
                return future

            return wrapped

        if func:
            return wrapper(func)
        return wrapper

    @classmethod
    def future2result_or_raise(cls, future):
        exc_future = future.exception()
        if exc_future:
            logger.error({'messsage':'future2result_or_raise',  'exception':exc_future})
            raise exc_future
        return future.result()