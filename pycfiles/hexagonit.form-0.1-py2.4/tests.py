# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hexagonit/form/tests.py
# Compiled at: 2006-10-07 14:17:38
import unittest
from doctest import DocFileSuite, ELLIPSIS

def test_suite():
    return unittest.TestSuite((DocFileSuite('orderable.txt', package='hexagonit.form.orderable', optionflags=ELLIPSIS),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')