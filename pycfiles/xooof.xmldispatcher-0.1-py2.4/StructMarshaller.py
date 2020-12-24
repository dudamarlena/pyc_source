# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/tools/marshallers/StructMarshaller.py
# Compiled at: 2008-10-01 10:39:37
from types import StringType, UnicodeType
from IXMLDispatcherMarshaller import IXMLDispatcherMarshaller
from xooof.xmlstruct import xmlstruct

class StructMarshaller(IXMLDispatcherMarshaller):
    __module__ = __name__

    def __init__(self, structFactory, encoding=None):
        self.__structFactory = structFactory
        self.__encoding = encoding

    def marshall(self, o):
        if o is not None:
            if not isinstance(o, xmlstruct.IXMLStruct):
                raise TypeError, 'object must be None or IXMLStruct'
            return o.xsToXML(self.__encoding)
        else:
            return ''
        return

    def marshallId(self, s):
        if self.__encoding and type(s) is UnicodeType:
            s = s.encode(self.__encoding)
        return s

    def unmarshall(self, s):
        if s:
            return xmlstruct.fromXML(self.__structFactory, s)
        else:
            return
        return

    def unmarshallId(self, s):
        return s