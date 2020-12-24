# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/worker.py
# Compiled at: 2019-03-20 04:11:58
# Size of source mod 2**32: 976 bytes
from .account import Account
from .blockchainobject import BlockchainObject
from .instance import BlockchainInstance
from graphenecommon.worker import Worker as GrapheneWorker, Workers as GrapheneWorkers

@BlockchainInstance.inject
class Worker(GrapheneWorker):
    __doc__ = ' Read data about a worker in the chain\n\n        :param str id: id of the worker\n        :param dexstore blockchain_instance: DexStore() instance to use when\n            accesing a RPC\n\n    '

    def define_classes(self):
        self.account_class = Account
        self.type_id = 14


@BlockchainInstance.inject
class Workers(GrapheneWorkers):
    __doc__ = ' Obtain a list of workers for an account\n\n        :param str account_name/id: Name/id of the account (optional)\n        :param dexstore blockchain_instance: DexStore() instance to use when\n            accesing a RPC\n    '

    def define_classes(self):
        self.account_class = Account
        self.worker_class = Worker