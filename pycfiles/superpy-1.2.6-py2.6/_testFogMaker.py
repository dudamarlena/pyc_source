# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\superpy\demos\pyfog\_testFogMaker.py
# Compiled at: 2010-06-04 07:07:11
"""Module to create test suite to test fog maker.

This lets you test things by doing something like

  "python setup.py test -m superpy.demos.pyfog._testFogMaker"

from the top-level directory.
"""
import unittest, doctest, fogMaker
test_suite = unittest.TestSuite()
test_suite.addTest(doctest.DocTestSuite(fogMaker))