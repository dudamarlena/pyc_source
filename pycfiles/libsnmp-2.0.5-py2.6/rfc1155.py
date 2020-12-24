# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/libsnmp/rfc1155.py
# Compiled at: 2010-01-29 19:07:45
import util, debug, logging, types, copy
log = logging.getLogger('Asn1Object')
log.setLevel(logging.INFO)
asnTagClasses = {'UNIVERSAL': 0, 
   'APPLICATION': 64, 
   'CONTEXT': 128, 
   'PRIVATE': 192}
asnTagFormats = {'PRIMITIVE': 0, 
   'CONSTRUCTED': 32}
asnTagNumbers = {'Integer': 2, 
   'OctetString': 4, 
   'Null': 5, 
   'ObjectID': 6, 
   'Sequence': 16, 
   'IPAddress': 0, 
   'Counter': 1, 
   'Guage': 2, 
   'TimeTicks': 3, 
   'Opaque': 4}

class Asn1Object:
    """Base class for all Asn1Objects This is only intended to
    support a specific subset of ASN1 stuff as defined by the RFCs to
    keep things as simple as possible."""
    asnTagClass = asnTagClasses['UNIVERSAL']
    asnTagFormat = asnTagFormats['PRIMITIVE']
    asnTagNumber = None
    value = None

    def __init__(self):
        pass

    def encode(self):
        """ encode() this Asn1Object using BER"""
        contents = self.encodeContents()
        resultlist = []
        resultlist.append(self.encodeIdentifier())
        resultlist.append(self.encodeLength(len(contents)))
        resultlist.append(contents)
        result = ('').join(resultlist)
        return result

    def decodeTag(self, stream):
        """Decode a BER tag field, returning the tag and the remainder
        of the stream"""
        tag = ord(stream[0])
        n = 1
        if tag & 31 == 31:
            tag = 0
            while 1:
                byte = ord(stream[n])
                tag = tag << 7 | byte & 127
                n += 1
                if not byte & 128:
                    break

        return (tag, stream[n:])

    def decodeLength(self, stream):
        """Decode a BER length field, returing the length and the
        remainder of the stream"""
        length = ord(stream[0])
        n = 1
        if length & 128:
            run = length & 127
            length = 0
            for i in xrange(run):
                length = length << 8 | ord(stream[n])
                n += 1

        return (
         length, stream[n:])

    def decode(self, stream):
        """decode() an octet stream into a sequence of Asn1Objects
        This method should be overridden by subclasses to define how
        to decode one of themselves from a fixed length stream.  This
        general case method looks at the identifier at the beginning
        of a stream of octets and uses the appropriate decode() method
        of that known object.  Attempts to decode() an unknown object
        type result in an error.  """
        if type(stream) != types.StringType:
            raise TypeError('stream should be of type StringType, not %s' % type(stream))
        objects = []
        while len(stream) > 0:
            (tag, stream) = self.decodeTag(stream)
            (length, stream) = self.decodeLength(stream)
            objectData = stream[:length]
            stream = stream[length:]
            try:
                decoder = tagDecodeDict[tag]()
            except KeyError:
                raise ValueError('Unknown ASN.1 Type %d' % tag)

            objects.append(decoder.decodeContents(objectData))

        return objects

    def encodeContents(self):
        """encodeContents should be overridden by subclasses to encode
        the contents of a particular type"""
        raise NotImplementedError

    def encodeIdentifier(self):
        """encodeIdentifier() returns encoded identifier octets for
        this object.  Section 6.3 of ITU-T-X.209 """
        if self.asnTagNumber < 31:
            result = chr(self.asnTagClass | self.asnTagFormat | self.asnTagNumber)
        else:
            resultlist = []
            resultlist.append(chr(self.asnTagClass | self.asnTagFormat | 31))
            integer = self.asnTagNumber
            while integer != -1:
                resultlist.append(chr(integer & 255))
                integer = integer >> 8

            result = ('').join(resultlist)
        return result

    def encodeLength(self, length):
        """encodeLength() takes the length of the contents and
        produces the encoding for that length.  Section 6.3 of
        ITU-T-X.209 """
        if length < 127:
            result = chr(length & 255)
        else:
            log.debug('Long length encoding required for length of %d' % length)
            resultlist = []
            numOctets = 0
            while length > 0:
                resultlist.insert(0, chr(length & 255))
                length = length >> 8
                numOctets += 1

            log.debug('long length encoding of: %d octets' % numOctets)
            numOctets = numOctets | 128
            resultlist.insert(0, chr(numOctets & 255))
            result = ('').join(resultlist)
        return result

    def encodeEndOfContents(self):
        return '\x00\x00'

    def __eq__(self, other):
        """
        Compare two instance by comparison of their value fields
        only.
        """
        return isinstance(other, self.__class__) and self.value == other.value

    def __ne__(self, other):
        """Compare two objects for inequality"""
        return not self == other

    def toObjectID(self):
        raise TypeError


