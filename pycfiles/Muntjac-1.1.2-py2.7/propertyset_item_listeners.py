# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/propertyset_item_listeners.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.test.server.component import abstract_listener_methods_test
from muntjac.data.util.propertyset_item import PropertysetItem
from muntjac.data.item import IPropertySetChangeEvent, IPropertySetChangeListener

class PropertysetItemListeners(abstract_listener_methods_test.AbstractListenerMethodsTest):

    def testPropertySetChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(PropertysetItem, IPropertySetChangeEvent, IPropertySetChangeListener)