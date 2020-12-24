# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mailtoplone/contentrules/tests/test_setup.py
# Compiled at: 2008-02-29 08:26:12
__author__ = 'Hans-Peter Locher <hans-peter.locher@inquant.de>'
__docformat__ = 'plaintext'
import unittest
from zope import component
from mailtoplone.contentrules.tests.base import MailToPloneContentrulesTestCase
from Products.CMFCore.utils import getToolByName
from zope.interface import implements, Interface
from zope.component import getUtility, getMultiAdapter
from zope.component.interfaces import IObjectEvent
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleCondition
from plone.contentrules.rule.interfaces import IRuleAction
from plone.contentrules.rule.interfaces import IExecutable
from plone.app.contentrules.rule import Rule
from mailtoplone.contentrules.conditions.emailheader import EmailHeaderCondition, EmailHeaderEditForm
from mailtoplone.contentrules.conditions.haspartoftype import HasPartOfTypeCondition, HasPartOfTypeEditForm
from mailtoplone.contentrules.conditions.sizeofmail import SizeOfMailCondition, SizeOfMailEditForm
from mailtoplone.contentrules.actions.deliver import DeliverAction, DeliverEditForm
MULTIMSG = 'MIME-Version: 1.0\nContent-Type: multipart/mixed;\n\tboundary="next"\nDate: Fri, 11 Jan 2008 14:22:33 +0100\nFrom: "Nobody"\nTo: "Nobody"\n\n--next\nContent-Type: text/plain;\n--next\nContent-Type: text/calendar;\n--next\nContent-Type: image/png;\n--next--\n'

class DummyEvent(object):
    __module__ = __name__
    implements(IObjectEvent)

    def __init__(self, obj):
        self.object = obj


