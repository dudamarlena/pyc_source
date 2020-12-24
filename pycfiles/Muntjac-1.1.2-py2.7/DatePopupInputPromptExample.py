# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/dates/DatePopupInputPromptExample.py
# Compiled at: 2013-04-04 15:36:38
from datetime import datetime
from babel.dates import format_date
from muntjac.api import VerticalLayout, PopupDateField
from muntjac.data.property import IValueChangeListener

class DatePopupInputPromptExample(VerticalLayout, IValueChangeListener):

    def __init__(self):
        super(DatePopupInputPromptExample, self).__init__()
        self.setSpacing(True)
        self._startDate = PopupDateField()
        self._startDate.setInputPrompt('Start date')
        self._startDate.setResolution(PopupDateField.RESOLUTION_DAY)
        self._startDate.addListener(self, IValueChangeListener)
        self._startDate.setImmediate(True)
        self.addComponent(self._startDate)

    def valueChange(self, event):
        app = self.getApplication()
        if app is not None:
            l = app.getLocale()
        value = event.getProperty().getValue()
        if value is None or not isinstance(value, datetime):
            self.getWindow().showNotification('Invalid date entered')
        else:
            dateOut = format_date(value, locale=l).encode('utf-8')
            self.getWindow().showNotification('Starting date: ' + dateOut)
        return