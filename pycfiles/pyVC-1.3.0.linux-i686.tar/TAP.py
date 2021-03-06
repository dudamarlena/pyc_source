# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyVC/Networks/TAP.py
# Compiled at: 2007-08-31 18:49:25
"""
Package containing the object for the TAP virtual network"""
__revision__ = '$Revision$'
from pyVC.Networks import Base

class Network(Base.Network):
    """This object defines a TAP Network"""
    __revision__ = '$Revision$'
    errors = ('notunmod', 'notundev', 'notunwr', 'notunuser', 'no_ifconfig_executable')
    platforms = ()
    max_vms = 1
    max_realmachines = 1

    def __init__(self, realmachines, lanname, **keywords):
        Base.Network.__init__(self, realmachines, lanname, **keywords)
        self.__interface = None
        return

    def start(self):
        """Starts the TAP virtual network"""
        from atexit import register
        for realmachine in self.realmachines:
            self.__interface = realmachine.tap()

        self.add_interface(realmachine, self.__interface, 0)
        self.status = 'started'
        register(self.stop)

    def stop(self):
        """Stops the TAP virtual network"""
        for realmachine in self.realmachines:
            try:
                self.del_interface(realmachine)
            except KeyError:
                pass

            realmachine.tap(self.__interface)

        self.status = 'stopped'

    def __repr__(self):
        return 'TAP("%s", subnet="%s", dns_servers="%s")' % (
         self.lanname,
         self.realmachine,
         self.dns_servers)

    def qemu(self, host):
        from pyVC.errors import NetworkError
        tap_command = ''
        if host.macaddrs:
            mac = host.macaddrs.pop(0)
            mac_command = ',macaddr=%s' % mac
            host.macaddrs.append(mac)
        else:
            mac_command = ''
        if self.realmachine.qemu_version not in ('0.7.0', '0.7.1', '0.7.2'):
            tap_command = '-net nic%s -net tap,ifname=%s,script=%s' % (mac_command, self.__interface, self.realmachine.config['global']['true_executable'])
            return ('', tap_command, '')
        else:
            raise NetworkError, (
             'ERROR: Unhandled Network type for QEMU version %s.' % self.realmachine.qemu_version,
             2,
             self.realmachine.hostname,
             self.lanname)

    def uml(self, host):
        tap_command = ''
        mac = host.macaddrs.pop(0)
        tap_command = '%s=tuntap,%s,,%s' % (host.interfaces.pop(0), mac, self.__interface)
        host.macaddrs.append(mac)
        return (
         '', tap_command, '')

    def xen(self, host):
        from lxml.etree import Element, SubElement
        interface = Element('interface', type='ethernet')
        SubElement(interface, 'target', dev=str(self.__interface))
        if host.macaddrs:
            mac = host.macaddrs.pop(0)
            SubElement(interface, 'mac', address=str(mac))
            host.macaddrs.append(mac)
        return interface