# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/smi/mibs/SNMPv2-CONF.py
# Compiled at: 2019-08-18 17:24:05
(MibNode,) = mibBuilder.importSymbols('SNMPv2-SMI', 'MibNode')

class ObjectGroup(MibNode):
    __module__ = __name__
    status = 'current'
    objects = ()
    description = ''

    def getStatus(self):
        return self.status

    def setStatus(self, v):
        self.status = v
        return self

    def getObjects(self):
        return getattr(self, 'objects', ())

    def setObjects(self, *args, **kwargs):
        if kwargs.get('append'):
            self.objects += args
        else:
            self.objects = args
        return self

    def getDescription(self):
        return getattr(self, 'description', '')

    def setDescription(self, v):
        self.description = v
        return self

    def asn1Print(self):
        return 'OBJECT-GROUP\n  OBJECTS { %s }\n  DESCRIPTION "%s"\n' % ((', ').join([ x for x in self.getObjects() ]), self.getDescription())


class NotificationGroup(MibNode):
    __module__ = __name__
    status = 'current'
    objects = ()
    description = ''

    def getStatus(self):
        return self.status

    def setStatus(self, v):
        self.status = v
        return self

    def getObjects(self):
        return getattr(self, 'objects', ())

    def setObjects(self, *args, **kwargs):
        if kwargs.get('append'):
            self.objects += args
        else:
            self.objects = args
        return self

    def getDescription(self):
        return getattr(self, 'description', '')

    def setDescription(self, v):
        self.description = v
        return self

    def asn1Print(self):
        return 'NOTIFICATION-GROUP\n  NOTIFICATIONS { %s }\n  DESCRIPTION "%s"\n' % ((', ').join([ x for x in self.getObjects() ]), self.getDescription())


class ModuleCompliance(MibNode):
    __module__ = __name__
    status = 'current'
    objects = ()
    description = ''

    def getStatus(self):
        return self.status

    def setStatus(self, v):
        self.status = v
        return self

    def getObjects(self):
        return getattr(self, 'objects', ())

    def setObjects(self, *args, **kwargs):
        if kwargs.get('append'):
            self.objects += args
        else:
            self.objects = args
        return self

    def getDescription(self):
        return getattr(self, 'description', '')

    def setDescription(self, v):
        self.description = v
        return self

    def asn1Print(self):
        return 'MODULE-COMPLIANCE\n  OBJECT { %s }\n  DESCRIPTION "%s"\n' % ((', ').join([ x for x in self.getObjects() ]), self.getDescription())


class AgentCapabilities(MibNode):
    __module__ = __name__
    status = 'current'
    description = ''
    reference = ''
    productRelease = ''

    def getStatus(self):
        return self.status

    def setStatus(self, v):
        self.status = v
        return self

    def getDescription(self):
        return getattr(self, 'description', '')

    def setDescription(self, v):
        self.description = v
        return self

    def getReference(self):
        return self.reference

    def setReference(self, v):
        self.reference = v
        return self

    def getProductRelease(self):
        return self.productRelease

    def setProductRelease(self, v):
        self.productRelease = v
        return self

    def asn1Print(self):
        return 'AGENT-CAPABILITIES\n  STATUS "%s"\n  PRODUCT-RELEASE "%s"\n  DESCRIPTION "%s"\n' % (self.getStatus(), self.getProductRelease(), self.getDescription())


mibBuilder.exportSymbols('SNMPv2-CONF', ObjectGroup=ObjectGroup, NotificationGroup=NotificationGroup, ModuleCompliance=ModuleCompliance, AgentCapabilities=AgentCapabilities)