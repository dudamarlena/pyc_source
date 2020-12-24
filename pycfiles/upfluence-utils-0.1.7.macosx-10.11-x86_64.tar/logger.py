# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/upfluence/thrift/decorator/logger.py
# Compiled at: 2017-06-08 17:59:34
import datetime, functools, tornado.gen
from upfluence.log import logger

def default_logger(func):

    @functools.wraps(func)
    @tornado.gen.coroutine
    def func_wrapper(*args, **kwargs):
        source = args[0].__class__.__name__
        start = datetime.datetime.now()
        logger.warning('Running method `%s` with [%s]' % (
         func.__name__,
         (',').join(map(lambda arg: str(arg).replace('\n', ' '), args))[:100]), extra={'source': source})
        try:
            result = yield tornado.gen.maybe_future(func(*args, **kwargs))
            delta = datetime.datetime.now() - start
            logger.warning('Finished method `%s` with [%s]. Took: %fms' % (
             func.__name__,
             (',').join(map(lambda arg: str(arg).replace('\n', ' '), args))[:100],
             delta.seconds * 1000 + delta.microseconds / 1000), extra={'source': source})
        except Exception as e:
            delta = datetime.datetime.now() - start
            logger.warning('Finished method `%s` with [%s] errored: %s. Took: %fms' % (
             func.__name__,
             (',').join(map(lambda arg: str(arg).replace('\n', ' '), args))[:100], e.__class__.__name__,
             delta.seconds * 1000 + delta.microseconds / 1000), extra={'source': source})
            raise e

        raise tornado.gen.Return(result)

    return func_wrapper