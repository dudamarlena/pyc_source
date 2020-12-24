# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python-fcc/tests/testcases.py
# Compiled at: 2011-04-16 22:45:28
import sys, unittest
sys.path.append('../')
from broadband_api import *
from FRNConversionsAPI import *
from block_conversion_api import *

class TestBroadbandAPI(unittest.TestCase):

    def setUp(self):
        self.bb = BroadbandApi()
        self.frnapi = FRNConversionsAPI()

    def test_Sweep(self):
        results = [
         True, True, False, False, False, False, False, False, False, False]
        for x in range(10):
            self.assertTrue((self.bb.get_data(latitude=41, longitude=-86 + x * 10)['status'] == 'OK') == results[x])

    def test_SF(self):
        result = self.bb.get_data(latitude=37, longitude=-122)
        self.assertTrue(result['status'] == 'OK')
        self.assertTrue('SpeedTestCounty' in result)

    def test_Chicago(self):
        result = self.bb.get_data(latitude=41, longitude=-87)
        self.assertTrue(result['status'] == 'OK')

    def test_Nowhere(self):
        result = self.bb.get_data(latitude=35, longitude=35)
        self.assertTrue(result['status'] == 'Fail')

    def test_FRN(self):
        result = self.frnapi.getInfo(frn='0017855545')
        self.assertTrue(result['Info']['frn'] == '0017855545')

    def test_companyName(self):
        result = self.frnapi.getInfo(frn='0017855545')
        self.assertTrue(result['Info']['companyName'] == 'Cygnus Telecommunications Corporation')

    def test_FRNapiIsDict(self):
        result1 = self.frnapi.getList(stateCode='IL')
        result2 = self.frnapi.getInfo(frn='0017855545')
        self.assertTrue(type(result1) == type({}) and type(result2) == type({}))

    def test_CygnusInIL(self):
        result = self.frnapi.getList(stateCode='IL')
        self.assertTrue('Cygnus Telecommunications Corporation' in [ x['companyName'] for x in result['Frns']['Frn'] ])


class TestBlockConversionAPI(unittest.TestCase):

    def setUp(self):
        self.bb = BlockConversionAPI()

    def test_SF(self):
        result = self.bb.get_block(latitude=37, longitude=-122)
        self.assertTrue(result['status'] == 'OK')
        self.assertTrue(result['State']['code'] == 'CA')
        self.assertTrue(result['Block']['FIPS'] == '060871001001002C')

    def test_Chicago(self):
        result = self.bb.get_block(latitude=41, longitude=-87)
        self.assertTrue(result['Block']['FIPS'] == '180739908004112')

    def test_Nowhere(self):
        result = self.bb.get_block(latitude=35, longitude=35)
        self.assertTrue(result['status'] == 'Fail')


if __name__ == '__main__':
    unittest.main()