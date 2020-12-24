# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/foundation/reports/report.py
# Compiled at: 2012-10-12 07:02:39
import logging
from xml.dom import minidom
from coils.core import NotImplementedException
from parser import Parser
from namespaces import XML_NAMESPACE, ALL_PROPS
PROP_METHOD = 0
PROP_NAMESPACE = 1
PROP_LOCALNAME = 2
PROP_DOMAIN = 3

class Report(object):

    def __init__(self, document, user_agent_description):
        self._source = document
        self._properties = None
        self._namespaces = None
        self._params = None
        self._hrefs = None
        self._uad = user_agent_description
        return

    @property
    def properties(self):
        if self._properties is None:
            (self._properties, self._namespaces) = Parser.properties(self._source, self._uad)
            if len(self._properties) == 0:
                properties = ALL_PROPS
        return (
         self._properties, self._namespaces)

    @property
    def report_name(self):
        raise NotImplementedException('This report is unnamed.')

    @property
    def parameters(self):
        raise NotImplementedException('This report does not implement parameter parsing.')

    @property
    def command(self):
        raise NotImplementedException('This report does not specify a Logic command.')

    @property
    def references(self):
        raise NotImplementedException('This report does not enumerate references.')