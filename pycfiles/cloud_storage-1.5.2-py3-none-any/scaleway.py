# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/silver/Projects/Public/cloud_ssh_config/cloud_ssh_config/cloud/scaleway.py
# Compiled at: 2018-11-01 09:06:46
from scaleway.apis import ComputeAPI

class cloud:

    def __init__(self, token, region='ams1'):
        self.region = region
        self.token = token

    def get_hosts(self):
        api = ComputeAPI(region=self.region, auth_token=self.token)
        servers = api.query().servers.get()
        hosts = {}
        for host in servers['servers']:
            if host['state'] == 'running':
                if host['public']:
                    hosts.update({host['hostname']: host['public_ip']['address']})

        return hosts