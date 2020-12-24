# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/test/test_download.py
# Compiled at: 2019-10-03 09:57:34
# Size of source mod 2**32: 1870 bytes
import os, shutil, unittest
from hstools import hydroshare

class TestDownload(unittest.TestCase):
    authfile = os.path.abspath('test/hs_auth_oauth')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_set_directory(self):
        """
        tests that the download directory is set properly
        """
        hs = hydroshare.hydroshare(authfile=(self.authfile))
        self.assertTrue(hs.download_dir == '.')
        hs.close()
        with self.assertRaises(Exception) as (context):
            hs = hydroshare.hydroshare(authfile=(self.authfile), save_dir='/dir_doesnt_exist')
        self.assertTrue('does not exist' in str(context.exception))
        hs.close()
        d = 'test_directory_please_remove'
        os.makedirs(d)
        hs = hydroshare.hydroshare(authfile=(self.authfile), save_dir=d)
        self.assertTrue(hs.download_dir == d)
        hs.close()
        os.rmdir(d)

    def test_get_file(self):
        d = os.path.join(os.path.dirname(__file__), 'test_directory_please_remove')
        os.makedirs(d)
        hs = hydroshare.hydroshare(authfile=(self.authfile), save_dir=d)
        self.assertTrue(hs.download_dir == d)
        resid = '1be4d7902c87481d85b93daad99cf471'
        hs.getResource(resid)
        self.assertTrue(os.path.exists(os.path.join(d, f"{resid}")))
        hs.close()
        shutil.rmtree(d)


if __name__ == '__main__':
    unittest.main()