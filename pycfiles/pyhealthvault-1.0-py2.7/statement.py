# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/statement.py
# Compiled at: 2015-12-15 14:25:38


class Statement:

    def __init__(self, statement_xml=None):
        self.statement = {}
        self.content_type = ''
        if statement_xml is not None:
            self.parse_xml(statement_xml)
        return

    def parse_xml(self, statement_xml):
        self.statement = self.get_culture_specific_dictionary(statement_xml, 'statement')
        self.content_type = statement_xml.xpath('content-type/text()')[0]

    def get_culture_specific_dictionary(self, info_element, key):
        XMLNS = '{http://www.w3.org/XML/1998/namespace}'
        result = {}
        for entry in info_element.xpath(key):
            lang = entry.get(XMLNS + 'lang', default='')
            result[lang] = entry.xpath('text()')[0]

        return result