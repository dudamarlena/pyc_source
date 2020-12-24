# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/reviewday/smokestack.py
# Compiled at: 2011-11-19 21:45:46
import json, httplib2

class SmokeStack(object):

    def __init__(self, url):
        self._jobs = None
        self.url = url
        return

    def jobs(self, git_hash=None):
        if not self._jobs:
            h = httplib2.Http()
            resp, content = h.request(self.url, 'GET')
            self._jobs = json.loads(content)
        if git_hash:
            jobs_with_hash = []
            for job in self._jobs:
                for job_type, data in job.iteritems():
                    if data['nova_revision'] == git_hash or data['glance_revision'] == git_hash or data['keystone_revision'] == git_hash:
                        jobs_with_hash.append(job)

            return jobs_with_hash
        return self._jobs