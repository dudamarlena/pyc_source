# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nsvlaninterfacebinding.py
# Compiled at: 2014-04-24 09:01:10
from nsbaseresource import NSBaseResource
__author__ = 'vlazarenko'

class NSVLANInterfaceBinding(NSBaseResource):

    def __init__(self, json_data=None):
        """
        Supplied with json_data the object can be pre-filled
        """
        super(NSVLANInterfaceBinding, self).__init__()
        self.options = {'id': '', 
           'ifnum': '', 
           'tagged': ''}
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        self.resourcetype = NSVLANInterfaceBinding.get_resourcetype()
        return

    @staticmethod
    def get_resourcetype():
        return 'vlan_interface_binding'

    def set_id(self, id):
        self.options['id'] = id

    def get_id(self):
        return self.options['id']

    def set_ifnum(self, ifnum):
        self.options['ifnum'] = ifnum

    def get_ifnum(self):
        return self.options['ifnum']

    def set_tagged(self, tagged):
        self.options['tagged'] = tagged

    def get_tagged(self):
        return self.options['tagged']

    @staticmethod
    def add(nitro, resource):
        __resource = NSVLANInterfaceBinding()
        __resource.set_id(resource.get_id())
        __resource.set_ifnum(resource.get_ifnum())
        __resource.set_tagged(resource.get_tagged())
        return __resource.add_resource(nitro)

    @staticmethod
    def delete(nitro, resource):
        __resource = NSVLANInterfaceBinding()
        __resource.set_id(resource.get_id())
        __resource.set_ifnum(resource.get_ifnum())
        __resource.set_tagged(resource.get_tagged())
        nsresponse = __resource.delete_resource(nitro, object_name=__resource.get_id())
        return nsresponse

    @staticmethod
    def get(nitro, resource):
        """
        Use this API to fetch service resource of given name.
        """
        __resource = NSVLANInterfaceBinding()
        __resource.set_id(resource.get_id())
        __resource.get_resource(nitro, object_name=__resource.get_id())
        return __resource