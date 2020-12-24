# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/component/abstract_component_style_names.py
# Compiled at: 2013-04-04 15:36:37
from unittest import TestCase
from muntjac.ui.abstract_component import AbstractComponent

class TestAbstractComponentStyleNames(TestCase):

    def testSetMultiple(self):
        component = self.getComponent()
        component.setStyleName('style1 style2')
        self.assertEquals(component.getStyleName(), 'style1 style2')

    def testSetAdd(self):
        component = self.getComponent()
        component.setStyleName('style1')
        component.addStyleName('style2')
        self.assertEquals(component.getStyleName(), 'style1 style2')

    def testAddSame(self):
        component = self.getComponent()
        component.setStyleName('style1 style2')
        component.addStyleName('style1')
        self.assertEquals(component.getStyleName(), 'style1 style2')

    def testSetRemove(self):
        component = self.getComponent()
        component.setStyleName('style1 style2')
        component.removeStyleName('style1')
        self.assertEquals(component.getStyleName(), 'style2')

    def testAddRemove(self):
        component = self.getComponent()
        component.addStyleName('style1')
        component.addStyleName('style2')
        component.removeStyleName('style1')
        self.assertEquals(component.getStyleName(), 'style2')

    def testRemoveMultipleWithExtraSpaces(self):
        component = self.getComponent()
        component.setStyleName('style1 style2 style3')
        component.removeStyleName(' style1  style3 ')
        self.assertEquals(component.getStyleName(), 'style2')

    def testSetWithExtraSpaces(self):
        component = self.getComponent()
        component.setStyleName(' style1  style2 ')
        self.assertEquals(component.getStyleName(), 'style1 style2')

    def getComponent(self):
        return AbstractComponent()