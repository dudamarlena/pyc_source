# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/jyu/portalview/tests/test_doctest.py
# Compiled at: 2009-11-16 03:44:25
import unittest, doctest
from zope.testing import doctestunit
from zope.component import testing, eventtesting
from Testing import ZopeTestCase as ztc
from jyu.portalview.tests import base
import interlude

def test_suite():
    return unittest.TestSuite([ztc.ZopeDocFileSuite('README.txt', package='jyu.portalview', test_class=base.FunctionalTestCase, optionflags=doctest.IGNORE_EXCEPTION_DETAIL | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, globs=dict(interact=interlude.interact))])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')