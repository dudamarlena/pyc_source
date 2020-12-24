# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mittepro/utils.py
# Compiled at: 2019-11-05 13:30:44
# Size of source mod 2**32: 629 bytes
import json

def is_json(value):
    try:
        parsed = json.loads(value)
        return True
    except Exception:
        return False


def merge_two_dicts(d1, d2):
    d3 = d1.copy()
    d3.update(d2)
    return d3


def item_in_dict(dictionary, item):
    return item in dictionary and dictionary[item]


def item_not_in_dict(dictionary, item):
    return item not in dictionary or not dictionary[item]


def attr_in_instance(instance, attr):
    return hasattr(instance, attr) and getattr(instance, attr)


def attr_not_in_instance(instance, attr):
    return not hasattr(instance, attr) or not getattr(instance, attr)