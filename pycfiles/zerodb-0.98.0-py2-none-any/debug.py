# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/util/debug.py
# Compiled at: 2016-03-08 18:12:41
import pickle, six

class DebugUnpickler(pickle.Unpickler):
    """
    Unpickler which returns class names instead of unpickling (for debug purposes)
    """

    def find_class(self, module, name):
        return name


if six.PY2:
    DebugUnpickler.dispatch[pickle.REDUCE] = lambda x: None

def debug_loads(obj):
    up = DebugUnpickler(six.BytesIO(obj))
    return up.load()