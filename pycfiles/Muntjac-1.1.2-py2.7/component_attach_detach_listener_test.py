# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/components/component_attach_detach_listener_test.py
# Compiled at: 2013-04-04 15:36:37
from unittest import TestCase
from muntjac.ui.label import Label
from muntjac.ui.horizontal_layout import HorizontalLayout
from muntjac.ui.grid_layout import GridLayout
from muntjac.ui.absolute_layout import AbsoluteLayout
from muntjac.ui.css_layout import CssLayout
from muntjac.ui.abstract_ordered_layout import AbstractOrderedLayout
from muntjac.ui.component_container import IComponentAttachListener, IComponentDetachListener

class ComponentAttachDetachListenerTest(TestCase):

    def resetVariables(self):
        self._attachCounter = 0
        self._attachedComponent = None
        self._attachTarget = None
        self._foundInContainer = False
        self._detachCounter = 0
        self._detachedComponent = None
        self._detachedTarget = None
        self._indexOfComponent = -1
        self._componentArea = None
        self._componentPosition = None
        return

    def setUp(self):
        super(ComponentAttachDetachListenerTest, self).setUp()
        self._attachCounter = 0
        self._attachedComponent = None
        self._attachTarget = None
        self._foundInContainer = False
        self._detachCounter = 0
        self._detachedComponent = None
        self._detachedTarget = None
        self._indexOfComponent = -1
        self._componentArea = None
        self._componentPosition = None
        self._olayout = HorizontalLayout()
        listener = MyAttachListener(self)
        self._olayout.addListener(listener, IComponentAttachListener)
        listener = MyDetachListener(self)
        self._olayout.addListener(listener, IComponentDetachListener)
        self._gridlayout = GridLayout()
        listener = MyAttachListener(self)
        self._gridlayout.addListener(listener, IComponentAttachListener)
        listener = MyDetachListener(self)
        self._gridlayout.addListener(listener, IComponentDetachListener)
        self._absolutelayout = AbsoluteLayout()
        listener = MyAttachListener(self)
        self._absolutelayout.addListener(listener, IComponentAttachListener)
        listener = MyDetachListener(self)
        self._absolutelayout.addListener(listener, IComponentDetachListener)
        self._csslayout = CssLayout()
        listener = MyAttachListener(self)
        self._csslayout.addListener(listener, IComponentAttachListener)
        listener = MyDetachListener(self)
        self._csslayout.addListener(listener, IComponentDetachListener)
        return

    def testOrderedLayoutAttachListener(self):
        self.resetVariables()
        comp = Label()
        self._olayout.addComponent(comp)
        self.assertEquals(1, self._attachCounter)
        self.assertEquals(comp, self._attachedComponent)
        self.assertEquals(self._olayout, self._attachTarget)
        self.assertTrue(self._foundInContainer)
        self.assertFalse(self._indexOfComponent == -1)

    def testOrderedLayoutDetachListener(self):
        comp = Label()
        self._olayout.addComponent(comp)
        self.resetVariables()
        self._olayout.removeComponent(comp)
        self.assertEquals(1, self._detachCounter)
        self.assertEquals(comp, self._detachedComponent)
        self.assertEquals(self._olayout, self._detachedTarget)
        self.assertFalse(self._foundInContainer)
        self.assertEquals(-1, self._indexOfComponent)

    def testGridLayoutAttachListener(self):
        self.resetVariables()
        comp = Label()
        self._gridlayout.addComponent(comp)
        self.assertEquals(1, self._attachCounter)
        self.assertEquals(comp, self._attachedComponent)
        self.assertEquals(self._gridlayout, self._attachTarget)
        self.assertTrue(self._foundInContainer)
        self.assertIsNotNone(self._componentArea)

    def testGridLayoutDetachListener(self):
        comp = Label()
        self._gridlayout.addComponent(comp)
        self.resetVariables()
        self._gridlayout.removeComponent(comp)
        self.assertEquals(1, self._detachCounter)
        self.assertEquals(comp, self._detachedComponent)
        self.assertEquals(self._gridlayout, self._detachedTarget)
        self.assertFalse(self._foundInContainer)
        self.assertIsNone(self._componentArea)

    def testAbsoluteLayoutAttachListener(self):
        self.resetVariables()
        comp = Label()
        self._absolutelayout.addComponent(comp)
        self.assertEquals(1, self._attachCounter)
        self.assertEquals(comp, self._attachedComponent)
        self.assertEquals(self._absolutelayout, self._attachTarget)
        self.assertTrue(self._foundInContainer)
        self.assertIsNotNone(self._componentPosition)

    def testAbsoluteLayoutDetachListener(self):
        comp = Label()
        self._absolutelayout.addComponent(comp)
        self.resetVariables()
        self._absolutelayout.removeComponent(comp)
        self.assertEquals(1, self._detachCounter)
        self.assertEquals(comp, self._detachedComponent)
        self.assertEquals(self._absolutelayout, self._detachedTarget)
        self.assertFalse(self._foundInContainer)
        self.assertIsNone(self._componentPosition)

    def testCSSLayoutAttachListener(self):
        self.resetVariables()
        comp = Label()
        self._csslayout.addComponent(comp)
        self.assertEquals(1, self._attachCounter)
        self.assertEquals(comp, self._attachedComponent)
        self.assertEquals(self._csslayout, self._attachTarget)
        self.assertTrue(self._foundInContainer)

    def testCSSLayoutDetachListener(self):
        comp = Label()
        self._csslayout.addComponent(comp)
        self.resetVariables()
        self._csslayout.removeComponent(comp)
        self.assertEquals(1, self._detachCounter)
        self.assertEquals(comp, self._detachedComponent)
        self.assertEquals(self._csslayout, self._detachedTarget)
        self.assertFalse(self._foundInContainer)


