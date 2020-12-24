# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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