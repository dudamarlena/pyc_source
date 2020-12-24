# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/mcts/utils.py
# Compiled at: 2015-03-25 05:47:48
# Size of source mod 2**32: 804 bytes
import random, numpy as np

def rand_max(iterable, key=None):
    """
    A max function that tie breaks randomly instead of first-wins as in
    built-in max().
    :param iterable: The container to take the max from
    :param key: A function to compute tha max from. E.g.:
      >>> rand_max([-2, 1], key=lambda x:x**2
      -2
      If key is None the identity is used.
    :return: The entry of the iterable which has the maximum value. Tie
    breaks are random.
    """
    if key is None:
        key = lambda x: x
    max_v = -np.inf
    max_l = []
    for item, value in zip(iterable, [key(i) for i in iterable]):
        if value == max_v:
            max_l.append(item)
        elif value > max_v:
            max_l = [
             item]
            max_v = value
            continue

    return random.choice(max_l)