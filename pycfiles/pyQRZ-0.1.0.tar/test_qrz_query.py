# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zeb/code/git/pyQRZ/tests/test_qrz_query.py
# Compiled at: 2017-05-28 17:04:04
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