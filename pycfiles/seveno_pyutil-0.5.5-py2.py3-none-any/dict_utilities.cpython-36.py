# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomislav/dev/seveno_pyutil/build/lib/seveno_pyutil/dict_utilities.py
# Compiled at: 2019-01-17 13:53:03
# Size of source mod 2**32: 158 bytes


def inverted(dct):
    """
    Converts::

        d = {'a': 1, 'b': 2}

    To::

        {1: 'a', 2: 'b'}
    """
    return {v:k for k, v in dct.items()}