# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/utils/random.py
# Compiled at: 2019-10-15 07:28:51
# Size of source mod 2**32: 554 bytes
import random
from .itis import is_seq

def random_sample(seq, ratio_or_num=None):
    assert is_seq(seq)
    seq = list(seq)
    if ratio_or_num is None:
        return random.choice(seq)
    else:
        count = ratio_or_num
        if ratio_or_num < 1:
            count = round(ratio_or_num * len(seq))
        count = min(int(count), len(seq))
        if count <= 0:
            return []
        return random.sample(seq, count)


def random_shuffle(seq):
    assert is_seq(seq)
    seq = list(seq)
    _seq = seq[:]
    random.shuffle(_seq)
    return _seq