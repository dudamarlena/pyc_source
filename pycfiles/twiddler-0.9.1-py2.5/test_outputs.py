# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/tests/test_outputs.py
# Compiled at: 2008-07-24 14:48:01
import unittest
from zope.testing.doctest import DocFileSuite, REPORT_NDIFF, ELLIPSIS
options = REPORT_NDIFF | ELLIPSIS

def test_suite():
    return unittest.TestSuite((
     DocFileSuite('../output/default.txt', optionflags=options),
     DocFileSuite('../output/emailer.txt', optionflags=options)))


if __name__ == '__main__':
    unittest.main(default='test_suite')