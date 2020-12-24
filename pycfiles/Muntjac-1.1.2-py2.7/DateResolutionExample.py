# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/dates/DateResolutionExample.py
# Compiled at: 2013-04-04 15:36:38
from datetime import datetime
from muntjac.api import VerticalLayout, InlineDateField, ComboBox
from muntjac.data.property import IValueChangeListener
from muntjac.data.util.indexed_container import IndexedContainer

class DateResolutionExample(VerticalLayout, IValueChangeListener):
    resolution_PROPERTY_NAME = 'name'
    _resolutions = [
     InlineDateField.RESOLUTION_YEAR,
     InlineDateField.RESOLUTION_MONTH,
     InlineDateField.RESOLUTION_DAY,
     InlineDateField.RESOLUTION_HOUR,
     InlineDateField.RESOLUTION_MIN,
     InlineDateField.RESOLUTION_SEC,
     InlineDateField.RESOLUTION_MSEC]
    _resolutionNames = [
     'Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'Millisecond']

    def __init__(self):
        super(DateResolutionExample, self).__init__()
        self.setSpacing(True)
        self._datetime = InlineDateField('Please select the starting time:')
        self._datetime.setValue(datetime.today())
        self._datetime.setResolution(InlineDateField.RESOLUTION_DAY)
        self._datetime.setImmediate(True)
        self._localeSelection = ComboBox('Select resolution:')
        self._localeSelection.setNullSelectionAllowed(False)
        self._localeSelection.addListener(self, IValueChangeListener)
        self._localeSelection.setImmediate(True)
        self._localeSelection.setContainerDataSource(self.getResolutionContainer())
        self._localeSelection.setItemCaptionPropertyId(self.resolution_PROPERTY_NAME)
        self._localeSelection.setItemCaptionMode(ComboBox.ITEM_CAPTION_MODE_PROPERTY)
        self.addComponent(self._datetime)
        self.addComponent(self._localeSelection)

    def valueChange(self, event):
        self._datetime.setResolution(event.getProperty().getValue())
        self._datetime.requestRepaint()

    def getResolutionContainer(self):
        resolutionContainer = IndexedContainer()
        resolutionContainer.addContainerProperty(self.resolution_PROPERTY_NAME, str, None)
        for i, res in enumerate(self._resolutions):
            added = resolutionContainer.addItem(res)
            added.getItemProperty(self.resolution_PROPERTY_NAME).setValue(self._resolutionNames[i])

        return resolutionContainer