# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitcoin/units.py
# Compiled at: 2017-07-08 11:42:23
# Size of source mod 2**32: 492 bytes
"""
Defines the bitcoin currency units and equivalences and methods to handle them
"""
BTC_PER_SATOSHI = 100000000

def btc_to_satoshi(value):
    """
    Given a BTC value, transforms the value into satoshis and returns it
    """
    return int(value * BTC_PER_SATOSHI)


def satoshi_to_btc(value):
    """
    Given a satoshi value, transforms the value into BTC and returns it
    """
    return value / BTC_PER_SATOSHI