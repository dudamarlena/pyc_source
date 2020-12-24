# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/zeb/code/git/pyQRZ/tests/test_qrz_query.py
# Compiled at: 2017-05-28 17:04:04
# Size of source mod 2**32: 1247 bytes
import os, sys, unittest
sys.path.insert(0, os.path.abspath('..'))
from qrz import QRZ, CallsignNotFound, QRZerror
VALID_SESSION = '\n<?xml version="1.0" ?> \n<QRZDatabase version="1.33">\n  <Session>\n    <Key>2331uf894c4bd29f3923f3bacf02c532d7bd9</Key> \n    <Count>123</Count> \n    <SubExp>Wed Jan 1 12:34:03 2013</SubExp> \n    <GMTime>Sun Aug 16 03:51:47 2012</GMTime> \n  </Session>\n</QRZDatabase>\n'

class test_QRZ(unittest.TestCase):

    def test_all(self):
        qrz = QRZ()
        result = qrz.callsign('w7atc')
        self.assertEqual(result['fname'], 'ZEB M')
        self.assertEqual(result['name'], 'PALMER')
        self.assertEqual(result['addr2'], 'Nampa')
        self.assertEqual(result['state'], 'ID')
        self.assertEqual(result['country'], 'United States')

    def test_session_expire(self):
        qrz = QRZ()
        result = qrz.callsign('w7atc')
        self.assertEqual(result['fname'], 'ZEB M')
        qrz._session_key += '_test_invalid'
        result = qrz.callsign('w7atc')
        self.assertEqual(result['fname'], 'ZEB M')

    def test_invalid_callsign(self):
        qrz = QRZ()
        with self.assertRaises(CallsignNotFound) as (context):
            result = qrz.callsign('w7atcw7atc')