# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/services/administrator/perflog.py
# Compiled at: 2012-10-12 07:02:39


class PerformanceLog(object):

    def __init__(self):
        self._data = {}

    @property
    def data(self):
        return self._data

    def clear(self):
        self._data = {}

    def insert_record(self, lname, oname, runtime=0.0, error=False):
        runtime = round(runtime, 4)
        if lname not in self.data:
            self.data[lname] = {}
        if oname not in self.data[lname]:
            self.data[lname][oname] = {'total': runtime, 'counter': 1, 'errors': 0, 
               'max': runtime, 
               'min': runtime}
        else:
            self.data[lname][oname]['counter'] += 1
            self.data[lname][oname]['total'] += runtime
            if error:
                self.data[lname][oname]['errors'] += 1
            elif runtime > self.data[lname][oname]['max']:
                self.data[lname][oname]['max'] = runtime
            elif runtime < self.data[lname][oname]['min']:
                self.data[lname][oname]['min'] = runtime