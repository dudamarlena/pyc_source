# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nsservicegroupmemberstat.py
# Compiled at: 2015-12-01 16:20:42
from nsbaseresource import NSBaseResource

class NSServiceGroupMemberStat(NSBaseResource):

    def __init__(self, json_data=None):
        super(NSServiceGroupMemberStat, self).__init__()
        self.options = {'servicegroupname': '', 
           'ip': '', 
           'servername': '', 
           'port': '', 
           'clearstats': '', 
           'avgsvrttfb': '', 
           'primaryipaddress': '', 
           'primaryport': '', 
           'servicetype': '', 
           'state': '', 
           'totalrequests': '', 
           'requestsrate': '', 
           'totalresponses': '', 
           'responsesrate': '', 
           'totalrequestbytes': '', 
           'requestbytesrate': '', 
           'totalresponsebytes': '', 
           'responsebytesrate': '', 
           'curclntconnections': '', 
           'surgecount': '', 
           'cursrvrconnections': '', 
           'svrestablishedconn': '', 
           'curreusepool': '', 
           'maxclients': ''}
        self.resourcetype = NSServiceGroupMemberStat.get_resourcetype()
        if json_data is not None:
            for key in json_data.keys():
                if self.options.has_key(key):
                    self.options[key] = json_data[key]

        return

    @staticmethod
    def get_resourcetype():
        return 'servicegroupmember'

    def set_servicegroupname(self, name):
        self.options['servicegroupname'] = name

    def get_servicegroupname(self):
        return self.options['servicegroupname']

    def set_ip(self, ip):
        self.options['ip'] = ip

    def get_ip(self):
        return self.options['ip']

    def set_servername(self, name):
        self.options['servername'] = name

    def get_servername(self):
        return self.options['servername']

    def set_port(self, port):
        self.options['port'] = port

    def get_port(self):
        return self.options['port']

    def get_primaryipaddress(self):
        return self.options['primaryipaddress']

    def get_primaryport(self):
        return self.options['primaryport']

    def get_state(self):
        return self.options['state']

    def get_cursrvrconnections(self):
        return self.options['cursrvrconnections']

    @staticmethod
    def get(nitro, sgmember):
        __sgmember = NSServiceGroupMemberStat()
        __sgmember.set_servicegroupname(sgmember.get_servicegroupname())
        __sgmember.set_ip(sgmember.get_ip())
        __sgmember.set_servername(sgmember.get_servername())
        __sgmember.set_port(sgmember.get_port())
        __url = nitro.get_url('stat') + NSServiceGroupMemberStat.get_resourcetype() + __sgmember.get_stat_args()
        __json_sgmemberst = nitro.get(__url).get_response_field(NSServiceGroupMemberStat.get_resourcetype())
        __sgmembers = []
        for json_sgmember in __json_sgmemberst:
            __sgmembers.append(NSServiceGroupMemberStat(json_sgmember))

        return __sgmembers