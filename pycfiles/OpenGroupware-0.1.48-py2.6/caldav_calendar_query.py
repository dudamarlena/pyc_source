# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/foundation/reports/caldav_calendar_query.py
# Compiled at: 2012-10-12 07:02:39
from xml.dom import minidom
from pytz import timezone
from datetime import datetime
from namespaces import XML_NAMESPACE, ALL_PROPS
from report import Report

class caldav_calendar_query(Report):

    def __init__(self, document, user_agent_description):
        Report.__init__(self, document, user_agent_description)

    @property
    def report_name(self):
        return 'calendar-query'

    @property
    def parameters(self):
        if self._params is None:
            _params = {}
            ranges = self._source.getElementsByTagNameNS('urn:ietf:params:xml:ns:caldav', 'time-range')
            if len(ranges) == 0:
                ranges = self._source.getElementsByTagNameNS('http://calendarserver.org/ns/', 'time-range')
            if len(ranges) > 0:
                time_range = ranges[0]
                if 'start' in time_range.attributes.keys():
                    value = datetime.strptime(time_range.attributes['start'].value, '%Y%m%dT%H%M%SZ')
                    value = value.replace(tzinfo=timezone('UTC'))
                    _params['start'] = value
                if 'end' in time_range.attributes.keys():
                    value = datetime.strptime(time_range.attributes['end'].value, '%Y%m%dT%H%M%SZ')
                    value = value.replace(tzinfo=timezone('UTC'))
                    _params['end'] = value
            self._params = _params
        return self._params

    @property
    def command(self):
        return 'appointment::get-range'