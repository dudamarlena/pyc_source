# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/componentcontainer/add_remove_component_test.py
# Compiled at: 2013-04-04 15:36:37
from unittest import TestCase
from muntjac.test.muntjac_classes import MuntjacClasses
from muntjac.ui.custom_layout import CustomLayout
from muntjac.ui.horizontal_layout import HorizontalLayout
from muntjac.ui.label import Label

class AddRemoveComponentTest(TestCase):

    def testRemoveComponentFromWrongContainer(self, componentContainer=None):
        if componentContainer is None:
            containerClasses = MuntjacClasses.getComponentContainersSupportingAddRemoveComponent()
            containerClasses.remove(CustomLayout)
            self.testRemoveComponentFromWrongContainer(CustomLayout('dummy'))
            for c in containerClasses:
                self.testRemoveComponentFromWrongContainer(c())

        else:
            hl = HorizontalLayout()
            label = Label()
            hl.addComponent(label)
            componentContainer.removeComponent(label)
            self.assertEquals(hl, label.getParent(), 'Parent no longer ' + 'correct for ' + componentContainer.__class__.__name__)
        return