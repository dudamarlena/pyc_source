# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyVC/Networks/User.py
# Compiled at: 2007-08-31 18:49:25
"""
Package containing the object for the User-mode virtual network.
"""
__revision__ = '$Revision$'
from pyVC.Networks import Base

class Network(Base.Network):
    """This object defines a User-mode Network"""
    __revision__ = '$Revision$'
    errors = ()
    platforms = ()

    def __init__(self, realmachines, lanname, **keywords):
        Base.Network.__init__(self, realmachines, lanname, **keywords)
        self.status = None
        return

    def start(self):
        """Starts the User-mode virtual network"""
        pass

    def stop(self):
        """Stops the User-mode virtual network"""
        pass

    def __repr__(self):
        return 'User("%s", %s, subnet="%s", dns_servers="%s")' % (
         self.lanname,
         self.realmachine,
         self.dns_servers)

    def qemu(self, host):
        from pyVC.errors import NetworkError
        user_command = ''
        if host.macaddrs:
            mac = host.macaddrs.pop(0)
            mac_command = ',macaddr=%s' % mac
            host.macaddrs.append(mac)
        else:
            mac_command = ''
        if self.realmachine.qemu_version in ('0.7.0', '0.7.1', '0.7.2'):
            user_command = '-user-net'
            return ('', user_command, '')
        else:
            user_command = '-net nic%s -net user,hostname=%s' % (mac_command, host.vmname)
            return ('', user_command, '')

    def uml(self, host):
        raise NotImplementedError

    def xen(self, host):
        from lxml.etree import Element, SubElement
        interface = Element('interface', type='user')
        if host.macaddrs:
            mac = host.macaddrs.pop(0)
            SubElement(interface, 'mac', address=str(mac))
            host.macaddrs.append(mac)
        return interface