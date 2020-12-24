# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jquery/widget/resteditor/tests.py
# Compiled at: 2007-05-24 08:27:53
"""jquery.resteditor Test Module

$Id: test_doc.py 276 2007-05-19 22:00:47Z roger.ineichen $
"""
__docformat__ = 'reStructuredText'
import unittest
from zope.testing import doctest
from zope.app.testing import placelesssetup
from z3c.form import testing

def test_suite():
    return unittest.TestSuite((doctest.DocFileSuite('README.txt', setUp=testing.setUp, tearDown=testing.tearDown, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),))