# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rc/firewall.py
# Compiled at: 2020-04-21 13:44:18
# Size of source mod 2**32: 1256 bytes


class Firewall:

    def __init__(self, *, provider, name, direction='in', action='allow', ports, ips=['0.0.0.0/0']):
        self.provider = provider
        self.name = name
        self.direction = direction
        self.action = action
        self.ports = ports
        self.ips = ips

    def __eq__(self, other):
        return (
         self.provider, self.name, self.direction, self.action, self.ports, self.ips) == (
         other.provider, other.name, other.action,
         other.ports, other.ips)

    def __expr__(self):
        if 'direction' == 'in':
            return f"Firewall(provider={self.provider}, name={self.name}, direction={self.direction}, action={self.action}, ports={self.ports}, ips={self.ips})"
        return f"Firewall(provider={self.provider}, name={self.name}, direction={self.direction}, action={self.action}, ports={self.ports}, ips={self.ips})"

    def machines(self):
        return self.provider.firewall_machines(self)

    def delete(self):
        return self.provider.delete_firewall(self)

    def add_to_machine(self, machine):
        return self.provider.add_firewall(machine, self)

    def remove_from_machine(self, machine):
        return self.provider.remove_firewall(machine, self)