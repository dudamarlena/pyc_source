# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/despres/MAIN/Users/despres/Desktop/reaper/scripts/reapy/reapy/tools/json.py
# Compiled at: 2019-03-01 11:35:38
# Size of source mod 2**32: 858 bytes
"""Encode and decode ``reapy`` objects as JSON."""
import importlib, json

class ReapyEncoder(json.JSONEncoder):

    def default(self, x):
        core = importlib.import_module('reapy.core')
        if any(isinstance(x, getattr(core, c)) for c in core.__all__):
            return x._to_dict()
        return json.JSONEncoder.default(self, x)


def loads(s):
    return json.loads(s, object_hook=object_hook)


def dumps(x):
    return json.dumps(x, cls=ReapyEncoder)


def object_hook(x):
    if '__reapy__' not in x:
        return x
    core = importlib.import_module('reapy.core')
    reapy_class = getattr(core, x['class'])
    return reapy_class(*x['args'], **x['kwargs'])