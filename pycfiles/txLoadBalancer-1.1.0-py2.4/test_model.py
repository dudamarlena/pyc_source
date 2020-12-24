# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/txlb/test/test_model.py
# Compiled at: 2008-07-05 02:21:36
from twisted.trial import unittest
from txlb import model
from txlb.model import HostMapper as Host
from txlb.schedulers import leastc, roundr

class HostMapperTests(unittest.TestCase):
    """
    Test the methods in the HostMapper class as well as related functions.
    """
    __module__ = __name__

    def setUp(self):
        """
        Set up a series of HostMapper instances for use in the tests.
        """
        self.proxyServices = [
         Host('web', '127.0.0.1:8080', 'prod', leastc, 'host1', '127.0.0.1:7001', True), Host('web', '127.0.0.1:8080', 'prod', leastc, 'host2', '127.0.0.1:7002'), Host('web', '127.0.0.1:8080', 'prod', leastc, 'host3', '127.0.0.1:7003'), Host('web', '127.0.0.1:8080', 'test', leastc, 'host4', '127.0.0.1:7004', False), Host('web', '127.0.0.1:8080', 'test', leastc, 'host5', '127.0.0.1:7005'), Host('web', '127.0.0.1:8080', 'test', leastc, 'host6', '127.0.0.1:7006'), Host('dns', '127.0.0.1:8053', 'corp', roundr, 'host7', '127.0.0.1:7007', True), Host('dns', '127.0.0.1:8053', 'corp', roundr, 'host8', '127.0.0.1:7008')]

    def test_hostMapper(self):
        """
        Test that the parameters passed to the HostMapper as set on the
        expected attributes of the object.
        """
        h = self.proxyServices[0]
        self.assertEquals(h.proxyName, 'web')
        self.assertEquals(h.proxyAddresses, [('127.0.0.1', 8080)])
        self.assertEquals(h.groupName, 'prod')
        self.assertEquals(h.hostName, 'host1')
        self.assertEquals(h.hostAddress, ('127.0.0.1', 7001))
        self.assertEquals(h.groupEnabled, True)
        h = self.proxyServices[3]
        self.assertEquals(h.groupName, 'test')
        self.assertEquals(h.groupEnabled, False)
        h = self.proxyServices[(-1)]
        self.assertEquals(h.proxyName, 'dns')
        self.assertEquals(h.groupEnabled, None)
        return

    def test_convertMapperToModel(self):
        """
        Check that the converter function properly creates the appropriate
        proxy model classes.
        """
        proxies = model.convertMapperToModel(self.proxyServices)
        self.assertEquals(len(proxies), 2)
        for proxy in proxies:
            group = proxy.getEnabledGroup()
            if proxy.name == 'web':
                self.assertTrue(group.name == 'prod')
                self.assertEquals(len(group.getHosts()), 3)
            elif proxy.name == 'dns':
                self.assertTrue(group.name == 'corp')
                self.assertEquals(len(group.getHosts()), 2)
            groups = proxy.getGroups()
            if proxy.name == 'web':
                self.assertEquals(len(groups), 2)
            elif proxy.name == 'dns':
                self.assertEquals(len(groups), 1)