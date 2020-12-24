# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/silver/Projects/Public/cloud_ssh_config/cloud_ssh_config/ssh_config/ssh_config.py
# Compiled at: 2018-10-24 08:01:39
import six

class config:

    def __init__(self, user='ubuntu', prefix='', key='~/.ssh/id_rsa'):
        self.user = user
        self.prefix = prefix
        self.key = key

    def get_config(self, hosts):
        for host, ip in six.iteritems(hosts):
            print 'Host ' + str(self.prefix) + host
            print '    HostName ' + ip
            print '    User ' + self.user
            print '    IdentityFile ' + self.key
            print ''

        return True