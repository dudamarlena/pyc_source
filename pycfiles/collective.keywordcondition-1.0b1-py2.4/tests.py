# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/keywordcondition/tests.py
# Compiled at: 2007-12-19 19:55:03
import unittest
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from zope.interface import implements, Interface
from zope.component import getUtility, getMultiAdapter
from zope.component.interfaces import IObjectEvent
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleCondition
from plone.contentrules.rule.interfaces import IExecutable
from plone.app.contentrules.rule import Rule
import collective.keywordcondition
from collective.keywordcondition.keyword import KeywordCondition
from collective.keywordcondition.keyword import KeywordEditForm
ptc.setupPloneSite()

class DummyEvent(object):
    __module__ = __name__
    implements(IObjectEvent)

    def __init__(self, obj):
        self.object = obj


class TestKeywordCondition(ptc.PloneTestCase):
    __module__ = __name__

    class layer(PloneSite):
        __module__ = __name__

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', collective.keywordcondition)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def testRegistered(self):
        element = getUtility(IRuleCondition, name='collective.keywordcondition.Keyword')
        self.assertEquals('collective.keywordcondition.Keyword', element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)
        return

    def testInvokeAddView(self):
        element = getUtility(IRuleCondition, name='collective.keywordcondition.Keyword')
        storage = getUtility(IRuleStorage)
        storage['foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')
        adding = getMultiAdapter((rule, self.portal.REQUEST), name='+condition')
        addview = getMultiAdapter((adding, self.portal.REQUEST), name=element.addview)
        addview.createAndAdd(data={'keywords': ['Foo', 'Bar']})
        e = rule.conditions[0]
        self.failUnless(isinstance(e, KeywordCondition))
        self.assertEquals(['Foo', 'Bar'], e.keywords)

    def testInvokeEditView(self):
        element = getUtility(IRuleCondition, name='collective.keywordcondition.Keyword')
        e = KeywordCondition()
        editview = getMultiAdapter((e, self.folder.REQUEST), name=element.editview)
        self.failUnless(isinstance(editview, KeywordEditForm))

    def testExecute(self):
        e = KeywordCondition()
        e.keywords = ['Foo', 'Bar']
        self.folder.invokeFactory('Document', 'd1')
        self.folder.d1.setSubject(['Bar'])
        self.folder.invokeFactory('Document', 'd2')
        self.folder.d2.setSubject(['Baz'])
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder.d1)), IExecutable)
        self.assertEquals(True, ex())
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder.d2)), IExecutable)
        self.assertEquals(False, ex())


def test_suite():
    return unittest.TestSuite([unittest.makeSuite(TestKeywordCondition)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')