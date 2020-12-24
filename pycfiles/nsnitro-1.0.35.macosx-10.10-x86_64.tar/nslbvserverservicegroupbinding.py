# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nslbvserverservicegroupbinding.py
# Compiled at: 2014-04-24 09:01:10
from nsbaseresource import NSBaseResource
__author__ = 'ptravers'

class NSLBVServerServiceGroupBinding(NSBaseResource):

    def __init__(self, json_data=None):
        """
        Supplied with json_data the object can be pre-filled
        """
        super(NSLBVServerServiceGroupBinding, self).__init__()
        self.options = {'weight': '', 
           'name': '', 
           'servicename': '', 
           'servicegroupname': ''}
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        self.resourcetype = NSLBVServerServiceGroupBinding.get_resourcetype()
        return

    @staticmethod
    def get_resourcetype():
        return 'lbvserver_servicegroup_binding'

    def set_servicename(self, servicename):
        """
        The service name bound to the selected load balancing virtual server.
        Default value: 0
        Minimum length =  1.
        """
        self.options['servicename'] = servicename

    def get_servicename(self):
        """
        The service name bound to the selected load balancing virtual server.
        Default value: 0
        Minimum length =  1.
        """
        return self.options['servicename']

    def set_weight(self, weight):
        """
        The weight for the specified service.
        Default value: 0
        Minimum value =  1
        Maximum value =  100
        """
        self.options['weight'] = weight

    def get_weight(self):
        """
        The weight for the specified service.
        Default value: 0
        Minimum value =  1
        Maximum value =  100
        """
        return self.options['weight']

    def set_name(self, name):
        """
        The virtual server name to which the service is bound.
        Default value: 0
        Minimum length =  1.
        """
        self.options['name'] = name

    def get_name(self):
        """
        The virtual server name to which the service is bound.
        Default value: 0
        Minimum length =  1.
        """
        return self.options['name']

    def set_servicegroupname(self, servicegroupname):
        """
        The name of the service group that is bound.
        Default value: 0
        Minimum length =  1.
        """
        self.options['servicegroupname'] = servicegroupname

    def get_servicegroupname(self):
        """
        The name of the service group that is bound.
        Default value: 0
        Minimum length =  1.
        """
        return self.options['servicegroupname']

    @staticmethod
    def get(nitro, vserver_servicegroup_binding):
        """
        Use this API to fetch configured vserver_servicegroup_binding resources of a given name.
        """
        __url = nitro.get_url() + NSLBVServerServiceGroupBinding.get_resourcetype() + '/' + vserver_servicegroup_binding.get_name()
        __json_services = nitro.get(__url).get_response_field(NSLBVServerServiceGroupBinding.get_resourcetype())
        __services = []
        for json_service in __json_services:
            __services.append(NSLBVServerServiceGroupBinding(json_service))

        return __services

    @staticmethod
    def add(nitro, vserver_servicegroup_binding):
        """
        Use this API to add vserver_servicegroup_binding.
        """
        __vserver_servicegroup_binding = NSLBVServerServiceGroupBinding()
        __vserver_servicegroup_binding.set_name(vserver_servicegroup_binding.get_name())
        __vserver_servicegroup_binding.set_servicename(vserver_servicegroup_binding.get_servicename())
        __vserver_servicegroup_binding.set_weight(vserver_servicegroup_binding.get_weight())
        __vserver_servicegroup_binding.set_servicegroupname(vserver_servicegroup_binding.get_servicegroupname())
        return __vserver_servicegroup_binding.update_resource(nitro)

    @staticmethod
    def delete(nitro, vserver_servicegroup_binding):
        """
        Use this API to delete vserver_servicegroup_binding of a given name.
        """
        __vserver_servicegroup_binding = NSLBVServerServiceGroupBinding()
        __vserver_servicegroup_binding.set_name(vserver_servicegroup_binding.get_name())
        __vserver_servicegroup_binding.set_servicename(vserver_servicegroup_binding.get_servicename())
        __vserver_servicegroup_binding.set_servicegroupname(vserver_servicegroup_binding.get_servicegroupname())
        nsresponse = __vserver_servicegroup_binding.delete_resource(nitro)
        return nsresponse