# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/indexed_container_listeners.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.data.util.indexed_container import IndexedContainer
from muntjac.data.property import ValueChangeEvent, IValueChangeListener
from muntjac.test.server.component import abstract_listener_methods_test
from muntjac.data.container import IPropertySetChangeEvent, IPropertySetChangeListener

class IndexedContainerListeners(abstract_listener_methods_test.AbstractListenerMethodsTest):

    def testValueChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(IndexedContainer, ValueChangeEvent, IValueChangeListener)

    def testPropertySetChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(IndexedContainer, IPropertySetChangeEvent, IPropertySetChangeListener)