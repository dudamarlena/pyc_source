# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/c2/sample/csvworkflow/tests/testSetup.py
# Compiled at: 2010-06-17 01:27:12
import unittest, Testing
from plone.app.contentrules.tests.base import ContentRulesTestCase
from Products.CMFCore.permissions import AccessContentsInformation
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import ListFolderContents
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import _checkPermission as checkPerm
from unittest import TestSuite, makeSuite
from WFtest import *
from c2.sample.csvworkflow.tests.base import C2CsvworkflowTestCase

class TestWorkflowAction(C2CsvworkflowTestCase):

    def afterSetUp(self):
        workflow_id = 'c2.sample.csvworkflow'
        self.workflow = self.portal.portal_workflow
        self.workflow.setDefaultChain(workflow_id)
        self.portal.acl_users._doAddUser('test_user', 'secret', ['Manager'], [])
        self.folder.invokeFactory('Document', 'd1')
        self.doc = self.folder.d1

    def testInitialState(self):
        initial_state = 'private'
        self.assertEquals(self.workflow.getInfoFor(self.doc, 'review_state'), initial_state)

    def testAllState(self):
        workflow_id = self.workflow.getChainFor(self.doc)[0]
        states = ['private', 'pending', 'published']
        wft = WFtest()
        self.assertEqual(set(wft.getWorkflowStateById(self.workflow, workflow_id)), set(states))

    def testTransitionAction(self):
        route_newstate = [
         ('submit', 'pending'),
         ('publish', 'published'),
         ('reject', 'private')]
        self.login('test_user')
        for (transition, new_state) in route_newstate:
            self.doc.portal_workflow.doActionFor(self.doc, transition)
            self.assertEquals(self.workflow.getInfoFor(self.doc, 'review_state'), new_state)

    def testTransitions(self):
        route = ['submit', 'publish']
        roles = ['Reviewer']
        transitions = ['reject']
        wft = WFtest()
        self.login('test_user')
        wft.doActionLoop(self.doc, route)
        self.portal.acl_users._doAddUser('test_user_2', 'secret', roles, [])
        self.login('test_user_2')
        self.assertEquals([ data['id'] for data in self.workflow.getTransitionsFor(self.doc) ], transitions)

    def testdPermissions(self):
        route = [
         'submit', 'publish']
        roles = ['Reviewer']
        accept_per = [AccessContentsInformation, View]
        reject_per = [ModifyPortalContent]
        wft = WFtest()
        self.portal.acl_users._doAddUser('test_user', 'secret', ['Manager'], [])
        self.login('test_user')
        wft.doActionLoop(self.doc, route)
        self.portal.acl_users._doAddUser('test_user_2', 'secret', roles, [])
        self.login('test_user_2')
        for hasper in accept_per:
            self.failUnless(checkPerm(hasper, self.doc))

        for not_hasper in reject_per:
            self.failIf(checkPerm(not_hasper, self.doc))


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestWorkflowAction))
    return suite