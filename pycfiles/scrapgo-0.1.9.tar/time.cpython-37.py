# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\scrapgo\scrapgo\lib\time\time.py
# Compiled at: 2019-04-07 06:25:11
# Size of source mod 2**32: 151 bytes
from random import random

def get_random_second(low, high, rnd=2):
    width = high - low
    v = low + random() * width
    return round(v, rnd)