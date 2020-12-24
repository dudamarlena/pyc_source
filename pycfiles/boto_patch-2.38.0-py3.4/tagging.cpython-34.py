# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/s3/tagging.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1732 bytes
from boto import handler
import xml.sax

class Tag(object):

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Key':
            self.key = value
        elif name == 'Value':
            self.value = value

    def to_xml(self):
        return '<Tag><Key>%s</Key><Value>%s</Value></Tag>' % (
         self.key, self.value)

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value


class TagSet(list):

    def startElement(self, name, attrs, connection):
        if name == 'Tag':
            tag = Tag()
            self.append(tag)
            return tag

    def endElement(self, name, value, connection):
        setattr(self, name, value)

    def add_tag(self, key, value):
        tag = Tag(key, value)
        self.append(tag)

    def to_xml(self):
        xml = '<TagSet>'
        for tag in self:
            xml += tag.to_xml()

        xml += '</TagSet>'
        return xml


class Tags(list):
    __doc__ = 'A container for the tags associated with a bucket.'

    def startElement(self, name, attrs, connection):
        if name == 'TagSet':
            tag_set = TagSet()
            self.append(tag_set)
            return tag_set

    def endElement(self, name, value, connection):
        setattr(self, name, value)

    def to_xml(self):
        xml = '<Tagging>'
        for tag_set in self:
            xml += tag_set.to_xml()

        xml += '</Tagging>'
        return xml

    def add_tag_set(self, tag_set):
        self.append(tag_set)