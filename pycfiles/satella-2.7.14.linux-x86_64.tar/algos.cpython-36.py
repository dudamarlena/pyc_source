# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/algos.py
# Compiled at: 2020-04-25 10:46:39
# Size of source mod 2**32: 695 bytes
import typing as tp
__all__ = ['merge_dicts']

def merge_dicts(v1: tp.Any, v2: tp.Any) -> tp.Any:
    """
    Try to merge two dicts/list together. If key collision is found, value from v2 will be taken.

    If the objects aren't dicts or lists, v2 will be returned.

    Lists will be concatenated, and dicts updated. v1 will be updated in-place!
    """
    if isinstance(v1, dict) and isinstance(v2, dict):
        for k in v2.keys():
            try:
                v1[k] = merge_dicts(v1[k], v2[k])
            except KeyError:
                v1[k] = v2[k]

        return v1
    else:
        if isinstance(v1, list):
            if isinstance(v2, list):
                v1.extend(v2)
                return v1
        return v2