# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/vpc/dhcpoptions.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2472 bytes
"""
Represents a DHCP Options set
"""
from boto.ec2.ec2object import TaggedEC2Object

class DhcpValueSet(list):

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'value':
            self.append(value)


class DhcpConfigSet(dict):

    def startElement(self, name, attrs, connection):
        if name == 'valueSet':
            if self._name not in self:
                self[self._name] = DhcpValueSet()
            return self[self._name]

    def endElement(self, name, value, connection):
        if name == 'key':
            self._name = value


class DhcpOptions(TaggedEC2Object):

    def __init__(self, connection=None):
        super(DhcpOptions, self).__init__(connection)
        self.id = None
        self.options = None

    def __repr__(self):
        return 'DhcpOptions:%s' % self.id

    def startElement(self, name, attrs, connection):
        retval = super(DhcpOptions, self).startElement(name, attrs, connection)
        if retval is not None:
            return retval
        if name == 'dhcpConfigurationSet':
            self.options = DhcpConfigSet()
            return self.options

    def endElement(self, name, value, connection):
        if name == 'dhcpOptionsId':
            self.id = value
        else:
            setattr(self, name, value)