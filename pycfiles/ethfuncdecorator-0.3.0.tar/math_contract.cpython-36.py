# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/utils/module_testing/math_contract.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 2885 bytes
MATH_BYTECODE = '606060405261022e806100126000396000f360606040523615610074576000357c01000000000000000000000000000000000000000000000000000000009004806316216f391461007657806361bc221a146100995780637cf5dab0146100bc578063a5f3c23b146100e8578063d09de08a1461011d578063dcf537b11461014057610074565b005b610083600480505061016c565b6040518082815260200191505060405180910390f35b6100a6600480505061017f565b6040518082815260200191505060405180910390f35b6100d26004808035906020019091905050610188565b6040518082815260200191505060405180910390f35b61010760048080359060200190919080359060200190919050506101ea565b6040518082815260200191505060405180910390f35b61012a6004805050610201565b6040518082815260200191505060405180910390f35b6101566004808035906020019091905050610217565b6040518082815260200191505060405180910390f35b6000600d9050805080905061017c565b90565b60006000505481565b6000816000600082828250540192505081905550600060005054905080507f3496c3ede4ec3ab3686712aa1c238593ea6a42df83f98a5ec7df9834cfa577c5816040518082815260200191505060405180910390a18090506101e5565b919050565b6000818301905080508090506101fb565b92915050565b600061020d6001610188565b9050610214565b90565b60006007820290508050809050610229565b91905056'
MATH_ABI = [
 {'constant':False, 
  'inputs':[],  'name':'return13', 
  'outputs':[
   {'name':'result', 
    'type':'int256'}], 
  'type':'function'},
 {'constant':True, 
  'inputs':[],  'name':'counter', 
  'outputs':[
   {'name':'', 
    'type':'uint256'}], 
  'type':'function'},
 {'constant':False, 
  'inputs':[
   {'name':'amt', 
    'type':'uint256'}], 
  'name':'increment', 
  'outputs':[
   {'name':'result', 
    'type':'uint256'}], 
  'type':'function'},
 {'constant':False, 
  'inputs':[
   {'name':'a', 
    'type':'int256'},
   {'name':'b', 
    'type':'int256'}], 
  'name':'add', 
  'outputs':[
   {'name':'result', 
    'type':'int256'}], 
  'type':'function'},
 {'constant':False, 
  'inputs':[],  'name':'increment', 
  'outputs':[
   {'name':'', 
    'type':'uint256'}], 
  'type':'function'},
 {'constant':False, 
  'inputs':[
   {'name':'a', 
    'type':'int256'}], 
  'name':'multiply7', 
  'outputs':[
   {'name':'result', 
    'type':'int256'}], 
  'type':'function'},
 {'anonymous':False, 
  'inputs':[
   {'indexed':False, 
    'name':'value',  'type':'uint256'}], 
  'name':'Increased', 
  'type':'event'}]