class Integer(Asn1Object):
    """An ASN.1 Integer type"""
    asnTagClass = asnTagClasses['UNIVERSAL']
    asnTagNumber = asnTagNumbers['Integer']
    MINVAL = -2147483648
    MAXVAL = 2147483647

    def __init__(self, value=0):
        Asn1Object.__init__(self)
        if not self.MINVAL <= value <= self.MAXVAL:
            log.debug('minval: %d' % self.MINVAL)
            log.debug('maxval: %d' % self.MAXVAL)
            raise ValueError('Integer value of %d is out of bounds' % value)
        self.value = value

    def __str__(self):
        return '%d' % self.value

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __long__(self):
        return self.value

    def __hex__(self):
        return hex(self.value)

    def __oct__(self):
        return oct(self.value)

    def __call__(self):
        """ Return the value of the Integer when referring to it directly
        """
        return self.value

    def __eq__(self, other):
        try:
            if self.value == long(other):
                return True
        except:
            raise

        return False

    def __add__(self, integer):
        """ Add a value
        """
        if not isinstance(integer, self.__class__):
            integer = self.__class__(integer)
        return self.__class__(self.value + integer.value)

    def __sub__(self, integer):
        if not isinstance(value, self.__class__):
            value = self.__class__(value)
        return self.__class__(self.value + integer.value)

    def __hash__(self):
        """ Standard Python integers are easy to hash
            so we just do the same thing.
        """
        return self.value.__hash__()

    def encodeContents(self):
        integer = self.value
        if integer == 0:
            return '\x00'
        else:
            if integer == -1:
                return b'\xff'
            if integer > 0:
                result = []
                while integer != 0:
                    result.insert(0, integer & 255)
                    integer >>= 8

                if result[0] & 128:
                    result.insert(0, 0)
                return ('').join(map(chr, result))
            result = []
            while integer != -1:
                result.insert(0, integer & 255)
                integer >>= 8

            if result[0] & 128 != 128:
                result.insert(0, 0)
            return ('').join(map(chr, result))

    def decodeContents(self, stream):
        """ Decode some input octet stream into a signed ASN.1 integer
        """
        input = map(ord, stream)
        log.debug('Decoding %s' % util.octetsToHex(stream))
        self.value = 0
        byte = input[0]
        if byte & 128 == 128:
            negbit = 128
            self.value = byte & 127
            for i in xrange(1, len(input)):
                negbit <<= 8
                self.value = self.value << 8 | input[i]

            self.value = self.value - negbit
        else:
            self.value = long(byte)
            for i in xrange(1, len(input)):
                self.value = self.value << 8 | input[i]

            log.debug('decoded as: %d' % self.value)
        return self

    def decodeTwosInteger1(self, stream):
        """ One algorithm for decoding twos complement Integers """
        bytes = map(ord, stream)
        if bytes[0] & 128:
            bytes.insert(0, -1)
        result = reduce(lambda x, y: x << 8 | y, bytes, 0)
        return result

    def decodeTwosInteger2(self, stream):
        """A second algorithm for decoding twos complement Integers
        Coded from scratch by jpw """
        val = 0
        byte = ord(stream[0])
        if byte & 128 == 128:
            negbit = 128
            val = byte & 127
            for i in range(len(stream) - 1):
                byte = ord(stream[(i + 1)])
                negbit <<= 8
                val = val << 8 | byte

            val = val - negbit
        else:
            val = byte
        for i in range(len(stream) - 1):
            byte = ord(stream[(i + 1)])
            val = val << 8 | byte

        return val

    def decodeTwosInteger3(self, stream):
        """ A third algorithm for decoding twos complement Integers
        Coded from scratch by jpw """
        val = 0
        bytes = map(ord, stream)
        if bytes[0] & 128:
            bytes[0] = bytes[0] & 127
            negbit = 128
            for i in bytes:
                negbit <<= 8
                val = val << 8 | i

            val = val - (negbit >> 8)
        for i in bytes:
            val = val << 8 | i

        return val

    def toObjectID(self):
        return ObjectID([self.value])


