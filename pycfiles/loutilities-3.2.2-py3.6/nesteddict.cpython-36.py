# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\nesteddict.py
# Compiled at: 2019-11-20 12:25:23
# Size of source mod 2**32: 6259 bytes
from copy import deepcopy

class parameterError(Exception):
    pass


def dotted2nested_set(d, key, value):
    """
    if key is in dotted notation, turn into nested dict
    e.g., dotted['k1.k2.k3'] into nested['k1']['k2']['k3']
    """
    keysplit = key.split('.')
    if len(keysplit) == 1:
        d[key] = value
    else:
        if keysplit[0] not in d:
            d[keysplit[0]] = {}
        dotted2nested_set(d[keysplit[0]], '.'.join(keysplit[1:]), value)


def dotted2nested_get(d, key):
    """
    if key is in dotted notation, turn into nested dict
    e.g., dotted['k1.k2.k3'] into nested['k1']['k2']['k3']
    """
    keysplit = key.split('.')
    if len(keysplit) == 1:
        return d[key]
    else:
        return dotted2nested_get(d[keysplit[0]], '.'.join(keysplit[1:]))


def nested2dotted_keys(d):
    keys = []
    for key in d:
        if isinstance(d[key], dict):
            keys += ['.'.join([key, subkey]) for subkey in nested2dotted_keys(d[key])]
        else:
            keys.append(key)

    return keys


def obj2dict(obj):
    if not hasattr(obj, '__dict__'):
        return obj
    else:
        result = {}
        for key, val in list(obj.__dict__.items()):
            if key.startswith('_'):
                pass
            else:
                element = []
                if isinstance(val, list):
                    for item in val:
                        element.append(obj2dict(item))

                else:
                    element = obj2dict(val)
                result[key] = element

        return result


class NestedDict(dict):

    def __init__(self, val={}):
        self.set(val)

    def __setitem__(self, key, val):
        dotted2nested_set(self.val, key, val)

    def __getitem__(self, key):
        return dotted2nested_get(self.val, key)

    def set(self, newval):
        """
        set val of class to supplied parameter

        if dict just copy
        convert object to dict
        raise error if not dict or object

        parameters:

        * newval - must be dict or obj, otherwise exception
        """
        if isinstance(newval, dict):
            self.val = deepcopy(newval)
        else:
            if hasattr(newval, '__dict__'):
                self.val = obj2dict(newval)
            else:
                raise parameterError('invalid parameter {}: newval must be dict or object'.format(newval))

    def to_dict(self):
        return self.val

    def to_dotted(self):
        dotted = {}
        for key in nested2dotted_keys(self.val):
            dotted[key] = dotted2nested_get(self.val, key)

        return dotted


class Dictate(object):
    __doc__ = '\n    Object view of a dict, updating the passed in dict when values are set\n    or deleted. "Dictate" the contents of a dict...:\n    '

    def __init__(self, d):
        object.__setattr__(self, '_Dictate__dict', d)

    def __getitem__(self, name):
        value = self._Dictate__dict[name]
        if isinstance(value, dict):
            value = Dictate(value)
        return value

    def __setitem__(self, name, value):
        self._Dictate__dict[name] = value

    def __delitem__(self, name):
        del self._Dictate__dict[name]

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self._Dictate__dict)

    def __str__(self):
        return str(self._Dictate__dict)