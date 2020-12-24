# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/selects/ComboBoxNewItemsExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, ComboBox
from muntjac.ui import abstract_select
from muntjac.data.property import IValueChangeListener

class ComboBoxNewItemsExample(VerticalLayout, IValueChangeListener, abstract_select.INewItemHandler):
    _cities = [
     'Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo',
     'Paris', 'Stockholm']

    def __init__(self):
        super(ComboBoxNewItemsExample, self).__init__()
        self._lastAdded = False
        self.setSpacing(True)
        self._l = ComboBox('Please select a city')
        for c in self._cities:
            self._l.addItem(c)

        self._l.setNewItemsAllowed(True)
        self._l.setNewItemHandler(self)
        self._l.setImmediate(True)
        self._l.addListener(self, IValueChangeListener)
        self.addComponent(self._l)

    def valueChange(self, event):
        if not self._lastAdded:
            self.getWindow().showNotification('Selected city: ' + str(event.getProperty()))
        self._lastAdded = False

    def addNewItem(self, newItemCaption):
        if not self._l.containsId(newItemCaption):
            self.getWindow().showNotification('Added city: ' + newItemCaption)
            self._lastAdded = True
            self._l.addItem(newItemCaption)
            self._l.setValue(newItemCaption)