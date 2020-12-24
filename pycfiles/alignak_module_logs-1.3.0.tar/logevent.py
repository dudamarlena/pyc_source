# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alignak/alignak-module-logs/alignak_module_logs/logevent.py
# Compiled at: 2017-03-11 05:29:19
"""
This module lists provide facilities to parse log type Broks.
The supported event are listed in the event_type variable
"""
import re
EVENT_TYPE_PATTERN = re.compile('^\\[[0-9]{10}] (?:HOST|SERVICE) (ALERT|NOTIFICATION|FLAPPING|DOWNTIME)(?: ALERT)?:.*')
EVENT_TYPES = {'NOTIFICATION': {'pattern': '\\[([0-9]{10})\\] (HOST|SERVICE) (NOTIFICATION): ([^\\;]*);([^\\;]*);(?:([^\\;]*);)?([^\\;]*);([^\\;]*);([^\\;]*)', 
                    'properties': [
                                 'time',
                                 'notification_type',
                                 'event_type',
                                 'contact',
                                 'hostname',
                                 'service_desc',
                                 'state',
                                 'notification_method',
                                 'output']}, 
   'ALERT': {'pattern': '^\\[([0-9]{10})] (HOST|SERVICE) (ALERT): ([^\\;]*);(?:([^\\;]*);)?([^\\;]*);([^\\;]*);([^\\;]*);([^\\;]*)', 
             'properties': [
                          'time',
                          'alert_type',
                          'event_type',
                          'hostname',
                          'service_desc',
                          'state',
                          'state_type',
                          'attempts',
                          'output']}, 
   'DOWNTIME': {'pattern': '^\\[([0-9]{10})] (HOST|SERVICE) (DOWNTIME) ALERT: ([^\\;]*);(?:([^\\;]*);)?([^\\;]*);([^\\;]*)', 
                'properties': [
                             'time',
                             'downtime_type',
                             'event_type',
                             'hostname',
                             'service_desc',
                             'state',
                             'output']}, 
   'FLAPPING': {'pattern': '^\\[([0-9]{10})] (HOST|SERVICE) (FLAPPING) ALERT: ([^\\;]*);(?:([^\\;]*);)?([^\\;]*);([^\\;]*)', 
                'properties': [
                             'time',
                             'alert_type',
                             'event_type',
                             'hostname',
                             'service_desc',
                             'state',
                             'output']}}

class LogEvent(object):
    """Class for parsing event logs
    Populates self.data with the log type's properties
    """

    def __init__(self, log):
        self.data = {}
        self.valid = False
        self.time = None
        self.event_type = 'unknown'
        event_type_match = EVENT_TYPE_PATTERN.match(log)
        if event_type_match:
            event_type = EVENT_TYPES[event_type_match.group(1)]
            properties_match = re.match(event_type['pattern'], log)
            if properties_match:
                self.valid = True
                for i, prop in enumerate(event_type['properties']):
                    self.data[prop] = properties_match.group(i + 1)

                self.data['time'] = int(self.data['time'])
                if 'event_type' in self.data:
                    self.event_type = self.data['event_type']
                if 'attempts' in self.data:
                    self.data['attempts'] = int(self.data['attempts'])
        return

    def __iter__(self):
        return self.data.iteritems()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __contains__(self, key):
        return key in self.data

    def __str__(self):
        return str(self.data)