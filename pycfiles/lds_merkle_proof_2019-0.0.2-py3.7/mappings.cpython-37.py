# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/lds_merkle_proof_2019/mappings.py
# Compiled at: 2020-01-23 11:57:46
# Size of source mod 2**32: 708 bytes
root = {'merkleRoot':0,  'targetHash':1, 
 'anchors':2, 
 'path':3}
path = {'left':0, 
 'right':1}
chain = {'btc':{'id':0, 
  'networks':{'mainnet':1, 
   'regtest':2, 
   'testnet':3}}, 
 'eth':{'id':1, 
  'networks':{'mainnet':1, 
   'ropsten':3, 
   'rinkeby':4}}, 
 'mocknet':{'id': -1}}

def findChainById(id):
    for i, dic in chain.items():
        if chain[i]['id'] == id:
            return i

    return ''


def findNetworkById(blockchain, id):
    networks = chain[blockchain]['networks']
    for i, dic in networks.items():
        if networks[i] == id:
            return i

    return ''