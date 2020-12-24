# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/rsl/xsd/simpletype.py
# Compiled at: 2009-01-23 20:16:30
"""
this module defines all builtin xsd simple types.
"""
import base64, binascii
from rsl.misc.isodate import parse_datetime
from rsl.misc.tzinfo import Local
from rsl.xsd.urtype import AnySimpleType

class IntegerType(AnySimpleType):
    """
    This represents the xsd-integer type.
    """

    def decode(self, data):
        """
        converts the given string to a python int.
        """
        return int(data)


class FloatType(AnySimpleType):
    """
    This represents the xsd-float type.
    """

    def decode(self, data):
        """
        converts the given string to a python float.
        """
        return float(data)


class BooleanType(AnySimpleType):
    """
    This represents the xsd-bool type.
    """

    def encode(self, data):
        """
        convert python bool to string.
        
        TODO: which encoding type to use? '1'/'0' or 'true'/'false'?
        """
        return str(data is True).lower()

    def decode(self, data):
        """
        convert string to python bool.
        """
        return bool(data)


class Base64Type(AnySimpleType):
    """
    the xsd-base64 type.
    """

    def encode(self, data):
        """
        encode python string to base64 string.
        """
        return base64.b64encode(data)

    def decode(self, data):
        """
        decode base64 data to python string.
        """
        return base64.b64decode(data)


class HexBinaryType(AnySimpleType):
    """
    the xsd - hexbinary type.
    """

    def encode(self, data):
        """
        convert python string to hexbinary representation.
        """
        return binascii.hexlify(data)

    def decode(self, data):
        """
        convert hexbinary representation to python string.
        """
        return binascii.unhexlify(data)


class DateTimeType(AnySimpleType):
    """
    the xsd-datetime type.
    """

    def preparedatetime(self, data):
        """ apply tzinfo and convert data to datetime if possible 
        time ... provides tuples and floating point numbers
        datetime ... date, time, datetime objects
        calendar ... Calendar objects
        
        if there is no tzinfo in date/time object assume local time
        
        @todo: currently only datetime objects are supported 
        """
        newdate = data
        if newdate.tzinfo is None:
            newdate = newdate.replace(tzinfo=Local)
        return newdate

    def encode(self, data):
        """
        convert datetime instance to string (iso8601).
        """
        return self.preparedatetime(data).isoformat()

    def decode(self, data):
        """
        parse iso-date to datetime instance.
        """
        return parse_datetime(data)


class DateType(DateTimeType):
    """
    the xsd-date type.
    """

    def encode(self, data):
        """
        convert datetime object to string according to xsd-standard.
        """
        return self.preparedatetime(data).strftime('%Y-%m-%d%z')


class TimeType(DateTimeType):
    """
    the xsd-time type.
    """

    def encode(self, data):
        """
        convert datetime object to string according to xsd-standard.
        """
        return self.preparedatetime(data).isoformat()[11:]