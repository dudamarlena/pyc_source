# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/foundation/reports/caldav_calendar_multiget.py
# Compiled at: 2012-10-12 07:02:39
from xml.dom import minidom
from pytz import timezone
from datetime import datetime
from namespaces import XML_NAMESPACE, ALL_PROPS
from report import Report

class caldav_calendar_multiget(Report):

    def __init__(self, document, user_agent_description):
        Report.__init__(self, document, user_agent_description)

    @property
    def report_name(self):
        return 'calendar-multiget'

    @property
    def parameters(self):
        return {}

    @property
    def references(self):
        self._hrefs = []
        hrefs = self._source.getElementsByTagNameNS('DAV:', 'href')
        for href in hrefs:
            self._hrefs.append(href.firstChild.data)

        return self._hrefs