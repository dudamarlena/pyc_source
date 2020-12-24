# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gratromv/Projects/enresoft/enresoft/enre/views/utils.py
# Compiled at: 2012-07-15 10:58:20
import inspect
from django.utils.importlib import import_module

def url_to_class(url, class_type=object):
    path = url
    if path.startswith('/'):
        path = path[1:]
    if path.endswith('/'):
        path = path[:-1]
    path = path.replace('/', '.')
    args = []
    while path.rfind('.') >= 0:
        arg = path[path.rfind('.') + 1:]
        path = path[0:path.rfind('.')]
        try:
            module = import_module(path)
            if not hasattr(module, arg):
                raise AttributeError("Class '%s' is not found in module '%s'." % (arg, path))
            cls = getattr(module, arg)
            if not inspect.isclass(cls):
                raise AttributeErrorError("Object '%s' is not a class." % repr(cls))
            if not issubclass(cls, class_type):
                raise AttributeError("Class '%s' is not a descendant of the '%s' class." % (cls.__name__, class_type.__name__))
            if len(args) > 0:
                args.reverse()
            return (
             cls, tuple(args), ('.').join((path, cls.__name__)))
        except ImportError as ex:
            args.append(arg)

    raise ImportError("Module not found in path '%s'" % url)