# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nshostname.py
# Compiled at: 2015-03-31 07:07:35
from nsbaseresource import NSBaseResource
__author__ = 'Aleksandar Topuzovic'

class NSHostname(NSBaseResource):

    def __init__(self, json_data=None):
        """
                Supplied with json_data the object can be pre-filled
                """
        super(NSHostname, self).__init__()
        self.options = {'hostname': ''}
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        self.resourcetype = NSHostname.get_resourcetype()
        return

    def get_hostname(self):
        return self.options['hostname']

    @staticmethod
    def get_resourcetype():
        return 'nshostname'

    @staticmethod
    def get(nitro):
        __url = nitro.get_url() + NSHostname.get_resourcetype()
        __json_nshostname = nitro.get(__url).get_response_field(NSHostname.get_resourcetype())
        if isinstance(__json_nshostname, list):
            return NSHostname(__json_nshostname[0])
        return NSHostname(__json_nshostname)