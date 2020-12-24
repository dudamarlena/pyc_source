# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsam/sastest.py
# Compiled at: 2019-02-11 18:59:27
from .sam_api import API, XMLBase, XMLRequest

class IcmpPingTest(XMLBase):

    def __init__(self, originatingVprnSite, target, targetType='vprnSite', id=0, administrativeState='enabled', displayedName='VPRN Icmp Ping Test', forwardingClass='be', profile='out', packetSize=98, packetsToSend=2, packetInterval=2, packetTimeout=2):
        self.xml = getattr(API, 'icmp.IcmpPing')()
        self.actionMask('create')
        self.tag('testTargetType', targetType)
        self.tag('targetIpAddress', target)
        self.tag('originatingVprnSite', originatingVprnSite)
        self.tag('id', id)
        self.tag('administrativeState', administrativeState)
        self.tag('displayedName', displayedName)
        self.tag('forwardingClass', forwardingClass)
        self.tag('profile', profile)
        self.tag('packetSize', packetSize)
        self.tag('packetsToSend', packetsToSend)
        self.tag('packetInterval', packetInterval)
        self.tag('packetTimeout', packetTimeout)


class adhocExecuteAndWait(XMLRequest):
    METHOD = 'sas.Test.adhocExecuteAndWait'

    def __init__(self, target, test, timeout=30, keepTest=False):
        XMLRequest.__init__(self)
        self.tag('testedObject', target)
        self.tag('timeout', int(timeout * 1000))
        self.tag('keepTest', keepTest)
        self.xml.test = API.test(test.xml)

    def request(self, conn, **kw):
        response = XMLRequest.request(self, conn, **kw)
        return response.result.getchildren()[0]