# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nscsvserverstat.py
# Compiled at: 2015-12-01 16:20:42
from nsbaseresource import NSBaseResource

class NSCSVServerStat(NSBaseResource):

    def __init__(self, json_data=None):
        super(NSCSVServerStat, self).__init__()
        self.options = {'name': '', 
           'clearstats': '', 
           'establishedconn': '', 
           'primaryipaddress': '', 
           'primaryport': '', 
           'type': '', 
           'state': '', 
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
           'sothreshold': '', 
           'totspillovers': '', 
           'labelledconn': '', 
           'pushlabel': '', 
           'deferredreq': '', 
           'deferredreqrate': '', 
           'invalidrequestresponse': '', 
           'invalidrequestresponsedropped': ''}
        self.resourcetype = NSCSVServerStat.get_resourcetype()
        if json_data is not None:
            for key in json_data.keys():
                if self.options.has_key(key):
                    self.options[key] = json_data[key]

        return

    @staticmethod
    def get_resourcetype():
        return 'csvserver'

    def set_name(self, name):
        self.options['name'] = name

    def get_name(self):
        return self.options['name']

    def get_state(self):
        return self.options['state']

    def get_primaryipaddress(self):
        return self.options['primaryipaddress']

    @staticmethod
    def get(nitro, csvserver):
        __csvs = NSCSVServerStat()
        __csvs.set_name(csvserver.get_name())
        __csvs.get_resource(nitro, urltype='stat')
        return __csvs

    @staticmethod
    def get_all(nitro):
        __url = nitro.get_url('stat') + NSCSVServerStat.get_resourcetype()
        __json_csvs = nitro.get(__url).get_response_field(NSCSVServerStat.get_resourcetype())
        __csvs = []
        for __json_vs in __json_csvs:
            __csvs.append(NSCSVServerStat(__json_vs))

        return __csvs