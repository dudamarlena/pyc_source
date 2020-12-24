# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/common/FlatDict.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from pprint import pprint
import collections

def key_prefix_replace(d, prefix, new_prefix=''):
    """
    replaces the list of prefix in keys of a flattened dict

    :param d: the flattened dict
    :param prefix: a list of prefixes that are replaced with a new prefix. Typically this will be ""
    :type prefix: list of str
    :param new_prefix: The new prefix. By default it is set to ""
    :return: the dict with the keys replaced as specified
    """
    items = []
    for k, v in d.items():
        new_key = k
        for p in prefix:
            new_key = new_key.replace(p, new_prefix, 1)

        items.append((new_key, v))

    return dict(items)


def flatten(d, parent_key='', sep='__'):
    """
    flattens the dict into a one dimensional dictionary

    :param d: multidimensional dict
    :param parent_key: replaces from the parent key
    :param sep: the separation character used when fattening. the default is __
    :return: the flattened dict
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))

    return dict(items)


class FlatDict(dict):
    """
    A data structure to manage a flattened dict. It is initialized by passing the dict
    at time of initialization.
    """

    @property
    def dict(self):
        return self.__dict__

    def __init__(self, d):
        self.__dict__ = flatten(d)

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def keys(self):
        return list(self.__dict__.keys())

    def values(self):
        return list(self.__dict__.values())

    def __cmp__(self, dictionary):
        return cmp(self.__dict__, dictionary)

    def __contains__(self, item):
        return item in self.__dict__

    def add(self, key, value):
        self.__dict__[key] = value

    def __iter__(self):
        return iter(self.__dict__)

    def __call__(self):
        return self.__dict__

    def __getattr__(self, attr):
        return self.get(attr)