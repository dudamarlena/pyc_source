# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_mysql\lib\mysql\connector\conversion.py
# Compiled at: 2017-12-07 02:34:36
# Size of source mod 2**32: 19712 bytes
"""Converting MySQL and Python types
"""
import datetime, time
from decimal import Decimal
from .constants import FieldType, FieldFlag, CharacterSet
from .catch23 import PY2, NUMERIC_TYPES, struct_unpack
from .custom_types import HexLiteral

class MySQLConverterBase(object):
    __doc__ = 'Base class for conversion classes\n\n    All class dealing with converting to and from MySQL data types must\n    be a subclass of this class.\n    '

    def __init__(self, charset='utf8', use_unicode=True):
        self.python_types = None
        self.mysql_types = None
        self.charset = None
        self.charset_id = 0
        self.use_unicode = None
        self.set_charset(charset)
        self.set_unicode(use_unicode)
        self._cache_field_types = {}

    def set_charset(self, charset):
        """Set character set"""
        if charset == 'utf8mb4':
            charset = 'utf8'
        else:
            if charset is not None:
                self.charset = charset
            else:
                self.charset = 'utf8'
        self.charset_id = CharacterSet.get_charset_info(self.charset)[0]

    def set_unicode(self, value=True):
        """Set whether to use Unicode"""
        self.use_unicode = value

    def to_mysql(self, value):
        """Convert Python data type to MySQL"""
        type_name = value.__class__.__name__.lower()
        try:
            return getattr(self, '_{0}_to_mysql'.format(type_name))(value)
        except AttributeError:
            return value

    def to_python(self, vtype, value):
        """Convert MySQL data type to Python"""
        if value == b'\x00' or value is None:
            if vtype[1] != FieldType.BIT:
                return
        if not self._cache_field_types:
            self._cache_field_types = {}
            for name, info in FieldType.desc.items():
                try:
                    self._cache_field_types[info[0]] = getattr(self, '_{0}_to_python'.format(name))
                except AttributeError:
                    pass

        try:
            return self._cache_field_types[vtype[1]](value, vtype)
        except KeyError:
            return value

    def escape(self, buf):
        """Escape buffer for sending to MySQL"""
        return buf

    def quote(self, buf):
        """Quote buffer for sending to MySQL"""
        return str(buf)


