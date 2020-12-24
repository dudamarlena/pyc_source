# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/wallet.py
# Compiled at: 2019-03-20 04:09:59
# Size of source mod 2**32: 599 bytes
from dexstorebase.account import PrivateKey
from graphenecommon.wallet import Wallet as GrapheneWallet
from graphenecommon.exceptions import InvalidWifError, KeyAlreadyInStoreException, KeyNotFound, NoWalletException, OfflineHasNoRPCException, WalletExists, WalletLocked
from .instance import BlockchainInstance

@BlockchainInstance.inject
class Wallet(GrapheneWallet):

    def define_classes(self):
        self.default_key_store_app_name = 'dexstore'
        self.privatekey_class = PrivateKey