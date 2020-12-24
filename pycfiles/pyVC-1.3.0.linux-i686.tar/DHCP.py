# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyVC/Helpers/DHCP.py
# Compiled at: 2007-08-31 18:49:24
__revision__ = '$Revision: 275 $'
from pyVC.Helpers import Base

class Helper(Base.Helper):
    __revision__ = '$Revision: 275 $'
    errors = ('nosudo', 'no_dhcpd_executable')
    platforms = ()

    def __init__(self, realmachine, networks, **keywords):
        Base.Helper.__init__(self, realmachine, networks, **keywords)
        self.__fd = None
        self.__pid = None
        return

    def start(self):
        from atexit import register
        from tempfile import NamedTemporaryFile
        from os import chmod
        if not self.__pid:
            interfaces = [ network.interface(self.realmachine) for network in self.networks ]
            self.__fd = NamedTemporaryFile()
            self.create_dhcpd_conf(self.__fd)
            chmod(self.__fd.name, 438)
            print '%s %s -q -f -cf %s %s' % (
             self.realmachine.sudo,
             self.realmachine.config['global']['dhcpd_executable'],
             self.__fd.name, (' ').join(interfaces))
            self.__pid = self.realmachine.popen('%s %s -q -f -cf %s %s' % (
             self.realmachine.sudo,
             self.realmachine.config['global']['dhcpd_executable'],
             self.__fd.name, (' ').join(interfaces)))
            self.status = 'started'
            register(self.stop)

    def stop(self):
        if self.__pid:
            pid = self.realmachine.popen('%s kill %s' % (self.realmachine.sudo, self.__pid))
            self.realmachine.wait(pid)
            self.realmachine.wait(self.__pid)
            self.status = 'stopped'
            self.__pid = None
        return

    def create_dhcpd_conf(self, dhcpfile):
        from pyVC.Helpers import Router, Interface
        from pyVC.Helpers.Tools import cidr2mask
        dhcpfile.write('ddns-update-style ad-hoc;\n')
        for network in self.networks:
            if network.subnet:
                (networkaddress, cidrmask) = network.subnet.split('/')
                netmask = cidr2mask(cidrmask)
                dhcpfile.write('subnet %s netmask %s {\n' % (
                 networkaddress,
                 netmask))
            if network.dns_servers:
                dhcpfile.write('  option domain-name-servers %s;\n' % network.dns_servers)
            for helper in network.helpers:
                if isinstance(helper, Router.Helper):
                    router = helper
                    for helper in network.helpers:
                        if isinstance(helper, Interface.Helper) and helper.realmachine == router.realmachine:
                            dhcpfile.write('  option routers %s;\n' % (',').join(helper.addrs))

            dhcpfile.write('  use-host-decl-names on;\n')
            for vm in network.vms:
                dhcpfile.write('  host %s {\n' % vm)
                if vm.macaddr:
                    dhcpfile.write('   hardware ethernet %s;\n' % vm.macaddrs[vm.networks.index(network)])
                dhcpfile.write('   fixed-address %s;\n' % network.ips(vm)[0])
                dhcpfile.write('   option host-name "%s";\n' % vm)
                dhcpfile.write('  }\n')

            dhcpfile.write('}\n')

        dhcpfile.flush()

    def __repr__(self):
        return 'DHCP(%s, %s)' % (self.realmachine, self.networks)

    def __str__(self):
        return 'DHCP Server on %s' % self.realmachine.used_interfaces