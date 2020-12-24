# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/suds/xsd/sxbuiltin.py
# Compiled at: 2009-11-06 13:02:39
"""
The I{sxbuiltin} module provides classes that represent
XSD I{builtin} schema objects.
"""
from logging import getLogger
from suds import *
from suds.xsd import *
from suds.sax.date import *
from suds.xsd.sxbase import XBuiltin
import datetime as dt
log = getLogger(__name__)

class XString(XBuiltin):
    """
    Represents an (xsd) <xs:string/> node
    """
    pass


class XAny(XBuiltin):
    """
    Represents an (xsd) <any/> node
    """

    def __init__(self, schema, name):
        XBuiltin.__init__(self, schema, name)
        self.nillable = False

    def get_child(self, name):
        child = XAny(self.schema, name)
        return (child, [])

    def any(self):
        return True


class XBoolean(XBuiltin):
    """
    Represents an (xsd) boolean builtin type.
    """
    translation = ({'1': True, 'true': True, '0': False, 'false': False}, {True: 'true', 1: 'true', False: 'false', 0: 'false'})

    def translate(self, value, topython=True):
        if topython:
            if isinstance(value, basestring):
                return XBoolean.translation[0].get(value)
            else:
                return
        else:
            if isinstance(value, (bool, int)):
                return XBoolean.translation[1].get(value)
            else:
                return value
        return


class XInteger(XBuiltin):
    """
    Represents an (xsd) xs:int builtin type.
    """

    def translate(self, value, topython=True):
        if topython:
            if isinstance(value, basestring) and len(value):
                return int(value)
            else:
                return
        else:
            if isinstance(value, int):
                return str(value)
            else:
                return value
        return


class XLong(XBuiltin):
    """
    Represents an (xsd) xs:long builtin type.
    """

    def translate(self, value, topython=True):
        if topython:
            if isinstance(value, basestring) and len(value):
                return long(value)
            else:
                return
        else:
            if isinstance(value, (int, long)):
                return str(value)
            else:
                return value
        return


class XFloat(XBuiltin):
    """
    Represents an (xsd) xs:float builtin type.
    """

    def translate(self, value, topython=True):
        if topython:
            if isinstance(value, basestring) and len(value):
                return float(value)
            else:
                return
        else:
            if isinstance(value, float):
                return str(value)
            else:
                return value
        return


class XDate(XBuiltin):
    """
    Represents an (xsd) xs:date builtin type.
    """

    def translate(self, value, topython=True):
        if topython:
            if isinstance(value, basestring) and len(value):
                return Date(value).date
            else:
                return
        else:
            if isinstance(value, dt.date):
                return str(Date(value))
            else:
                return value
        return


class XTime(XBuiltin):
    """
    Represents an (xsd) xs:time builtin type.
    """

    def translate(self, value, topython=True):
        if topython:
            if isinstance(value, basestring) and len(value):
                return Time(value).time
            else:
                return
        else:
            if isinstance(value, dt.date):
                return str(Time(value))
            else:
                return value
        return


class XDateTime(XBuiltin):
    """
    Represents an (xsd) xs:datetime builtin type.
    """

    def translate(self, value, topython=True):
        if topython:
            if isinstance(value, basestring) and len(value):
                return DateTime(value).datetime
            else:
                return
        else:
            if isinstance(value, dt.date):
                return str(DateTime(value))
            else:
                return value
        return


class Factory:
    tags = {'anyType': XAny, 
       'string': XString, 
       'normalizedString': XString, 
       'ID': XString, 
       'Name': XString, 
       'QName': XString, 
       'NCName': XString, 
       'anySimpleType': XString, 
       'anyURI': XString, 
       'NOTATION': XString, 
       'token': XString, 
       'language': XString, 
       'IDREFS': XString, 
       'ENTITIES': XString, 
       'IDREF': XString, 
       'ENTITY': XString, 
       'NMTOKEN': XString, 
       'NMTOKENS': XString, 
       'hexBinary': XString, 
       'base64Binary': XString, 
       'int': XInteger, 
       'integer': XInteger, 
       'unsignedInt': XInteger, 
       'positiveInteger': XInteger, 
       'negativeInteger': XInteger, 
       'nonPositiveInteger': XInteger, 
       'nonNegativeInteger': XInteger, 
       'long': XLong, 
       'unsignedLong': XLong, 
       'short': XInteger, 
       'unsignedShort': XInteger, 
       'byte': XInteger, 
       'unsignedByte': XInteger, 
       'float': XFloat, 
       'double': XFloat, 
       'decimal': XFloat, 
       'date': XDate, 
       'time': XTime, 
       'dateTime': XDateTime, 
       'duration': XString, 
       'gYearMonth': XString, 
       'gYear': XString, 
       'gMonthDay': XString, 
       'gDay': XString, 
       'gMonth': XString, 
       'boolean': XBoolean}

    @classmethod
    def maptag(cls, tag, fn):
        """
        Map (override) tag => I{class} mapping.
        @param tag: An xsd tag name.
        @type tag: str
        @param fn: A function or class.
        @type fn: fn|class.
        """
        cls.tags[tag] = fn

    @classmethod
    def create(cls, schema, name):
        """
        Create an object based on the root tag name.
        @param schema: A schema object.
        @type schema: L{schema.Schema}
        @param name: The name.
        @type name: str
        @return: The created object.
        @rtype: L{XBuiltin} 
        """
        fn = cls.tags.get(name)
        if fn is not None:
            return fn(schema, name)
        else:
            return XBuiltin(schema, name)
            return