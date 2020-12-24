# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/test/context/test_pdp.py
# Compiled at: 2012-06-19 10:10:36
"""NDG XACML PDP unit tests 

NERC DataGrid
"""
__author__ = 'P J Kershaw'
__date__ = '28/10/10'
__copyright__ = '(C) 2010 Science and Technology Facilities Council'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: test_pdp.py 8078 2012-06-19 14:10:35Z pjkersha $'
import unittest, logging
logging.basicConfig(level=logging.DEBUG)
from ndg.xacml.core.context.result import Decision
from ndg.xacml.test.context import XacmlContextBaseTestCase, TestContextHandler

class XacmlEvalPdpWithPermitOverridesPolicyTestCase(XacmlContextBaseTestCase):
    """Test PDP with permit overrides rule combining algorithm"""
    NOT_APPLICABLE_RESOURCE_ID = 'https://localhost'
    PRIVATE_RESOURCE_ID = 'http://localhost/private-resource'
    PUBLIC_RESOURCE_ID = 'http://localhost/resource-only-restricted'
    NOT_APPLICABLE_RESOURCE_ID = 'https://localhost'
    SINGLE_SUBJECT_ROLE_RESTRICTED_ID = 'http://localhost/single-subject-role-restricted'
    ACTION_AND_SINGLE_SUBJECT_ROLE_RESTRICTED_ID = 'http://localhost/action-and-single-subject-role-restricted'
    AT_LEAST_ONE_SUBJECT_ROLE_RESTRICTED_ID = 'http://localhost/at-least-one-of-subject-role-restricted'

    def setUp(self):
        self.pdp = self._createPDPfromNdgTest1Policy()

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

    def test08AtLeastOneSubjectRoleResource(self):
        request = self._createRequestCtx(self.__class__.AT_LEAST_ONE_SUBJECT_ROLE_RESTRICTED_ID, action='write')
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test09AtLeastOneSubjectRoleResourceDeniesAccess(self):
        request = self._createRequestCtx(self.__class__.AT_LEAST_ONE_SUBJECT_ROLE_RESTRICTED_ID, subjectRoles=('student', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test10PipAddsRequiredAttributeValToEnableAccess(self):
        ctxHandler = TestContextHandler()
        ctxHandler.pdp = self.pdp
        request = self._createRequestCtx(self.__class__.AT_LEAST_ONE_SUBJECT_ROLE_RESTRICTED_ID, subjectRoles=('student', ))
        response = ctxHandler.handlePEPRequest(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting PERMIT decision')

        return


if __name__ == '__main__':
    unittest.main()