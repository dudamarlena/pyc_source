# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hermit/ui/relocker.py
# Compiled at: 2019-06-13 12:22:01
# Size of source mod 2**32: 504 bytes
import asyncio
from .base import *
import hermit.ui.state as state

async def relock_wallet_if_timed_out():
    while True:
        await asyncio.sleep(0.5)
        await _handle_tick()


async def _handle_tick():
    if state.Live:
        state.Live = False
    else:
        if state.Wallet.unlocked():
            if state.Timeout > 0:
                state.Timeout = state.Timeout - 1
                if state.Timeout <= 0:
                    state.Timeout = 0
                    state.Wallet.lock()