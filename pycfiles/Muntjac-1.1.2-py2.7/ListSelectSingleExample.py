# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/selects/ListSelectSingleExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, ListSelect
from muntjac.data.property import IValueChangeListener

class ListSelectSingleExample(VerticalLayout, IValueChangeListener):
    _cities = [
     'Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo',
     'Paris', 'Stockholm']

    def __init__(self):
        super(ListSelectSingleExample, self).__init__()
        self.setSpacing(True)
        citySelect = ListSelect('Please select a city', self._cities)
        citySelect.setRows(7)
        citySelect.setNullSelectionAllowed(False)
        citySelect.select('Berlin')
        citySelect.setImmediate(True)
        citySelect.addListener(self, IValueChangeListener)
        self.addComponent(citySelect)

    def valueChange(self, event):
        self.getWindow().showNotification('Selected city: ' + str(event.getProperty()))