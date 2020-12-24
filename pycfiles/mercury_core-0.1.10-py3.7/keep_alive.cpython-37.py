# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/common/adhoc/keep_alive.py
# Compiled at: 2018-02-08 17:03:50
# Size of source mod 2**32: 186 bytes
from mercury.common.clients.router_req_client import RouterReqClient
c = RouterReqClient('tcp://localhost:9090')
print(c.transceiver({'_protocol_message': 'keep_alive'}))
input('=>')