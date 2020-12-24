# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tornado_extensions/concurrency.py
# Compiled at: 2013-09-03 05:36:04
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps
import tornado.ioloop, tornado.web
MAX_WORKERS = 5
EXECUTOR = ThreadPoolExecutor(max_workers=MAX_WORKERS)

class ExecutorMixin(object):
    """Mixin class for decorator run_on_executor"""
    executor = EXECUTOR
    io_loop = tornado.ioloop.IOLoop.current()


def unblock(f):
    """Decorator responsible for executing http method in
    background by using thread pool from concurrent.futures lib."""

    @tornado.web.asynchronous
    @wraps(f)
    def wrapper(*args, **kwargs):
        self = args[0]

        def callback(future):
            self.write(future.result())
            self.finish()

        future = EXECUTOR.submit(partial(f, *args, **kwargs))
        self.io_loop.add_future(future, lambda future: callback(future))
        return future

    return wrapper