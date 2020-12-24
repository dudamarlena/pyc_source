# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hermit/ui/state.py
# Compiled at: 2019-06-13 12:22:01
# Size of source mod 2**32: 183 bytes
from os import environ
from hermit.wallet import HDWallet
Timeout = 0
Live = False
Debug = 'DEBUG' in environ
Testnet = 'TESTNET' in environ
Wallet = HDWallet()
Session = None