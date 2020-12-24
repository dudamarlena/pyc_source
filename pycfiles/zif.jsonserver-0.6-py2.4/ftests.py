# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zif/jsonserver/ftests.py
# Compiled at: 2007-05-25 16:54:18
"""Functional tests for JSON Views
Original file z.a.publisher.xmlrpc/ftests.py
$Id: ftests.py 23 2006-12-16 17:08:48Z jwashin $
Mod by jmw 7 Oct 06 for JSON Views
"""
import zope.interface, zope.app.folder.folder, zope.publisher.interfaces.browser
from zope.app.testing import ztapi, functional, setup

def setUp(test):
    setup.setUpTestAsModule(test, 'zif.jsonserver.JSONViews')


def tearDown(test):
    ztapi.provideView(zope.app.folder.folder.IFolder, zope.publisher.interfaces.browser.IBrowserRequest, zope.interface, 'folderlist', None)
    ztapi.provideView(zope.app.folder.folder.IFolder, zope.publisher.interfaces.browser.IBrowserRequest, zope.interface, 'sum', None)
    ztapi.provideView(zope.app.folder.folder.IFolder, zope.publisher.interfaces.browser.IBrowserRequest, zope.interface, 'sum_form.html', None)
    setup.tearDownTestAsModule(test)
    return


def test_suite():
    return functional.FunctionalDocFileSuite('JSONViews.txt', setUp=setUp, tearDown=tearDown)


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='test_suite')