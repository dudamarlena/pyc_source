# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nsgslbvservergslbservicebinding.py
# Compiled at: 2015-12-01 16:20:42
from nsbaseresource import NSBaseResource

class NSGSLBVServerGSLBServiceBinding(NSBaseResource):

    def __init__(self, json_data=None):
        """
        Supplied with json_data the object can be pre-filled
        """
        super(NSGSLBVServerGSLBServiceBinding, self).__init__()
        self.options = {'name': '', 
           'weight': '', 
           'servicename': '', 
           'domainname': '', 
           'cnameentry': '', 
           'gslbthreshold': '', 
           'port': '', 
           'iscname': '', 
           'curstate': '', 
           'preferredlocation': '', 
           'svreffgslbstate': '', 
           'dynamicconfwt': '', 
           'sitepersistence': '', 
           'thresholdvalue': '', 
           'servicetype': '', 
           'ipaddress': '', 
           'cumulativeweight': '', 
           '__count': ''}
        self.resourcetype = NSGSLBVServerGSLBServiceBinding.get_resourcetype()
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        return

    @staticmethod
    def get_resourcetype():
        return 'gslbvserver_gslbservice_binding'

    def set_name(self, name):
        """
        """
        self.options['name'] = name

    def get_name(self):
        """
        """
        return self.options['name']

    def get_ipaddress(self):
        """
        """
        return self.options['ipaddress']

    @staticmethod
    def get(nitro, gslbservice_binding):
        """
        Use this API to fetch csvserver resource of given name.
        """
        __gslbservice_binding = NSGSLBVServerGSLBServiceBinding()
        __gslbservice_binding.set_name(gslbservice_binding.get_name())
        __gslbservice_binding.get_resource(nitro)
        return __gslbservice_binding