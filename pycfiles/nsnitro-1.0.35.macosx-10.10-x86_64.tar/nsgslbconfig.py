# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nsgslbconfig.py
# Compiled at: 2015-12-01 16:20:42
from nsbaseresource import NSBaseResource

class NSGSLBConfig(NSBaseResource):

    def __init__(self, json_data=None):
        """
        Supplied with json_data the object can be pre-filled
        """
        super(NSGSLBConfig, self).__init__()
        self.options = {'preview': '', 
           'debug': '', 
           'forcesync': '', 
           'nowarn': '', 
           'saveconfig': '', 
           'command': ''}
        self.resourcetype = NSGSLBConfig.get_resourcetype()
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        return

    @staticmethod
    def get_resourcetype():
        return 'gslbconfig'

    @staticmethod
    def sync(nitro):
        """
        Use this API to sync all gslb config.
        """
        pay_load = {'nowarn': True, 'saveconfig': True}
        __gslbconfi = NSGSLBConfig(pay_load)
        __gslbconfi.set_action('sync')
        response = __gslbconfi.add_resource(nitro)
        return response