class MyAttachListener(IComponentAttachListener):

    def __init__(self, test):
        self._test = test

    def componentAttachedToContainer(self, event):
        self._test._attachCounter += 1
        self._test._attachedComponent = event.getAttachedComponent()
        self._test._attachTarget = event.getContainer()
        it = self._test._attachTarget.getComponentIterator()
        while True:
            try:
                if it.next() == self._test._attachedComponent:
                    self._test._foundInContainer = True
                    break
            except StopIteration:
                break

        if isinstance(self._test._attachTarget, AbstractOrderedLayout):
            self._test._indexOfComponent = self._test._attachTarget.getComponentIndex(self._test._attachedComponent)
        elif isinstance(self._test._attachTarget, GridLayout):
            self._test._componentArea = self._test._attachTarget.getComponentArea(self._test._attachedComponent)
        elif isinstance(self._test._attachTarget, AbsoluteLayout):
            self._test._componentPosition = self._test._attachTarget.getPosition(self._test._attachedComponent)


class MyDetachListener(IComponentDetachListener):

    def __init__(self, test):
        self._test = test

    def componentDetachedFromContainer(self, event):
        self._test._detachCounter += 1
        self._test._detachedComponent = event.getDetachedComponent()
        self._test._detachedTarget = event.getContainer()
        it = self._test._detachedTarget.getComponentIterator()
        while True:
            try:
                if it.next() == self._test._detachedComponent:
                    self._test._foundInContainer = True
                    break
            except StopIteration:
                break

        if isinstance(self._test._detachedTarget, AbstractOrderedLayout):
            self._test._indexOfComponent = self._test._detachedTarget.getComponentIndex(self._test._detachedComponent)
        elif isinstance(self._test._detachedTarget, GridLayout):
            self._test._componentArea = self._test._detachedTarget.getComponentArea(self._test._detachedComponent)
        elif isinstance(self._test._detachedTarget, AbsoluteLayout):
            self._test._componentPosition = self._test._detachedTarget.getPosition(self._test._detachedComponent)