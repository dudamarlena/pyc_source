# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/secobj/memoizer.py
# Compiled at: 2012-08-27 06:29:54
import functools
from secobj.localization import _

def memoize(*args, **kwargs):
    cache = kwargs.get('cache', dict())
    method = kwargs.get('method', False)
    optkey = kwargs.get('optimizekey', True)
    callback = kwargs.get('createkey', None)

    def factory(func):

        @functools.wraps(func)
        def decorator(*args, **kwargs):
            keyargs = args if not method else args[1:]
            if callback is None:
                key = keyargs + tuple(kwargs.itervalues())
            else:
                key = callback(keyargs, kwargs)
            if optkey and len(key) == 1:
                key = key[0]
            try:
                return cache[key]
            except TypeError:
                return func(*args, **kwargs)
            except KeyError:
                value = func(*args, **kwargs)
                cache[key] = value
                return value

            return

        return decorator

    if len(args) > 1:
        raise TypeError, _('memoize() takes either 0 or 1 argument ({count} given)').format(len(args))
    else:
        if len(args) == 1 and not kwargs:
            return factory(args[0])
        else:
            return factory

    return