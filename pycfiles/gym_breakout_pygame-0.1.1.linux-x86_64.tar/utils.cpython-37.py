# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marcofavorito/.pyenv/versions/3.7.6/lib/python3.7/site-packages/gym_breakout_pygame/utils.py
# Compiled at: 2020-01-21 06:34:35
# Size of source mod 2**32: 1411 bytes
"""This module contains utility functions."""
from functools import reduce
from typing import List
from gym.spaces import Dict, Discrete

def encode(obs: List[int], spaces: List[int]) -> int:
    """
    Encode an observation from a list of gym.Discrete spaces in one number.
    :param obs: an observation belonging to the state space (a list of gym.Discrete spaces)
    :param spaces: the list of gym.Discrete spaces from where the observation is observed.
    :return: the encoded observation.
    """
    assert len(obs) == len(spaces)
    sizes = spaces
    result = obs[0]
    shift = sizes[0]
    for o, size in list(zip(obs, sizes))[1:]:
        result += o * shift
        shift *= size

    return result


def decode(obs: int, spaces: List[int]) -> List[int]:
    """
    Decode an observation from a list of gym.Discrete spaces in a list of integers.
    It assumes that obs has been encoded by using the 'utils.encode' function.
    :param obs: the encoded observation
    :param spaces: the list of gym.Discrete spaces from where the observation is observed.
    :return: the decoded observation.
    """
    result = []
    sizes = spaces[::-1]
    shift = reduce(lambda x, y: x * y, sizes) // sizes[0]
    for size in sizes[1:]:
        r = obs // shift
        result.append(r)
        obs %= shift
        shift //= size

    result.append(obs)
    return result[::-1]