class OctetString(Asn1Object):
    """An ASN.1 Octet String type"""
    asnTagClass = asnTagClasses['UNIVERSAL']
    asnTagNumber = asnTagNumbers['OctetString']

    def __init__(self, value=''):
        Asn1Object.__init__(self)
        self.value = copy.copy(value)

    def __str__(self):
        return self.value

    def encodeContents(self):
        """An OctetString is already encoded. Whee!"""
        return self.value

    def decodeContents(self, stream):
        """An OctetString is already decoded. Whee!  """
        self.value = stream
        return self

    def __hex__(self):
        return ('').join([ '%.2X' % ord(x) for x in self.value ])

    def __oct__(self):
        return ('').join([ '%3o' % ord(x) for x in self.value ])

    def toObjectID(self):
        return ObjectID([ ord(x) for x in self.value ])


class ObjectID(Asn1Object):
    """An ASN.1 Object Identifier type """
    asnTagClass = asnTagClasses['UNIVERSAL']
    asnTagFormat = asnTagFormats['PRIMITIVE']
    asnTagNumber = asnTagNumbers['ObjectID']

    def __init__(self, value=None):
        """Create an ObjectID - value is a list of subids as a string
        or list"""
        Asn1Object.__init__(self)
        if type(value) == types.StringType:
            value = value.strip('.')
            subidlist = value.split('.')
            self.value = []
            for subid in subidlist:
                number = int(subid)
                if number < 0 or number > 2147483647:
                    raise ValueError('SubID out of range')
                self.value.append(number)

        elif type(value) == types.ListType or type(value) == types.NoneType:
            self.value = copy.copy(value)
        elif type(value) == types.TupleType:
            self.value = list(value)
        elif type(value) == types.IntType:
            self.value = [
             value]
        elif isinstance(value, ObjectID):
            self.value = value.value[:]
        else:
            raise TypeError('unknown type passed as OID')

    def __str__(self):
        if self.value is not None:
            return '.' + ('.').join([ str(x) for x in self.value ])
        else:
            return ''
            return

    def __len__(self):
        """Return the length of the value field"""
        if self.value is None:
            return 0
        else:
            return len(self.value)
            return

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.value.__getitem__(key)
        else:
            return ObjectID(self.value.__getitem__(key))

    def __delitem__(self, key):
        self.value.__delitem__(key)

    def copy(self):
        """
        Return a copy of this object as a new object
        """
        return ObjectID(self.value)

    def append(self, subid):
        if type(subid) == types.IntType:
            self.value.append(subid)
        else:
            raise TypeError

    def extend(self, other):
        if isinstance(other, self.__class__):
            self.value.extend(other.value)
        else:
            self.value.extend(other)
        return

    def isPrefixOf(self, other):
        """
        Compares this ObjectID with another ObjectID and returns
        non-None if this ObjectID is a prefix of the other one.
        """
        if not isinstance(other, self.__class__):
            raise TypeError('Attempt to compare ObjectID with non-ObjectID: %s' % other.__repr__())
        if len(other) < len(self):
            return False
        for i in range(len(self)):
            if self.value[i] != other.value[i]:
                return False

        return True

    def encodeContents(self):
        """encode() an objectID into an octet stream """
        result = []
        idlist = self.value[:]
        idlist.reverse()
        subid1 = idlist.pop() * 40 + idlist.pop()
        idlist.reverse()
        idlist.insert(0, subid1)
        for subid in idlist:
            if subid < 128:
                result.append(chr(subid & 127))
            else:
                position = len(result)
                result.append(chr(subid & 127))
                subid = subid >> 7
                while subid > 0:
                    result.insert(position, chr(128 | subid & 127))
                    subid = subid >> 7

        return ('').join(result)

    def decodeContents(self, stream):
        """decode() a stream into an ObjectID()"""
        self.value = []
        bytes = map(ord, stream)
        if len(stream) == 0:
            raise ValueError('stream of zero length in %s' % self.__class__.__name__)
        if bytes[0] < 128:
            self.value.append(int(bytes[0] / 40))
            self.value.append(int(bytes[0] % 40))
        else:
            raise NotImplementedError('First octet is > 128! Unsupported oid detected')
        n = 1
        while n < len(bytes):
            subid = bytes[n]
            n += 1
            if subid & 128 == 128:
                val = subid & 127
                while subid & 128 == 128:
                    subid = bytes[n]
                    n += 1
                    val = val << 7 | subid & 127

                self.value.append(val)
            else:
                self.value.append(subid)

        return self

    def toObjectID(self):
        return ObjectID(copy.copy(self.value))


