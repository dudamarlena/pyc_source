# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.network/plonesocial/network/tests/test_tool.py
# Compiled at: 2012-08-14 05:16:46
import unittest2 as unittest
from zope.component import queryUtility
from plone.app.testing import TEST_USER_ID, setRoles
from plonesocial.network.testing import PLONESOCIAL_NETWORK_INTEGRATION_TESTING
from plonesocial.network.interfaces import INetworkGraph
from plonesocial.network.interfaces import INetworkTool

class TestNetworkTool(unittest.TestCase):
    layer = PLONESOCIAL_NETWORK_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_tool_available(self):
        tool = queryUtility(INetworkTool)
        self.assertTrue(INetworkGraph.providedBy(tool))