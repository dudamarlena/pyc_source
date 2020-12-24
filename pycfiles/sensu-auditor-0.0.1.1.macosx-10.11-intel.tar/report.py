# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benwaters/sensu-auditor/lib/python2.7/site-packages/sensu_auditor/report.py
# Compiled at: 2016-09-05 05:54:14
from __future__ import print_function
from datetime import datetime
import socket, pprint

class SensuReport(object):

    def get_groups(self):
        return self.content.keys()

    def get_group_by_check(self, check):
        for key in self.content.keys():
            if check in self.content[key]:
                return key

    def add_raw_entries(self, list_of_entries):
        for x in list_of_entries:
            self.content[x.category][x.check_name]['dt'] += x.downtime
            self.total_downtime += x.downtime

    def __init__(self, downtime):
        self.date = datetime.utcnow()
        self.hostname = socket.gethostname()
        self.total_downtime = float(downtime)
        self.content = {}

    def __str__(self):
        pprint.PrettyPrinter(indent=2)
        return ('Host: {}\nDate: {}\nTotal Downtime: {} (seconds) {} (minutes) {} (hours) \n{}').format(self.hostname, self.date, self.total_downtime, self.total_downtime / 60, self.total_downtime / 60.0 / 60.0, pprint.pformat(self.content))