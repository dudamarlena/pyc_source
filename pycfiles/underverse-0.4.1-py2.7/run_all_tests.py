# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\underverse\tests\run_all_tests.py
# Compiled at: 2012-02-20 12:39:35
import unittest, os
from load_tests import LoadTestCase
from find_tests import FindTestCase
from mapreduce_tests import MapReduceTestCase
from kv_test import KeyValueTestCase
from underverse import Underverse
from underverse.model import Document
from test_data_gen import Person
if __name__ == '__main__':
    uv = Underverse()
    test = uv.test_obj
    test.purge()
    data = []
    for p in range(250):
        data.append(Person())

    test.add(data)
    uv.dump('speed_test_smaller_obj.sql')
    if not os.path.exists('speed_test_smaller.sql'):
        uv = Underverse()
        test = uv.test
        test.purge()
        data = []
        for p in range(250):
            data.append(Person().__dict__)

        test.add(data)
        uv.dump('speed_test_smaller.sql')
    suite1 = unittest.TestLoader().loadTestsFromTestCase(LoadTestCase)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(FindTestCase)
    suite3 = unittest.TestLoader().loadTestsFromTestCase(MapReduceTestCase)
    suite4 = unittest.TestLoader().loadTestsFromTestCase(KeyValueTestCase)
    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([suite1, suite2, suite3, suite4]))