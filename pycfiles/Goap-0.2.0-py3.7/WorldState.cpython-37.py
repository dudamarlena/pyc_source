# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Goap/WorldState.py
# Compiled at: 2019-07-05 11:36:04
# Size of source mod 2**32: 1285 bytes


class WorldState(dict):
    __doc__ = "\n    ws = WorldState({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])\n    "

    def __init__(self, *args, **kwargs):
        (super(WorldState, self).__init__)(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(WorldState, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(WorldState, self).__delitem__(key)
        del self.__dict__[key]

    def __le__(self, other):
        for k, v in other.__dict__():
            if other.__dict__()['k'] != v:
                return False

        return True

    def __eq__(self, other):
        if other.items() != self.items():
            return False
        return True

    def __hash__(self):
        return hash(tuple(sorted(self.items())))