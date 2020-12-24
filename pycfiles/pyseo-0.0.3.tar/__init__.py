# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/__init__.py
# Compiled at: 2016-02-21 15:55:31
import unittest, test_pysentosa, os, sys
TOP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, TOP_DIR)

def pysentosa_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_pysentosa)
    return suite