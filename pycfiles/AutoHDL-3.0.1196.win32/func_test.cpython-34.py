# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python34\Lib\site-packages\autohdl\test\verilog\func_test.py
# Compiled at: 2015-05-16 03:26:42
# Size of source mod 2**32: 1707 bytes
import os, unittest, sys
from autohdl import cache
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../..')
from autohdl.verilog import get_instances
import yaml

class FuncTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.was = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        cache.CACHE_LOAD = False
        cache.CACHE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/in/tmp'
        if not os.path.exists(cache.CACHE_PATH):
            os.mkdir(cache.CACHE_PATH)
        self.maxDiff = None

    @classmethod
    def tearDownClass(self):
        os.chdir(self.was)

    def test_get_instances(self):
        for f in os.listdir(os.path.dirname(os.path.abspath(__file__)) + '/in/func'):
            get_instances(os.path.dirname(os.path.abspath(__file__)) + '/in/func/' + f)
            with open(os.path.dirname(os.path.abspath(__file__)) + '/gold/func/' + f + 'cache') as (af):
                expected = yaml.load(af)
            with open(os.path.dirname(os.path.abspath(__file__)) + '/in/tmp/' + f + 'cache') as (af):
                actual = yaml.load(af)
            actual.pop('version')
            self.assertEqual(actual, expected)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FuncTest)
    res = unittest.TextTestRunner(verbosity=2).run(suite)
    print(res.wasSuccessful())