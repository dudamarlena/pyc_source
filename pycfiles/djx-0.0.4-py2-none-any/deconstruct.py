# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/deconstruct.py
# Compiled at: 2019-02-14 00:35:17
from importlib import import_module
from django.utils.version import get_docs_version

def deconstructible(*args, **kwargs):
    """
    Class decorator that allow the decorated class to be serialized
    by the migrations subsystem.

    Accepts an optional kwarg `path` to specify the import path.
    """
    path = kwargs.pop('path', None)

    def decorator(klass):

        def __new__(cls, *args, **kwargs):
            obj = super(klass, cls).__new__(cls)
            obj._constructor_args = (args, kwargs)
            return obj

        def deconstruct(obj):
            """
            Returns a 3-tuple of class import path, positional arguments,
            and keyword arguments.
            """
            if path:
                module_name, _, name = path.rpartition('.')
            else:
                module_name = obj.__module__
                name = obj.__class__.__name__
            module = import_module(module_name)
            if not hasattr(module, name):
                raise ValueError('Could not find object %s in %s.\nPlease note that you cannot serialize things like inner classes. Please move the object into the main module body to use migrations.\nFor more information, see https://docs.djangoproject.com/en/%s/topics/migrations/#serializing-values' % (
                 name, module_name, get_docs_version()))
            return (path or '%s.%s' % (obj.__class__.__module__, name),
             obj._constructor_args[0],
             obj._constructor_args[1])

        klass.__new__ = staticmethod(__new__)
        klass.deconstruct = deconstruct
        return klass

    if not args:
        return decorator
    else:
        return decorator(*args, **kwargs)