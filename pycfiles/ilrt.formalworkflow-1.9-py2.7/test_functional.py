# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ilrt/formalworkflow/tests/test_functional.py
# Compiled at: 2013-06-23 12:02:23
import unittest
from Testing import ZopeTestCase as ztc
from ilrt.formalworkflow.tests import base

def test_suite():
    return unittest.TestSuite([
     ztc.ZopeDocFileSuite('tests/workflowprocess.txt', package='ilrt.formalworkflow', test_class=base.BaseFunctionalTestCase),
     ztc.ZopeDocFileSuite('tests/editorpastedelete.txt', package='ilrt.formalworkflow', test_class=base.BaseFunctionalTestCase),
     ztc.ZopeDocFileSuite('tests/iterationlocation.txt', package='ilrt.formalworkflow', test_class=base.BaseFunctionalTestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')