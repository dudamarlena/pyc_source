# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsam/find.py
# Compiled at: 2019-05-24 02:34:45
from .sam_api import API, XMLRequest, Filter, ResultFilter

class Find(XMLRequest):
    METHOD = 'find'

    def __init__(self, className):
        XMLRequest.__init__(self)
        self.className = className
        self.tag('fullClassName', className)

    def filter(self, conjunction=None):
        request_filter = Filter(conjunction)
        self.xml.append(request_filter.xml)
        return request_filter

    def result_fields(self, className=None):
        result_filter = ResultFilter(className)
        self.xml.append(result_filter.xml)
        return result_filter

    def request(self, conn, **kw):
        response = XMLRequest.request(self, conn, **kw)
        return response.result.getchildren()