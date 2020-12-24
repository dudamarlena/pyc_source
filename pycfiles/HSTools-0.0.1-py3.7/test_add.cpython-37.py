# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/test/test_add.py
# Compiled at: 2019-10-08 14:22:41
# Size of source mod 2**32: 3381 bytes
import os, unittest
from hstools import hydroshare

class TestAdd(unittest.TestCase):
    testfile = 'testfile1.txt'
    testfile2 = 'testfile2.txt'
    authfile = os.path.abspath('test/hs_auth_oauth')
    title = 'unit testing'
    abstract = 'this is a resource created by a unittest'
    keywords = ['test']

    def setUp(self):
        with open(self.testfile, 'w') as (f):
            f.write('this is a test file')
        with open(self.testfile2, 'w') as (f):
            f.write('this is a test file')

    def tearDown(self):
        os.remove(self.testfile)
        os.remove(self.testfile2)

    def test_add_file_to_resource(self):
        hs = hydroshare.hydroshare(authfile=(self.authfile))
        resid = hs.createResource((self.abstract), (self.title),
          (self.keywords),
          content_files=[])
        self.assertTrue(resid is not None)
        resid = hs.addContentToExistingResource(resid, [self.testfile])
        self.assertTrue(resid is not None)
        hs.hs.deleteResource(resid)
        hs.close()

    def test_add_wrong_path(self):
        hs = hydroshare.hydroshare(authfile=(self.authfile))
        resid = hs.createResource((self.abstract), (self.title),
          (self.keywords),
          content_files=[])
        self.assertTrue(resid is not None)
        with self.assertRaises(Exception):
            files = [
             'file_that_doesnt_exist.txt']
            resid = hs.addContentToExistingResource(resid, files)
        hs.hs.deleteResource(resid)
        hs.close()

    def test_add_multiple(self):
        hs = hydroshare.hydroshare(authfile=(self.authfile))
        resid = hs.createResource((self.abstract), (self.title),
          (self.keywords),
          content_files=[])
        self.assertTrue(resid is not None)
        files = [
         self.testfile, self.testfile2]
        resid = hs.addContentToExistingResource(resid, files)
        self.assertTrue(resid is not None)
        filenames = [r['file_name'] for r in hs.getResourceFiles(resid)]
        self.assertTrue(self.testfile in filenames)
        hs.hs.deleteResource(resid)
        hs.close()

    def test_file_already_exists(self):
        hs = hydroshare.hydroshare(authfile=(self.authfile))
        resid = hs.createResource((self.abstract), (self.title),
          (self.keywords),
          content_files=[
         self.testfile])
        self.assertTrue(resid is not None)
        with self.assertRaises(Exception):
            files = [
             self.testfile]
            resid = hs.addContentToExistingResource(resid, files)
        hs.hs.deleteResource(resid)
        hs.close()


if __name__ == '__main__':
    unittest.main()