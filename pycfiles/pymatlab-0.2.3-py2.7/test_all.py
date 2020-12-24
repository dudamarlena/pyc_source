# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_all.py
# Compiled at: 2013-10-24 08:37:24
import unittest, doctest
from tests import t_matlab

def test_suite():
    return unittest.TestSuite([
     t_matlab.test_suite(),
     doctest.DocFileSuite('../../README.txt')])