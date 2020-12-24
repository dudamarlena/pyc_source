# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/message.py
# Compiled at: 2019-03-20 14:33:47
# Size of source mod 2**32: 685 bytes
from graphenecommon.message import Message as GrapheneMessage, InvalidMessageSignature
from dexstorebase.account import PublicKey
from .account import Account
from .instance import BlockchainInstance
from .exceptions import InvalidMemoKeyException, AccountDoesNotExistsException, WrongMemoKey

@BlockchainInstance.inject
class Message(GrapheneMessage):
    MESSAGE_SPLIT = ('-----BEGIN DEXSTORE SIGNED MESSAGE-----', '-----BEGIN META-----',
                     '-----BEGIN SIGNATURE-----', '-----END DEXSTORE SIGNED MESSAGE-----')

    def define_classes(self):
        self.account_class = Account
        self.publickey_class = PublicKey