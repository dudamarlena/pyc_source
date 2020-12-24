# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\fakes.py
# Compiled at: 2016-04-11 03:21:39
# Size of source mod 2**32: 2736 bytes
from io import StringIO
from mad.log import Log, Event
from mad.storage import DataStorage
from mad.monitoring import CSVReport

class InMemoryDataStorage(DataStorage):

    def __init__(self, model):
        self._log = InMemoryLog()
        self._model = model
        self._opened_reports = {}

    @property
    def log(self):
        return self._log

    def model(self):
        return self._model

    def report_for(self, entity, format):
        if entity not in self._opened_reports:
            self._opened_reports[entity] = CSVReport(StringIO(), format)
        return self._opened_reports[entity]


class InMemoryFileSystem:

    def __init__(self):
        self.opened_files = {}

    def define(self, location, content):
        self.opened_files[location] = StringIO(content)

    def open_input_stream(self, location):
        if location not in self.opened_files:
            raise FileNotFoundError(location)
        return self.opened_files[location]

    def open_output_stream(self, location):
        if location not in self.opened_files:
            self.opened_files[location] = StringIO()
        return self.opened_files[location]

    def has_file(self, file):
        for any_location in self.opened_files:
            if any_location.endswith(file):
                return True

        return False


class InMemoryLog(Log):
    __doc__ = '\n    Hold the history of events in a list for later processing\n    '

    def __init__(self):
        self.entries = []

    def __repr__(self):
        return '\n'.join([str(each_entry) for each_entry in self.entries])

    def __len__(self):
        return len(self.entries)

    def __iter__(self):
        for each_entry in self.entries:
            yield each_entry

    @property
    def is_empty(self):
        return len(self) == 0

    @property
    def size(self):
        return len(self)

    def record(self, time, context, message):
        self.entries.append(Event(time, context, message))