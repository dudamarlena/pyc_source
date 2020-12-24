# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nsrunningconfig.py
# Compiled at: 2015-03-31 07:07:35
from nsbaseresource import NSBaseResource
__author__ = 'Aleksandar Topuzovic'

class NSRunningConfig(NSBaseResource):

    def __init__(self, json_data=None):
        """
        Supplied with json_data the object can be pre-filled
        """
        super(NSRunningConfig, self).__init__()
        self.options = {'withdefaults': '', 'response': ''}
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        self.resourcetype = NSRunningConfig.get_resourcetype()
        return

    def get_withdefaults(self):
        return self.options['withdefaults']

    def set_withdefaults(self, withdefaults):
        self.options['withdefaults'] = withdefaults

    def get_response(self):
        return self.options['response']

    @staticmethod
    def get_resourcetype():
        return 'nsrunningconfig'

    @staticmethod
    def get(nitro):
        __url = nitro.get_url() + NSRunningConfig.get_resourcetype()
        __json_nsversion = nitro.get(__url).get_response_field(NSRunningConfig.get_resourcetype())
        return NSRunningConfig(__json_nsversion)