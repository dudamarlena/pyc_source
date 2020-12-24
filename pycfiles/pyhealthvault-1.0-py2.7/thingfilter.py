# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/thingfilter.py
# Compiled at: 2015-12-15 14:25:04
from lxml import etree

class ThingFilter:

    def __init__(self):
        self.typeids = []

    def write_xml(self):
        _filter = etree.Element('filter')
        if self.typeids:
            self.add_typeids(_filter)
        return _filter

    def add_typeids(self, _filter):
        for i in self.typeids:
            typeid = etree.Element('type-id')
            typeid.text = i
            _filter.append(typeid)