# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/pykovi/glue_mock.py
# Compiled at: 2019-11-14 07:26:49
# Size of source mod 2**32: 875 bytes
import pykovi as pk, awswrangler as aw
from typing import Dict, Callable, Any
from pykovi.glue_jobs import GlueJobItem
import boto3

class GlueMock(aw.Glue):

    def __init__(self, session, mocked_jobs: Dict[(str, Callable[(..., Any)])]={}):
        self._session = session
        self._mocked_jobs = mocked_jobs

    @property
    def mocked_jobs(self):
        return self._mocked_jobs

    @mocked_jobs.setter
    def mocked_jobs(self, value):
        self._mocked_jobs = value

    def start_job_run(self, job_name: str, job_args: Dict[(str, Any)]={}, job_parameters: Dict[(str, Any)]={}):
        target_job = self.mocked_jobs.get(job_name)
        if target_job != None:
            return target_job(job_args=job_args, job_parameters=job_parameters)

    def create_job(self, glue_job_item: GlueJobItem):
        return {}