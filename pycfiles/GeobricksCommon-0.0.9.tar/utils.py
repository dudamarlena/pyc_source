# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/geobricks/geobricks/server/geobricks_common/geobricks_common/core/utils.py
# Compiled at: 2015-06-04 04:13:35
from copy import deepcopy

def dict_merge(a, b):
    """
    Source: https://www.xormedia.com/recursively-merge-dictionaries-in-python/
    """
    if b is not None:
        if not isinstance(b, dict):
            return b
        result = deepcopy(a)
        for k, v in b.iteritems():
            if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
            else:
                result[k] = deepcopy(v)

        return result
    return deepcopy(a)