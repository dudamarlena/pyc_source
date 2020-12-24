# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/thinggroupresponse.py
# Compiled at: 2016-01-05 13:14:41
from healthvaultlib.itemtypes.itemtype_resolver import ItemTypeResolver

class ThingGroupResponse:

    def __init__(self, group_xml):
        self.healthrecorditems = []
        resolver = ItemTypeResolver()
        for healthrecorditem in group_xml.xpath('thing'):
            typeid = healthrecorditem.xpath('type-id/text()')[0]
            item = resolver.get_class(typeid)(healthrecorditem)
            self.healthrecorditems.append(item)

        for partialitem in group_xml.xpath('unprocessed-thing-key-info'):
            typeid = healthrecorditem.xpath('type-id/text()')[0]
            item = resolver.get_class(typeid)(partialitem)
            self.healthrecorditems.append(item)