class Null(Asn1Object):
    """An ASN.1 Object Identifier type"""
    asnTagClass = asnTagClasses['UNIVERSAL']
    asnTagFormat = asnTagFormats['PRIMITIVE']
    asnTagNumber = asnTagNumbers['Null']

    def __str__(self):
        return '<Null>'

    def encodeContents(self):
        return ''

    def decodeContents(self, stream):
        if len(stream) != 0:
            raise ValueError('Input stream too long for %s' % self.__class__.__name__)
        return self


class Sequence(Asn1Object):
    """A Sequence is basically a list of name, value pairs with the
    name being an object Type and the value being an instance of an
    Asn1Object of that Type."""
    asnTagClass = asnTagClasses['UNIVERSAL']
    asnTagFormat = asnTagFormats['CONSTRUCTED']
    asnTagNumber = asnTagNumbers['Sequence']
    value = []

    def __init__(self, value=[]):
        Asn1Object.__init__(self)
        self.value = value

    def __str__(self):
        result = '['
        res = []
        for item in self.value:
            res.append('%s' % item)

        result += (', ').join(res)
        result += ']'
        return result

    def __len__(self):
        return len(self.value)

    def __getitem__(self, index):
        return self.value[index]

    def append(self, val):
        self.value.append(val)

    def encodeContents(self):
        """ To encode a Sequence, we simply encode() each sub-object
        in turn."""
        log.debug('Encoding sequence contents...')
        resultlist = []
        for elem in self.value:
            resultlist.append(elem.encode())

        result = ('').join(resultlist)
        return result

    def decodeContents(self, stream):
        """decode a sequence of objects"""
        objectList = self.decode(stream)
        self.value = objectList
        return self


class SequenceOf(Sequence):
    """A SequenceOf is a special kind of sequence that places a
    constraint on the kind of objects it can contain.  It is variable
    in length."""
    asnTagClass = asnTagClasses['UNIVERSAL']
    asnTagFormat = asnTagFormats['CONSTRUCTED']
    asnTagNumber = asnTagNumbers['Sequence']

    def __init__(self, componentType=Asn1Object, value=None):
        Sequence.__init__(self)
        self.componentType = componentType
        self.value = []
        if value:
            for item in value:
                self.append(item)

    def append(self, value):
        if not isinstance(value, self.componentType):
            raise ValueError('%s: cannot contain components of type: %s' % (self.__class__.__name__, value.__class__.__name__))
        Sequence.append(self, value)


