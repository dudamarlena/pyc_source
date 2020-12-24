# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/resolve/tests/test_docs.py
# Compiled at: 2008-11-24 11:46:12
import unittest
from doctest import DocFileSuite, REPORT_NDIFF, ELLIPSIS
options = REPORT_NDIFF | ELLIPSIS

def test_suite():
    return unittest.TestSuite((
     DocFileSuite('../readme.txt', optionflags=options),))