# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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