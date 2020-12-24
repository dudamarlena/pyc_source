# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nslbmonitorservicebinding.py
# Compiled at: 2014-04-24 09:01:10
from nsbaseresource import NSBaseResource
__author__ = 'vlazarenko'

class NSLBMonitorServiceBinding(NSBaseResource):

    def __init__(self, json_data=None):
        """
        Supplied with json_data the object can be pre-filled
        """
        super(NSLBMonitorServiceBinding, self).__init__()
        self.options = {'monitorname': '', 'servicename': '', 
           'dup_state': '', 
           'dup_weight': '', 
           'servicegroupname': '', 
           'state': '', 
           'weight': ''}
        self.resourcetype = NSLBMonitorServiceBinding.get_resourcetype()
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        return

    @staticmethod
    def get_resourcetype():
        return 'lbmonitor_service_binding'

    def set_monitorname(self, monitorname):
        self.options['monitorname'] = monitorname

    def get_monitorname(self):
        return self.options['monitorname']

    def set_servicename(self, servicename):
        self.options['servicename'] = servicename

    def get_servicename(self):
        return self.options['servicename']

    def set_dup_state(self, dup_state):
        self.options['dup_state'] = dup_state

    def get_dup_state(self):
        return self.options['dup_state']

    def set_dup_weight(self, dup_weight):
        self.options['dup_weight'] = dup_weight

    def get_dup_weight(self):
        return self.options['dup_weight']

    def set_servicegroupname(self, servicegroupname):
        self.options['servicegroupname'] = servicegroupname

    def get_servicegroupname(self):
        return self.options['servicegroupname']

    def set_state(self, state):
        self.options['state'] = state

    def get_state(self):
        return self.options['state']

    def set_weight(self, weight):
        self.options['weight'] = weight

    def get_weight(self):
        return self.options['weight']

    @staticmethod
    def add(nitro, resource):
        """
        Use this API to add lbmonitor_service_binding.
        """
        __resource = NSLBMonitorServiceBinding()
        __resource.set_monitorname(resource.get_monitorname())
        __resource.set_servicename(resource.get_servicename())
        __resource.set_dup_state(resource.get_dup_state())
        __resource.set_dup_weight(resource.get_dup_weight())
        __resource.set_servicegroupname(resource.get_servicegroupname())
        __resource.set_state(resource.get_state())
        __resource.set_weight(resource.get_weight())
        return __resource.update_resource(nitro)

    @staticmethod
    def delete(nitro, resource):
        """
        Use this API to delete lbmonitor_service_binding of a given name.
        """
        __resource = NSLBMonitorServiceBinding()
        __resource.set_monitorname(resource.get_monitorname())
        __resource.set_servicename(resource.get_servicename())
        __resource.set_servicegroupname(resource.get_servicegroupname())
        nsresponse = __resource.delete_resource(nitro, object_name=__resource.get_monitorname())
        return nsresponse