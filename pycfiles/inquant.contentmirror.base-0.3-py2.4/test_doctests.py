# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/inquant/contentmirror/base/tests/test_doctests.py
# Compiled at: 2008-04-14 11:51:37
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 57037 $'
__version__ = '$Revision: 57037 $'[11:-2]
import unittest, doctest
from Testing import ZopeTestCase as ztc
from inquant.contentmirror.base.tests import base
doctests = ('README.rst').split()

def test_suite():
    return unittest.TestSuite([ ztc.ZopeDocFileSuite(dtfile, package='inquant.contentmirror.base', test_class=base.CMFunctionalTestCase, optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE) for dtfile in doctests ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')