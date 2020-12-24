# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nsservicegroupstat.py
# Compiled at: 2015-12-01 16:20:42
from nsbaseresource import NSBaseResource

class NSServiceGroupStat(NSBaseResource):

    def __init__(self, json_data=None):
        super(NSServiceGroupStat, self).__init__()
        self.options = {'servicegroupname': '', 
           'clearstats': '', 
           'state': '', 
           'servicetype': ''}
        self.resourcetype = NSServiceGroupStat.get_resourcetype()
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        return

    @staticmethod
    def get_resourcetype():
        return 'servicegroup'

    def set_servicegroupname(self, name):
        self.options['servicegroupname'] = name

    def get_servicegroupname(self):
        return self.options['servicegroupname']

    def get_state(self):
        return self.options['state']

    def get_servicetype(self):
        return self.options['servicetype']

    @staticmethod
    def get(nitro, servicegroupst):
        __servicegroupst = NSServiceGroupStat()
        __servicegroupst.set_servicegroupname(servicegroupst.get_servicegroupname())
        __servicegroupst.get_resource(nitro, 'stat', __servicegroupst.get_servicegroupname())
        return __servicegroupst

    @staticmethod
    def get_all(nitro):
        __url = nitro.get_url('stat') + NSServiceGroupStat.get_resourcetype()
        __json_sgstat = nitro.get(__url).get_response_field(NSServiceGroupStat.get_resourcetype())
        __sgstats = []
        for json_sgstat in __json_sgstat:
            __sgstats.append(NSServiceGroupStat(json_sgstat))

        return __sgstats