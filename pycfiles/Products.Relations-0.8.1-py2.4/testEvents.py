# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/tests/testEvents.py
# Compiled at: 2008-09-11 19:48:09
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Products.PloneTestCase import PloneTestCase
import Products.Relations.processor as processor
from Products.Relations.events import RelationConnectedEvent
from Products.Relations.events import RelationDisconnectedEvent
from Products.Relations.events import IRelationConnectedEvent
from Products.Relations.events import IRelationDisconnectedEvent
from zope.component import adapter
from zope.component import provideHandler
from zope.event import notify
import common
common.installWithinPortal()
connectedresult = None
disconnectedresult = None

@adapter(IRelationConnectedEvent)
def connectedsubscriber(event):
    globals()['connectedresult'] = event.references


@adapter(IRelationDisconnectedEvent)
def disconnectedsubscriber(event):
    globals()['disconnectedresult'] = event.references


class TestEvents(PloneTestCase.PloneTestCase):
    __module__ = __name__
    TYPES = ('SimpleType', 'ComplexType')
    RULESETS = ('OneRuleset', 'AnotherRuleset')

    def afterSetUp(self):
        self.objs = common.createObjects(self, self.TYPES)
        self.rulesets = [ common.createRuleset(self, j) for j in self.RULESETS ]

    def testEventNotify(self):
        provideHandler(connectedsubscriber)
        provideHandler(disconnectedsubscriber)
        globals()['connectedresult'] = None
        globals()['disconnectedresult'] = None
        c_data = [
         1, 2, 3]
        c_event = RelationConnectedEvent(self.portal, c_data)
        notify(c_event)
        self.assertEquals(connectedresult, c_data)
        self.assertEquals(disconnectedresult, None)
        d_data = [
         4, 5, 6]
        d_event = RelationDisconnectedEvent(self.portal, d_data)
        notify(d_event)
        self.assertEquals(connectedresult, c_data)
        self.assertEquals(disconnectedresult, d_data)
        return

    def testConnectEventAndDisconnectEvent(self):
        provideHandler(connectedsubscriber)
        provideHandler(disconnectedsubscriber)
        triples = [ (self.objs[0].UID(), self.objs[1].UID(), ruleset.getId()) for ruleset in self.rulesets ]
        processor.process(self.portal, connect=[triples[0]])
        self.assertEquals(len(connectedresult), 1)
        ref = connectedresult[0]
        self.assertEquals((ref.sourceUID, ref.targetUID), (
         self.objs[0].UID(), self.objs[1].UID()))
        processor.process(self.portal, disconnect=[triples[0]])
        self.assertEquals(len(disconnectedresult), 1)
        ref = disconnectedresult[0]
        self.assertEquals((ref.sourceUID, ref.targetUID), (
         self.objs[0].UID(), self.objs[1].UID()))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestEvents))
    return suite


if __name__ == '__main__':
    framework()