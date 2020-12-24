# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nsversion.py
# Compiled at: 2014-04-24 09:01:10
from nsbaseresource import NSBaseResource
__author__ = 'ivanxx@gmail.com'

class NSVersion(NSBaseResource):

    def __init__(self, json_data=None):
        """
        Supplied with json_data the object can be pre-filled
        """
        super(NSVersion, self).__init__()
        self.options = {'version': '', 'mode': ''}
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        self.resourcetype = NSVersion.get_resourcetype()
        return

    def get_version(self):
        return self.options['version']

    def get_mode(self):
        return self.options['mode']

    @staticmethod
    def get_resourcetype():
        return 'nsversion'

    @staticmethod
    def get(nitro):
        __url = nitro.get_url() + NSVersion.get_resourcetype()
        __json_nsversion = nitro.get(__url).get_response_field(NSVersion.get_resourcetype())
        return NSVersion(__json_nsversion)