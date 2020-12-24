# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ahankins/Documents/code/git/pybagit/test/bagcreate.py
# Compiled at: 2014-11-17 12:16:38
import unittest, os, shutil
from pybagit.bagit import BagIt

class CreateTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        if os.path.exists(os.path.join(os.getcwd(), 'test', 'newtestbag')):
            shutil.rmtree(os.path.join(os.getcwd(), 'test', 'newtestbag'))

    def test_minimal_bag_creation(self):
        newbag = BagIt(os.path.join(os.getcwd(), 'test', 'newtestbag'), extended=False)
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test', 'newtestbag')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test', 'newtestbag', 'bagit.txt')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test', 'newtestbag', 'manifest-sha1.txt')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test', 'newtestbag', 'data')))
        self.assertFalse(os.path.exists(os.path.join(os.getcwd(), 'test', 'newtestbag', 'bag-info.txt')))
        self.assertFalse(os.path.exists(os.path.join(os.getcwd(), 'test', 'newtestbag', 'fetch.txt')))
        self.assertFalse(os.path.exists(os.path.join(os.getcwd(), 'test', 'newtestbag', 'tagmanifest-sha1.txt')))

    def test_extended_bag_creation(self):
        newbag = BagIt(os.path.join(os.getcwd(), 'test', 'newtestbag'))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test', 'newtestbag')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test', 'newtestbag', 'bagit.txt')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test', 'newtestbag', 'manifest-sha1.txt')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test', 'newtestbag', 'data')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test', 'newtestbag', 'bag-info.txt')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test', 'newtestbag', 'fetch.txt')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test', 'newtestbag', 'tagmanifest-sha1.txt')))

    def test_unicode_characters_in_bagnam(self):
        newbag = BagIt(os.path.join(os.getcwd(), 'test', 'tëst'))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test', 'tëst')))


def suite():
    test_suite = unittest.makeSuite(CreateTest, 'test')
    return test_suite