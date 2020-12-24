# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/silver/Projects/Public/cloud_ssh_config/cloud_ssh_config/cloud/do.py
# Compiled at: 2018-10-24 16:18:43
import digitalocean

class cloud:

    def __init__(self, token):
        self.manager = digitalocean.Manager(token=token)

    def get_hosts(self):
        my_droplets = self.manager.get_all_droplets()
        hosts = {}
        for host in my_droplets:
            if host.ip_address:
                hosts.update({host.name: host.ip_address})

        return hosts