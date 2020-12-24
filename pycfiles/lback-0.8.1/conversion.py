# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: mysql\connector\conversion.pyc
# Compiled at: 2014-07-26 22:44:23
"""Converting MySQL and Python types
"""
import struct, datetime, time
from decimal import Decimal
from mysql.connector.constants import FieldType, FieldFlag, CharacterSet

class HexLiteral(str):
    """Class holding MySQL hex literals"""

    def __new__(cls, str_, charset='utf8'):
        hexed = [ ('{0:x}').format(ord(i)) for i in str_.encode(charset) ]
        obj = str.__new__(cls, ('').join(hexed))
        obj.charset = charset
        obj.original = str_
        return obj

    def __str__(self):
        return '0x' + self


class MySQLConverterBase(object):
    """Base class for conversion classes

    All class dealing with converting to and from MySQL data types must
    be a subclass of this class.
    """

    def __init__(self, charset='utf8', use_unicode=True):
        self.python_types = None
        self.mysql_types = None
        self.charset = None
        self.charset_id = 0
        self.use_unicode = None
        self.set_charset(charset)
        self.set_unicode(use_unicode)
        return

    def set_charset(self, charset):
        """Set character set"""
        if charset is not None:
            self.charset = charset
        else:
            self.charset = 'utf8'
        self.charset_id = CharacterSet.get_charset_info(self.charset)[0]
        return

    def set_unicode(self, value=True):
        """Set whether to use Unicode"""
        self.use_unicode = value

    def to_mysql(self, value):
        """Convert Python data type to MySQL"""
        return value

    def to_python(self, vtype, value):
        """Convert MySQL data type to Python"""
        return value

    def escape(self, buf):
        """Escape buffer for sending to MySQL"""
        return buf

    def quote(self, buf):
        """Quote buffer for sending to MySQL"""
        return str(buf)


