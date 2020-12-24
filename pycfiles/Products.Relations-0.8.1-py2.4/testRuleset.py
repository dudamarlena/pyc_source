# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/tests/testRuleset.py
# Compiled at: 2008-09-11 19:48:09
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
import transaction
from Products.PloneTestCase import PloneTestCase
from OFS.SimpleItem import SimpleItem
from Products.CMFCore import interfaces as icmfcore
from Products.CMFCore.utils import getToolByName
from Products.Relations.config import *
import Products.Relations.interfaces as interfaces, Products.Relations.brain as brain, Products.Relations.ruleset as rulesetmodule, Products.Relations.processor as processor, common
common.installWithinPortal()

class TestLibrary(PloneTestCase.PloneTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.library = getToolByName(self.portal, RELATIONS_LIBRARY)

    def testRegister(self):
        ttool = getToolByName(self.portal, 'portal_types')
        construct = ttool.constructContent
        self.loginAsPortalOwner()
        self.library.getFolder().invokeFactory('Ruleset', 'ruleset1')
        self.logout()
        self.login()
        construct('Ruleset', self.folder, 'ruleset2')
        ruleset1 = getattr(self.library.getFolder(), 'ruleset1')
        ruleset2 = getattr(self.folder, 'ruleset2')
        self.library.registerRuleset(ruleset2)
        for ruleset in (ruleset1, ruleset2):
            self.assertEquals(ruleset, self.library.getRuleset(ruleset.getId()))

        self.assertEquals([ruleset1, ruleset2], self.library.getRulesets())

    def testAllowedContentTypes(self):
        self.loginAsPortalOwner()
        types = self.library.allowedContentTypes()
        self.assertEquals(len(types), 2)
        for t in types:
            self.assert_(str(t).endswith('Ruleset>') or str(t).endswith('Ruleset Collection>'), '%s not recognized' % str(t))

        self.logout()

    def testInvokeFactory(self):
        self.loginAsPortalOwner()
        lib = self.library.getFolder()
        lib.invokeFactory('Ruleset', 'allowed')
        self.assertRaises(ValueError, self.folder.invokeFactory, 'Ruleset', 'disallowed')
        self.assertRaises(ValueError, lib.invokeFactory, 'SimpleType', 'disallowed')
        self.logout()

    def testActions(self):
        at = getToolByName(self.portal, 'portal_actions')

        def hasaction(obj):
            category = 'object'
            filtered_actions = at.listFilteredActionsFor(obj)
            if category not in filtered_actions.keys():
                return False
            for action in filtered_actions[category]:
                if action['id'] == 'relations':
                    return action

            return False

        self.assert_(not hasaction(self.library))
        self.loginAsPortalOwner()
        f = self.library.getFolder()
        f.invokeFactory('Ruleset', 'samerel')
        self.library.addReference(self.library, 'samerel')
        self.logout()
        self.login()
        self.assert_(not hasaction(self.library))
        self.loginAsPortalOwner()
        self.portal.portal_workflow.doActionFor(f.samerel, 'publish')
        self.logout()
        self.login()
        self.assert_(not hasaction(self.library))
        self.loginAsPortalOwner()
        self.assert_(hasaction(self.library), "'relations' action n/a")
        self.logout()
        self.login()
        self.assert_(not hasaction(self.folder))

    def testRenameLibrary(self):
        self.loginAsPortalOwner()
        rename = self.portal.manage_renameObject
        try:
            rename(RELATIONS_LIBRARY, 'another_id')
        except:
            pass
        else:
            self.assert_(False, 'Success in renaming %s.' % RELATIONS_LIBRARY)

    def testGetRulesetsOrderSupport(self):
        self.loginAsPortalOwner()
        folder = self.library.getFolder()
        folder.invokeFactory('Ruleset', 'second')
        folder.invokeFactory('Ruleset', 'first')
        folder.invokeFactory('Ruleset Collection', 'collection')
        collection = folder.collection
        collection.invokeFactory('Ruleset', 'third')
        collection.invokeFactory('Ruleset Collection', 'collection')
        collection.collection.invokeFactory('Ruleset', 'fourth')

        def ids():
            return [ obj.getId() for obj in self.library.getRulesets() ]

        self.assertEquals(ids(), ['second', 'first', 'third', 'fourth'])
        folder.moveObjectsToTop(['first'])
        self.assertEquals(ids(), ['first', 'second', 'third', 'fourth'])


class DummyComponent(SimpleItem, rulesetmodule.RuleBase):
    __module__ = __name__
    __implements__ = (interfaces.IVocabularyProvider, interfaces.IPrimaryImplicator, interfaces.IImplicator, interfaces.IValidator, interfaces.IFinalizer, interfaces.IReferenceActionProvider, interfaces.IReferenceLayerProvider, interfaces.IReferenceLayer)
    gen_methods = ('makeVocabulary', 'isValidTarget', 'implyOnConnect', 'implyOnDisconnect',
                   'validateConnected', 'validateDisconnected', 'finalizeOnConnect',
                   'finalizeOnDisconnect', 'addHook', 'delHook')

    def __init__(self, ruleset):
        self._ruleset = ruleset
        self.calls = {}
        methodnames = self.gen_methods + ('connect', 'disconnect', 'provideReferenceLayer',
                                          'listActionsFor')
        for methname in methodnames:
            self.calls[methname] = []

    def connect(self, source, target, metadata=None):
        self.calls['connect'].append((source, target, metadata))
        impl = rulesetmodule.DefaultPrimaryImplicator(self.getRuleset())
        return impl.connect(source, target, metadata)

    def disconnect(self, reference):
        ruleset = self.getRuleset()
        self.calls['disconnect'].append((ruleset, reference))
        impl = rulesetmodule.DefaultPrimaryImplicator(ruleset)
        return impl.disconnect(reference)

    def provideReferenceLayer(self, reference):
        self.calls['provideReferenceLayer'].append((reference,))
        return self

    def listActionsFor(self, reference):
        self.calls['listActionsFor'].append((reference,))
        return []


def makeMethod(methname):

    def method(self, *args):
        self.calls[methname].append(args)

    return method


for methname in DummyComponent.gen_methods:
    setattr(DummyComponent, methname, makeMethod(methname))

class Chain(processor.Chain):
    __module__ = __name__

    def __repr__(self):
        l = self.added + self.deleted
        return '<Chain with %s items: %s>' % (len(l), l)


class TestRuleset(PloneTestCase.PloneTestCase):
    __module__ = __name__
    TYPES = ('SimpleFolder', 'SimpleType')

    def afterSetUp(self):
        objs = common.createObjects(self, self.TYPES)
        self.brains = [ brain.makeBrainAggregate(self.portal, obj.UID()) for obj in objs ]
        self.ruleset = common.createRuleset(self, 'ruleset')

    def testForward(self):
        component = DummyComponent(self.ruleset)
        self.ruleset._setObject('component', component)
        chain = Chain()
        calls = component.calls
        self.ruleset.implyOnConnect(self.brains[0], self.brains[1], chain)
        self.assertEquals(calls['connect'], [
         (
          self.brains[0], self.brains[1], None)])
        self.assertEquals(calls['implyOnConnect'], [
         (
          chain.added[0], chain)])
        self.assertEquals(calls['provideReferenceLayer'], [
         (
          chain.added[0],)])
        self.assertEquals(calls['addHook'], [
         (
          chain.added[0],)])
        ref_ctl = getToolByName(self.portal, REFERENCE_CATALOG)
        ref = ref_ctl(sourceUID=self.brains[0].UID, targetUID=self.brains[1].UID, relationship=self.ruleset.getId())[0].getObject()
        self.assertEquals(ref, chain.added[0])
        self.assertEquals(len(chain.added), 1)
        self.assertNotEquals(chain.added[0], None)
        self.ruleset.makeVocabulary(self.brains[0])
        self.assertEquals(calls['makeVocabulary'], [
         (
          self.brains[0], None)])
        self.ruleset.makeVocabulary(self.brains[1], self.brains[:])
        self.assertEquals(calls['makeVocabulary'][1], (
         self.brains[1], self.brains))
        self.ruleset.listActionsFor(chain.added[0])
        self.assertEquals(calls['listActionsFor'], [(chain.added[0],)])
        for method in ('validateConnected', 'validateDisconnected', 'finalizeOnConnect',
                       'finalizeOnDisconnect', 'implyOnDisconnect'):
            getattr(self.ruleset, method)(chain.added[0], chain)
            self.assertEquals(calls[method], [
             (
              chain.added[0], chain)])

        self.assertEquals(calls['delHook'], [(chain.added[0],)])
        return

    def testMultipleForward(self):
        component1 = DummyComponent(self.ruleset)
        component2 = DummyComponent(self.ruleset)
        self.ruleset._setObject('component1', component1)
        self.ruleset._setObject('component2', component2)
        chain = Chain()
        self.ruleset.implyOnConnect(self.brains[0], self.brains[1], chain)
        for component in (component1, component2):
            self.assertEquals(component.calls['implyOnConnect'], [
             (
              chain.added[0], chain)])

    def testAllowedContentTypes(self):
        types = self.ruleset.allowedContentTypes()
        self.assert_(len(types) > 0)
        for ti in types:
            self.assert_(icmfcore.ITypeInformation.providedBy(ti), '%s not a type information.' % ti)

    def testInvokeFactory(self):
        ti = self.ruleset.allowedContentTypes()[0]
        self.ruleset.invokeFactory(ti.id, 'allowed')
        self.assertRaises(ValueError, self.folder.invokeFactory, ti.id, 'disallowed')
        self.assertRaises(ValueError, self.ruleset.invokeFactory, self.TYPES[0], 'disallowed')

    def testRenameRulesetInLibrary(self):
        library = getToolByName(self.portal, RELATIONS_LIBRARY)
        self.loginAsPortalOwner()
        library.invokeFactory('Ruleset', 'some_id')
        ruleset = library.getRuleset('some_id')
        chain = Chain()
        ruleset.implyOnConnect(self.brains[0], self.brains[1], chain)
        ref = chain.added[(-1)]
        transaction.savepoint()
        library.manage_renameObject('some_id', 'something_else')
        self.assertEquals(ref.relationship, 'something_else')
        ref_ctl = getToolByName(self.portal, REFERENCE_CATALOG)
        search_kwargs = {'sourceUID': self.brains[0].UID, 'targetUID': self.brains[1].UID}
        search_kwargs['relationship'] = 'some_id'
        self.assertEquals(len(ref_ctl(**search_kwargs)), 0)
        search_kwargs['relationship'] = 'something_else'
        self.assertEquals(len(ref_ctl(**search_kwargs)), 1)
        pt = getToolByName(self.portal, 'portal_types')
        self.assert_('Relations Library' in [ ti.getId() for ti in pt.listTypeInfo() ])

    def testCopyRulesetInLibrary(self):
        library = getToolByName(self.portal, RELATIONS_LIBRARY)
        self.loginAsPortalOwner()
        library.invokeFactory('Ruleset', 'some_id')
        self.assertEquals(len(library.getRefs(RELATIONSHIP_LIBRARY)), 2)
        cb = library.manage_copyObjects('some_id')
        library.manage_pasteObjects(cb)
        self.assertEquals(len(library.getRefs(RELATIONSHIP_LIBRARY)), 3)

    def testDefaultPrimaryImplicator(self):
        ref_ctl = getToolByName(self.portal, REFERENCE_CATALOG)
        impl = rulesetmodule.DefaultPrimaryImplicator(self.ruleset)
        ref = impl.connect(self.brains[0], self.brains[1])
        self.assertNotEquals(ref, None)
        brains = ref_ctl(sourceUID=self.brains[0].UID, targetUID=self.brains[1].UID, relationship=self.ruleset.getId())
        self.assertEquals(len(brains), 1)
        self.assertEquals(ref, brains[0].getObject())
        ref2 = impl.connect(self.brains[0], self.brains[1])
        self.assertNotEquals(ref2, None)
        brains = ref_ctl(sourceUID=self.brains[0].UID, targetUID=self.brains[1].UID, relationship=self.ruleset.getId())
        self.assertEquals(len(brains), 1)
        return

    def testReferenceWithBrains(self):
        chain = Chain()
        self.ruleset.implyOnConnect(self.brains[0], self.brains[1], chain)
        ref = self.brains[0].getObject().getReferenceImpl()[0]
        self.assertEquals(ref.getSourceBrain(), self.brains[0])
        self.assertEquals(ref.getTargetBrain(), self.brains[1])
        self.assertEquals(ref.getSourceObject(), self.brains[0].getObject())
        self.assertEquals(ref.getTargetObject(), self.brains[1].getObject())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    tests = (TestLibrary, TestRuleset)
    for test in tests:
        suite.addTest(makeSuite(test))

    return suite


if __name__ == '__main__':
    framework()