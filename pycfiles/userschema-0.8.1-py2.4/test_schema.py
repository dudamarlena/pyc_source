# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/userschema/tests/test_schema.py
# Compiled at: 2007-01-23 12:52:22
"""Unit tests for the schema module.

$Id: test_schema.py,v 1.3 2007/01/23 17:52:22 tseaver Exp $
"""
import unittest

def test_suite():
    from zope.testing.doctest import DocFileTest
    return unittest.TestSuite((DocFileTest('csv-schema.txt', package='userschema'), DocFileTest('html-form-schema.txt', package='userschema'), DocFileTest('etree-schema.txt', package='userschema')))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')