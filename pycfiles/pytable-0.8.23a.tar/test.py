# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/tests/test.py
# Compiled at: 2004-09-01 13:19:13
"""Test everything in one go"""
import unittest, types

def moduleSuite(module):
    return unittest.TestLoader().loadTestsFromModule(module)


import test_basic, test_dbdriver, test_dbschema, test_schemabuilder, test_sqlgeneration, test_lazyresultset, test_datatypedetermination, test_foreignkeyprop, test_dbrow, test_namespaces
suite = unittest.TestSuite([ moduleSuite(module) for module in [test_schemabuilder, test_basic, test_dbdriver, test_dbschema, test_sqlgeneration, test_lazyresultset, test_datatypedetermination, test_foreignkeyprop, test_dbrow, test_namespaces] ])
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)