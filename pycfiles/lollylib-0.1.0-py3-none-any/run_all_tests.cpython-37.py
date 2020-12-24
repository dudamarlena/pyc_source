# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\ASSETS\PROG_PYTHON\2019\lollylib\lollylib\tests\run_all_tests.py
# Compiled at: 2019-06-20 11:51:21
# Size of source mod 2**32: 151 bytes
import unittest
loader = unittest.TestLoader()
start_dir = '.'
suite = loader.discover(start_dir)
runner = unittest.TextTestRunner()
runner.run(suite)