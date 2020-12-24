# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/devel/durian/durian/match/strategy.py
# Compiled at: 2009-09-12 09:43:32
from collections import deque

def deepmatch(needle, haystack):
    """With a needle dictionary, recursively match all its keys to
    the haystack dictionary."""
    stream = deque([(needle, haystack)])
    while True:
        (atom_left, atom_right) = stream.pop()
        for (key, value) in atom_left.items():
            if isinstance(value, dict):
                if key not in atom_right:
                    return False
                stream.append((value, atom_right[key]))
            elif atom_right.get(key) != value:
                return False

        if not stream:
            break

    return True