# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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