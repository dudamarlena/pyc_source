# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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