# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/video/amf.py
# Compiled at: 2009-09-07 17:44:28
"""
AMF metadata (inside Flash video, FLV file) parser.

Documentation:

 - flashticle: Python project to read Flash (formats SWF, FLV and AMF)
   http://undefined.org/python/#flashticle

Author: Victor Stinner
Creation date: 4 november 2006
"""
from hachoir_core.field import FieldSet, ParserError, UInt8, UInt16, UInt32, PascalString16, Float64
from hachoir_core.tools import timestampUNIX

def parseUTF8(parent):
    yield PascalString16(parent, 'value', charset='UTF-8')


def parseDouble(parent):
    yield Float64(parent, 'value')


def parseBool(parent):
    yield UInt8(parent, 'value')


def parseArray(parent):
    yield UInt32(parent, 'count')
    for index in xrange(parent['count'].value):
        yield AMFObject(parent, 'item[]')


def parseObjectAttributes(parent):
    while True:
        item = Attribute(parent, 'attr[]')
        yield item
        if item['key'].value == '':
            break


def parseMixedArray(parent):
    yield UInt32(parent, 'count')
    for index in xrange(parent['count'].value + 1):
        item = Attribute(parent, 'item[]')
        yield item
        if not item['key'].value:
            break


def parseDate(parent):
    yield Float64(parent, 'timestamp_microsec')
    yield UInt16(parent, 'timestamp_sec')


def parseNothing(parent):
    raise StopIteration()


class AMFObject(FieldSet):
    __module__ = __name__
    CODE_DATE = 11
    tag_info = {0: (parseDouble, 'Double'), 1: (parseBool, 'Boolean'), 2: (parseUTF8, 'UTF-8 string'), 3: (parseObjectAttributes, 'Object attributes'), 8: (parseMixedArray, 'Mixed array'), 9: (parseNothing, 'End of object'), 10: (parseArray, 'Array'), CODE_DATE: (parseDate, 'Date')}

    def __init__(self, *args, **kw):
        FieldSet.__init__(self, *args, **kw)
        code = self['type'].value
        try:
            (self.parser, desc) = self.tag_info[code]
            if code == self.CODE_DATE:
                self.createValue = self.createValueDate
        except KeyError:
            raise ParserError('AMF: Unable to parse type %s' % code)

    def createFields(self):
        yield UInt8(self, 'type')
        for field in self.parser(self):
            yield field

    def createValueDate(self):
        value = self['timestamp_microsec'].value * 0.001 - self['timestamp_sec'].value * 60
        return timestampUNIX(value)


class Attribute(AMFObject):
    __module__ = __name__

    def __init__(self, *args):
        AMFObject.__init__(self, *args)
        self._description = None
        return

    def createFields(self):
        yield PascalString16(self, 'key', charset='UTF-8')
        yield UInt8(self, 'type')
        for field in self.parser(self):
            yield field

    def createDescription(self):
        return 'Attribute "%s"' % self['key'].value