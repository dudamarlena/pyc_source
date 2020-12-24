# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dwjor/Google Drive/Code/Python/django-cryptapi/cryptapi/helpers.py
# Compiled at: 2020-05-06 18:55:44
# Size of source mod 2**32: 1339 bytes
import string, random
from math import floor, log10
from cryptapi.choices import COIN_MULTIPLIERS, TOKEN_DICT
from cryptapi.utils import build_query_string

def get_coin_multiplier(coin, default=None):
    return COIN_MULTIPLIERS.get(coin, default)


def build_erc681_uri(coin, address, value):
    base_uri = 'ethereum:{target_address}'
    multiplier = get_coin_multiplier(coin, default=None)
    if multiplier:
        value = int(value * multiplier)
        _token = TOKEN_DICT.get(coin)
        if _token:
            value = int(value * 10 ** _token[4])
            return (base_uri + '/transfer?{query}').format(target_address=(_token[2]),
              query=(build_query_string({'address':address,  'uint256':value})))
        if coin in ('eth', ):
            return (base_uri + '?{query}').format(target_address=address,
              query=(build_query_string({'value': value})))
    return ''


def round_sig(x, sig=4):
    return round(x, sig - int(floor(log10(abs(x)))) - 1)


def generate_nonce(length=32):
    sequence = string.ascii_letters + string.digits
    return ''.join([random.choice(sequence) for i in range(length)])