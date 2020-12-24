# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/upfluence/thrift/decorator/catcher.py
# Compiled at: 2017-06-08 17:09:14
import os, functools, tornado.gen, upfluence.error_logger, thrift.Thrift
unit_name = os.environ.get('UNIT_NAME', 'unknown')

def catcher(error_class, *err_args, **err_kwargs):

    def catcher_decorator(func):

        @functools.wraps(func)
        @tornado.gen.coroutine
        def func_wrapper(*args, **kwargs):
            try:
                result = yield tornado.gen.maybe_future(func(*args, **kwargs))
            except Exception as e:
                try:
                    class_name = args[0].__class__.__name__
                except:
                    class_name = ''

                for namespace in err_kwargs.get('exception_namespaces', []):
                    if e.__class__.__module__.startswith(namespace):
                        raise e

                upfluence.error_logger.client.capture_exception(extra={'class_name': class_name, 
                   'func_name': func.__name__})
                raise error_class(*err_args)

            raise tornado.gen.Return(result)

        return func_wrapper

    return catcher_decorator


default_catcher = catcher(thrift.Thrift.TApplicationException, thrift.Thrift.TApplicationException.INTERNAL_ERROR, exception_namespaces=[
 'thrift'])