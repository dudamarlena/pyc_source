# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: bson/binary.py
# Compiled at: 2014-07-29 17:29:28
try:
    from uuid import UUID
except ImportError:
    pass

from bson.py3compat import PY3, binary_type
BINARY_SUBTYPE = 0
FUNCTION_SUBTYPE = 1
OLD_BINARY_SUBTYPE = 2
OLD_UUID_SUBTYPE = 3
UUID_SUBTYPE = 4
JAVA_LEGACY = 5
CSHARP_LEGACY = 6
ALL_UUID_SUBTYPES = (
 OLD_UUID_SUBTYPE, UUID_SUBTYPE, JAVA_LEGACY, CSHARP_LEGACY)
MD5_SUBTYPE = 5
USER_DEFINED_SUBTYPE = 128

class Binary(binary_type):
    """Representation of BSON binary data.

    This is necessary because we want to represent Python strings as
    the BSON string type. We need to wrap binary data so we can tell
    the difference between what should be considered binary data and
    what should be considered a string when we encode to BSON.

    Raises TypeError if `data` is not an instance of :class:`str`
    (:class:`bytes` in python 3) or `subtype` is not an instance of
    :class:`int`. Raises ValueError if `subtype` is not in [0, 256).

    .. note::
      In python 3 instances of Binary with subtype 0 will be decoded
      directly to :class:`bytes`.

    :Parameters:
      - `data`: the binary data to represent
      - `subtype` (optional): the `binary subtype
        <http://bsonspec.org/#/specification>`_
        to use
    """
    _type_marker = 5

    def __new__(cls, data, subtype=BINARY_SUBTYPE):
        if not isinstance(data, binary_type):
            raise TypeError('data must be an instance of %s' % (
             binary_type.__name__,))
        if not isinstance(subtype, int):
            raise TypeError('subtype must be an instance of int')
        if subtype >= 256 or subtype < 0:
            raise ValueError('subtype must be contained in [0, 256)')
        self = binary_type.__new__(cls, data)
        self.__subtype = subtype
        return self

    @property
    def subtype(self):
        """Subtype of this binary data.
        """
        return self.__subtype

    def __getnewargs__(self):
        data = super(Binary, self).__getnewargs__()[0]
        if PY3 and not isinstance(data, binary_type):
            data = data.encode('latin-1')
        return (
         data, self.__subtype)

    def __eq__(self, other):
        if isinstance(other, Binary):
            return (self.__subtype, binary_type(self)) == (
             other.subtype, binary_type(other))
        return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return 'Binary(%s, %s)' % (binary_type.__repr__(self), self.__subtype)


class UUIDLegacy(Binary):
    """UUID wrapper to support working with UUIDs stored as legacy
    BSON binary subtype 3.

    .. doctest::

      >>> import uuid
      >>> from bson.binary import Binary, UUIDLegacy, UUID_SUBTYPE
      >>> my_uuid = uuid.uuid4()
      >>> coll = db.test
      >>> coll.uuid_subtype = UUID_SUBTYPE
      >>> coll.insert({'uuid': Binary(my_uuid.bytes, 3)})
      ObjectId('...')
      >>> coll.find({'uuid': my_uuid}).count()
      0
      >>> coll.find({'uuid': UUIDLegacy(my_uuid)}).count()
      1
      >>> coll.find({'uuid': UUIDLegacy(my_uuid)})[0]['uuid']
      UUID('...')
      >>>
      >>> # Convert from subtype 3 to subtype 4
      >>> doc = coll.find_one({'uuid': UUIDLegacy(my_uuid)})
      >>> coll.save(doc)
      ObjectId('...')
      >>> coll.find({'uuid': UUIDLegacy(my_uuid)}).count()
      0
      >>> coll.find({'uuid': {'$in': [UUIDLegacy(my_uuid), my_uuid]}}).count()
      1
      >>> coll.find_one({'uuid': my_uuid})['uuid']
      UUID('...')

    Raises TypeError if `obj` is not an instance of :class:`~uuid.UUID`.

    :Parameters:
      - `obj`: An instance of :class:`~uuid.UUID`.
    """

    def __new__(cls, obj):
        if not isinstance(obj, UUID):
            raise TypeError('obj must be an instance of uuid.UUID')
        self = Binary.__new__(cls, binary_type(obj.bytes), OLD_UUID_SUBTYPE)
        self.__uuid = obj
        return self

    def __getnewargs__(self):
        return (
         self.__uuid,)

    @property
    def uuid(self):
        """UUID instance wrapped by this UUIDLegacy instance.
        """
        return self.__uuid

    def __repr__(self):
        return "UUIDLegacy('%s')" % self.__uuid