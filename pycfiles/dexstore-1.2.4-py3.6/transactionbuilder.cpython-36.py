# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/transactionbuilder.py
# Compiled at: 2019-03-20 04:09:59
# Size of source mod 2**32: 1890 bytes
from graphenecommon.transactionbuilder import TransactionBuilder as GrapheneTransactionBuilder, ProposalBuilder as GrapheneProposalBuilder
from dexstorebase import operations, transactions
from dexstorebase.account import PrivateKey, PublicKey
from dexstorebase.objects import Operation
from dexstorebase.signedtransactions import Signed_Transaction
from .amount import Amount
from .asset import Asset
from .account import Account
from .instance import BlockchainInstance

@BlockchainInstance.inject
class ProposalBuilder(GrapheneProposalBuilder):
    __doc__ = ' Proposal Builder allows us to construct an independent Proposal\n        that may later be added to an instance ot TransactionBuilder\n\n        :param str proposer: Account name of the proposing user\n        :param int proposal_expiration: Number seconds until the proposal is\n            supposed to expire\n        :param int proposal_review: Number of seconds for review of the\n            proposal\n        :param .transactionbuilder.TransactionBuilder: Specify\n            your own instance of transaction builder (optional)\n        :param instance blockchain_instance: Blockchain instance\n    '

    def define_classes(self):
        self.operation_class = Operation
        self.operations = operations
        self.account_class = Account


@BlockchainInstance.inject
class TransactionBuilder(GrapheneTransactionBuilder):
    __doc__ = ' This class simplifies the creation of transactions by adding\n        operations and signers.\n    '

    def define_classes(self):
        self.account_class = Account
        self.asset_class = Asset
        self.operation_class = Operation
        self.operations = operations
        self.privatekey_class = PrivateKey
        self.publickey_class = PublicKey
        self.signed_transaction_class = Signed_Transaction
        self.amount_class = Amount