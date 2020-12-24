# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/tests/test_region.py
# Compiled at: 2010-02-09 00:00:15
"""
Contributors can be viewed at:
http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt 

$LicenseInfo:firstyear=2008&license=apachev2$

Copyright 2009, Linden Research, Inc.

Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0
or in 
    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt

$/LicenseInfo$
"""
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