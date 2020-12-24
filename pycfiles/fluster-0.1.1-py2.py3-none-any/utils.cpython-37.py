# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/Documents/repos/parsely/fluster/fluster/utils.py
# Compiled at: 2019-04-24 11:52:27
# Size of source mod 2**32: 407 bytes


def round_controlled(cycled_iterable, rounds=1):
    """Return after <rounds> passes through a cycled iterable."""
    round_start = None
    rounds_completed = 0
    for item in cycled_iterable:
        if round_start is None:
            round_start = item
        else:
            if item == round_start:
                rounds_completed += 1
        if rounds_completed == rounds:
            return
        yield item