# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/ploneformgen/readonlystringfield/tests/test_docs.py
# Compiled at: 2009-03-24 10:52:00
import unittest, doctest
from Testing import ZopeTestCase as ztc
from quintagroup.ploneformgen.readonlystringfield.tests.base import ReadOnlyStringFieldFunctionalTestCase

def test_suite():
    return unittest.TestSuite([ztc.FunctionalDocFileSuite('readonlystringfield.txt', package='quintagroup.ploneformgen.readonlystringfield.tests', test_class=ReadOnlyStringFieldFunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)])