# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/tests/test_all.py
# Compiled at: 2019-07-15 11:59:22
# Size of source mod 2**32: 123 bytes
import unittest
all_tests = unittest.TestLoader().discover('./tests')
unittest.TextTestRunner(verbosity=1).run(all_tests)