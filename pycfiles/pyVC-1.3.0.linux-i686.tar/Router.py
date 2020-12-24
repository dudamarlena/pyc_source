# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyVC/Helpers/Router.py
# Compiled at: 2007-08-31 18:49:25
__revision__ = '$Revision: 277 $'
from pyVC.Helpers import Base

class Helper(Base.Helper):
    __revision__ = '$Revision: 277 $'
    init = {}
    errors = ('nosudo', 'no_iptables_executable')
    platforms = 'Linux'

    def __init__(self, realmachine, networks, **keywords):
        Base.Helper.__init__(self, realmachine, networks, **keywords)

    def start(self):
        from atexit import register
        from pyVC.errors import MachineError
        if True not in self.init:
            pid = self.realmachine.popen('%s %s -t nat -F' % (
             self.realmachine.sudo,
             self.realmachine.config['global']['iptables_executable']))
            self.realmachine.wait(pid)
            if self.realmachine.platform == 'Linux':
                print '%s sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"' % self.realmachine.sudo
                pid = self.realmachine.popen('%s sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"' % self.realmachine.sudo)
                self.realmachine.wait(pid)
            else:
                raise MachineError, (
                 'ERROR: Cannot enable routing on architecture %s.' % self.realmachine.platform,
                 'norouting',
                 self.realmachine.hostname)
            self.init[True] = None
        for network in self.networks:
            if network.subnet:
                print '%s %s -t nat -A POSTROUTING -s %s -j MASQUERADE' % (
                 self.realmachine.sudo,
                 self.realmachine.config['global']['iptables_executable'],
                 network.subnet)
                pid = self.realmachine.popen('%s %s -t nat -A POSTROUTING -s %s -j MASQUERADE' % (
                 self.realmachine.sudo,
                 self.realmachine.config['global']['iptables_executable'],
                 network.subnet))
                self.realmachine.wait(pid)

        self.status = 'started'
        register(self.stop)
        return

    def stop(self):
        pid = self.realmachine.popen('%s %s -t nat -F' % (
         self.realmachine.sudo,
         self.realmachine.config['global']['iptables_executable']))
        self.realmachine.wait(pid)
        self.status = 'stopped'

    def _get_subnet(self):
        return self._subnet

    def __repr__(self):
        return 'Router(%s, %s, %s)' % (self.realmachine, self.networks, self._subnet)

    def __str__(self):
        return 'Router for %s' % self._subnet

    subnet = property(_get_subnet)