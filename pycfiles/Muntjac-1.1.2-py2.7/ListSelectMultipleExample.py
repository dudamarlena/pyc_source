# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/selects/ListSelectMultipleExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, ListSelect
from muntjac.data.property import IValueChangeListener

class ListSelectMultipleExample(VerticalLayout, IValueChangeListener):
    _cities = [
     'Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo',
     'Paris', 'Stockholm']

    def __init__(self):
        super(ListSelectMultipleExample, self).__init__()
        self.setSpacing(True)
        l = ListSelect('Please select some cities')
        for c in self._cities:
            l.addItem(c)

        l.setRows(7)
        l.setNullSelectionAllowed(True)
        l.setMultiSelect(True)
        l.setImmediate(True)
        l.addListener(self, IValueChangeListener)
        self.addComponent(l)

    def valueChange(self, event):
        self.getWindow().showNotification('Selected cities: %s' % list(event.getProperty().getValue()))