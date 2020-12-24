# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/th13f/dev/drf-batch-requests/drf_batch/utils.py
# Compiled at: 2017-10-04 06:21:22
# Size of source mod 2**32: 398 bytes


def get_attribute(instance, attrs):
    for attr in attrs:
        if instance is None:
            return
        if attr == '*':
            pass
        else:
            if isinstance(instance, list):
                instance = list(map(lambda i: i[attr], instance))
            else:
                instance = instance[attr]

    return instance