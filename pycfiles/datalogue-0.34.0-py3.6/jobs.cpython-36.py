# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/clients/jobs.py
# Compiled at: 2020-04-24 18:45:43
# Size of source mod 2**32: 1959 bytes
from typing import List, Union
from datalogue.clients.http import _HttpClient, HttpMethod
from datalogue.models.job import Job, _job_from_payload
from datalogue.dtl_utils import _parse_list
from datalogue.errors import DtlError
from uuid import UUID

class _JobsClient:
    __doc__ = '\n    Client to interact with the Scheduled pipelines\n    '

    def __init__(self, http_client: _HttpClient):
        self.http_client = http_client
        self.service_uri = '/scout'

    def list(self, page: int=1, item_per_page: int=25) -> Union[(DtlError, List[Job])]:
        """
        List the scheduled jobs

        :param page: page to be retrieved
        :param item_per_page: number of jobs to be put in a page
        :return: Returns a List of all the available Datastores or an error message as a string
        """
        res = self.http_client.make_authed_request(self.service_uri + f"/jobs?page={page}&size={item_per_page}", HttpMethod.GET)
        if isinstance(res, DtlError):
            return res
        else:
            return _parse_list(_job_from_payload)(res)

    def cancel(self, job_id: UUID) -> Union[(DtlError, Job)]:
        """"
        Cancel a Job given job_id.

        :param job_id:
        :return: Returns the Job object canceled or an error
        """
        res = self.http_client.make_authed_request(self.service_uri + f"/jobs/{str(job_id)}/cancel", HttpMethod.POST)
        if isinstance(res, DtlError):
            return res
        else:
            return _job_from_payload(res)

    def get(self, job_id: UUID) -> Union[(DtlError, Job)]:
        """"
        Get a Job given job_id.

        :param job_id:
        :return: Returns the Job object or an error
        """
        res = self.http_client.make_authed_request(self.service_uri + f"/jobs/{str(job_id)}/status", HttpMethod.GET)
        if isinstance(res, DtlError):
            return res
        else:
            return _job_from_payload(res)