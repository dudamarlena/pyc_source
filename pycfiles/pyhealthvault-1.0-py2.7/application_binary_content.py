# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/application_binary_content.py
# Compiled at: 2015-12-14 13:21:04


class ApplicationBinaryContent:

    def __init__(self, content_xml=None):
        self.content_type = ''
        self.culture_specific_content = {}
        if content_xml is not None:
            self.parse_xml(content_xml)
        return

    def parse_xml(self, content_xml):
        XMLNS = '{http://www.w3.org/XML/1998/namespace}'
        for content in content_xml.xpath('logo'):
            self.culture_specific_content[content.get(XMLNS + 'lang', default='')] = content.xpath('text()')[0]

        self.content_type = content_xml.xpath('content-type/text()')[0]