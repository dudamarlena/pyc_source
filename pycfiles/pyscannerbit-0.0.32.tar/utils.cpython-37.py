# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gmartine/pyscannerbit/pyscannerbit/utils.py
# Compiled at: 2020-03-04 01:47:30
# Size of source mod 2**32: 716 bytes
import copy

def _merge(a, b, path=None):
    """merges b into a"""
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                _merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass
            else:
                continue
        else:
            a[key] = copy.deepcopy(b[key])

    return a