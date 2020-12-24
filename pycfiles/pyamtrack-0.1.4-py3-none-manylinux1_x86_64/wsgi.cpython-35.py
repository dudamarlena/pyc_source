# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/wsgi.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 1386 bytes
__doc__ = "PyAMS_utils.wsgi module\n\nThis module provides a method decorator which can store it's value into request environment\n"
__docformat__ = 'restructuredtext'

def wsgi_environ_cache(*names):
    """Wrap a function/method to cache its result for call into request.environ

    :param [string...] names: keys to cache into environ; len(names) must
        be equal to the result's length or scalar
    """

    def decorator(func):

        def function_wrapper(self, request):
            scalar = len(names) == 1
            try:
                env = [request.environ[cached_key] for cached_key in names]
            except KeyError:
                env = func(self, request)
                if scalar:
                    env = [
                     env]
                request.environ.update(zip(names, env))

            if scalar:
                return env[0]
            return env

        return function_wrapper

    return decorator