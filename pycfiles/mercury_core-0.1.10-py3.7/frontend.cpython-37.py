# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/common/clients/rpc/frontend.py
# Compiled at: 2018-01-29 12:10:54
# Size of source mod 2**32: 2752 bytes
import logging
from mercury.common.clients.router_req_client import RouterReqClient
log = logging.getLogger(__name__)

class RPCFrontEndClient(RouterReqClient):
    __doc__ = 'Client for RPC Front End'
    service_name = 'RPC frontend'

    def get_job(self, job_id, projection=None):
        """

        :param job_id:
        :param projection:
        :return:
        """
        payload = {'endpoint':'get_job', 
         'args':[
          job_id], 
         'kwargs':{'projection': projection}}
        return self.transceiver(payload)

    def get_job_status(self, job_id):
        """

        :param job_id:
        :return:
        """
        payload = {'endpoint':'get_job_status', 
         'args':[
          job_id]}
        return self.transceiver(payload)

    def get_job_tasks(self, job_id, projection=None):
        """

        :param job_id:
        :param projection:
        :return:
        """
        payload = {'endpoint':'get_job_tasks', 
         'args':[
          job_id], 
         'kwargs':{'projection': projection}}
        return self.transceiver(payload)

    def get_task(self, task_id):
        """

        :param task_id:
        :return:
        """
        payload = {'endpoint':'get_task', 
         'args':[
          task_id]}
        return self.transceiver(payload)

    def get_jobs(self, projection=None):
        """

        :param projection:
        :return:
        """
        payload = {'endpoint':'get_jobs', 
         'kwargs':{'projection': projection}}
        return self.transceiver(payload)

    def create_job(self, query, instruction):
        """

        :param query:
        :param instruction:
        :return:
        """
        payload = {'endpoint':'create_job', 
         'args':[
          query, instruction]}
        log.debug('Dispatching query {query} : {instruction}')
        return self.transceiver(payload)