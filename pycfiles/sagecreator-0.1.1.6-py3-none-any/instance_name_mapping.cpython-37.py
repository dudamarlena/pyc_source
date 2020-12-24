# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rjuga255/sagecreator/sagebase/plugins/lookups/instance_name_mapping.py
# Compiled at: 2019-03-09 21:19:41
# Size of source mod 2**32: 1518 bytes
from ansible.plugins.lookup import LookupBase
import boto.ec2

class LookupModule(LookupBase):

    def __init__(self, loader=None, templar=None, **kwargs):
        (super(LookupModule, self).__init__)(loader, templar, **kwargs)
        self.conn = boto.ec2.connect_to_region('us-east-1')

    def run(self, terms, variables=None, **kwargs):
        env = kwargs.get('env')
        owner = kwargs.get('owner')
        service = kwargs.get('service')
        instances = kwargs.get('instances')
        reservations = self.conn.get_all_instances(filters={'tag:Environment':env,  'tag:Owner':owner,  'tag:Service':service})
        counter = max([self.get_num_from_tag(i.tags['Name']) for r in reservations if 'Name' in i.tags if '-' in i.tags['Name'] if i.state in ('running',
                                                                                                                                               'pending',
                                                                                                                                               'stopped') for i in r if '-' in i.tags['Name'] if i.state in ('running',
                                                                                                                                                                                                             'pending',
                                                                                                                                                                                                             'stopped')] or [0])
        ret_val = []
        counter = counter + 1
        for instance in instances:
            ret_val.append(dict(id=(instance['id']), name=('{}-{}-{:02d}-{}'.format(owner, service, counter, env)),
              private_ip=(instance['private_ip']),
              public_dns_name=(instance['public_dns_name']),
              region=(instance['region'])))
            counter = counter + 1

        return ret_val

    def get_num_from_tag(self, str):
        if str:
            val = str.split('-')[(-2)]
            if val.isdigit():
                return int(val)
        return 0