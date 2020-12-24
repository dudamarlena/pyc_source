# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ahankins/Documents/code/git/pybagit/test/bagupdate.py
# Compiled at: 2014-11-17 13:14:42
import unittest, os, shutil
from pybagit.bagit import BagIt

class UpdateTest(unittest.TestCase):

    def setUp(self):
        self.bag = BagIt(os.path.join(os.getcwd(), 'test', 'testbag'))
        self.invalid_bag = BagIt(os.path.join(os.getcwd(), 'test', 'invalid_bag'))

    def tearDown(self):
        if os.path.exists(os.path.join(os.getcwd(), 'test', 'invalid_bag')):
            shutil.rmtree(os.path.join(os.getcwd(), 'test', 'invalid_bag'))

    def test_update(self):
        self.bag.update()
        self.assertEquals(len(self.bag.bag_errors), 0)

    def test_is_valid(self):
        self.bag.update()
        self.assertEquals(self.bag.is_valid(), True)

    def test_not_valid(self):
        os.remove(self.invalid_bag.manifest_file)
        self.invalid_bag.validate()
        self.assertEquals(self.invalid_bag.is_valid(), False)


def suite():
    test_suite = unittest.makeSuite(UpdateTest, 'test')
    return test_suite