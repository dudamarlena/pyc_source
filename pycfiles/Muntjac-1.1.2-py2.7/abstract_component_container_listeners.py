# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/component/abstract_component_container_listeners.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.test.server.component.abstract_listener_methods_test import AbstractListenerMethodsTest
from muntjac.ui.horizontal_layout import HorizontalLayout
from muntjac.ui.vertical_layout import VerticalLayout
from muntjac.ui.component_container import ComponentDetachEvent, IComponentDetachListener, ComponentAttachEvent, IComponentAttachListener

class TestAbstractComponentContainerListeners(AbstractListenerMethodsTest):

    def testComponentDetachListenerAddGetRemove(self):
        self._testListenerAddGetRemove(HorizontalLayout, ComponentDetachEvent, IComponentDetachListener)

    def testComponentAttachListenerAddGetRemove(self):
        self._testListenerAddGetRemove(VerticalLayout, ComponentAttachEvent, IComponentAttachListener)