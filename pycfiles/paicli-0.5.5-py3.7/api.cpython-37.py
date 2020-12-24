# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paicli/api.py
# Compiled at: 2019-07-22 01:15:24
# Size of source mod 2**32: 3846 bytes
"""paicli: A CLI tool for PAI (Platform for AI).

Author: Sotetsu KOYAMADA
"""
import json, requests
from .utils import to_str

class API(object):
    __doc__ = 'API client for PAI\n\n    See: https://github.com/Microsoft/pai/blob/master/rest-server/README.md\n    '

    def __init__(self, config):
        self.config = config

    def post_token(self, username, password, expiration=500000):
        url = '{}/api/{}/token'.format(self.config.api_uri, self.config.api_version)
        headers = {'Content-type': 'application/json'}
        data = json.dumps({'username':username, 
         'password':password, 
         'expiration':expiration})
        res = requests.post(url, headers=headers, data=data)
        if res.ok:
            return to_str(res.content)
        res.raise_for_status()

    def put_user(self):
        pass

    def delete_user(self):
        """Admin only."""
        pass

    def put_user_username_virtualclusters(self):
        """Admin only."""
        pass

    def get_jobs(self, username=''):
        url = '{}/api/{}/jobs'.format(self.config.api_uri, self.config.api_version)
        params = {} if not username else {'username': username}
        res = requests.get(url=url, params=params)
        if res.ok:
            return to_str(res.content)
        res.raise_for_status()

    def get_user_username_jobs_jobname(self, username, jobname):
        url = '{}/api/{}/user/{}/jobs/{}'.format(self.config.api_uri, self.config.api_version, username, jobname)
        res = requests.get(url)
        if res.ok:
            return to_str(res.content)
        res.raise_for_status()

    def get_jobs_jobname_config(self, jobname):
        pass

    def get_user_username_jobs_jobname_ssh(self, username, jobname):
        url = '{}/api/{}/user/{}/jobs/{}/ssh'.format(self.config.api_uri, self.config.api_version, username, jobname)
        res = requests.get(url)
        if res.ok:
            return to_str(res.content)
        res.raise_for_status()

    def post_user_username_jobs(self, username, job_config_json):
        url = '{}/api/{}/user/{}/jobs'.format(self.config.api_uri, self.config.api_version, username)
        headers = self._headers_with_auth()
        res = requests.post(url, headers=headers, data=job_config_json)
        if res.ok:
            return to_str(res.content)
        res.raise_for_status()

    def get_user_username_jobs_jobname_ssh(self, username, jobname):
        url = '{}/api/{}/user/{}/jobs/{}/ssh'.format(self.config.api_uri, self.config.api_version, username, jobname)
        res = requests.get(url)
        if res.ok:
            return to_str(res.content)
        res.raise_for_status()

    def put_user_username_jobs_jobname_executiontype(self, username, jobname, value):
        url = '{}/api/{}/user/{}/jobs/{}/executionType'.format(self.config.api_uri, self.config.api_version, username, jobname)
        headers = self._headers_with_auth()
        data = json.dumps({'value': value})
        res = requests.put(url, headers=headers, data=data)
        if res.ok:
            return to_str(res.content)
        res.raise_for_status()

    def get_virtualclusters(self):
        pass

    def get_virtualclusters_vcname(self, vcname):
        pass

    def _headers_with_auth(self):
        self.config.load_access_token()
        headers = {'Authorization':'Bearer {}'.format(self.config.access_token), 
         'Content-type':'application/json'}
        return headers