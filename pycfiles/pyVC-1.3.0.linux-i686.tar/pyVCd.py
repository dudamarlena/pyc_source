# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyVC/pyVCd.py
# Compiled at: 2007-08-31 18:49:27
__revision__ = '$Revision: 245 $'
import Pyro

class pyVCdData(Pyro.core.ObjBase):

    def __init__(self):
        Pyro.core.ObjBase.__init__(self)
        self._machines = {}
        self._specification = None
        return

    def add_machine(self, machine):
        """
        Adds a real machine to the pyVC ring.
        """
        from pyVC.Machine import Machine
        if issubclass(type(machine), Machine):
            self._machines[None] = machine
        else:
            machine = Pyro.core.getAttrProxyForURI(machine)
            print 'DEBUG: joined machine: ', machine.hostname
            self._machines[machine.hostname] = machine
        return

    def del_machine(self, hostname):
        """
        Deletes a real machine from the pyVC ring.
        """
        if hostname in self.machines():
            del self._machines[hostname]
            print 'DEBUG: lost machine: ', hostname

    def host(self, vmname):
        for network in self._networks:
            for host in network.vms:
                if host.vmname == vmname:
                    return host

    def _get_machinenames(self):
        return [ machine.hostname for machine in self._machines.values() ]

    def _get_machines(self):
        return [ machine for machine in self._machines.values() ]

    def _get_hosts(self):
        hosts = []
        for network in self._networks:
            for host in network.vms:
                if host.vmname not in hosts:
                    hosts.append(host.vmname)

        return hosts

    def start(self, filename):
        from pyVC.Specifications.VCML import Specification
        from pyVC.errors import pyVCdError
        for machine in self._machines.values():
            machine.refresh()

        if not self._specification:
            try:
                self._specification = Specification(self._machines, filename)
                self._networks = self._specification.create()
                self._specification.start()
            except:
                self._specification = None
                self._networks = {}
                raise

        else:
            raise pyVCdError, ('ERROR: Specification is already loaded.', 1)
        return

    def stop(self):
        from pyVC.errors import pyVCdError
        if self._specification:
            self._specification.stop()
            self._networks = {}
            self._specification = None
        else:
            raise pyVCdError, ('ERROR: Specification is not loaded.', 2)
        return

    def status(self):
        from pyVC.errors import pyVCdError
        if self._specification:
            return self._specification.status()
        else:
            raise pyVCdError, ('ERROR: Specification is not loaded.', 2)

    def initserver(self, vmname):
        from pyVC.errors import pyVCdError
        host = self.host(vmname)
        if host.status != 'started':
            raise pyVCdError, ('ERROR: VM not found / running.', 3)
        rc = host.console(socket=True)
        if rc == None:
            raise pyVCdError, ('ERROR: Console already in use.', 4)
        else:
            return rc
        return

    def startserver(self, vmname):
        self.host(vmname).serve()

    machinenames = property(_get_machinenames)
    machines = property(_get_machines)
    hosts = property(_get_hosts)