class IPAddress(OctetString):
    """An IpAddress is a special type of OctetString.  It represents a
    32-bit internet address as an OctetString of length 4, in network
    byte order.  """
    asnTagClass = asnTagClasses['APPLICATION']
    asnTagFormat = asnTagFormats['PRIMITIVE']
    asnTagNumber = asnTagNumbers['IPAddress']

    def __init__(self, value=None):
        OctetString.__init__(self, value)
        if type(value) == types.StringType:
            self.value = ''
            listform = value.split('.')
            if len(listform) != 4:
                raise ValueError('IPAddress must be of length 4')
            for item in listform:
                self.value += chr(int(item))

        elif type(value) == types.ListType:
            if len(value) != 4:
                raise ValueError('IPAddress must be of length 4')
        else:
            self.value = ''

    def decodeContents(self, stream):
        """An IPAddress is already decoded. Whee!"""
        self.value = stream
        return self

    def __str__(self):
        result = []
        for item in self.value:
            result.append('%d' % ord(item))

        return ('.').join(result)

    def toObjectID(self):
        return ObjectID([ ord(x) for x in self.value ])


class NetworkAddress(IPAddress):
    """ A Network Address is a CHOICE with only one possible value:
        internet
    """
    name = 'internet'


class Counter(Integer):
    """ A counter starts at zero and keeps going to a maximum integer
        value of 2^32-1 where it wraps back to zero.
    """
    asnTagClass = asnTagClasses['APPLICATION']
    asnTagFormat = asnTagFormats['PRIMITIVE']
    asnTagNumber = asnTagNumbers['Counter']
    MINVAL = 0
    MAXVAL = 4294967295

    def __add__(self, val):
        """ We only add to a counter, and we check for a wrap
            condition.
        """
        if self.value + val > self.MAXVAL:
            self.value = val - (self.MAXVAL - self.value)
        else:
            self.value += val

    def decodeContents(self, stream):
        result = Integer.decodeContents(self, stream)
        if self.value < 0:
            self.value += 4294967296
        return self


class Guage(Integer):
    """ A Guage is a non negative integer.  It may increase or
        decrease. It latches at a maximum value.
    """
    asnTagClass = asnTagClasses['APPLICATION']
    asnTagFormat = asnTagFormats['PRIMITIVE']
    asnTagNumber = asnTagNumbers['Guage']
    MINVAL = 0
    MAXVAL = 4294967295

    def __add__(self, val):
        """Add to the Guage, latching at the maximum"""
        if self.value + val > MAXVAL:
            self.value = MAXVAL
        else:
            self.value += val

    def __sub__(self, val):
        """Subtract from the Guage, latching at zerod """
        if self.value - val < self.MINVAL:
            self.value = self.MINVAL
        else:
            self.value -= val


class TimeTicks(Integer):
    """ TimeTicks is the number of hundredths of a second since an
        epoch, specified at object creation time
    """
    asnTagClass = asnTagClasses['APPLICATION']
    asnTagFormat = asnTagFormats['PRIMITIVE']
    asnTagNumber = asnTagNumbers['TimeTicks']
    MINVAL = 0
    MAXVAL = 4294967295
    epoch = None

    def __init__(self, value=0, epoch=None):
        Integer.__init__(self, value)
        if epoch:
            self.epoch = epoch

    def _todo__str__(self):
        """
        Format the TimeTicks value into an actual
        time/date stamp based on the epoch.
        """
        return ''


class Opaque(OctetString):
    """Opaque is a fun type that allows you to pass arbitrary ASN.1
    encoded stuff in an object. The value is some ASN.1 syntax encoded
    using BER which this object encodes as an OctetString.  We don't
    do any decoding of this object because we don't have to, and that
    makes this all much quicker.  """
    pass


class DecodeError(Exception):

    def __init__(self, args=None):
        self.args = args


tagDecodeDict = {2: Integer, 
   4: OctetString, 
   5: Null, 
   6: ObjectID, 
   48: Sequence, 
   64: IPAddress, 
   65: Counter, 
   66: Guage, 
   67: TimeTicks, 
   68: Opaque}