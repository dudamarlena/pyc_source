# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jsonrpcdjango/loader.py
# Compiled at: 2019-10-14 11:34:17
# Size of source mod 2**32: 758 bytes


def load_service_instance(path):
    try:
        from django.utils.importlib import import_module
    except:
        from importlib import import_module

    from django.core.exceptions import ImproperlyConfigured
    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]
    try:
        mod = import_module(module)
    except ImportError as e:
        try:
            raise ImproperlyConfigured('Error importing JSON-RPC service instance %s: "%s"' % (path, e))
        finally:
            e = None
            del e

    except ValueError as e:
        try:
            raise ImproperlyConfigured('Error importing JSON-RPC instance: %s' % e)
        finally:
            e = None
            del e

    try:
        obj = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" JSON-RPC instance' % (module, attr))

    return obj