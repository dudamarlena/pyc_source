# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/test/context/test_pdp_with_first_applicable_rule_combining_algorithm.py
# Compiled at: 2011-10-13 03:46:34
"""
Created on 26 Aug 2011

@author: rwilkinson
"""
import logging, unittest
from ndg.xacml.parsers.etree.factory import ReaderFactory
from ndg.xacml.core.context.pdp import PDP
from ndg.xacml.core.context.result import Decision
from ndg.xacml.test import XACML_FIRSTAPPLICABLE_FILEPATH
from ndg.xacml.test.context import XacmlContextBaseTestCase
logging.basicConfig(level=logging.DEBUG)

class Test(XacmlContextBaseTestCase):
    NOT_APPLICABLE_RESOURCE_ID = 'https://localhost'
    PRIVATE_RESOURCE_ID = 'http://localhost/private-resource'
    PUBLIC_RESOURCE_ID = 'http://localhost/resource-only-restricted'
    NOT_APPLICABLE_RESOURCE_ID = 'https://localhost'
    SINGLE_SUBJECT_ROLE_RESTRICTED_ID = 'http://localhost/single-subject-role-restricted'
    ACTION_AND_SINGLE_SUBJECT_ROLE_RESTRICTED_ID = 'http://localhost/action-and-single-subject-role-restricted'
    AT_LEAST_ONE_SUBJECT_ROLE_RESTRICTED_ID = 'http://localhost/at-least-one-of-subject-role-restricted'
    LEVEL1_ID = 'http://localhost/hierarchy/dir1'
    LEVEL2_ID = 'http://localhost/hierarchy/dir1/dir2'
    LEVEL3_ID = 'http://localhost/hierarchy/dir1/dir2/dir3'
    LEVEL1_NOINHERIT_ID = 'http://localhost/hierarchynoinherit/dir1'
    LEVEL2_NOINHERIT_ID = 'http://localhost/hierarchynoinherit/dir1/dir2'
    LEVEL3_NOINHERIT_ID = 'http://localhost/hierarchynoinherit/dir1/dir2/dir3'

    def setUp(self):
        self.pdp = PDP.fromPolicySource(XACML_FIRSTAPPLICABLE_FILEPATH, ReaderFactory)

    def test01NotApplicable(self):
        request = self._createRequestCtx(self.__class__.NOT_APPLICABLE_RESOURCE_ID)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.NOT_APPLICABLE, 'Expecting not applicable decision')

        return

    def test02PublicallyAccessibleResource(self):
        request = self._createRequestCtx(self.__class__.PUBLIC_RESOURCE_ID, includeSubject=False)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test03PrivateResource(self):
        request = self._createRequestCtx(self.__class__.PRIVATE_RESOURCE_ID)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test04SingleSubjectRoleRestrictedResource(self):
        request = self._createRequestCtx(self.__class__.SINGLE_SUBJECT_ROLE_RESTRICTED_ID)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test05SingleSubjectRoleRestrictedResourceDeniesAccess(self):
        request = self._createRequestCtx(self.__class__.SINGLE_SUBJECT_ROLE_RESTRICTED_ID, subjectRoles=('student', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test06ActionAndSingleSubjectRoleRestrictedResource(self):
        request = self._createRequestCtx(self.__class__.ACTION_AND_SINGLE_SUBJECT_ROLE_RESTRICTED_ID)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test07ActionAndSingleSubjectRoleRestrictedResourceDeniesAccess(self):
        request = self._createRequestCtx(self.__class__.ACTION_AND_SINGLE_SUBJECT_ROLE_RESTRICTED_ID, action='write')
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test10HierachyLevel1Resource(self):
        request = self._createRequestCtx(self.__class__.LEVEL1_ID, subjectRoles=('postdoc', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test11HierachyLevel1Resource(self):
        request = self._createRequestCtx(self.__class__.LEVEL1_ID, subjectRoles=('admin', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test12HierachyLevel2Resource(self):
        request = self._createRequestCtx(self.__class__.LEVEL2_ID, subjectRoles=('admin', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test13HierachyLevel2Resource(self):
        request = self._createRequestCtx(self.__class__.LEVEL2_ID, subjectRoles=('staff', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test14HierachyLevel3Resource(self):
        request = self._createRequestCtx(self.__class__.LEVEL3_ID, subjectRoles=('staff', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test15HierachyLevel3Resource(self):
        request = self._createRequestCtx(self.__class__.LEVEL3_ID, subjectRoles=('postdoc', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test16HierachyLevel3Resource(self):
        request = self._createRequestCtx(self.__class__.LEVEL3_ID, subjectRoles=('admin', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test20HierachyLevel1Resource(self):
        request = self._createRequestCtx(self.__class__.LEVEL1_NOINHERIT_ID, subjectRoles=('postdoc', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test21HierachyLevel1Resource(self):
        request = self._createRequestCtx(self.__class__.LEVEL1_NOINHERIT_ID, subjectRoles=('admin', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test22HierachyLevel2Resource(self):
        request = self._createRequestCtx(self.__class__.LEVEL2_NOINHERIT_ID, subjectRoles=('admin', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test23HierachyLevel2Resource(self):
        request = self._createRequestCtx(self.__class__.LEVEL2_NOINHERIT_ID, subjectRoles=('staff', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test24HierachyLevel3Resource(self):
        request = self._createRequestCtx(self.__class__.LEVEL3_NOINHERIT_ID, subjectRoles=('staff', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test25HierachyLevel3Resource(self):
        request = self._createRequestCtx(self.__class__.LEVEL3_NOINHERIT_ID, subjectRoles=('postdoc', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test26HierachyLevel3Resource(self):
        request = self._createRequestCtx(self.__class__.LEVEL3_NOINHERIT_ID, subjectRoles=('admin', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return


if __name__ == '__main__':
    unittest.main()