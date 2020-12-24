# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mailtoplone/contentrules/tests/test_doctests.py
# Compiled at: 2008-02-29 08:26:12
__author__ = 'Hans-Peter Locher <hans-peter.locher@inquant.de>'
__docformat__ = 'plaintext'
import unittest, doctest
from Testing import ZopeTestCase as ztc
from mailtoplone.contentrules.tests import base
doctests = [
 'README.rst']

def test_suite():
    return unittest.TestSuite([ ztc.ZopeDocFileSuite(dtfile, package='mailtoplone.contentrules', test_class=base.MailToPloneContentrulesFunctionalTestCase, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS) for dtfile in doctests ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')