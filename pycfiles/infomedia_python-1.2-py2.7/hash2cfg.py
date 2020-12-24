# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/exedre/Dropbox/exedre@gmail.com/Dropbox/Work/GeCo-dev/infomedia-1.0/build/lib/infomedia/hash2cfg/test/hash2cfg.py
# Compiled at: 2012-07-21 10:59:54
import unittest, infomedia
from infomedia.hash2cfg import *

class Hash2CfgTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_h2c_missing(self):
        self.assertIsNone(hash2cfg(None, 'test'))
        self.assertIsNone(hash2cfg([1, 2], 'test'))
        self.assertIsNone(hash2cfg('test', 'test'))
        return

    def test_c2h_exception(self):
        self.assertRaises(ConfigNotExistsError, cfg2hash, 'file_not_found')
        self.assertRaises(ConfigNotProtectedError, cfg2hash, '/etc/passwd', secure=True)

    def test_c2h_base_file(self):
        open('/tmp/test.1', 'w').write('\nNO INI FILE HERE\n            ')
        self.assertRaises(ParseError, cfg2hash, '/tmp/test.1')
        open('/tmp/test.1', 'w').write('\nA=1\nB=2\nC=3\n            ')
        self.assertRaises(MissingSectionHeaderError, cfg2hash, '/tmp/test.1')
        open('/tmp/test.1', 'w').write('\n[SEC]\nA=1\nB=2\nC=3\n            ')
        self.assertEqual({'SEC': {'A': '1', 'B': '2', 'C': '3'}}, cfg2hash('/tmp/test.1', extra=False))