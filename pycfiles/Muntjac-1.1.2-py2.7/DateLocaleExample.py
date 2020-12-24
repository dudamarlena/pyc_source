# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/dates/DateLocaleExample.py
# Compiled at: 2013-04-04 15:36:38
from datetime import datetime
from muntjac.api import VerticalLayout, InlineDateField, ComboBox
from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.data.property import IValueChangeListener

class DateLocaleExample(VerticalLayout, IValueChangeListener):

    def __init__(self):
        super(DateLocaleExample, self).__init__()
        self.setSpacing(True)
        self._datetime = InlineDateField('Please select the starting time:')
        self._datetime.setValue(datetime.today())
        self._datetime.setResolution(InlineDateField.RESOLUTION_MIN)
        self._datetime.setImmediate(True)
        self._datetime.setShowISOWeekNumbers(True)
        self._localeSelection = ComboBox('Select date format:')
        self._localeSelection.addListener(self, IValueChangeListener)
        self._localeSelection.setImmediate(True)
        self._localeSelection.setContainerDataSource(ExampleUtil.getLocaleContainer())
        self._localeSelection.setNullSelectionAllowed(False)
        self.addComponent(self._datetime)
        self.addComponent(self._localeSelection)

    def valueChange(self, event):
        selected = self._localeSelection.getItem(event.getProperty().getValue())
        self._datetime.setLocale(selected.getItemProperty(ExampleUtil.locale_PROPERTY_LOCALE).getValue())
        self._datetime.requestRepaint()