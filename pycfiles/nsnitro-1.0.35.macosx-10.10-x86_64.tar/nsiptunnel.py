# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nsiptunnel.py
# Compiled at: 2014-04-24 09:01:10
from nsbaseresource import NSBaseResource
__author__ = 'Aleksandar Topuzovic'

class NSIPTunnel(NSBaseResource):

    def __init__(self, json_data=None):
        """
        Supplied with json_data the object can be pre-filled
        """
        super(NSIPTunnel, self).__init__()
        self.options = {'remote': '', 
           'remotesubnetmask': '', 
           'name': '', 
           'sysname': '', 
           'local': '', 
           'protocol': '', 
           'type': '', 
           'encapip': '', 
           'channel': '', 
           'secure': ''}
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        self.resourcetype = NSIPTunnel.get_resourcetype()
        return

    @staticmethod
    def get_resourcetype():
        return 'iptunnel'

    def set_name(self, name):
        """
        The name of the ip tunnel.
        Minimum length = 1
        """
        self.options['name'] = name

    def get_name(self):
        """
        The name of the ip tunnel.
        Minimum length = 1
        """
        return self.options['name']

    def set_remote(self, remote):
        """
        The remote-ip or subnet of the tunnel.
        Minimum length = 1
        """
        self.options['remote'] = remote

    def get_remote(self):
        """
        The remote-ip or subnet of the tunnel.
        Minimum length = 1
        """
        return self.options['remote']

    def set_remotesubnetmask(self, remotesubnetmask):
        """
        The remote-subnet mask of the tunnel.
        """
        self.options['remotesubnetmask'] = remotesubnetmask

    def get_remotesubnetmask(self):
        """
        The remote-subnet mask of the tunnel.
        """
        return self.options['remotesubnetmask']

    def set_local(self, local):
        """
        The local-ip of the tunnel.
        """
        self.options['local'] = local

    def get_local(self):
        """
        The local-ip of the tunnel.
        """
        return self.options['local']

    def set_protocol(self, protocol):
        """
        The IP tunneling protocol.
        Default value: IPIP
        """
        self.options['protocol'] = protocol

    def get_protocol(self):
        """
        The IP tunneling protocol.
        Default value: IPIP
        """
        return self.options['protocol']

    def set_secure(self, secure):
        """
        Secure communication using IPSec.
        Default value: NO
        """
        self.options['secure'] = secure

    def get_secure(self):
        """
        Secure communication using IPSec.
        Default value: NO
        """
        return self.options['secure']

    def get_sysname(self):
        """
        The name of the ip tunnel.
        """
        return self.options['sysname']

    def get_type(self):
        """
        The type of this tunnel.
        """
        return self.options['type']

    def get_encapip(self):
        """
        The effective local-ip of the tunnel. Used as the source of the encapsulated packets.
        """
        return self.options['encapip']

    def get_channel(self):
        """
        The tunnel which is bound to a netbridge.
        """
        return self.options['channel']

    @staticmethod
    def add(nitro, iptunnel):
        __iptunnel = NSIPTunnel()
        __iptunnel.set_name(iptunnel.get_name())
        __iptunnel.set_remote(iptunnel.get_remote())
        __iptunnel.set_remotesubnetmask(iptunnel.get_remotesubnetmask())
        __iptunnel.set_local(iptunnel.get_local())
        __iptunnel.set_protocol(iptunnel.get_protocol())
        __iptunnel.set_secure(iptunnel.get_secure())
        return __iptunnel.add_resource(nitro)

    @staticmethod
    def delete(nitro, iptunnel):
        __iptunnel = NSIPTunnel()
        __iptunnel.set_name(iptunnel.get_name())
        nsresponse = __iptunnel.delete_resource(nitro, object_name=__iptunnel.get_name())
        return nsresponse

    @staticmethod
    def get_all(nitro):
        """
        Use this API to fetch all iptunnel resources that are configured on netscaler.
        """
        __url = nitro.get_url() + NSIPTunnel.get_resourcetype()
        __json_iptunnels = nitro.get(__url).get_response_field(NSIPTunnel.get_resourcetype())
        __iptunnels = []
        for json_iptunnel in __json_iptunnels:
            __iptunnels.append(NSIPTunnel(json_iptunnel))

        return __iptunnels