class MySQLConverter(MySQLConverterBase):
    __doc__ = 'Default conversion class for MySQL Connector/Python.\n\n     o escape method: for escaping values send to MySQL\n     o quoting method: for quoting values send to MySQL in statements\n     o conversion mapping: maps Python and MySQL data types to\n       function for converting them.\n\n    Whenever one needs to convert values differently, a converter_class\n    argument can be given while instantiating a new connection like\n    cnx.connect(converter_class=CustomMySQLConverterClass).\n\n    '

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
            if isinstance(value, NUMERIC_TYPES):
                return value
            else:
                if isinstance(value, (bytes, bytearray)):
                    value = value.replace(b'\\', b'\\\\')
                    value = value.replace(b'\n', b'\\n')
                    value = value.replace(b'\r', b'\\r')
                    value = value.replace(b"'", b"\\'")
                    value = value.replace(b'"', b'\\"')
                    value = value.replace(b'\x1a', b'\\\x1a')
                else:
                    value = value.replace('\\', '\\\\')
                    value = value.replace('\n', '\\n')
                    value = value.replace('\r', '\\r')
                    value = value.replace("'", "\\'")
                    value = value.replace('"', '\\"')
                    value = value.replace('\x1a', '\\\x1a')
            return value

    def quote(self, buf):
        """
        Quote the parameters for commands. General rules:
          o numbers are returns as bytes using ascii codec
          o None is returned as bytearray(b'NULL')
          o Everything else is single quoted '<buf>'

        Returns a bytearray object.
        """
        if isinstance(buf, NUMERIC_TYPES):
            if PY2:
                if isinstance(buf, float):
                    return repr(buf)
                else:
                    return str(buf)
            else:
                return str(buf).encode('ascii')
        else:
            if isinstance(buf, type(None)):
                return bytearray(b'NULL')
            else:
                return bytearray(b"'" + buf + b"'")

    def to_mysql(self, value):
        """Convert Python data type to MySQL"""
        type_name = value.__class__.__name__.lower()
        try:
            return getattr(self, '_{0}_to_mysql'.format(type_name))(value)
        except AttributeError:
            raise TypeError("Python '{0}' cannot be converted to a MySQL type".format(type_name))

    def to_python(self, vtype, value):
        """Convert MySQL data type to Python"""
        if value == 0:
            if vtype[1] != FieldType.BIT:
                return
            if value is None:
                return
            if not self._cache_field_types:
                self._cache_field_types = {}
                for name, info in FieldType.desc.items():
                    try:
                        self._cache_field_types[info[0]] = getattr(self, '_{0}_to_python'.format(name))
                    except AttributeError:
                        pass

        else:
            try:
                return self._cache_field_types[vtype[1]](value, vtype)
            except KeyError:
                try:
                    return value.decode('utf-8')
                except UnicodeDecodeError:
                    return value

            except ValueError as err:
                raise ValueError('%s (field %s)' % (err, vtype[0]))
            except TypeError as err:
                raise TypeError('%s (field %s)' % (err, vtype[0]))
            except:
                raise

    def _int_to_mysql(self, value):
        """Convert value to int"""
        return int(value)

    def _long_to_mysql(self, value):
        """Convert value to int"""
        return int(value)

    def _float_to_mysql(self, value):
        """Convert value to float"""
        return float(value)

    def _str_to_mysql(self, value):
        """Convert value to string"""
        if PY2:
            return str(value)
        else:
            return self._unicode_to_mysql(value)

    def _unicode_to_mysql(self, value):
        """Convert unicode"""
        charset = self.charset
        charset_id = self.charset_id
        if charset == 'binary':
            charset = 'utf8'
            charset_id = CharacterSet.get_charset_info(charset)[0]
        encoded = value.encode(charset)
        if charset_id in CharacterSet.slash_charsets:
            if b'\\' in encoded:
                return HexLiteral(value, charset)
        return encoded

    def _bytes_to_mysql(self, value):
        """Convert value to bytes"""
        return value

    def _bytearray_to_mysql(self, value):
        """Convert value to bytes"""
        return bytes(value)

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
        pass

    def _datetime_to_mysql(self, value):
        """
        Converts a datetime instance to a string suitable for MySQL.
        The returned string has format: %Y-%m-%d %H:%M:%S[.%f]

        If the instance isn't a datetime.datetime type, it return None.

        Returns a bytes.
        """
        if value.microsecond:
            fmt = '{0:d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:06d}'
            return fmt.format(value.year, value.month, value.day, value.hour, value.minute, value.second, value.microsecond).encode('ascii')
        else:
            fmt = '{0:d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'
            return fmt.format(value.year, value.month, value.day, value.hour, value.minute, value.second).encode('ascii')

    def _date_to_mysql(self, value):
        """
        Converts a date instance to a string suitable for MySQL.
        The returned string has format: %Y-%m-%d

        If the instance isn't a datetime.date type, it return None.

        Returns a bytes.
        """
        return '{0:d}-{1:02d}-{2:02d}'.format(value.year, value.month, value.day).encode('ascii')

    def _time_to_mysql(self, value):
        """
        Converts a time instance to a string suitable for MySQL.
        The returned string has format: %H:%M:%S[.%f]

        If the instance isn't a datetime.time type, it return None.

        Returns a bytes.
        """
        if value.microsecond:
            return value.strftime('%H:%M:%S.%f').encode('ascii')
        else:
            return value.strftime('%H:%M:%S').encode('ascii')

    def _struct_time_to_mysql(self, value):
        """
        Converts a time.struct_time sequence to a string suitable
        for MySQL.
        The returned string has format: %Y-%m-%d %H:%M:%S

        Returns a bytes or None when not valid.
        """
        return time.strftime('%Y-%m-%d %H:%M:%S', value).encode('ascii')

    def _timedelta_to_mysql(self, value):
        """
        Converts a timedelta instance to a string suitable for MySQL.
        The returned string has format: %H:%M:%S

        Returns a bytes.
        """
        seconds = abs(value.days * 86400 + value.seconds)
        if value.microseconds:
            fmt = '{0:02d}:{1:02d}:{2:02d}.{3:06d}'
            if value.days < 0:
                mcs = 1000000 - value.microseconds
                seconds -= 1
            else:
                mcs = value.microseconds
        else:
            fmt = '{0:02d}:{1:02d}:{2:02d}'
        if value.days < 0:
            fmt = '-' + fmt
        else:
            hours, remainder = divmod(seconds, 3600)
            mins, secs = divmod(remainder, 60)
            if value.microseconds:
                result = fmt.format(hours, mins, secs, mcs)
            else:
                result = fmt.format(hours, mins, secs)
        if PY2:
            return result
        else:
            return result.encode('ascii')

    def _decimal_to_mysql(self, value):
        """
        Converts a decimal.Decimal instance to a string suitable for
        MySQL.

        Returns a bytes or None when not valid.
        """
        if isinstance(value, Decimal):
            return str(value).encode('ascii')

    def row_to_python(self, row, fields):
        """Convert a MySQL text result row to Python types

        The row argument is a sequence containing text result returned
        by a MySQL server. Each value of the row is converted to the
        using the field type information in the fields argument.

        Returns a tuple.
        """
        i = 0
        result = [None] * len(fields)
        if not self._cache_field_types:
            self._cache_field_types = {}
            for name, info in FieldType.desc.items():
                try:
                    self._cache_field_types[info[0]] = getattr(self, '_{0}_to_python'.format(name))
                except AttributeError:
                    pass

        for field in fields:
            field_type = field[1]
            if row[i] == 0 and field_type != FieldType.BIT or row[i] is None:
                i += 1
            else:
                try:
                    result[i] = self._cache_field_types[field_type](row[i], field)
                except KeyError:
                    try:
                        result[i] = row[i].decode('utf-8')
                    except UnicodeDecodeError:
                        result[i] = row[i]

                except (ValueError, TypeError) as err:
                    err.message = '{0} (field {1})'.format(str(err), field[0])
                    raise

                i += 1

        return tuple(result)

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
    _LONG_to_python = _INT_to_python
    _LONGLONG_to_python = _INT_to_python

    def _DECIMAL_to_python(self, value, desc=None):
        """
        Returns value as a decimal.Decimal.
        """
        val = value.decode(self.charset)
        return Decimal(val)

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
            int_val = b'\x00' * (8 - len(int_val)) + int_val
        return struct_unpack('>Q', int_val)[0]

    def _DATE_to_python(self, value, dsc=None):
        """
        Returns DATE column type as datetime.date type.
        """
        try:
            parts = value.split(b'-')
            return datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))
        except ValueError:
            return

    _NEWDATE_to_python = _DATE_to_python

    def _TIME_to_python(self, value, dsc=None):
        """
        Returns TIME column type as datetime.time type.
        """
        time_val = None
        try:
            hms, mcs = value.split(b'.')
            mcs = int(mcs.ljust(6, b'0'))
        except ValueError:
            hms = value
            mcs = 0

        try:
            hours, mins, secs = [int(d) for d in hms.split(b':')]
            if value[0] == 45 or value[0] == '-':
                mins, secs, mcs = -mins, -secs, -mcs
            time_val = datetime.timedelta(hours=hours, minutes=mins, seconds=secs,
              microseconds=mcs)
        except ValueError:
            raise ValueError('Could not convert {0} to python datetime.timedelta'.format(value))
        else:
            return time_val

    def _DATETIME_to_python(self, value, dsc=None):
        """
        Returns DATETIME column type as datetime.datetime type.
        """
        datetime_val = None
        try:
            date_, time_ = value.split(b' ')
            if len(time_) > 8:
                hms, mcs = time_.split(b'.')
                mcs = int(mcs.ljust(6, b'0'))
            else:
                hms = time_
                mcs = 0
            dtval = [int(i) for i in date_.split(b'-')] + [int(i) for i in hms.split(b':')] + [mcs]
            datetime_val = (datetime.datetime)(*dtval)
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
        """Returns SET column type as set

        Actually, MySQL protocol sees a SET as a string type field. So this
        code isn't called directly, but used by STRING_to_python() method.

        Returns SET column type as a set.
        """
        set_type = None
        val = value.decode(self.charset)
        if not val:
            return set()
        else:
            try:
                set_type = set(val.split(','))
            except ValueError:
                raise ValueError('Could not convert set %s to a sequence.' % value)

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
        if self.charset == 'binary':
            return value
        else:
            if isinstance(value, (bytes, bytearray)):
                if self.use_unicode:
                    return value.decode(self.charset)
            return value

    _VAR_STRING_to_python = _STRING_to_python

    def _BLOB_to_python(self, value, dsc=None):
        """Convert BLOB data type to Python"""
        if dsc is not None and dsc[7] & FieldFlag.BINARY:
            if PY2:
                return value
            return bytes(value)
        else:
            return self._STRING_to_python(value, dsc)

    _LONG_BLOB_to_python = _BLOB_to_python
    _MEDIUM_BLOB_to_python = _BLOB_to_python
    _TINY_BLOB_to_python = _BLOB_to_python