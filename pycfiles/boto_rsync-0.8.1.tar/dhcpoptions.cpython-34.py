# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/vpc/dhcpoptions.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2472 bytes
__doc__ = '\nRepresents a DHCP Options set\n'
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