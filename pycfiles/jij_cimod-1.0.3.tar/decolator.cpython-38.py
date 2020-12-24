# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/ssd/workspace/linux/workspace/Jij/cimod/cimod/utils/decolator.py
# Compiled at: 2020-04-28 17:44:22
# Size of source mod 2**32: 930 bytes


def disabled(func):

    def wrapper(*args, **kwargs):
        raise NotImplementedError('The function {} is disabled.'.format(func.__name__))

    return wrapper


def recalc(func):

    def wrapper(self, *args, **kwargs):
        self._re_calculate = True
        self._re_calculate_indices = True
        return func(self, *args, **kwargs)

    return wrapper