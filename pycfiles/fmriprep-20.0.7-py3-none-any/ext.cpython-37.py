# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_vendor/msgpack/ext.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 6034 bytes
from collections import namedtuple
import datetime, sys, struct
PY2 = sys.version_info[0] == 2
if PY2:
    int_types = (
     int, long)
    _utc = None
else:
    int_types = int
    try:
        _utc = datetime.timezone.utc
    except AttributeError:
        _utc = datetime.timezone(datetime.timedelta(0))

    class ExtType(namedtuple('ExtType', 'code data')):
        __doc__ = 'ExtType represents ext type in msgpack.'

        def __new__(cls, code, data):
            if not isinstance(code, int):
                raise TypeError('code must be int')
            if not isinstance(data, bytes):
                raise TypeError('data must be bytes')
            if not 0 <= code <= 127:
                raise ValueError('code must be 0~127')
            return super(ExtType, cls).__new__(cls, code, data)


    class Timestamp(object):
        __doc__ = 'Timestamp represents the Timestamp extension type in msgpack.\n\n    When built with Cython, msgpack uses C methods to pack and unpack `Timestamp`. When using pure-Python\n    msgpack, :func:`to_bytes` and :func:`from_bytes` are used to pack and unpack `Timestamp`.\n\n    This class is immutable: Do not override seconds and nanoseconds.\n    '
        __slots__ = [
         'seconds', 'nanoseconds']

        def __init__(self, seconds, nanoseconds=0):
            """Initialize a Timestamp object.

        :param int seconds:
            Number of seconds since the UNIX epoch (00:00:00 UTC Jan 1 1970, minus leap seconds).
            May be negative.

        :param int nanoseconds:
            Number of nanoseconds to add to `seconds` to get fractional time.
            Maximum is 999_999_999.  Default is 0.

        Note: Negative times (before the UNIX epoch) are represented as negative seconds + positive ns.
        """
            if not isinstance(seconds, int_types):
                raise TypeError('seconds must be an interger')
            if not isinstance(nanoseconds, int_types):
                raise TypeError('nanoseconds must be an integer')
            if not 0 <= nanoseconds < 1000000000:
                raise ValueError('nanoseconds must be a non-negative integer less than 999999999.')
            self.seconds = seconds
            self.nanoseconds = nanoseconds

        def __repr__(self):
            """String representation of Timestamp."""
            return 'Timestamp(seconds={0}, nanoseconds={1})'.format(self.seconds, self.nanoseconds)

        def __eq__(self, other):
            """Check for equality with another Timestamp object"""
            if type(other) is self.__class__:
                return self.seconds == other.seconds and self.nanoseconds == other.nanoseconds
            return False

        def __ne__(self, other):
            """not-equals method (see :func:`__eq__()`)"""
            return not self.__eq__(other)

        def __hash__(self):
            return hash((self.seconds, self.nanoseconds))

        @staticmethod
        def from_bytes(b):
            """Unpack bytes into a `Timestamp` object.

        Used for pure-Python msgpack unpacking.

        :param b: Payload from msgpack ext message with code -1
        :type b: bytes

        :returns: Timestamp object unpacked from msgpack ext payload
        :rtype: Timestamp
        """
            if len(b) == 4:
                seconds = struct.unpack('!L', b)[0]
                nanoseconds = 0
            else:
                if len(b) == 8:
                    data64 = struct.unpack('!Q', b)[0]
                    seconds = data64 & 17179869183
                    nanoseconds = data64 >> 34
                else:
                    if len(b) == 12:
                        nanoseconds, seconds = struct.unpack('!Iq', b)
                    else:
                        raise ValueError('Timestamp type can only be created from 32, 64, or 96-bit byte objects')
            return Timestamp(seconds, nanoseconds)

        def to_bytes(self):
            """Pack this Timestamp object into bytes.

        Used for pure-Python msgpack packing.

        :returns data: Payload for EXT message with code -1 (timestamp type)
        :rtype: bytes
        """
            if self.seconds >> 34 == 0:
                data64 = self.nanoseconds << 34 | self.seconds
                if data64 & 18446744069414584320 == 0:
                    data = struct.pack('!L', data64)
                else:
                    data = struct.pack('!Q', data64)
            else:
                data = struct.pack('!Iq', self.nanoseconds, self.seconds)
            return data

        @staticmethod
        def from_unix(unix_sec):
            """Create a Timestamp from posix timestamp in seconds.

        :param unix_float: Posix timestamp in seconds.
        :type unix_float: int or float.
        """
            seconds = int(unix_sec // 1)
            nanoseconds = int(unix_sec % 1 * 1000000000)
            return Timestamp(seconds, nanoseconds)

        def to_unix(self):
            """Get the timestamp as a floating-point value.

        :returns: posix timestamp
        :rtype: float
        """
            return self.seconds + self.nanoseconds / 1000000000.0

        @staticmethod
        def from_unix_nano(unix_ns):
            """Create a Timestamp from posix timestamp in nanoseconds.

        :param int unix_ns: Posix timestamp in nanoseconds.
        :rtype: Timestamp
        """
            return Timestamp(*divmod(unix_ns, 1000000000))

        def to_unix_nano(self):
            """Get the timestamp as a unixtime in nanoseconds.

        :returns: posix timestamp in nanoseconds
        :rtype: int
        """
            return self.seconds * 1000000000 + self.nanoseconds

        def to_datetime(self):
            """Get the timestamp as a UTC datetime.

        Python 2 is not supported.

        :rtype: datetime.
        """
            return datetime.datetime.fromtimestamp(self.to_unix(), _utc)

        @staticmethod
        def from_datetime(dt):
            """Create a Timestamp from datetime with tzinfo.

        Python 2 is not supported.

        :rtype: Timestamp
        """
            return Timestamp.from_unix(dt.timestamp())