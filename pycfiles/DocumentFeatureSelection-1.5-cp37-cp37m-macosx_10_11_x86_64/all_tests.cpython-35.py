# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/document-feature-selection/tests/all_tests.py
# Compiled at: 2017-02-23 10:26:28
# Size of source mod 2**32: 762 bytes
__author__ = 'kensuke-mi'
import sys, unittest
python_version = sys.version_info

def suite():
    suite = unittest.TestSuite()
    if python_version >= (3, 0, 0):
        from .test_data_converter import TestDataConverter
        from .test_PMI_python3 import TestPmiPython3
        from .test_tf_idf import TestTfIdf
        from .test_soa_python3 import TestSoaPython3
        from .test_bns_python3 import TestBnsPython3
        suite.addTest(unittest.makeSuite(TestDataConverter))
        suite.addTest(unittest.makeSuite(TestPmiPython3))
        suite.addTest(unittest.makeSuite(TestTfIdf))
        suite.addTest(unittest.makeSuite(TestSoaPython3))
        suite.addTest(unittest.makeSuite(TestBnsPython3))
    return suite