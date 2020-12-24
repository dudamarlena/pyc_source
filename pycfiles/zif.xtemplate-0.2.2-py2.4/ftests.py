# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zif/xtemplate/ftests.py
# Compiled at: 2007-08-25 13:41:36
"""Functional tests for JSON Views
Original file z.a.publisher.xmlrpc/ftests.py
$Id: ftests.py 23 2006-12-16 17:08:48Z jwashin $
Mod by jmw 7 Oct 06 for JSON Views
"""
import zope.interface, zope.app.folder.folder, zope.publisher.interfaces.browser
from zope.app.testing import ztapi, functional, setup
from zope.testing import doctest

def setUp(test):
    setup.setUpTestAsModule(test, 'zif.xtemplate.README')


def tearDown(test):
    setup.tearDownTestAsModule(test)


def test_suite():
    return functional.FunctionalDocFileSuite('README.txt', setUp=setUp, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='test_suite')