# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/tests/test_region.py
# Compiled at: 2010-02-09 00:00:15
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import unittest
from pyogp.lib.base.exc import *
from pyogp.lib.client.region import Region
from pyogp.lib.base.message.message import Message, Block
import pyogp.lib.base.tests.config

class TestRegion(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.region = Region(global_x=256, global_y=256, seed_capability_url='fake_url', udp_blacklist=[], sim_ip=1, sim_port=1, circuit_code=1, agent=None, settings=None, message_handler=None)
        return

    def tearDown(self):
        pass

    def test_region_basic_attributes(self):
        self.assertEquals(self.region.sim_ip, 1)
        self.assertEquals(self.region.grid_y, 1)
        self.assertEquals(self.region.grid_x, 1)
        self.assertEquals(self.region.global_y, 256)
        self.assertEquals(self.region.global_x, 256)
        self.assertEquals(self.region.seed_capability_url, 'fake_url')
        self.assertEquals(self.region.agent, None)
        self.assertEquals(self.region.circuit_code, 1)
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRegion))
    return suite