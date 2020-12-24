# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: bson/objectid.py
# Compiled at: 2014-07-29 17:29:28
"""Tools for working with MongoDB `ObjectIds
<http://dochub.mongodb.org/core/objectids>`_.
"""
import binascii, calendar, datetime
try:
    import hashlib
    _md5func = hashlib.md5
except ImportError:
    import md5
    _md5func = md5.new

import os, random, socket, struct, threading, time
from bson.errors import InvalidId
from bson.py3compat import PY3, b, binary_type, text_type, bytes_from_hex, string_types
from bson.tz_util import utc
EMPTY = b('')
ZERO = b('\x00')

def _machine_bytes():
    """Get the machine portion of an ObjectId.
    """
    machine_hash = _md5func()
    if PY3:
        machine_hash.update(socket.gethostname().encode())
    else:
        machine_hash.update(socket.gethostname())
    return machine_hash.digest()[0:3]


class ObjectId(object):
    """A MongoDB ObjectId.
    """
    _inc = random.randint(0, 16777215)
    _inc_lock = threading.Lock()
    _machine_bytes = _machine_bytes()
    __slots__ = '__id'
    _type_marker = 7

    def __init__(self, oid=None):
        """Initialize a new ObjectId.

        If `oid` is ``None``, create a new (unique) ObjectId. If `oid`
        is an instance of (:class:`basestring` (:class:`str` or :class:`bytes`
        in python 3), :class:`ObjectId`) validate it and use that.  Otherwise,
        a :class:`TypeError` is raised. If `oid` is invalid,
        :class:`~bson.errors.InvalidId` is raised.

        :Parameters:
          - `oid` (optional): a valid ObjectId (12 byte binary or 24 character
            hex string)

        .. versionadded:: 1.2.1
           The `oid` parameter can be a ``unicode`` instance (that contains
           only hexadecimal digits).

        .. mongodoc:: objectids
        """
        if oid is None:
            self.__generate()
        else:
            self.__validate(oid)
        return

    @classmethod
    def from_datetime(cls, generation_time):
        """Create a dummy ObjectId instance with a specific generation time.

        This method is useful for doing range queries on a field
        containing :class:`ObjectId` instances.

        .. warning::
           It is not safe to insert a document containing an ObjectId
           generated using this method. This method deliberately
           eliminates the uniqueness guarantee that ObjectIds
           generally provide. ObjectIds generated with this method
           should be used exclusively in queries.

        `generation_time` will be converted to UTC. Naive datetime
        instances will be treated as though they already contain UTC.

        An example using this helper to get documents where ``"_id"``
        was generated before January 1, 2010 would be:

        >>> gen_time = datetime.datetime(2010, 1, 1)
        >>> dummy_id = ObjectId.from_datetime(gen_time)
        >>> result = collection.find({"_id": {"$lt": dummy_id}})

        :Parameters:
          - `generation_time`: :class:`~datetime.datetime` to be used
            as the generation time for the resulting ObjectId.

        .. versionchanged:: 1.8
           Properly handle timezone aware values for
           `generation_time`.

        .. versionadded:: 1.6
        """
        if generation_time.utcoffset() is not None:
            generation_time = generation_time - generation_time.utcoffset()
        ts = calendar.timegm(generation_time.timetuple())
        oid = struct.pack('>i', int(ts)) + ZERO * 8
        return cls(oid)

    @classmethod
    def is_valid(cls, oid):
        """Checks if a `oid` string is valid or not.

        :Parameters:
          - `oid`: the object id to validate

        .. versionadded:: 2.3
        """
        if not oid:
            return False
        try:
            ObjectId(oid)
            return True
        except (InvalidId, TypeError):
            return False

    def __generate(self):
        """Generate a new value for this ObjectId.
        """
        oid = EMPTY
        oid += struct.pack('>i', int(time.time()))
        oid += ObjectId._machine_bytes
        oid += struct.pack('>H', os.getpid() % 65535)
        ObjectId._inc_lock.acquire()
        oid += struct.pack('>i', ObjectId._inc)[1:4]
        ObjectId._inc = (ObjectId._inc + 1) % 16777215
        ObjectId._inc_lock.release()
        self.__id = oid

    def __validate(self, oid):
        """Validate and use the given id for this ObjectId.

        Raises TypeError if id is not an instance of
        (:class:`basestring` (:class:`str` or :class:`bytes`
        in python 3), ObjectId) and InvalidId if it is not a
        valid ObjectId.

        :Parameters:
          - `oid`: a valid ObjectId
        """
        if isinstance(oid, ObjectId):
            self.__id = oid.__id
        elif isinstance(oid, string_types):
            if len(oid) == 12:
                if isinstance(oid, binary_type):
                    self.__id = oid
                else:
                    raise InvalidId('%s is not a valid ObjectId' % oid)
            elif len(oid) == 24:
                try:
                    self.__id = bytes_from_hex(oid)
                except (TypeError, ValueError):
                    raise InvalidId('%s is not a valid ObjectId' % oid)

            else:
                raise InvalidId('%s is not a valid ObjectId' % oid)
        else:
            raise TypeError('id must be an instance of (%s, %s, ObjectId), not %s' % (
             binary_type.__name__,
             text_type.__name__, type(oid)))

    @property
    def binary(self):
        """12-byte binary representation of this ObjectId.
        """
        return self.__id

    @property
    def generation_time(self):
        """A :class:`datetime.datetime` instance representing the time of
        generation for this :class:`ObjectId`.

        The :class:`datetime.datetime` is timezone aware, and
        represents the generation time in UTC. It is precise to the
        second.

        .. versionchanged:: 1.8
           Now return an aware datetime instead of a naive one.

        .. versionadded:: 1.2
        """
        t = struct.unpack('>i', self.__id[0:4])[0]
        return datetime.datetime.fromtimestamp(t, utc)

    def __getstate__(self):
        """return value of object for pickling.
        needed explicitly because __slots__() defined.
        """
        return self.__id

    def __setstate__(self, value):
        """explicit state set from pickling
        """
        if isinstance(value, dict):
            oid = value['_ObjectId__id']
        else:
            oid = value
        if PY3 and isinstance(oid, text_type):
            self.__id = oid.encode('latin-1')
        else:
            self.__id = oid

    def __str__(self):
        if PY3:
            return binascii.hexlify(self.__id).decode()
        return binascii.hexlify(self.__id)

    def __repr__(self):
        return "ObjectId('%s')" % (str(self),)

    def __eq__(self, other):
        if isinstance(other, ObjectId):
            return self.__id == other.__id
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, ObjectId):
            return self.__id != other.__id
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, ObjectId):
            return self.__id < other.__id
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, ObjectId):
            return self.__id <= other.__id
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, ObjectId):
            return self.__id > other.__id
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, ObjectId):
            return self.__id >= other.__id
        return NotImplemented

    def __hash__(self):
        """Get a hash value for this :class:`ObjectId`.

        .. versionadded:: 1.1
        """
        return hash(self.__id)