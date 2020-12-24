# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/etheno/genesis.py
# Compiled at: 2019-06-27 23:49:12
# Size of source mod 2**32: 4048 bytes
from web3.auto import w3
from .utils import format_hex_address

class Account(object):

    def __init__(self, address, balance=None, private_key=None):
        self._address = address
        self.balance = balance
        self._private_key = private_key

    @property
    def address(self):
        return self._address

    @property
    def private_key(self):
        return self._private_key


def make_genesis(network_id=111550642089583, difficulty=20, gas_limit=200000000000, accounts=None, byzantium_block=0, dao_fork_block=0, homestead_block=0, eip150_block=0, eip155_block=0, eip158_block=0, constantinople_block=None):
    if accounts:
        alloc = {format_hex_address(acct.address):{'balance':'%d' % acct.balance,  'privateKey':format_hex_address(acct.private_key)} for acct in accounts}
    else:
        alloc = {}
    ret = {'config':{'chainId':network_id,  'byzantiumBlock':byzantium_block, 
      'daoForkBlock':dao_fork_block, 
      'homesteadBlock':homestead_block, 
      'eip150Block':eip150_block, 
      'eip155Block':eip155_block, 
      'eip158Block':eip158_block}, 
     'difficulty':'%d' % difficulty, 
     'gasLimit':'%d' % gas_limit, 
     'alloc':alloc}
    if constantinople_block is not None:
        ret['config']['constantinopleBlock'] = constantinople_block
    return ret


def geth_to_parity(genesis):
    """Converts a Geth style genesis to Parity style"""
    ret = {'name':'etheno', 
     'engine':{'instantSeal': None}, 
     'genesis':{'seal':{'generic': '0x0'}, 
      'difficulty':'0x%s' % genesis['difficulty'], 
      'gasLimit':'0x%s' % genesis['gasLimit'], 
      'author':list(genesis['alloc'])[-1]}, 
     'params':{'networkID':'0x%x' % genesis['config']['chainId'], 
      'maximumExtraDataSize':'0x20', 
      'minGasLimit':'0x%s' % genesis['gasLimit'], 
      'gasLimitBoundDivisor':'1', 
      'eip150Transition':'0x%x' % genesis['config']['eip150Block'], 
      'eip160Transition':'0x0', 
      'eip161abcTransition':'0x0', 
      'eip161dTransition':'0x0', 
      'eip155Transition':'0x%x' % genesis['config']['eip155Block'], 
      'eip98Transition':'0x7fffffffffffff', 
      'maxCodeSize':24576, 
      'maxCodeSizeTransition':'0x0', 
      'eip140Transition':'0x0', 
      'eip211Transition':'0x0', 
      'eip214Transition':'0x0', 
      'eip658Transition':'0x0', 
      'wasmActivationTransition':'0x0'}, 
     'accounts':dict(genesis['alloc'])}
    if 'constantinopleBlock' in genesis['config']:
        block = '0x%x' % genesis['config']['constantinopleBlock']
        ret['params']['eip145Transition'] = block
        ret['params']['eip1014Transition'] = block
        ret['params']['eip1052Transition'] = block
    return ret


def make_accounts(num_accounts, default_balance=None):
    ret = []
    for i in range(num_accounts):
        acct = w3.eth.account.create()
        ret.append(Account(address=(int(acct.address, 16)), private_key=(int(acct.privateKey.hex(), 16)), balance=default_balance))

    return ret