# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/backend/rpc_client.py
# Compiled at: 2018-11-30 15:05:10
# Size of source mod 2**32: 1463 bytes
from mercury.common.clients.router_req_client import RouterReqClient
from mercury.common.asyncio.clients.async_router_req_client import AsyncRouterReqClient

class RPCClient(RouterReqClient):
    service_name = 'RPC Service'

    def update_task(self, update_data):
        """

        :param update_data:
        :return:
        """
        return self.transceiver({'endpoint':'update_task', 
         'args':[
          update_data]})

    def complete_task(self, result_data):
        """
        :param result_data:
        :return:
        """
        return self.transceiver({'endpoint':'complete_task', 
         'args':[
          result_data]})


class AsyncRPCClient(AsyncRouterReqClient):
    service_name = 'RPC client'

    async def update_task(self, update_data):
        """

        :param update_data:
        :return:
        """
        return await self.transceiver({'endpoint':'update_task', 
         'args':[
          update_data]})

    async def complete_task(self, result_data):
        """
        :param result_data:
        :return:
        """
        return await self.transceiver({'endpoint':'complete_task', 
         'args':[
          result_data]})

    async def get_active_tasks_by_mercury_id(self, mercury_id):
        return await self.transceiver({'endpoint':'get_active_tasks_by_mercury_id', 
         'args':[
          mercury_id]})