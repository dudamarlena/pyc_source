# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pandaspipe/_util.py
# Compiled at: 2016-02-16 17:37:52


def match_in_dict(keys, values):
    """(list, list) -> dict
    :param keys: list of keys
    :param values: list of values
    :return: dict with key:value from keys and values
    """
    assert len(keys) == len(values)
    return {keys[i]:values[i] for i in range(0, len(keys))}


def equals_for_dict(d1, d2):
    """(dict(str, DataFrame), dict(str, DataFrame)) -> bool
    Deep compare for two specific dict
    :param d1: Dict with string key and dataframe values
    :param d2: Dict with string key and dataframe values
    :return: equals bool
    """
    if len(d1.keys()) != len(d2.keys()):
        return False
    else:
        for key in d1.keys():
            obj1 = d1.get(key)
            obj2 = d2.get(key)
            if obj2 is None:
                return False
            if obj1.columns.tolist() == obj2.columns.tolist():
                return obj1.equals(obj2)
            return False

        return


def patch_list(lst, obj):
    if isinstance(obj, list):
        lst.extend(obj)
    else:
        lst.append(obj)
    return lst


def isSubset(list_, sub_list):
    return set(sub_list) <= set(list_)