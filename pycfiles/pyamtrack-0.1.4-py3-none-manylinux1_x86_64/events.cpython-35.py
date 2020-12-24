# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/events.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 1196 bytes
__doc__ = 'PyAMS_form.events module\n\nData extraction event.\n'
from zope.interface import implementer
from zope.lifecycleevent import ObjectCreatedEvent
from pyams_form.interfaces.form import IDataExtractedEvent, IFormCreatedEvent
__docformat__ = 'restructuredtext'

@implementer(IFormCreatedEvent)
class FormCreatedEvent(ObjectCreatedEvent):
    """FormCreatedEvent"""

    def __init__(self, form):
        super(FormCreatedEvent, self).__init__(form)
        self.request = form.request


@implementer(IDataExtractedEvent)
class DataExtractedEvent:
    """DataExtractedEvent"""

    def __init__(self, data, errors, form):
        self.data = data
        self.errors = errors
        self.form = form