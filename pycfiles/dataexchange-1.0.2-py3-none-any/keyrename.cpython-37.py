# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dataexchange\dataexchange\json\keyrename.py
# Compiled at: 2020-01-21 03:26:24
# Size of source mod 2**32: 578 bytes


def list_keyrename(data, keys):
    output_list = []
    for item in data:
        for key, value in keys.items():
            try:
                item.update({value: item.pop(key)})
            except KeyError as e:
                try:
                    return f"KeyError: {e} key not exist."
                finally:
                    e = None
                    del e

        output_list.append(item)

    return output_list


def dict_keyrename(data, keys):
    for key, value in keys.items():
        try:
            data.update({value: data.pop(key)})
        except KeyError as e:
            try:
                return f"KeyError: {e} key not exist."
            finally:
                e = None
                del e

    return data