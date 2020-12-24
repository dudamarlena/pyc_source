# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/runner.py
# Compiled at: 2018-12-13 08:22:07
import sys, unittest
from tests import test_converter, test_transformer, test_fourier_filter, test_stog
loader = unittest.TestLoader()
suite = unittest.TestSuite()
suite.addTests(loader.loadTestsFromModule(test_converter))
suite.addTests(loader.loadTestsFromModule(test_transformer))
suite.addTests(loader.loadTestsFromModule(test_fourier_filter))
suite.addTests(loader.loadTestsFromModule(test_stog))
runner = unittest.TextTestRunner(verbosity=3, buffer=True)
result = runner.run(suite).wasSuccessful()
sys.exit(not result)