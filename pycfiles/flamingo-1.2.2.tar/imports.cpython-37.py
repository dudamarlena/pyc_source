# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/utils/imports.py
# Compiled at: 2020-04-28 06:15:31
# Size of source mod 2**32: 1580 bytes
import importlib, inspect, runpy, re
SCRIPT_RE = re.compile('^[^:]+::[a-zA-Z0-9_]+$')
MODULE_RE = re.compile('^[a-zA-Z0-9_.]+$')

def acquire(item, types=None):
    path = item
    if types:
        if not isinstance(types, tuple):
            types = (
             types,)
    elif isinstance(item, str):
        if MODULE_RE.match(item):
            try:
                item = importlib.import_module(item)
                path = inspect.getfile(item)
            except Exception:
                if '.' in item:
                    module_name, attr_name = item.rsplit('.', 1)
                else:
                    module_name = item
                    attr_name = None
                module = importlib.import_module(module_name)
                path = inspect.getfile(module)
                if attr_name:
                    item = getattr(module, attr_name)
                else:
                    item = module

        else:
            if SCRIPT_RE.match(item):
                script, attr_name = item.split('::')
                values = runpy.run_path(script)
                if attr_name not in values:
                    raise ImportError("script '{}' has no attribute '{}'".format(script, attr_name))
                item = values[attr_name]
                path = script
            else:
                raise ValueError("invalid import string '{}'".format(item))
    if types and not isinstance(item, types):
        raise ValueError("'{}' has wrong type. Allowed types: {}".format(attr_name, ', '.join([i.__name__ for i in types])))
    return (item, path)