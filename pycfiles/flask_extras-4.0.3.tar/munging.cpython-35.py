# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taborc/git/spog/flask_extras/flask_extras/filters/munging.py
# Compiled at: 2017-01-09 16:41:25
# Size of source mod 2**32: 2593 bytes
"""Filters for working with data structures, munging, etc..."""
from collections import defaultdict

def filter_list(lst, vals):
    """Filter a list by vals.

    Args:
        lst (dict): The dictionary to filter.

    Returns:
        string (dict): The filtered dict.
    """
    if any([not lst, not isinstance(lst, list), not isinstance(vals, list)]):
        return lst
    return list(set(lst).difference(set(vals)))


def filter_vals(obj, vals):
    """Filter a dictionary by values.

    Args:
        obj (dict): The dictionary to filter.

    Returns:
        obj (dict): The filtered dict.
    """
    if obj is None or not isinstance(vals, list):
        return obj
    newdict = {}
    for k, v in obj.items():
        if v in vals:
            pass
        else:
            newdict[k] = v

    return newdict


def filter_keys(obj, keys):
    """Filter a dictionary by keys.

    Args:
        obj (dict): The dictionary to filter.

    Returns:
        obj (dict): The filtered dict.
    """
    if obj is None or not isinstance(keys, list):
        return obj
    newdict = {}
    for k, v in obj.items():
        if k in keys:
            pass
        else:
            newdict[k] = v

    return newdict


def group_by(objs, groups={}, attr='name'):
    """Group a list of objects into a dict grouped by specified keys.

    Args:
        objs: A list of objects
        keys: A dict of keys and their corresponding names to match on.
        attr: The attr to use to get fields for matching (default: {'name'})

    Returns:
        A grouped dictionary and objects.
        dict

    >>> group_by(
        [obj1, obj2], groups={'name1': 'g1', 'name2': 'g1'}, attr='name')
    """
    grouped = defaultdict(list)
    seen = []
    group_matches = groups.keys()
    for obj in objs:
        obj_label = None
        if attr is not None and hasattr(obj, attr):
            obj_label = getattr(obj, attr)
        if obj_label is not None and obj_label in seen:
            pass
        else:
            seen.append(obj_label)
            if obj_label in group_matches:
                for label, group in groups.items():
                    if obj_label == label:
                        grouped[group].append(obj)

            else:
                grouped['__unlabeled'].append(obj)

    return grouped