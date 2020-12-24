# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/RESTinpy/decorators.py
# Compiled at: 2009-04-22 07:30:36


def rename_param(source, target):

    def decorator(fn):

        def wrapper(*args, **kw_args):
            new_kw_args = dict(kw_args)
            new_kw_args[target] = new_kw_args[source]
            del new_kw_args[source]
            return fn(*args, **new_kw_args)

        return wrapper

    return decorator


def drop_param(*param_names):

    def decorator(fn):

        def wrapper(*args, **kw_args):
            new_kw_args = dict(kw_args)
            for p in param_names:
                del new_kw_args[p]

            return fn(*args, **new_kw_args)

        return wrapper

    return decorator