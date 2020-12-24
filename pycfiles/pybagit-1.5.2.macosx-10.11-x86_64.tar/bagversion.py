# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ahankins/Documents/code/git/pybagit/test/bagversion.py
# Compiled at: 2014-11-17 13:14:38
import unittest, os
from pybagit.bagit import BagIt

class VersionTest(unittest.TestCase):

    def setUp(self):
        self.bag = BagIt(os.path.join(os.getcwd(), 'test', 'testbag'))

    def tearDown(self):
        pass

    def test_versions(self):
        self.assertEquals(self.bag.bag_major_version, 0)
        self.assertEquals(self.bag.bag_minor_version, 96)
        binfo = self.bag.get_bag_info()
        self.assertEquals(binfo['version'], '0.96')
        self.assertEquals(binfo['encoding'], 'utf-8')
        self.assertEquals(binfo['hash'], 'sha1')


def suite():
    test_suite = unittest.makeSuite(VersionTest, 'test')
    return test_suite