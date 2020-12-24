# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\01_work\15_phd\11_python_neural_mass_models\pyrates\pyrates\frontend\utility.py
# Compiled at: 2019-06-26 16:26:50
# Size of source mod 2**32: 821 bytes
from typing import Union

def deep_freeze(freeze: Union[(dict, list, set, tuple)]):
    """

    Parameters
    ----------
    freeze

    Returns
    -------
    frozen
    """
    if isinstance(freeze, dict):
        try:
            frozen = frozenset(freeze.items())
        except TypeError:
            temp = set()
            for key, item in freeze.items():
                temp.add((key, deep_freeze(item)))

            frozen = frozenset(temp)

    elif isinstance(freeze, list):
        try:
            frozen = tuple(freeze)
        except TypeError as e:
            raise e

    else:
        try:
            hash(freeze)
        except TypeError as e:
            raise e
        else:
            frozen = freeze
        return frozen