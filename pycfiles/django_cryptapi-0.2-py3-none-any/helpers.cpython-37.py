# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dwjor/Google Drive/Code/Python/django-cryptapi/cryptapi/helpers.py
# Compiled at: 2018-11-16 06:46:09
# Size of source mod 2**32: 534 bytes
import string, random
from math import floor, log10
from cryptapi.choices import COIN_MULTIPLIERS

def get_coin_multiplier(coin, default=None):
    return COIN_MULTIPLIERS.get(coin, default)


def round_sig(x, sig=4):
    return round(x, sig - int(floor(log10(abs(x)))) - 1)


def generate_nonce(length=32):
    sequence = string.ascii_letters + string.digits
    return ''.join([random.choice(sequence) for i in range(length)])