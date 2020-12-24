# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nslbvserverstat.py
# Compiled at: 2015-12-01 16:20:42
from nsbaseresource import NSBaseResource

class NSLBVServerStat(NSBaseResource):

    def __init__(self, json_data=None):
        super(NSLBVServerStat, self).__init__()
        self.options = {'name': '', 
           'clearstats': '', 
           'sortby': '', 
           'sortorder': '', 
           'vsvrsurgecount': '', 
           'establishedconn': '', 
           'inactsvcs': '', 
           'vslbhealth': '', 
           'primaryipaddress': '', 
           'primaryport': '', 
           'type': '', 
           'state': '', 
           'actsvcs': '', 
           'tothits': '', 
           'hitsrate': '', 
           'totalrequests': '', 
           'requestsrate': '', 
           'totalresponses': '', 
           'responsesrate': '', 
           'totalrequestbytes': '', 
           'requestbytesrate': '', 
           'totalresponsebytes': '', 
           'responsebytesrate': '', 
           'totalpktsrecvd': '', 
           'pktsrecvdrate': '', 
           'totalpktssent': '', 
           'pktssentrate': '', 
           'curclntconnections': '', 
           'cursrvrconnections': '', 
           'surgecount': '', 
           'svcsurgecount': '', 
           'sothreshold': '', 
           'totspillovers': '', 
           'labelledconn': '', 
           'pushlabel': '', 
           'deferredreq': '', 
           'deferredreqrate': '', 
           'invalidrequestresponse': '', 
           'invalidrequestresponsedropped': ''}
        self.resourcetype = NSLBVServerStat.get_resourcetype()
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        return

    @staticmethod
    def get_resourcetype():
        return 'lbvserver'

    def set_name(self, name):
        self.options['name'] = name

    def get_name(self):
        return self.options['name']

    def set_clearstats(self, method):
        self.options['clearstats'] = method

    def get_clearstats(self):
        return self.options['clearstats']

    def set_sortby(self, sortby):
        self.options['sortby'] = sortby

    def get_sortby(self):
        return self.options['sortby']

    def get_primaryipaddress(self):
        return self.options['primaryipaddress']

    def get_primaryport(self):
        return self.options['primaryport']

    def get_type(self):
        return self.options['type']

    def get_state(self):
        return self.options['state']

    def get_primaryipaddress(self):
        return self.options['primaryipaddress']

    @staticmethod
    def get(nitro, lbvserver):
        """
        Use this api to fetch lbvserver's stat info of given name.
        """
        __lbvserver = NSLBVServerStat()
        __lbvserver.set_name(lbvserver.get_name())
        __lbvserver.get_resource(nitro, 'stat')
        return __lbvserver

    @staticmethod
    def get_all(nitro):
        """
        Use this api to fetch all lbvserver' stat info
        """
        __url = nitro.get_url('stat') + NSLBVServerStat.get_resourcetype()
        __json_lbvservers = nitro.get(__url).get_response_field(NSLBVServerStat.get_resourcetype())
        __lbvservers = []
        for json_lbvserver in __json_lbvservers:
            __lbvservers.append(NSLBVServerStat(json_lbvserver))

        return __lbvservers