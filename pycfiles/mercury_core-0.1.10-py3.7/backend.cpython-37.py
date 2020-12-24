# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/common/clients/rpc/backend.py
# Compiled at: 2018-01-29 12:10:54
# Size of source mod 2**32: 1969 bytes
import logging
from mercury.common.clients.router_req_client import RouterReqClient
log = logging.getLogger(__name__)

class BackEndClient(RouterReqClient):
    service_name = 'RPC backend'

    def register(self, device_info, agent_info):
        """

        :param device_info:
        :param agent_info:
        :return:
        """
        _payload = {'endpoint':'register', 
         'args':[
          device_info, agent_info]}
        return self.transceiver(_payload)

    def update(self, mercury_id, update_data):
        """

        :param mercury_id:
        :param update_data:
        :return:
        """
        _payload = {'endpoint':'update', 
         'args':[
          mercury_id, update_data]}
        return self.transceiver(_payload)

    def complete_task(self, return_data):
        """
        :param return_data:
        :return:
        """
        _payload = {'endpoint':'complete_task', 
         'args':[
          return_data]}
        return self.transceiver(_payload)

    def update_task(self, update_data):
        """
        :param update_data:
        :return:
        """
        _payload = {'endpoint':'update_task', 
         'args':[
          update_data]}
        return self.transceiver(_payload)