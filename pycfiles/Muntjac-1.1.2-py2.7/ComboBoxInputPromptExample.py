# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/selects/ComboBoxInputPromptExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, ComboBox
from muntjac.data.property import IValueChangeListener

class ComboBoxInputPromptExample(VerticalLayout, IValueChangeListener):
    _cities = [
     'Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo',
     'Paris', 'Stockholm']

    def __init__(self):
        super(ComboBoxInputPromptExample, self).__init__()
        self.setMargin(True, False, False, False)
        l = ComboBox()
        l.setInputPrompt('Please select a city')
        l.setImmediate(True)
        l.addListener(self, IValueChangeListener)
        for c in self._cities:
            l.addItem(c)

        self.addComponent(l)

    def valueChange(self, event):
        self.getWindow().showNotification('Selected city: ' + str(event.getProperty()))