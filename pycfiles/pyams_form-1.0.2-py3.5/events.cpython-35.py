# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/events.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 1196 bytes
"""PyAMS_form.events module

Data extraction event.
"""
from zope.interface import implementer
from zope.lifecycleevent import ObjectCreatedEvent
from pyams_form.interfaces.form import IDataExtractedEvent, IFormCreatedEvent
__docformat__ = 'restructuredtext'

@implementer(IFormCreatedEvent)
class FormCreatedEvent(ObjectCreatedEvent):
    __doc__ = 'Form created event'

    def __init__(self, form):
        super(FormCreatedEvent, self).__init__(form)
        self.request = form.request


@implementer(IDataExtractedEvent)
class DataExtractedEvent:
    __doc__ = 'Data extracted event'

    def __init__(self, data, errors, form):
        self.data = data
        self.errors = errors
        self.form = form