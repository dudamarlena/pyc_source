# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/test/context/test_pdp_with_match_combinations.py
# Compiled at: 2011-10-13 03:46:34
"""
Created on 26 Aug 2011

@author: rwilkinson
"""
import logging, unittest
from ndg.xacml.parsers.etree.factory import ReaderFactory
from ndg.xacml.core.context.pdp import PDP
from ndg.xacml.core.context.result import Decision
from ndg.xacml.test import XACML_SUBJECTMATCH_FILEPATH
from ndg.xacml.test.context import XacmlContextBaseTestCase
logging.basicConfig(level=logging.DEBUG)

class Test(XacmlContextBaseTestCase):
    NOT_APPLICABLE_RESOURCE_ID = 'https://localhost'
    RESOURCE_ID = 'http://localhost/role-combinations'

    def setUp(self):
        self.pdp = PDP.fromPolicySource(XACML_SUBJECTMATCH_FILEPATH, ReaderFactory)

    def test01_01RoleCombination1(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_ID, subjectRoles=('role1',
                                                                                   'role2',
                                                                                   'role3'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test01_02RoleCombination1(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_ID, subjectRoles=('role1',
                                                                                   'role2'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test01_03RoleCombination1(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_ID, subjectRoles=('role1',
                                                                                   'role3'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test01_04RoleCombination1(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_ID, subjectRoles=('role2',
                                                                                   'role3'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test01_05RoleCombination1(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_ID, subjectRoles=('role1', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test01_06RoleCombination1(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_ID, subjectRoles=('role2', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test01_07RoleCombination1(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_ID, subjectRoles=('role3', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test01_08RoleCombination1(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_ID, subjectRoles=('role1',
                                                                                   'role2',
                                                                                   'role3',
                                                                                   'role5'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test02_01RoleCombination1(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_ID, subjectRoles=('role4', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test02_02RoleCombination1(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_ID, subjectRoles=('role2',
                                                                                   'role4'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test03_01RoleCombination3(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_ID, subjectRoles=('role5',
                                                                                   'role6'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test03_02RoleCombination3(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_ID, subjectRoles=('role2',
                                                                                   'role3',
                                                                                   'role5',
                                                                                   'role6'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test03_03RoleCombination3(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_ID, subjectRoles=('role1',
                                                                                   'role3',
                                                                                   'role5'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test03_04RoleCombination3(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_ID, subjectRoles=('role1',
                                                                                   'role3',
                                                                                   'role6'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test04_01RoleAllCombinations(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_ID, subjectRoles=('role1',
                                                                                   'role2',
                                                                                   'role3',
                                                                                   'role4',
                                                                                   'role5',
                                                                                   'role6'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return


if __name__ == '__main__':
    unittest.main()