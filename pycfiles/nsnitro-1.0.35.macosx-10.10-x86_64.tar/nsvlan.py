# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nsvlan.py
# Compiled at: 2014-04-24 09:01:10
from nsbaseresource import NSBaseResource
__author__ = 'vlazarenko'

class NSVLAN(NSBaseResource):

    def __init__(self, json_data=None):
        """
        Supplied with json_data the object can be pre-filled
        """
        super(NSVLAN, self).__init__()
        self.options = {'id': '', 
           'ipv6dynamicrouting': '', 
           'rnat': '', 
           'portbitmap': '', 
           'tagbitmap': '', 
           'ifaces': '', 
           'tagifaces': ''}
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        self.resourcetype = NSVLAN.get_resourcetype()
        return

    @staticmethod
    def get_resourcetype():
        return 'vlan'

    def set_id(self, id):
        self.options['id'] = id

    def get_id(self):
        return self.options['id']

    def set_ipv6dynamicrouting(self, ipv6dynamicrouting):
        self.options['ipv6dynamicrouting'] = ipv6dynamicrouting

    def get_ipv6dynamicrouting(self):
        return self.options['ipv6dynamicrouting']

    def get_rnat(self):
        return self.options['rnat']

    def get_portbitmap(self):
        return self.options['portbitmap']

    def get_tagbitmap(self):
        return self.options['tagbitmap']

    def get_ifaces(self):
        return self.options['ifaces']

    def get_tagifaces(self):
        return self.options['tagifaces']

    @staticmethod
    def add(nitro, vlan):
        __vlan = NSVLAN()
        __vlan.set_id(vlan.get_id())
        __vlan.set_ipv6dynamicrouting(vlan.get_ipv6dynamicrouting())
        return __vlan.add_resource(nitro)

    @staticmethod
    def update(nitro, vlan):
        __vlan = NSVLAN()
        __vlan.set_id(vlan.get_id())
        __vlan.set_ipv6dynamicrouting(vlan.get_ipv6dynamicrouting())
        return __vlan.update_resource(nitro)

    @staticmethod
    def delete(nitro, vlan):
        __vlan = NSVLAN()
        __vlan.set_id(vlan.get_id())
        nsresponse = __vlan.delete_resource(nitro, object_name=__vlan.get_id())
        return nsresponse

    @staticmethod
    def get_all(nitro):
        """
        Use this API to fetch all vlan resources that are configured on netscaler.
        """
        __url = nitro.get_url() + NSVLAN.get_resourcetype()
        __json_vlans = nitro.get(__url).get_response_field(NSVLAN.get_resourcetype())
        __vlans = []
        for json_vlan in __json_vlans:
            __vlans.append(NSVLAN(json_vlan))

        return __vlans