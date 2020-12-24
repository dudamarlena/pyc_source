# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/methods/putthings.py
# Compiled at: 2015-12-14 10:31:10
from lxml import etree
from healthvaultlib.methods.method import Method
from healthvaultlib.methods.methodbase import RequestBase, ResponseBase
from healthvaultlib.objects.thingkey import ThingKey

class PutThingsRequest(RequestBase):

    def __init__(self, items):
        super(PutThingsRequest, self).__init__()
        self.name = 'PutThings'
        self.version = 2
        self.healthrecorditems = items

    def get_info(self):
        info = etree.Element('info')
        for item in self.healthrecorditems:
            info.append(item.write_xml())

        return info


class PutThingsResponse(ResponseBase):

    def __init__(self, items):
        super(PutThingsResponse, self).__init__()
        self.name = 'PutThings'
        self.version = 1
        self.healthrecorditems = items

    def parse_response(self, response):
        self.parse_info(response)
        i = 0
        for key in self.info.xpath('thing-id'):
            thing_key = ThingKey(key)
            self.healthrecorditems[i].key = thing_key
            i += 1


class PutThings(Method):

    def __init__(self, items):
        self.request = PutThingsRequest(items)
        self.response = PutThingsResponse(items)