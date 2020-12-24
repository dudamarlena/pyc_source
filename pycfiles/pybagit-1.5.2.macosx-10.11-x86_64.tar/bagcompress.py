# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ahankins/Documents/code/git/pybagit/test/bagcompress.py
# Compiled at: 2014-11-17 13:14:49
import unittest, os, shutil
from pybagit.bagit import BagIt

class CompressTest(unittest.TestCase):

    def setUp(self):
        self.bag = BagIt(os.path.join(os.getcwd(), 'test', 'testbag'))

    def tearDown(self):
        if os.path.exists(os.path.join(os.getcwd(), 'test', 'testbag.tgz')):
            os.remove(os.path.join(os.getcwd(), 'test', 'testbag.tgz'))
        if os.path.exists(os.path.join(os.getcwd(), 'test', 'testbag.zip')):
            os.remove(os.path.join(os.getcwd(), 'test', 'testbag.zip'))
        if os.path.exists(os.path.join(os.getcwd(), 'test', 'newzipbag')):
            shutil.rmtree(os.path.join(os.getcwd(), 'test', 'newzipbag'))
        if os.path.exists(os.path.join(os.getcwd(), 'test', 'newtgzbag')):
            shutil.rmtree(os.path.join(os.getcwd(), 'test', 'newtgzbag'))
        if os.path.exists(os.path.join(os.getcwd(), 'test', 'newzipbag.zip')):
            os.remove(os.path.join(os.getcwd(), 'test', 'newzipbag.zip'))
        if os.path.exists(os.path.join(os.getcwd(), 'test', 'newtgzbag.tgz')):
            os.remove(os.path.join(os.getcwd(), 'test', 'newtgzbag.tgz'))

    def test_compress_tgz(self):
        self.bag.package(os.path.join(os.getcwd(), 'test'))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test', 'testbag.tgz')))

    def test_compress_zip(self):
        self.bag.package(os.path.join(os.getcwd(), 'test'), method='zip')
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test', 'testbag.zip')))

    def test_uncompress_tgz(self):
        newbag = BagIt(os.path.join(os.getcwd(), 'test', 'newtgzbag'))
        newbag.package(os.path.join(os.getcwd(), 'test'))
        shutil.rmtree(os.path.join(os.getcwd(), 'test', 'newtgzbag'))
        tgzbag = BagIt(os.path.join(os.getcwd(), 'test', 'newtgzbag.tgz'))
        self.assertTrue(os.path.exists(tgzbag.bag_directory))

    def test_uncompress_zip(self):
        newbag = BagIt(os.path.join(os.getcwd(), 'test', 'newzipbag'))
        newbag.package(os.path.join(os.getcwd(), 'test'), method='zip')
        shutil.rmtree(os.path.join(os.getcwd(), 'test', 'newzipbag'))
        zipbag = BagIt(os.path.join(os.getcwd(), 'test', 'newzipbag.zip'))
        self.assertTrue(os.path.exists(zipbag.bag_directory))


def suite():
    test_suite = unittest.makeSuite(CompressTest, 'test')
    return test_suite