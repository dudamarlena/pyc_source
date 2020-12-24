# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/common/clients/rpc/queue.py
# Compiled at: 2018-01-29 12:10:54
# Size of source mod 2**32: 442 bytes
import logging
from mercury.common.clients.router_req_client import RouterReqClient
log = logging.getLogger(__name__)

class QueueServiceClient(RouterReqClient):
    service_name = 'RPC Queue Service'

    def enqueue_task(self, task):
        """

        :param task:
        :return:
        """
        _payload = {'endpoint':'enqueue_task', 
         'args':[
          task]}
        return self.transceiver(_payload)