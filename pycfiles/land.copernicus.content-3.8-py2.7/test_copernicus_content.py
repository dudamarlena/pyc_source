# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/tests/test_copernicus_content.py
# Compiled at: 2017-09-19 09:07:49
""" Test suites for eea.indicators
"""
import unittest, doctest
from Testing import ZopeTestCase as ztc
from land.copernicus.content.tests import base
OPTION_FLAGS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    contenttypes = ztc.ZopeDocFileSuite('doc/contenttypes.txt', package='land.copernicus.content', test_class=base.BaseCopernicusContentTestCase, optionflags=OPTION_FLAGS)
    overview = ztc.FunctionalDocFileSuite('doc/overview.txt', package='land.copernicus.content', test_class=base.BaseCopernicusContentTestCase, optionflags=OPTION_FLAGS)
    return unittest.TestSuite([contenttypes, overview])