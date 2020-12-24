# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/snmpmanager.py
# Compiled at: 2014-04-24 09:01:10
from nsbaseresource import NSBaseResource
__author__ = 'ndenev@gmail.com'

class SNMPManager(NSBaseResource):

    def __init__(self, json_data=None):
        """
        Supplied with json_data the object can be pre-filled
        """
        super(SNMPManager, self).__init__()
        self.options = {'ipaddress': '', 'netmask': '', 
           'domainresolveretry': '', 
           'ip': '', 
           'domain': ''}
        self.resourcetype = SNMPManager.get_resourcetype()
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        return

    @staticmethod
    def get_resourcetype():
        return 'snmpmanager'

    def set_ipaddress(self, ipaddress):
        self.options['ipaddress'] = ipaddress

    def get_ipaddress(self):
        return self.options['ipaddress']

    def set_netmask(self, netmask):
        self.options['netmask'] = netmask

    def get_netmask(self):
        return self.options['netmask']

    def set_domainresolveretry(self, domainresolveretry):
        self.options['domainresolveretry'] = domainresolveretry

    def get_domainresolveretry(self):
        return self.options['domainresolveretry']

    def get_ip(self):
        return self.options['ip']

    def get_domain(self):
        return self.options['domain']

    @staticmethod
    def add(nitro, snmpmanager):
        __snmpmanager = SNMPManager()
        __snmpmanager.set_ipaddress(snmpmanager.get_ipaddress())
        __snmpmanager.set_netmask(snmpmanager.get_netmask())
        __snmpmanager.set_domainresolveretry(snmpmanager.get_domainresolveretry())
        return __snmpmanager.add_resource(nitro)

    @staticmethod
    def delete(nitro, snmpmanager):
        __snmpmanager = SNMPManager()
        __snmpmanager.set_ipaddress(snmpmanager.get_ipaddress())
        return __snmpmanager.delete_resource(nitro)

    @staticmethod
    def update(nitro, snmpmanager):
        __snmpmanager = SNMPManager()
        __snmpmanager.set_ipaddress(snmpmanager.get_ipaddress())
        __snmpmanager.set_netmask(snmpmanager.get_netmask())
        __snmpmanager.set_domainresolveretry(snmpmanager.get_domainresolveretry())
        return __snmpmanager.update_resource(nitro)

    @staticmethod
    def get(nitro, snmpmanager):
        __snmpmanager = SNMPManager()
        __snmpmanager.set_ipaddress(snmpmanager.get_ipaddress())
        __snmpmanager.get_resource(nitro, object_name=__snmpmanager.get_ipaddress())
        return __snmpmanager

    @staticmethod
    def get_all(nitro):
        __url = nitro.get_url() + SNMPManager.get_resourcetype()
        __json_snmpmanagers = nitro.get(__url).get_response_field(SNMPManager.get_resourcetype())
        __snmpmanagers = []
        for json_snmpmanager in __json_snmpmanagers:
            __snmpmanagers.append(SNMPManager(json_snmpmanager))

        return __snmpmanagers