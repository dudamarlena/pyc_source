# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/proposal.py
# Compiled at: 2019-03-20 04:11:58
# Size of source mod 2**32: 933 bytes
from .account import Account
from .instance import BlockchainInstance
from graphenecommon.proposal import Proposal as GrapheneProposal, Proposals as GrapheneProposals

@BlockchainInstance.inject
class Proposal(GrapheneProposal):
    __doc__ = ' Read data about a Proposal Balance in the chain\n\n        :param str id: Id of the proposal\n        :param dexstore blockchain_instance: DexStore() instance to use when accesing a RPC\n\n    '

    def define_classes(self):
        self.type_id = 10
        self.account_class = Account


@BlockchainInstance.inject
class Proposals(GrapheneProposals):
    __doc__ = ' Obtain a list of pending proposals for an account\n\n        :param str account: Account name\n        :param dexstore blockchain_instance: DexStore() instance to use when accesing a RPC\n    '

    def define_classes(self):
        self.account_class = Account
        self.proposal_class = Proposal