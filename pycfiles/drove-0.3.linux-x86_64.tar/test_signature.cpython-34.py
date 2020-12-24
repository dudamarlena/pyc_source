# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/tests/util/test_signature.py
# Compiled at: 2015-02-16 06:29:50
# Size of source mod 2**32: 737 bytes
import os, hashlib, unittest
from drove.util.signature import hmac_fd
RESULT_HASH = '58e788c2210dd61f5d040b814a1416e5526' + 'cf0ddf59b3f3462ae19ea696746ee'

class TestSignature(unittest.TestCase):

    def test_hmac_fd(self):
        """Testing util.signature.hmac_fd: default hahser"""
        sample_file = os.path.join(os.path.dirname(__file__), 'test_lexer.py')
        with open(sample_file, 'rb') as (f):
            self.assertEquals(hmac_fd(f), RESULT_HASH)
        with open(sample_file, 'rb') as (f):
            self.assertEquals(hmac_fd(f, hasher=hashlib.sha256()), RESULT_HASH)