class TestSetup(MailToPloneContentrulesTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.setRoles(('Manager', ))
        self.portal.invokeFactory('InBox', 'inbox')

    def testEmailHeaderRegistered(self):
        element = getUtility(IRuleCondition, name='mailtoplone.contentrules.conditions.EmailHeader')
        self.assertEquals('mailtoplone.contentrules.conditions.EmailHeader', element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)
        return

    def testEmailHeaderInvokeAddView(self):
        element = getUtility(IRuleCondition, name='mailtoplone.contentrules.conditions.EmailHeader')
        storage = getUtility(IRuleStorage)
        storage['foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')
        adding = getMultiAdapter((rule, self.portal.REQUEST), name='+condition')
        addview = getMultiAdapter((adding, self.portal.REQUEST), name=element.addview)
        addview.createAndAdd(data={'header': 'Subject', 'value': 'Somevalue'})
        e = rule.conditions[0]
        self.failUnless(isinstance(e, EmailHeaderCondition))
        self.assertEquals('Subject', e.header)
        self.assertEquals('Somevalue', e.value)

    def testEmailHeaderInvokeEditView(self):
        element = getUtility(IRuleCondition, name='mailtoplone.contentrules.conditions.EmailHeader')
        e = EmailHeaderCondition()
        editview = getMultiAdapter((e, self.folder.REQUEST), name=element.editview)
        self.failUnless(isinstance(editview, EmailHeaderEditForm))

    def testEmailHeaderExecutor(self):
        e = EmailHeaderCondition()
        e.header = 'Subject'
        e.value = 'test'
        self.portal.inbox.invokeFactory('Email', 'e1')
        self.portal.inbox.e1.data = 'Subject: test'
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e1)), IExecutable)
        self.assertEquals(True, ex())
        self.portal.inbox.invokeFactory('Email', 'e2')
        self.portal.inbox.e2.data = 'Subject: laa'
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e2)), IExecutable)
        self.assertEquals(False, ex())
        self.portal.inbox.invokeFactory('Email', 'e3')
        self.portal.inbox.e2.data = 'laa: test'
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e3)), IExecutable)
        self.assertEquals(False, ex())
        self.portal.inbox.invokeFactory('Email', 'e4')
        self.portal.inbox.e2.data = ''
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e4)), IExecutable)
        self.assertEquals(False, ex())
        e.value = '*'
        self.portal.inbox.invokeFactory('Email', 'e5')
        self.portal.inbox.e5.data = 'Subject: BornToBeA*'
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e5)), IExecutable)
        self.assertEquals(True, ex())
        self.portal.inbox.invokeFactory('Email', 'e6')
        self.portal.inbox.e6.data = 'Subject: BornToBeWild'
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e6)), IExecutable)
        self.assertEquals(False, ex())

    def testHasPartOfTypeRegistered(self):
        element = getUtility(IRuleCondition, name='mailtoplone.contentrules.conditions.HasPartOfType')
        self.assertEquals('mailtoplone.contentrules.conditions.HasPartOfType', element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)
        return

    def testHasPartOfTypeInvokeAddView(self):
        element = getUtility(IRuleCondition, name='mailtoplone.contentrules.conditions.HasPartOfType')
        storage = getUtility(IRuleStorage)
        storage['foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')
        adding = getMultiAdapter((rule, self.portal.REQUEST), name='+condition')
        addview = getMultiAdapter((adding, self.portal.REQUEST), name=element.addview)
        addview.createAndAdd(data={'maintype': 'text', 'subtype': 'plain'})
        e = rule.conditions[0]
        self.failUnless(isinstance(e, HasPartOfTypeCondition))
        self.assertEquals('text', e.maintype)
        self.assertEquals('plain', e.subtype)

    def testHasPartOfTypeInvokeEditView(self):
        element = getUtility(IRuleCondition, name='mailtoplone.contentrules.conditions.HasPartOfType')
        e = HasPartOfTypeCondition()
        editview = getMultiAdapter((e, self.folder.REQUEST), name=element.editview)
        self.failUnless(isinstance(editview, HasPartOfTypeEditForm))

    def testHasPartOfTypeExecutor(self):
        e = HasPartOfTypeCondition()
        self.portal.inbox.invokeFactory('Email', 'e1')
        self.portal.inbox.e1.data = MULTIMSG
        e.maintype = 'text'
        e.subtype = 'calendar'
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e1)), IExecutable)
        self.assertEquals(True, ex())
        e.maintype = 'image'
        e.subtype = 'png'
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e1)), IExecutable)
        self.assertEquals(True, ex())
        e.maintype = 'video'
        e.subtype = 'mpeg'
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e1)), IExecutable)
        self.assertEquals(False, ex())
        e.maintype = 'video'
        e.subtype = ''
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e1)), IExecutable)
        self.assertEquals(False, ex())
        e.maintype = ''
        e.subtype = 'mpeg'
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e1)), IExecutable)
        self.assertEquals(False, ex())
        e.maintype = 'text'
        e.subtype = ''
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e1)), IExecutable)
        self.assertEquals(True, ex())
        e.maintype = ''
        e.subtype = 'plain'
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e1)), IExecutable)
        self.assertEquals(True, ex())
        e.maintype = ''
        e.subtype = ''
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e1)), IExecutable)
        self.assertEquals(True, ex())

    def testSizeOfMailRegistered(self):
        element = getUtility(IRuleCondition, name='mailtoplone.contentrules.conditions.SizeOfMail')
        self.assertEquals('mailtoplone.contentrules.conditions.SizeOfMail', element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)
        return

    def testSizeOfMailInvokeAddView(self):
        element = getUtility(IRuleCondition, name='mailtoplone.contentrules.conditions.SizeOfMail')
        storage = getUtility(IRuleStorage)
        storage['foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')
        adding = getMultiAdapter((rule, self.portal.REQUEST), name='+condition')
        addview = getMultiAdapter((adding, self.portal.REQUEST), name=element.addview)
        addview.createAndAdd(data={'operator': '>=', 'size': '10'})
        e = rule.conditions[0]
        self.failUnless(isinstance(e, SizeOfMailCondition))
        self.assertEquals('>=', e.operator)
        self.assertEquals('10', e.size)

    def testSizeOfMailInvokeEditView(self):
        element = getUtility(IRuleCondition, name='mailtoplone.contentrules.conditions.SizeOfMail')
        e = SizeOfMailCondition()
        editview = getMultiAdapter((e, self.folder.REQUEST), name=element.editview)
        self.failUnless(isinstance(editview, SizeOfMailEditForm))

    def testSizeOfMailExecutor(self):
        e = SizeOfMailCondition()
        self.portal.inbox.invokeFactory('Email', 'e1')
        self.portal.inbox.e1.data = 'x' * 1024 * 1024 * 2
        e.operator = '>='
        e.size = 2
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e1)), IExecutable)
        self.assertEquals(True, ex())
        e.operator = '<='
        e.size = 2
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e1)), IExecutable)
        self.assertEquals(True, ex())
        e.operator = '>='
        e.size = 1
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e1)), IExecutable)
        self.assertEquals(True, ex())
        e.operator = '<='
        e.size = 1
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e1)), IExecutable)
        self.assertEquals(False, ex())
        e.operator = '>='
        e.size = 3
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e1)), IExecutable)
        self.assertEquals(False, ex())
        e.operator = '<='
        e.size = 3
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e1)), IExecutable)
        self.assertEquals(True, ex())

    def testDeliverRegistered(self):
        element = getUtility(IRuleAction, name='mailtoplone.contentrules.actions.deliver')
        self.assertEquals('mailtoplone.contentrules.actions.deliver', element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)
        return

    def testDeliverInvokeAddView(self):
        element = getUtility(IRuleAction, name='mailtoplone.contentrules.actions.deliver')
        storage = getUtility(IRuleStorage)
        storage['foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')
        adding = getMultiAdapter((rule, self.portal.REQUEST), name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST), name=element.addview)
        addview.createAndAdd(data={'key': 'searchkey'})
        e = rule.actions[0]
        self.failUnless(isinstance(e, DeliverAction))
        self.assertEquals('searchkey', e.key)

    def testDeliverInvokeEditView(self):
        element = getUtility(IRuleAction, name='mailtoplone.contentrules.actions.deliver')
        e = DeliverAction()
        editview = getMultiAdapter((e, self.folder.REQUEST), name=element.editview)
        self.failUnless(isinstance(editview, DeliverEditForm))

    def testDeliverExecutor(self):
        self.portal.invokeFactory('InBox', 'destinbox1')
        self.portal.invokeFactory('InBox', 'destinbox2')
        e = DeliverAction()
        e.key = 'destinbox1'
        self.portal.inbox.invokeFactory('Email', 'e1')
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.inbox.e1)), IExecutable)
        ex()
        self.assertEquals(True, len(self.portal.destinbox1.objectIds()) == 1)
        self.assertEquals(True, len(self.portal.destinbox2.objectIds()) == 0)
        self.assertEquals(True, len(self.portal.inbox.objectIds()) == 1)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite