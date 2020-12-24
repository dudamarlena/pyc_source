# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/selects/OptionGroupsExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, OptionGroup, Label
from muntjac.data.property import IValueChangeListener

class OptionGroupsExample(VerticalLayout, IValueChangeListener):
    _cities = [
     'Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo',
     'Paris', 'Stockholm']

    def __init__(self):
        super(OptionGroupsExample, self).__init__()
        self.setSpacing(True)
        citySelect = OptionGroup('Please select a city', self._cities)
        citySelect.setNullSelectionAllowed(False)
        citySelect.select('Berlin')
        citySelect.setImmediate(True)
        citySelect.addListener(self, IValueChangeListener)
        self.addComponent(citySelect)
        self.addComponent(Label('<h3>Multi-selection</h3>', Label.CONTENT_XHTML))
        citySelect = OptionGroup('Please select cities', self._cities)
        citySelect.setMultiSelect(True)
        citySelect.setNullSelectionAllowed(False)
        citySelect.select('Berlin')
        citySelect.setImmediate(True)
        citySelect.addListener(self, IValueChangeListener)
        self.addComponent(citySelect)

    def valueChange(self, event):
        v = event.getProperty().getValue()
        if isinstance(v, set):
            v = list(v)
        self.getWindow().showNotification('Selected city: %s' % v)