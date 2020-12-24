# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyVC/Helpers/Interface.py
# Compiled at: 2007-08-31 18:49:25
__revision__ = '$Revision: 275 $'
from pyVC.Helpers import Base

class Helper(Base.Helper):
    __revision__ = '$Revision: 275 $'
    errors = ('nosudo', 'no_ifconfig_executable')
    platforms = ()

    def __init__(self, realmachine, networks, addrs, **keywords):
        Base.Helper.__init__(self, realmachine, networks, **keywords)
        self._addrs = addrs.split(',')
        self._interfaces = {}

    def _get_addrs(self):
        """
        Returns a list of IP addresses to be assigned to the network interface.
        """
        return self._addrs

    def start(self):
        from atexit import register
        from pyVC.Helpers.Tools import AliasGenerator, cidr2mask
        for network in self._networks:
            alias_generator = AliasGenerator()
            self._interfaces[network.lanname] = []
            mask = ''
            if network.subnet:
                mask = cidr2mask(network.subnet.split('/')[1])
            else:
                mask = '255.255.255.0'
            for addr in self._addrs:
                alias_suffix = alias_generator.next()
                while network.interface(self.realmachine) + alias_suffix in self.realmachine.used_interfaces + self.realmachine.pyvc_interfaces:
                    alias_suffix = alias_generator.next()

                ifname = network.interface(self.realmachine) + alias_suffix
                pid = self.realmachine.popen('%s %s %s %s netmask %s' % (
                 self.realmachine.sudo,
                 self.realmachine.config['global']['ifconfig_executable'],
                 ifname,
                 addr,
                 mask))
                self.realmachine.wait(pid)
                pid = self.realmachine.popen('%s %s %s up' % (
                 self.realmachine.sudo,
                 self.realmachine.config['global']['ifconfig_executable'],
                 network.interface(self.realmachine)))
                self.realmachine.wait(pid)
                self.realmachine.add_interface(ifname)
                self._interfaces[network.lanname].append(ifname)

        self.status = 'started'
        register(self.stop)

    def stop(self):
        if self.status == 'started':
            for network in self._networks:
                for ifname in self._interfaces[network.lanname]:
                    pid = self.realmachine.popen('%s %s %s down' % (
                     self.realmachine.sudo,
                     self.realmachine.config['global']['ifconfig_executable'],
                     ifname))
                    self.realmachine.wait(pid)

            self.status = 'stopped'

    def __repr__(self):
        return 'Interface(%s, %s, %s)' % (self.realmachine, self.networks, self._addrs)

    def __str__(self):
        return 'Interface %s on %s' % (self._addrs, self._iface)

    addrs = property(_get_addrs)