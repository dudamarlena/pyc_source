# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hermit/ui/toolbar.py
# Compiled at: 2019-06-13 16:57:32
# Size of source mod 2**32: 694 bytes
import asyncio
from .base import *
import hermit.ui.state as state
Bars = '#' * DeadTime + ' ' * DeadTime

def bottom_toolbar():
    debug_status = ''
    testnet_status = ''
    wallet_status = ''
    if state.Debug:
        debug_status = 'DEBUG'
    else:
        if state.Testnet:
            testnet_status = 'TESTNET'
        b = DeadTime - state.Timeout
        if state.Wallet.unlocked():
            wallet_status = 'wallet UNLOCKED ' + Bars[b:b + DeadTime]
        else:
            wallet_status = 'wallet locked'
    return 'Hermit --- {0:<16} {1:>10} {2:>8}'.format(wallet_status, testnet_status, debug_status)