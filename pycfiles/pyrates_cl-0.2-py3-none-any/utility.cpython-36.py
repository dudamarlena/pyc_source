# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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