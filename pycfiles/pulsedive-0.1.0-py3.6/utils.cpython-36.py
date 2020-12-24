# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pulsedive/utils.py
# Compiled at: 2018-09-19 06:36:09
# Size of source mod 2**32: 489 bytes


def flatten(value, prefix=''):
    if isinstance(value, list):
        ret = {}
        for idx, e in enumerate(value):
            flattened = flatten(e, prefix=('{}[{}]'.format(prefix, idx)))
            ret.update(flattened)

        return ret
    else:
        if isinstance(value, dict):
            ret = {}
            for field, e in value.items():
                flattened = flatten(e, prefix=('{}[{}]'.format(prefix, field)))
                ret.update(flattened)

            return ret
        return {prefix: value}