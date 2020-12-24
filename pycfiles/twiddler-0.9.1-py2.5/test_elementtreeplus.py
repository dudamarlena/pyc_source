# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/tests/test_elementtreeplus.py
# Compiled at: 2008-07-24 14:48:01
import unittest
from doctest import DocFileSuite, ELLIPSIS

def test_suite():
    return unittest.TestSuite((
     DocFileSuite('elementtreeplus.txt', optionflags=ELLIPSIS),))


if __name__ == '__main__':
    unittest.main(default='test_suite')