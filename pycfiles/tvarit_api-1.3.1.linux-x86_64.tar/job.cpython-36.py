# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/narendra/.pyenv/versions/aws/lib/python3.6/site-packages/tvarit_api/resources/job.py
# Compiled at: 2019-09-30 09:24:29
# Size of source mod 2**32: 714 bytes
from .base import Base

class Job(Base):

    def __init__(self, api):
        super(Job, self).__init__(api)
        self.api = api

    def run_job(self, job):
        endpoint = '/jobs'
        return self.api.POST(endpoint, json=job)

    def rerun_job(self, job_id):
        endpoint = '/{}/rerun'.format(job_id)
        return self.api.POST(endpoint)

    def abort_job(self, job_id):
        endpoint = '/{}/abort'.format(job_id)
        return self.api.POST(endpoint)

    def job_status(self, job_id):
        endpoint = '/{}/status'.format(job_id)
        return self.api.POST(endpoint)

    def job_logs(self, job_id):
        endpoint = '/{}/logs'.format(job_id)
        return self.api.POST(endpoint)