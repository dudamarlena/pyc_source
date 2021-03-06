# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/libmetric/alarm.py
# Compiled at: 2017-11-20 07:48:26


class InstantAlarm(object):

    def __init__(self, **kwargs):
        self.alarm_operator = kwargs['alarm_operator']
        self.alarm_threshold = float(kwargs['alarm_threshold'])
        self.data_frame = kwargs['data_frame']
        self.series = kwargs['series']
        self.value = self._aggregate_series()

    def _aggregate_series(self):
        return float(self.data_frame[self.series].item())

    def evaluate(self):
        print ('Question: {} {} {}?').format(self.alarm_threshold, self.alarm_operator, self.value)
        response = False
        if self.alarm_operator == 'gt':
            if self.alarm_threshold > self.value:
                response = True
        elif self.alarm_operator == 'gte':
            if self.alarm_threshold >= self.value:
                response = True
        elif self.alarm_operator == 'lt':
            if self.alarm_threshold < self.value:
                response = True
        elif self.alarm_operator == 'lte':
            if self.alarm_threshold <= self.value:
                response = True
        elif self.alarm_operator == 'eq':
            if self.alarm_threshold == self.value:
                response = True
        return response


class RangeAlarm(InstantAlarm):

    def __init__(self, **kwargs):
        self.alarm_operator = kwargs['alarm_operator']
        self.alarm_threshold = float(kwargs['alarm_threshold'])
        self.data_frame = kwargs['data_frame']
        self.aggregation = kwargs['aggregation']
        self.series = kwargs['series']
        self.value = self._aggregate_series()

    def _aggregate_series(self):
        if self.aggregation == 'avg':
            self.value = float(self.data_frame[self.series].mean())
        elif self.aggregation == 'min':
            self.value = float(self.data_frame[self.series].min())
        elif self.aggregation == 'max':
            self.value = float(self.data_frame[self.series].max())
        else:
            self.value = float(self.data_frame[self.series].sum())