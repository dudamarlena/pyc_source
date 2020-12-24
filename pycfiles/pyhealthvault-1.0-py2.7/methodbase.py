# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/methods/methodbase.py
# Compiled at: 2015-11-17 12:43:50
from lxml import etree

class MethodBase(object):

    def __init__(self, name, version):
        self.name = name
        self.version = version


class RequestBase(MethodBase):

    def __init__(self):
        pass


class ResponseBase(MethodBase):

    def __init__(self):
        self.info = None
        self.NSMAP = None
        return

    def set_info_namespace(self):
        if self.version == 1:
            return {'wc': 'urn:com.microsoft.wc.methods.response.%s' % self.name}
        return {'wc': 'urn:com.microsoft.wc.methods.response.%s%d' % (self.name, self.version)}

    def parse_info(self, response):
        if self.NSMAP is None:
            self.NSMAP = self.set_info_namespace()
        self.info = response.xpath('/response/wc:info', namespaces=self.NSMAP)[0]
        return