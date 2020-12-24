# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ensembl_map/util.py
# Compiled at: 2020-03-31 18:43:44
# Size of source mod 2**32: 796 bytes
import re

def assert_valid_position(start=None, end=None):
    if start is not None:
        if start < 1:
            raise ValueError(f"Start must be >= 1 ({start})")
    else:
        if end is not None:
            if end < 1:
                raise ValueError(f"End must be >= 1 ({end})")
        if start is not None:
            if end is not None and start > end:
                raise ValueError(f"Start ({start}) must be <= end ({end})")


def is_ensembl_id(feature):
    """String looks like an Ensembl Stable ID."""
    return bool(re.match('ENS[A-Z]+\\d{11}(?:\\.\\d)?', feature.upper()))


def singleton(cls):
    """Wrapper that implements a class as a singleton."""
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance