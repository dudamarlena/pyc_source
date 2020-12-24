# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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