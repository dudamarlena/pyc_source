# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/referercredentials/tests.py
# Compiled at: 2007-08-27 17:51:44
"""HTTP-Referer Credentials Test Setup

$Id: tests.py 77105 2007-06-26 17:05:05Z srichter $
"""
__docformat__ = 'reStructuredText'
import unittest, zope.component
from zope.app.session import session, http, interfaces
from zope.app.testing import placelesssetup
from zope.testing import doctest
from zope.testing.doctestunit import DocFileSuite

def setUp(test):
    placelesssetup.setUp()
    zope.component.provideAdapter(session.ClientId)
    zope.component.provideAdapter(session.Session)
    zope.component.provideUtility(http.CookieClientIdManager(), interfaces.IClientIdManager)
    zope.component.provideUtility(session.PersistentSessionDataContainer(), interfaces.ISessionDataContainer)


def test_suite():
    return unittest.TestSuite((DocFileSuite('README.txt', setUp=setUp, tearDown=placelesssetup.tearDown, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')