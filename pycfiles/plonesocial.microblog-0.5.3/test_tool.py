# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.microblog/plonesocial/microblog/tests/test_tool.py
# Compiled at: 2013-04-29 04:20:50
import time, unittest2 as unittest
from zope.interface import directlyProvides
from zope.component import queryUtility
from AccessControl import getSecurityManager
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName
from plone.app.testing import TEST_USER_ID, setRoles
from plone.app.testing import login, logout
from plonesocial.microblog.testing import PLONESOCIAL_MICROBLOG_INTEGRATION_TESTING
from plonesocial.microblog.interfaces import IStatusContainer
from plonesocial.microblog.interfaces import IMicroblogTool
from plonesocial.microblog.interfaces import IMicroblogContext
from plonesocial.microblog.statusupdate import StatusUpdate

class TestMicroblogTool(unittest.TestCase):
    layer = PLONESOCIAL_MICROBLOG_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_tool_available(self):
        tool = queryUtility(IMicroblogTool)
        self.assertTrue(IStatusContainer.providedBy(tool))


class TestMicroblogToolContextBlacklisting(unittest.TestCase):
    layer = PLONESOCIAL_MICROBLOG_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        workflowTool = getToolByName(self.portal, 'portal_workflow')
        workflowTool.setDefaultChain('simple_publication_workflow')
        workflowTool.updateRoleMappings()
        self.portal.invokeFactory('Folder', 'f1', title='Folder 1')
        f1 = self.portal['f1']
        directlyProvides(f1, IMicroblogContext)
        f1.reindexObject()
        self.portal.invokeFactory('Folder', 'f2', title='Folder 2')
        f2 = self.portal['f2']
        directlyProvides(f2, IMicroblogContext)
        f2.reindexObject()
        workflowTool.doActionFor(f2, 'publish')
        self.assertEqual(workflowTool.getInfoFor(f1, 'review_state'), 'private')
        self.assertEqual(workflowTool.getInfoFor(f2, 'review_state'), 'published')
        tool = queryUtility(IMicroblogTool)
        self.su1 = su1 = StatusUpdate('test #foo', f1)
        tool.add(su1)
        self.su2 = su2 = StatusUpdate('test #foo', f2)
        tool.add(su2)
        tool.flush_queue()
        acl_users = getToolByName(self.portal, 'acl_users')
        acl_users.userFolderAddUser('user1', 'secret', ['Member'], [])

    def tearDown(self):
        time.sleep(1)

    def test_allowed_status_user(self):
        """The base implementation does not test access controls.
        The tool should provide those.
        """
        logout()
        login(self.portal, 'user1')
        sm = getSecurityManager()
        user = getSecurityManager().getUser()
        self.assertEqual(user.getId(), 'user1')
        self.assertFalse(sm.checkPermission(View, self.portal['f1']))
        self.assertTrue(sm.checkPermission(View, self.portal['f2']))
        tool = queryUtility(IMicroblogTool)
        self.assertEqual(list(tool.values()), [self.su2])

    def test_allowed_status_manager(self):
        """The default test user owns both IMicroblogContexts
        thus has access to both."""
        tool = queryUtility(IMicroblogTool)
        self.assertEqual(list(tool.values()), [self.su2, self.su1])