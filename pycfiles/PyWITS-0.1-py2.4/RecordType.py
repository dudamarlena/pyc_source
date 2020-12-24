# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/PyWITS/Objects/RecordType.py
# Compiled at: 2008-05-01 02:04:25
TRIGGER_TIME = 'time'
TRIGGER_DEPTH = 'depth'
TRIGGER_EVENT = 'event'
TRIGGER_TIME_DEPTH = 'timedepth'

class RecordType:
    __module__ = __name__

    def __init__(self, id=None, logical_record_type=None, auto=None, trigger=None, data_source=None, record_items=None):
        self.id = id
        self.logical_record_type = logical_record_type
        self.auto = auto
        self.trigger = trigger
        self.data_source = data_source
        if record_items is not None:
            self.record_items = record_items
        else:
            self.record_items = []
        return

    def __repr__(self):
        t = 'Record Type'
        if self.id is not None:
            t += ' ID: ' + str(self.id)
        if self.logical_record_type is not None:
            t += ' LRT: ' + str(self.logical_record_type)
        if self.auto is not None:
            t += ' Auto: ' + str(self.auto)
        if self.trigger is not None:
            t += ' Trig: ' + str(self.trigger)
        if self.data_source is not None:
            t += ' Data Source: ' + str(self.data_source)
        return t