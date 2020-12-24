# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/core/sentiel.py
# Compiled at: 2019-08-08 16:17:45
# Size of source mod 2**32: 1214 bytes
try:
    import copyreg
except ImportError:
    import copy_reg as copyreg

class Sentinel(object):
    _existing_instances = {}

    def __init__(self, name):
        super(Sentinel, self).__init__()
        self._name = name
        self._existing_instances[self._name] = self

    def __repr__(self):
        return '<{0}>'.format(self._name)

    def __getnewargs__(self):
        return (
         self._name,)

    def __new__(cls, name, obj_id=None):
        existing_instance = cls._existing_instances.get(name)
        if existing_instance is not None:
            return existing_instance
        else:
            return super(Sentinel, cls).__new__(cls)


def _sentinel_unpickler(name, obj_id=None):
    if name in Sentinel._existing_instances:
        return Sentinel._existing_instances[name]
    else:
        return Sentinel(name)


def _sentinel_pickler(sentinel):
    return (
     _sentinel_unpickler, sentinel.__getnewargs__())


copyreg.pickle(Sentinel, _sentinel_pickler, _sentinel_unpickler)
NOTHING = Sentinel('NOTHING')
REQUIRED = Sentinel('REQUIRED')