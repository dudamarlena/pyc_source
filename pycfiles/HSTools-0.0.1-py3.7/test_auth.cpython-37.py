# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/test/test_auth.py
# Compiled at: 2019-10-03 09:54:39
# Size of source mod 2**32: 1129 bytes
import os, unittest
from hstools import auth

class TestAuth(unittest.TestCase):
    bauthfile = os.path.abspath('./test/hs_auth_basic')
    oauthfile = os.path.abspath('./test/hs_auth_oauth')

    def test_oauth(self):
        with self.assertRaises(Exception):
            hs = auth.oauth2_authorization(authfile='/tmp/auth')
            hs.session.close()
        hs = auth.oauth2_authorization(authfile=(self.oauthfile))
        self.assertTrue(hs is not None)
        hs.session.close()

    def test_basic_auth(self):
        with self.assertRaises(Exception):
            hs = auth.oauth2_authorization(authfile='/tmp/auth')
            hs.session.close()
        hs = auth.basic_authorization(authfile=(self.bauthfile))
        self.assertTrue(hs is not None)
        hs.session.close()


if __name__ == '__main__':
    unittest.main()