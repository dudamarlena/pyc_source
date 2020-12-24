# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/net/www/xml.py
# Compiled at: 2016-07-25 10:38:46
"""XML parsers"""
import re, xmllib
illegal = re.compile(b'[^\t\r\n -\xff]')
xmllib.illegal = illegal

def join_xml_attrs(attrs):
    attr_list = [
     '']
    for (attrname, value) in attrs.items():
        attr_list.append('%s="%s"' % (attrname, string.strip(value)))

    return string.join(attr_list, ' ')


class XMLParser(xmllib.XMLParser):

    def __init__(self):
        xmllib.XMLParser.__init__(self)
        self.accumulator = ''

    def handle_data(self, data):
        if data:
            self.accumulator = '%s%s' % (self.accumulator, data)

    def handle_comment(self, data):
        if data:
            self.accumulator = '%s<!--%s-->' % (self.accumulator, data)

    def unknown_starttag(self, tag, attrs):
        self.accumulator = '%s<%s%s>' % (self.accumulator, tag, join_xml_attrs(attrs))

    def unknown_endtag(self, tag):
        self.accumulator = '%s</%s>' % (self.accumulator, tag)


class XMLFilter(XMLParser):

    def handle_comment(self, data):
        pass

    def unknown_starttag(self, tag, attrs):
        pass

    def unknown_endtag(self, tag):
        pass


def filter_xml(str, filter=None):
    """Process XML using some XML parser/filter"""
    if filter is None:
        filter = XMLFilter()
    filter.feed(str)
    return filter.accumulator