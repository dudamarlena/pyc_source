# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/test/functions/test_logical_functions.py
# Compiled at: 2012-06-19 10:10:37
"""NDG XACML tests for logical functions

NERC DataGrid
"""
__author__ = 'R B Wilkinson'
__date__ = '13/03/12'
__copyright__ = ''
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: test_logical_functions.py 8078 2012-06-19 14:10:35Z pjkersha $'
import logging
from os import path
import unittest
from ndg.xacml.parsers.etree.factory import ReaderFactory
from ndg.xacml.core.context.pdp import PDP
from ndg.xacml.core.context.result import Decision
from ndg.xacml.test.context import XacmlContextBaseTestCase
logging.basicConfig(level=logging.DEBUG)
THIS_DIR = path.dirname(__file__)
XACML_NOTTEST_FILEPATH = path.join(THIS_DIR, 'policy_not.xml')
XACML_ANDTEST_FILEPATH = path.join(THIS_DIR, 'policy_and.xml')

class Test(XacmlContextBaseTestCase):
    RESOURCE1_ID = 'http://localhost/resource1'
    RESOURCE2_ID = 'http://localhost/resource2'
    RESOURCE3_ID = 'http://localhost/resource3'
    RESOURCE4_ID = 'http://localhost/resource4'
    RESOURCE5_ID = 'http://localhost/resource5'
    RESOURCE6_ID = 'http://localhost/resource6'
    RESOURCE7_ID = 'http://localhost/resource7'

    def test01_01NotTrue(self):
        self.pdp = PDP.fromPolicySource(XACML_NOTTEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE1_ID, subjectRoles=('role1', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test01_02NotFalse(self):
        self.pdp = PDP.fromPolicySource(XACML_NOTTEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE2_ID, subjectRoles=('role1', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test02_01And0Args(self):
        self.pdp = PDP.fromPolicySource(XACML_ANDTEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE1_ID, subjectRoles=('role1', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test02_02And1ArgTrue(self):
        self.pdp = PDP.fromPolicySource(XACML_ANDTEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE2_ID, subjectRoles=('role1', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test02_03And1ArgFalse(self):
        self.pdp = PDP.fromPolicySource(XACML_ANDTEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE3_ID, subjectRoles=('role1', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test02_04And2ArgsTrue(self):
        self.pdp = PDP.fromPolicySource(XACML_ANDTEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE4_ID, subjectRoles=('role1',
                                                                                    'role2'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test02_05And2ArgsFalse(self):
        self.pdp = PDP.fromPolicySource(XACML_ANDTEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE5_ID, subjectRoles=('role1',
                                                                                    'role2'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test02_06And3ArgsTrue(self):
        self.pdp = PDP.fromPolicySource(XACML_ANDTEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE6_ID, subjectRoles=('role1',
                                                                                    'role2',
                                                                                    'role3'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test02_07And3ArgsFalse(self):
        self.pdp = PDP.fromPolicySource(XACML_ANDTEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE7_ID, subjectRoles=('role1',
                                                                                    'role2',
                                                                                    'role3'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return


if __name__ == '__main__':
    unittest.main()