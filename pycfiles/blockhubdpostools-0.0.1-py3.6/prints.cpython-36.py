# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prints.py
# Compiled at: 2017-12-21 16:23:41
# Size of source mod 2**32: 1605 bytes
import dbtools, api
localnode = dbtools.ArkNode(user='postgres',
  password='Dwl1ml12_3#')
address_delegate = 'AZse3vk8s3QEX1bqijFb21aSBeoF6vqLYE'
delegate_pubkey = '0218b77efb312810c9a549e2cc658330fcc07f554d465673e08fa304fa59e67a0a'
normal_addres = 'AJwHyHAArNmzGfmDnsJenF857ATQevg8HY'
actions = localnode.get_events_vote_cluster(address_delegate)
share = localnode.tbw(address_delegate)[0]
for i in share:
    print(i, share[i])