# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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