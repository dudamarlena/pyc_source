# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_sdk/http/rpc.py
# Compiled at: 2018-05-22 15:52:43
# Size of source mod 2**32: 1002 bytes
from mercury_sdk.http.base import InterfaceBase

class JobInterfaceBase(InterfaceBase):
    SERVICE_URI = 'api/rpc/jobs'

    def get(self, job_id='', params=None, extra_headers=None):
        """

        :param job_id:
        :param params:
        :param extra_headers:
        :return:
        """
        return super(JobInterfaceBase, self).get(item=job_id, params=params, extra_headers=extra_headers)

    def status(self, job_id):
        """

        :param job_id:
        :return:
        """
        return self.get('/{}/status'.format(job_id))

    def tasks(self, job_id):
        """

        :param job_id:
        :return:
        """
        return self.get('/{}/tasks'.format(job_id))

    def submit(self, query, instruction):
        """

        :param query:
        :param instruction:
        :return:
        """
        return self.post(item=None, data={'query':query, 
         'instruction':instruction})