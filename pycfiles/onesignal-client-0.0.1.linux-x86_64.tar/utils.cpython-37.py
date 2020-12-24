# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grelek/projects/onesignal-notifications/venv/lib/python3.7/site-packages/onesignal/utils.py
# Compiled at: 2019-02-27 07:16:52
# Size of source mod 2**32: 316 bytes


def merge_dicts(first_dict, *dicts):
    """
    Merge several dicts

    This function is needed for Python 2 support. It will be REMOVED on January 1, 2020.
    Python 3 alternative: x = {**a, **b}
    """
    new_dict = first_dict.copy()
    for dict_ in dicts:
        new_dict.update(dict_)

    return new_dict