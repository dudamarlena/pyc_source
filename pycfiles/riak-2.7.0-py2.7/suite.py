# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/tests/suite.py
# Compiled at: 2016-10-17 19:06:50
import os.path, unittest

def additional_tests():
    top_level = os.path.join(os.path.dirname(__file__), '../../')
    start_dir = os.path.dirname(__file__)
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().discover(start_dir, top_level_dir=top_level))
    return suite