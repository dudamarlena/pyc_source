# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/utils/collections.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = '\n    pocoo.utils.collections\n    ~~~~~~~~~~~~~~~~~~~~~~~\n\n    Collection utilities.\n\n    :copyright: 2006 by Armin Ronacher, Georg Brandl.\n    :license: GNU GPL, see LICENSE for more details.\n'

class CallbackDict(dict):
    """
    A dictionary that calls an arbitrary function on
    setting and deleting values.
    """
    __module__ = __name__

    def __init__(self, _callback_, **kwds):
        dict.__init__(self, **kwds)
        self._cb = _callback_

    def clear(self):
        for key in self:
            self._cb(self, key, None)

        super(CallbackDict, self).clear()
        return

    def update(self, *args, **kwargs):
        for (key, value) in dict(*args, **kwargs).iteritems():
            self._cb(self, key, value)
            self[key] = value

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self._cb(self, key, value)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._cb(self, key, None)
        return


class AttrDict(dict):
    """
    A dictionary for which attribute access is equivalent
    to item access.
    """
    __module__ = __name__

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]


def dict_diff(d1, d2):
    """
    Return the difference of dictionaries ``d1`` and ``d2``::

        >>> d1 = {"foo": "bar", "spam": "eggs"}
        >>> d2 = {"foo": "bar", "spam": "EGGS"}
        >>> dict_diff(d1, d2)
        {'spam': 'EGGS'}
    """
    set1 = set(d1.items())
    set2 = set(d2.items())
    diff = set2 - set1.intersection(set2)
    return dict(diff)