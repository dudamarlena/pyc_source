# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/c2/patch/plone3mail/tests.py
# Compiled at: 2010-02-22 08:31:42
from email import message_from_string
import unittest
from zope.testing import doctestunit
from zope.component import testing
from zope.component import getSiteManager
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from AccessControl import Unauthorized
from Products.CMFCore.permissions import AddPortalMember
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost
from Products.CMFPlone.migrations.migration_util import safeEditProperty
ptc.setupPloneSite()
import c2.patch.plone3mail
member_id = 'new_member'

class TestCase(ptc.PloneTestCase):
    __module__ = __name__

    class layer(PloneSite):
        __module__ = __name__

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', c2.patch.plone3mail)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

    def afterSetUp(self):
        self.registration = self.portal.portal_registration
        self.portal.acl_users.userFolderAddUser('userid', 'password', (), (), ())
        self.portal.acl_users._doAddGroup('groupid', ())

    def testMailPassword(self):
        mails = self.portal.MailHost = MockMailHost('MailHost')
        sm = getSiteManager(self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mails, IMailHost)
        self.registration.addMember(member_id, 'secret', properties={'username': member_id, 'email': 'foo@bar.com'})
        self.portal.setTitle('Täst Portal')
        self.portal.email_from_name = 'Täst Admin'
        self.portal.email_from_address = 'bar@baz.com'
        self.registration.mailPassword(member_id, self.app['REQUEST'])
        self.assertEqual(len(mails.messages), 1)
        msg = message_from_string(str(mails.messages[0]))
        self.assertEqual(msg['Subject'], '=?utf-8?q?Password_reset_request?=')
        self.assertEqual(msg['From'], '=?utf-8?b?IlTDpHN0IEFkbWluIiA=?=<bar@baz.com>')
        self.assertEqual(msg['Content-Type'], 'text/plain; charset=utf-8')

    def testRegisteredNotify(self):
        mails = self.portal.MailHost = MockMailHost('MailHost')
        sm = getSiteManager(self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mails, IMailHost)
        self.registration.addMember(member_id, 'secret', properties={'username': member_id, 'email': 'foo@bar.com'})
        self.portal.setTitle('Täst Portal')
        self.portal.email_from_name = 'Täst Admin'
        self.portal.email_from_address = 'bar@baz.com'
        self.registration.registeredNotify(member_id)
        self.assertEqual(len(mails.messages), 1)
        msg = message_from_string(str(mails.messages[0]))
        self.assertEqual(msg['Subject'], '=?utf-8?q?User_Account_Information_for_T=C3=A4st_Portal?=')
        self.assertEqual(msg['From'], '=?utf-8?b?IlTDpHN0IEFkbWluIiA=?=<bar@baz.com>')
        self.assertEqual(msg['Content-Type'], 'text/plain; charset=utf-8')
        self.assertEqual(msg['To'], 'foo@bar.com')

    def testRegisteredNotifyNonUtf8(self):
        mails = self.portal.MailHost = MockMailHost('MailHost')
        sm = getSiteManager(self.portal)
        self.portal._updateProperty('email_charset', 'ISO-2022-JP')
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mails, IMailHost)
        self.registration.addMember(member_id, 'secret', properties={'username': member_id, 'email': 'foo@bar.com'})
        self.portal.setTitle('Täst Portal')
        self.portal.email_from_name = 'Täst Admin'
        self.portal.email_from_address = 'bar@baz.com'
        self.registration.registeredNotify(member_id)
        self.assertEqual(len(mails.messages), 1)
        msg = message_from_string(str(mails.messages[0]))
        self.assertEqual(msg['Subject'], '=?iso-2022-jp?b?VXNlciBBY2NvdW50IEluZm9ybWF0aW9uIGZvciBUP3N0IFBvcnRhbA==?=')
        self.assertEqual(msg['From'], '=?iso-2022-jp?b?IlQ/c3QgQWRtaW4iIA==?=<bar@baz.com>')
        self.assertEqual(msg['Content-Type'], 'text/plain; charset=ISO-2022-JP')
        self.assertEqual(msg['To'], 'foo@bar.com')


def test_suite():
    return unittest.TestSuite([unittest.makeSuite(TestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')