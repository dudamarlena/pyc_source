# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/test/test_create.py
# Compiled at: 2019-10-10 13:37:25
# Size of source mod 2**32: 2447 bytes
import os, shutil, unittest
from hstools import hydroshare
from hstools.resource import ResourceMetadata

class TestCreate(unittest.TestCase):
    testfile = 'testfile.txt'
    authfile = os.path.abspath('test/hs_auth_oauth')

    def setUp(self):
        with open(self.testfile, 'w') as (f):
            f.write('this is a test file')

    def tearDown(self):
        os.remove(self.testfile)

    def test_no_files(self):
        title = 'unit testing'
        abstract = 'this is a resource created by a unittest'
        keywords = ['test']
        hs = hydroshare.hydroshare(authfile=(self.authfile))
        resid = hs.createResource(abstract, title,
          keywords,
          content_files=[])
        self.assertTrue(resid is not None)
        scimeta = hs.getResourceMetadata(resid)
        self.assertTrue(type(scimeta) == ResourceMetadata)
        hs.hs.deleteResource(resid)
        hs.close()

    def test_file_doesnt_exist(self):
        title = 'unit testing'
        abstract = 'this is a resource created by a unittest'
        keywords = ['test']
        hs = hydroshare.hydroshare(authfile=(self.authfile))
        with self.assertRaises(Exception):
            resid = hs.createResource(abstract, title,
              keywords,
              content_files=[
             'wrong_name.txt'])
        hs.close()

    def test_one_file(self):
        title = 'unit testing'
        abstract = 'this is a resource created by a unittest'
        keywords = ['test']
        hs = hydroshare.hydroshare(authfile=(self.authfile))
        resid = hs.createResource(abstract, title,
          keywords,
          content_files=[
         self.testfile])
        self.assertTrue(resid is not None)
        scimeta = hs.getResourceMetadata(resid)
        self.assertTrue(type(scimeta) == ResourceMetadata)
        hs.hs.deleteResource(resid)
        hs.close()


if __name__ == '__main__':
    unittest.main()