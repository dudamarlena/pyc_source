# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/abstract_property_listeners.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.data.util.abstract_property import AbstractProperty
from muntjac.data.property import ValueChangeEvent, IValueChangeListener, IReadOnlyStatusChangeEvent, IReadOnlyStatusChangeListener
from muntjac.data.util.object_property import ObjectProperty
from muntjac.test.server.component import abstract_listener_methods_test

class TestAbstractPropertyListeners(abstract_listener_methods_test.AbstractListenerMethodsTest):

    def testValueChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(AbstractProperty, ValueChangeEvent, IValueChangeListener, ObjectProperty(''))

    def testReadOnlyStatusChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(AbstractProperty, IReadOnlyStatusChangeEvent, IReadOnlyStatusChangeListener, ObjectProperty(''))