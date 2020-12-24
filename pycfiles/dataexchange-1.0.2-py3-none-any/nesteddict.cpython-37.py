# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dataexchange\dataexchange\json\nesteddict.py
# Compiled at: 2020-01-22 11:36:36
# Size of source mod 2**32: 954 bytes
from dataexchange.json.keyrename import dict_keyrename
from dataexchange.json.keyrename import list_keyrename

def nested_dict(data, raw_data, depth, keys):
    var_store = []
    for idx, item in enumerate(depth, 0):
        var_store.append(item)
        popper = data.pop(item)
        try:
            if isinstance(popper, dict):
                for key, val in keys.items():
                    popper[key]

                popper = dict_keyrename(popper, keys)
            else:
                if isinstance(popper, list):
                    x = popper[0]
                    for key, val in keys.items():
                        x[key]

                    popper = list_keyrename(popper, keys)
        except KeyError:
            pass

        data = popper
        if idx == 0:
            raw_data[var_store[0]] = data
        elif idx == 1:
            raw_data[var_store[0]][var_store[1]] = data
            continue

    return raw_data