# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/abiosgaming/utils.py
# Compiled at: 2015-11-26 00:49:29
"""Useful utilities"""
import collections

def named_tuple(mapping):
    """
    Function to turn a collections.Mapping into a namedtuple of namedtuples

    Takes dict, collections.defaultdict,
    collections.OrderedDict, or collections.Counter
    recursively turn it into a named_tuple

    :param mapping: object to be converted to namedtuple
    :rtype: collections.namedtuple of collections.namedtuple
    """
    if isinstance(mapping, collections.Mapping):
        for key, value in mapping.items():
            mapping[key] = named_tuple(value)

        return namedtuple_from_mapping(mapping)
    return mapping


def namedtuple_from_mapping(mapping, name='NamedTuple'):
    """
    Function to take a mpping and created a namedtuple

    :param mapping: mapping to be converted to namedtuple
    :rtype: namedtuple
    """
    this_namedtuple_maker = collections.namedtuple(name, mapping.keys())
    return this_namedtuple_maker(**mapping)