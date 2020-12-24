# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\tools\json.py
# Compiled at: 2020-03-21 05:23:32
# Size of source mod 2**32: 1694 bytes
"""Encode and decode ``reapy`` objects as JSON."""
import importlib, json, operator, sys

class ClassCache(dict):
    _core = None

    def __missing__(self, key):
        if self._core is None:
            self._core = importlib.import_module('reapy.core')
        self[key] = getattr(self._core, key)
        return self[key]


_CLASS_CACHE = ClassCache()

class ReapyEncoder(json.JSONEncoder):

    def default(self, x):
        if hasattr(x, '_to_dict'):
            return x._to_dict()
        if callable(x):
            return {'__callable__':True,  'module_name':x.__module__, 
             'name':x.__qualname__}
        if isinstance(x, slice):
            return {'__slice__':True, 
             'args':(x.start, x.stop, x.step)}
        return json.JSONEncoder.default(self, x)


def loads(s):
    return json.loads(s, object_hook=object_hook)


def dumps(x):
    return json.dumps(x, cls=ReapyEncoder)


def object_hook(x):
    if '__reapy__' in x:
        reapy_class = _CLASS_CACHE[x['class']]
        return reapy_class(*x['args'], **x['kwargs'])
    if '__callable__' in x:
        module_name, name = x['module_name'], x['name']
        try:
            module = sys.modules[module_name]
        except KeyError:
            module = importlib.import_module(module_name)

        return operator.attrgetter(name)(sys.modules[module_name])
    if '__slice__' in x:
        return slice(*x['args'])
    return x