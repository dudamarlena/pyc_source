# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/thingformat.py
# Compiled at: 2015-12-15 14:25:14
from lxml import etree

class ThingFormat:

    def __init__(self):
        self.sections = []
        self.xml = None
        return

    def write_xml(self):
        _format = etree.Element('format')
        if self.sections:
            self.add_sections(_format)
        if 'xml' in self.sections:
            xml = etree.Element('xml')
            if self.xml is not None:
                xml.append(etree.fromstring(self.xml))
            _format.append(xml)
        return _format

    def add_sections(self, _filter):
        for i in self.sections:
            if i in ('core', 'audits', 'effectivepermissions', 'digitalsignatures',
                     'tags', 'blobpayload'):
                section = etree.Element('section')
                section.text = i
                _filter.append(section)