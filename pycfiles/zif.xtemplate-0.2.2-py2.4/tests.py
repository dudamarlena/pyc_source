# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zif/xtemplate/tests.py
# Compiled at: 2007-08-25 13:41:36
"""Unit tests for HTML Sanitizer
Original file z.a.publisher.xmlrpc/ftests.py
$Id: tests.py 23 2007-03-19 jwashin $
"""
import zope.interface, zope.publisher.interfaces.browser
from zope.testing import doctest
from zope.testing.doctestunit import DocTestSuite
import unittest

def test_suite():
    suite = unittest.TestSuite(doctest.DocFileSuite('sanitizer_README.txt', optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))
    suite.addTest(DocTestSuite('zif.xtemplate.lxmlhtmlutils'))
    return suite


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='test_suite')