class MySQLConverter(MySQLConverterBase):
    """Default conversion class for MySQL Connector/Python.
     o escape method: for escaping values send to MySQL
     o quoting method: for quoting values send to MySQL in statements
     o conversion mapping: maps Python and MySQL data types to
       function for converting them.

    Whenever one needs to convert values differently, a converter_class
    argument can be given while instantiating a new connection like
    cnx.connect(converter_class=CustomMySQLConverterClass).

    """

    def __init__(self, charset=None, use_unicode=True):
        MySQLConverterBase.__init__(self, charset, use_unicode)
        self._cache_field_types = {}

    def escape(self, value):
        """
        Escapes special characters as they are expected to by when MySQL
        receives them.
        As found in MySQL source mysys/charset.c

        Returns the value if not a string, or the escaped string.
        """
        if value is None:
            return value
        else:
            if isinstance(value, (int, float, long, Decimal, HexLiteral)):
                return value
            res = value
            res = res.replace('\\', '\\\\')
            res = res.replace('\n', '\\n')
            res = res.replace('\r', '\\r')
            res = res.replace("'", "\\'")
            res = res.replace('"', '\\"')
            res = res.replace('\x1a', '\\\x1a')
            return res

    def quote(self, buf):
        """
        Quote the parameters for commands. General rules:
          o numbers are returns as str type (because operation expect it)
          o None is returned as str('NULL')
          o String are quoted with single quotes '<string>'

        Returns a string.
        """
        if isinstance(buf, (int, float, long, Decimal, HexLiteral)):
            return str(buf)
        else:
            if isinstance(buf, type(None)):
                return 'NULL'
            else:
                return "'%s'" % buf

            return

    def to_mysql(self, value):
        """Convert Python data type to MySQL"""
        type_name = value.__class__.__name__.lower()
        return getattr(self, '_%s_to_mysql' % str(type_name))(value)

    def _int_to_mysql(self, value):
        """Convert value to int"""
        return int(value)

    def _long_to_mysql(self, value):
        """Convert value to long"""
        return long(value)

    def _float_to_mysql(self, value):
        """Convert value to float"""
        return float(value)

    def _str_to_mysql(self, value):
        """Convert value to string"""
        return str(value)

    def _unicode_to_mysql(self, value):
        """
        Encodes value, a Python unicode string, to whatever the
        character set for this converter is set too.
        """
        encoded = value.encode(self.charset)
        if self.charset_id in CharacterSet.slash_charsets:
            if '\\' in encoded:
                return HexLiteral(value, self.charset)
        return encoded

    def _bool_to_mysql(self, value):
        """Convert value to boolean"""
        if value:
            return 1
        else:
            return 0

    def _nonetype_to_mysql(self, value):
        """
        This would return what None would be in MySQL, but instead we
        leave it None and return it right away. The actual conversion
        from None to NULL happens in the quoting functionality.

        Return None.
        """
        return

    def _datetime_to_mysql(self, value):
        """
        Converts a datetime instance to a string suitable for MySQL.
        The returned string has format: %Y-%m-%d %H:%M:%S[.%f]

        If the instance isn't a datetime.datetime type, it return None.

        Returns a string.
        """
        if value.microsecond:
            return '%d-%02d-%02d %02d:%02d:%02d.%06d' % (
             value.year, value.month, value.day,
             value.hour, value.minute, value.second,
             value.microsecond)
        return '%d-%02d-%02d %02d:%02d:%02d' % (
         value.year, value.month, value.day,
         value.hour, value.minute, value.second)

    def _date_to_mysql(self, value):
        """
        Converts a date instance to a string suitable for MySQL.
        The returned string has format: %Y-%m-%d

        If the instance isn't a datetime.date type, it return None.

        Returns a string.
        """
        return '%d-%02d-%02d' % (value.year, value.month, value.day)

    def _time_to_mysql(self, value):
        """
        Converts a time instance to a string suitable for MySQL.
        The returned string has format: %H:%M:%S[.%f]

        If the instance isn't a datetime.time type, it return None.

        Returns a string or None when not valid.
        """
        if value.microsecond:
            return value.strftime('%H:%M:%S.%%06d') % value.microsecond
        return value.strftime('%H:%M:%S')

    def _struct_time_to_mysql(self, value):
        """
        Converts a time.struct_time sequence to a string suitable
        for MySQL.
        The returned string has format: %Y-%m-%d %H:%M:%S

        Returns a string or None when not valid.
        """
        return time.strftime('%Y-%m-%d %H:%M:%S', value)

    def _timedelta_to_mysql(self, value):
        """
        Converts a timedelta instance to a string suitable for MySQL.
        The returned string has format: %H:%M:%S

        Returns a string.
        """
        hours, remainder = divmod(value.seconds, 3600)
        mins, secs = divmod(remainder, 60)
        hours = hours + value.days * 24
        if value.microseconds:
            return '%02d:%02d:%02d.%06d' % (hours, mins, secs,
             value.microseconds)
        return '%02d:%02d:%02d' % (hours, mins, secs)

    def _decimal_to_mysql(self, value):
        """
        Converts a decimal.Decimal instance to a string suitable for
        MySQL.

        Returns a string or None when not valid.
        """
        if isinstance(value, Decimal):
            return str(value)
        else:
            return

    def to_python(self, flddsc, value):
        """
        Converts a given value coming from MySQL to a certain type in Python.
        The flddsc contains additional information for the field in the
        table. It's an element from MySQLCursor.description.

        Returns a mixed value.
        """
        if value == '\x00' and flddsc[1] != FieldType.BIT:
            return
        else:
            if value is None:
                return
            if not self._cache_field_types:
                self._cache_field_types = {}
                for name, info in FieldType.desc.items():
                    try:
                        self._cache_field_types[info[0]] = getattr(self, ('_{0}_to_python').format(name))
                    except AttributeError:
                        pass

            try:
                return self._cache_field_types[flddsc[1]](value, flddsc)
            except KeyError:
                return str(value)
            except ValueError as err:
                raise ValueError('%s (field %s)' % (err, flddsc[0]))
            except TypeError as err:
                raise TypeError('%s (field %s)' % (err, flddsc[0]))
            except:
                raise

            return

    def _FLOAT_to_python(self, value, desc=None):
        """
        Returns value as float type.
        """
        return float(value)

    _DOUBLE_to_python = _FLOAT_to_python

    def _INT_to_python(self, value, desc=None):
        """
        Returns value as int type.
        """
        return int(value)

    _TINY_to_python = _INT_to_python
    _SHORT_to_python = _INT_to_python
    _INT24_to_python = _INT_to_python

    def _LONG_to_python(self, value, desc=None):
        """
        Returns value as long type.
        """
        return int(value)

    _LONGLONG_to_python = _LONG_to_python

    def _DECIMAL_to_python(self, value, desc=None):
        """
        Returns value as a decimal.Decimal.
        """
        return Decimal(value)

    _NEWDECIMAL_to_python = _DECIMAL_to_python

    def _str(self, value, desc=None):
        """
        Returns value as str type.
        """
        return str(value)

    def _BIT_to_python(self, value, dsc=None):
        """Returns BIT columntype as integer"""
        int_val = value
        if len(int_val) < 8:
            int_val = '\x00' * (8 - len(int_val)) + int_val
        return struct.unpack('>Q', int_val)[0]

    def _DATE_to_python(self, value, dsc=None):
        """
        Returns DATE column type as datetime.date type.
        """
        try:
            parts = value.split('-')
            return datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))
        except ValueError:
            return

        return

    _NEWDATE_to_python = _DATE_to_python

    def _TIME_to_python(self, value, dsc=None):
        """
        Returns TIME column type as datetime.time type.
        """
        time_val = None
        try:
            hms, mcs = value.split('.')
            mcs = int(mcs.ljust(6, '0'))
        except ValueError:
            hms = value
            mcs = 0

        try:
            hour, mins, sec = [ int(d) for d in hms.split(':') ]
            time_val = datetime.timedelta(hours=hour, minutes=mins, seconds=sec, microseconds=mcs)
        except ValueError:
            raise ValueError('Could not convert %s to python datetime.timedelta' % value)
        else:
            return time_val

        return

    def _DATETIME_to_python(self, value, dsc=None):
        """
        Returns DATETIME column type as datetime.datetime type.
        """
        datetime_val = None
        try:
            date_, time_ = value.split(' ')
            if len(time_) > 8:
                hms, mcs = time_.split('.')
                mcs = int(mcs.ljust(6, '0'))
            else:
                hms = time_
                mcs = 0
            dtval = [ int(value) for value in date_.split('-') ] + [ int(value) for value in hms.split(':') ] + [mcs]
            datetime_val = datetime.datetime(*dtval)
        except ValueError:
            datetime_val = None

        return datetime_val

    _TIMESTAMP_to_python = _DATETIME_to_python

    def _YEAR_to_python(self, value, desc=None):
        """Returns YEAR column type as integer"""
        try:
            year = int(value)
        except ValueError:
            raise ValueError('Failed converting YEAR to int (%s)' % value)

        return year

    def _SET_to_python(self, value, dsc=None):
        """Returns SET column typs as set

        Actually, MySQL protocol sees a SET as a string type field. So this
        code isn't called directly, but used by STRING_to_python() method.

        Returns SET column type as a set.
        """
        set_type = None
        try:
            set_type = set(value.split(','))
        except ValueError:
            raise ValueError('Could not convert SET %s to a set.' % value)

        return set_type

    def _STRING_to_python(self, value, dsc=None):
        """
        Note that a SET is a string too, but using the FieldFlag we can see
        whether we have to split it.

        Returns string typed columns as string type.
        """
        if dsc is not None:
            if dsc[7] & FieldFlag.SET:
                return self._SET_to_python(value, dsc)
            if dsc[7] & FieldFlag.BINARY:
                return value
        if self.use_unicode:
            try:
                return unicode(value, self.charset)
            except:
                raise

        return str(value)

    _VAR_STRING_to_python = _STRING_to_python

    def _BLOB_to_python(self, value, dsc=None):
        """Convert BLOB data type to Python"""
        if dsc is not None:
            if dsc[7] & FieldFlag.BINARY:
                return value
        return self._STRING_to_python(value, dsc)

    _LONG_BLOB_to_python = _BLOB_to_python
    _MEDIUM_BLOB_to_python = _BLOB_to_python
    _TINY_BLOB_to_python = _BLOB_to_python