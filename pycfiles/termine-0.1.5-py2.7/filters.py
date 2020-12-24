# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/termine/filters.py
# Compiled at: 2012-07-14 06:28:13
from termine.genericlogger import logger
from datetime import datetime

class GWFilter:

    def __init__(self, client):
        logger.debug('initializing GWFilter')
        self.dtfmt = '%Y-%m-%dT%H:%M:%SZ'
        self.start_str = '%Y-%m-%dT00:00:00Z'
        self.end_str = '%Y-%m-%dT23:59:59Z'
        self.FilterGroup = client.factory.create('ns2:FilterGroup')
        self.FilterGroup.op = 'and'
        self.Appointment = client.factory.create('ns2:FilterEntry')
        self.Appointment.field = '@type'
        self.Appointment.value = 'Appointment'
        self.Appointment.op = 'eq'
        self.Start = client.factory.create('ns2:FilterEntry')
        self.x = client.factory.create('ns2:FilterDate')
        self.End = client.factory.create('ns2:FilterEntry')
        self.y = client.factory.create('ns2:FilterDate')

    def specificdate(self, dt):
        """ Find all appointments on a specific date. These are the
        appointments that start on or before the date and end on
        or after the specific date. This way we also capture e.g. 
        appointments that span an entire week and include the specific
        date """
        logger.debug('GWFilter.specificdate(%s)' % dt)
        s = datetime.strptime(dt.strftime(self.start_str), self.dtfmt)
        e = datetime.strptime(dt.strftime(self.end_str), self.dtfmt)
        self.Start.field = 'startDate'
        self.Start.op = 'fieldLTE'
        self.Start.date = s.strftime(self.dtfmt)
        self.End.field = 'endDate'
        self.End.op = 'fieldGTE'
        self.End.date = e.strftime(self.dtfmt)
        self.FilterGroup.element.append(self.Appointment)
        self.FilterGroup.element.append(self.Start)
        self.FilterGroup.element.append(self.End)
        print self.FilterGroup
        return self.FilterGroup

    def today(self):
        logger.debug('GWFilter.today()')
        self.Start.field = 'startDate'
        self.Start.op = 'fieldLTE'
        self.Start.date = self.x.Today
        self.End.field = 'endDate'
        self.End.op = 'fieldGTE'
        self.End.date = self.x.Today
        self.FilterGroup.element.append(self.Appointment)
        self.FilterGroup.element.append(self.Start)
        self.FilterGroup.element.append(self.End)
        return self.FilterGroup

    def yesterday(self):
        logger.debug('GWFilter.yesterday()')
        self.Start.field = 'startDate'
        self.Start.op = 'fieldLTE'
        self.Start.date = self.x.Yesterday
        self.End.field = 'endDate'
        self.End.op = 'fieldGTE'
        self.End.date = self.x.Yesterday
        self.FilterGroup.element.append(self.Appointment)
        self.FilterGroup.element.append(self.Start)
        self.FilterGroup.element.append(self.End)
        return self.FilterGroup

    def tomorrow(self):
        logger.debug('GWFilter.tomorrow()')
        self.Start.field = 'startDate'
        self.Start.op = 'fieldLTE'
        self.Start.date = self.x.Tomorrow
        self.End.field = 'endDate'
        self.End.op = 'fieldGTE'
        self.End.date = self.x.Tomorrow
        self.FilterGroup.element.append(self.Appointment)
        self.FilterGroup.element.append(self.Start)
        self.FilterGroup.element.append(self.End)
        return self.FilterGroup

    def thisweek(self):
        logger.debug('GWFilter.thisweek()')
        self.Start.field = 'startDate'
        self.Start.op = 'fieldLTE'
        self.Start.date = self.x.ThisWeek
        self.End.field = 'endDate'
        self.End.op = 'fieldGTE'
        self.End.date = self.x.ThisWeek
        self.FilterGroup.element.append(self.Appointment)
        self.FilterGroup.element.append(self.Start)
        self.FilterGroup.element.append(self.End)
        return self.FilterGroup

    def thismonth(self):
        logger.debug('GWFilter.thismonth()')
        self.Start.field = 'startDate'
        self.Start.op = 'fieldLTE'
        self.Start.date = self.x.ThisMonth
        self.End.field = 'endDate'
        self.End.op = 'fieldGTE'
        self.End.date = self.x.ThisMonth
        self.FilterGroup.element.append(self.Appointment)
        self.FilterGroup.element.append(self.Start)
        self.FilterGroup.element.append(self.End)
        return self.FilterGroup

    def thisyear(self):
        logger.debug('GWFilter.thisyear()')
        self.Start.field = 'startDate'
        self.Start.op = 'fieldLTE'
        self.Start.date = self.x.ThisYear
        self.End.field = 'endDate'
        self.End.op = 'fieldGTE'
        self.End.date = self.x.ThisYear
        self.FilterGroup.element.append(self.Appointment)
        self.FilterGroup.element.append(self.Start)
        self.FilterGroup.element.append(self.End)
        return self.FilterGroup