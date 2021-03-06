# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/dates/DateInlineExample.py
# Compiled at: 2013-04-04 15:36:38
from datetime import datetime
from babel.dates import format_date
from muntjac.api import VerticalLayout, InlineDateField
from muntjac.data.property import IValueChangeListener

class DateInlineExample(VerticalLayout, IValueChangeListener):

    def __init__(self):
        super(DateInlineExample, self).__init__()
        self.setSpacing(True)
        self._datetime = InlineDateField('Please select the starting time:')
        self._datetime.setValue(datetime.today())
        self._datetime.setResolution(InlineDateField.RESOLUTION_DAY)
        self._datetime.addListener(self, IValueChangeListener)
        self._datetime.setImmediate(True)
        self.addComponent(self._datetime)

    def valueChange(self, event):
        app = self.getApplication()
        if app is not None:
            l = app.getLocale()
        dateOut = format_date(event.getProperty().getValue(), locale=l).encode('utf-8')
        self.getWindow().showNotification('Starting date: ' + dateOut)
        return