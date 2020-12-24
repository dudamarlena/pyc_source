# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/javaobj.py
# Compiled at: 2011-03-29 08:24:06
"""Provides functions for reading and writing (writing is WIP currently) Java objects
serialized or will be deserialized by ObjectOutputStream. This form of object
representation is a standard data interchange format in Java world.

javaobj module exposes an API familiar to users of the standard library marshal, pickle and json modules.

See: http://download.oracle.com/javase/6/docs/platform/serialization/spec/protocol.html
"""
import StringIO, struct
try:
    import logging
except ImportError:

    def log_debug(message, ident=0):
        pass


    def log_error(message, ident=0):
        pass


else:
    _log = logging.getLogger(__name__)

    def log_debug(message, ident=0):
        _log.debug(' ' * (ident * 2) + str(message))


    def log_error(message, ident=0):
        _log.error(' ' * (ident * 2) + str(message))


__version__ = '$Revision: 20 $'

def load(file_object):
    """
    Deserializes Java primitive data and objects serialized by ObjectOutputStream
    from a file-like object.
    """
    marshaller = JavaObjectUnmarshaller(file_object)
    return marshaller.readObject()


def loads(string):
    """
    Deserializes Java objects and primitive data serialized by ObjectOutputStream
    from a string.
    """
    f = StringIO.StringIO(string)
    marshaller = JavaObjectUnmarshaller(f)
    return marshaller.readObject()


def dumps(object):
    """
    Serializes Java primitive data and objects unmarshaled by load(s) before into string.
    """
    marshaller = JavaObjectMarshaller()
    return marshaller.dump(object)


class JavaClass(object):

    def __init__(self):
        self.name = None
        self.serialVersionUID = None
        self.flags = None
        self.fields_names = []
        self.fields_types = []
        self.superclass = None
        return

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '[%s:0x%X]' % (self.name, self.serialVersionUID)


class JavaObject(object):
    classdesc = None

    def get_class(self):
        return self.classdesc


class JavaObjectConstants():
    STREAM_MAGIC = 44269
    STREAM_VERSION = 5
    TC_NULL = 112
    TC_REFERENCE = 113
    TC_CLASSDESC = 114
    TC_OBJECT = 115
    TC_STRING = 116
    TC_ARRAY = 117
    TC_CLASS = 118
    TC_BLOCKDATA = 119
    TC_ENDBLOCKDATA = 120
    TC_RESET = 121
    TC_BLOCKDATALONG = 122
    TC_EXCEPTION = 123
    TC_LONGSTRING = 124
    TC_PROXYCLASSDESC = 125
    TC_ENUM = 126
    TC_MAX = 126
    SC_WRITE_METHOD = 1
    SC_BLOCK_DATA = 8
    SC_SERIALIZABLE = 2
    SC_EXTERNALIZABLE = 4
    SC_ENUM = 16
    TYPE_BYTE = 'B'
    TYPE_CHAR = 'C'
    TYPE_DOUBLE = 'D'
    TYPE_FLOAT = 'F'
    TYPE_INTEGER = 'I'
    TYPE_LONG = 'J'
    TYPE_SHORT = 'S'
    TYPE_BOOLEAN = 'Z'
    TYPE_OBJECT = 'L'
    TYPE_ARRAY = '['
    TYPECODES_LIST = [
     TYPE_BYTE,
     TYPE_CHAR,
     TYPE_DOUBLE,
     TYPE_FLOAT,
     TYPE_INTEGER,
     TYPE_LONG,
     TYPE_SHORT,
     TYPE_BOOLEAN,
     TYPE_OBJECT,
     TYPE_ARRAY]
    BASE_REFERENCE_IDX = 8257536


class JavaObjectUnmarshaller(JavaObjectConstants):

    def __init__(self, stream=None):
        self.opmap = {self.TC_NULL: self.do_null, 
           self.TC_CLASSDESC: self.do_classdesc, 
           self.TC_OBJECT: self.do_object, 
           self.TC_STRING: self.do_string, 
           self.TC_ARRAY: self.do_array, 
           self.TC_CLASS: self.do_class, 
           self.TC_BLOCKDATA: self.do_blockdata, 
           self.TC_REFERENCE: self.do_reference}
        self.current_object = None
        self.reference_counter = 0
        self.references = []
        self.object_stream = stream
        self._readStreamHeader()
        return

    def readObject(self):
        try:
            res = self._read_and_exec_opcode(ident=0)
            position_bak = self.object_stream.tell()
            the_rest = self.object_stream.read()
            if len(the_rest):
                log_error('Warning!!!!: Stream still has %s bytes left. Enable debug mode of logging to see the hexdump.' % len(the_rest))
                log_debug(self._create_hexdump(the_rest))
            else:
                log_debug('Java Object unmarshalled succesfully!')
            self.object_stream.seek(position_bak)
            return res
        except Exception, e:
            self._oops_dump_state()
            raise

    def _readStreamHeader(self):
        (magic, version) = self._readStruct('>HH')
        if magic != self.STREAM_MAGIC or version != self.STREAM_VERSION:
            raise IOError('The stream is not java serialized object. Invalid stream header: %04X%04X' % (magic, version))

    def _read_and_exec_opcode(self, ident=0, expect=None):
        (opid,) = self._readStruct('>B')
        log_debug('OpCode: 0x%X' % opid, ident)
        if expect and opid not in expect:
            raise IOError('Unexpected opcode 0x%X' % opid)
        return self.opmap.get(opid, self.do_unknown)(ident=ident)

    def _readStruct(self, unpack):
        length = struct.calcsize(unpack)
        ba = self.object_stream.read(length)
        return struct.unpack(unpack, ba)

    def _readString(self):
        (length,) = self._readStruct('>H')
        ba = self.object_stream.read(length)
        return ba

    def do_classdesc(self, parent=None, ident=0):
        clazz = JavaClass()
        log_debug('[classdesc]', ident)
        ba = self._readString()
        clazz.name = ba
        log_debug('Class name: %s' % ba, ident)
        (serialVersionUID, newHandle, classDescFlags) = self._readStruct('>LLB')
        clazz.serialVersionUID = serialVersionUID
        clazz.flags = classDescFlags
        self._add_reference(clazz)
        log_debug('Serial: 0x%X newHandle: 0x%X. classDescFlags: 0x%X' % (serialVersionUID, newHandle, classDescFlags), ident)
        (length,) = self._readStruct('>H')
        log_debug('Fields num: 0x%X' % length, ident)
        clazz.fields_names = []
        clazz.fields_types = []
        for fieldId in range(length):
            (type,) = self._readStruct('>B')
            field_name = self._readString()
            field_type = None
            field_type = self._convert_char_to_type(type)
            if field_type == self.TYPE_ARRAY:
                field_type = self._read_and_exec_opcode(ident=ident + 1, expect=[self.TC_STRING, self.TC_REFERENCE])
            elif field_type == self.TYPE_OBJECT:
                field_type = self._read_and_exec_opcode(ident=ident + 1, expect=[self.TC_STRING, self.TC_REFERENCE])
            log_debug('FieldName: 0x%X' % type + ' ' + str(field_name) + ' ' + str(field_type), ident)
            assert field_name is not None
            assert field_type is not None
            clazz.fields_names.append(field_name)
            clazz.fields_types.append(field_type)

        if parent:
            parent.__fields = clazz.fields_names
            parent.__types = clazz.fields_types
        (opid,) = self._readStruct('>B')
        if opid != self.TC_ENDBLOCKDATA:
            raise NotImplementedError("classAnnotation isn't implemented yet")
        log_debug('OpCode: 0x%X' % opid, ident)
        superclassdesc = self._read_and_exec_opcode(ident=ident + 1, expect=[self.TC_CLASSDESC, self.TC_NULL, self.TC_REFERENCE])
        log_debug(str(superclassdesc), ident)
        clazz.superclass = superclassdesc
        return clazz

    def do_blockdata(self, parent=None, ident=0):
        log_debug('[blockdata]', ident)
        (length,) = self._readStruct('>B')
        ba = self.object_stream.read(length)
        return ba

    def do_class(self, parent=None, ident=0):
        log_debug('[class]', ident)
        classdesc = self._read_and_exec_opcode(ident=ident + 1, expect=[self.TC_CLASSDESC, self.TC_PROXYCLASSDESC, self.TC_NULL, self.TC_REFERENCE])
        log_debug('Classdesc: %s' % classdesc, ident)
        self._add_reference(classdesc)
        return classdesc

    def do_object(self, parent=None, ident=0):
        java_object = JavaObject()
        log_debug('[object]', ident)
        classdesc = self._read_and_exec_opcode(ident=ident + 1, expect=[self.TC_CLASSDESC, self.TC_PROXYCLASSDESC, self.TC_NULL, self.TC_REFERENCE])
        self._add_reference(java_object)
        java_object.classdesc = classdesc
        if classdesc.flags & self.SC_EXTERNALIZABLE and not classdesc.flags & self.SC_BLOCK_DATA:
            raise NotImplementedError("externalContents isn't implemented yet")
        if classdesc.flags & self.SC_SERIALIZABLE:
            tempclass = classdesc
            megalist = []
            megatypes = []
            while tempclass:
                log_debug('>>> ' + str(tempclass.fields_names) + ' ' + str(tempclass), ident)
                fieldscopy = tempclass.fields_names[:]
                fieldscopy.extend(megalist)
                megalist = fieldscopy
                fieldscopy = tempclass.fields_types[:]
                fieldscopy.extend(megatypes)
                megatypes = fieldscopy
                tempclass = tempclass.superclass

            log_debug('Values count: %s' % str(len(megalist)), ident)
            log_debug('Prepared list of values: %s' % str(megalist), ident)
            log_debug('Prepared list of types: %s' % str(megatypes), ident)
            for (field_name, field_type) in zip(megalist, megatypes):
                res = self._read_value(field_type, ident, name=field_name)
                java_object.__setattr__(field_name, res)

        if classdesc.flags & self.SC_SERIALIZABLE and classdesc.flags & self.SC_WRITE_METHOD or classdesc.flags & self.SC_EXTERNALIZABLE and classdesc.flags & self.SC_BLOCK_DATA:
            (opid,) = self._readStruct('>B')
            if opid != self.TC_ENDBLOCKDATA:
                self.object_stream.seek(-1, mode=1)
                raise NotImplementedError("objectAnnotation isn't fully implemented yet")
        return java_object

    def do_string(self, parent=None, ident=0):
        log_debug('[string]', ident)
        ba = self._readString()
        self._add_reference(str(ba))
        return str(ba)

    def do_array(self, parent=None, ident=0):
        log_debug('[array]', ident)
        classdesc = self._read_and_exec_opcode(ident=ident + 1, expect=[self.TC_CLASSDESC, self.TC_PROXYCLASSDESC, self.TC_NULL, self.TC_REFERENCE])
        array = []
        self._add_reference(array)
        (size,) = self._readStruct('>i')
        log_debug('size: ' + str(size), ident)
        type_char = classdesc.name[0]
        assert type_char == self.TYPE_ARRAY
        type_char = classdesc.name[1]
        if type_char == self.TYPE_OBJECT or type_char == self.TYPE_ARRAY:
            for i in range(size):
                res = self._read_and_exec_opcode(ident=ident + 1)
                log_debug('Object value: %s' % str(res), ident)
                array.append(res)

        for i in range(size):
            res = self._read_value(type_char, ident)
            log_debug('Native value: %s' % str(res), ident)
            array.append(res)

        return array

    def do_reference(self, parent=None, ident=0):
        (handle,) = self._readStruct('>L')
        log_debug('## Reference handle: 0x%x' % handle, ident)
        return self.references[(handle - self.BASE_REFERENCE_IDX)]

    def do_null(self, parent=None, ident=0):
        return

    def do_unknown(self, parent=None, ident=0):
        raise RuntimeError('Unknown OpCode')

    def _create_hexdump(self, src, length=16):
        FILTER = ('').join([ len(repr(chr(x))) == 3 and chr(x) or '.' for x in range(256) ])
        result = []
        for i in xrange(0, len(src), length):
            s = src[i:i + length]
            hexa = (' ').join([ '%02X' % ord(x) for x in s ])
            printable = s.translate(FILTER)
            result.append('%04X   %-*s  %s\n' % (i, length * 3, hexa, printable))

        return ('').join(result)

    def _read_value(self, field_type, ident, name=''):
        if len(field_type) > 1:
            field_type = field_type[0]
        if field_type == self.TYPE_BOOLEAN:
            (val,) = self._readStruct('>B')
            res = bool(val)
        elif field_type == self.TYPE_BYTE:
            (res,) = self._readStruct('>b')
        elif field_type == self.TYPE_SHORT:
            (res,) = self._readStruct('>h')
        elif field_type == self.TYPE_INTEGER:
            (res,) = self._readStruct('>i')
        elif field_type == self.TYPE_LONG:
            (res,) = self._readStruct('>q')
        elif field_type == self.TYPE_FLOAT:
            (res,) = self._readStruct('>f')
        elif field_type == self.TYPE_DOUBLE:
            (res,) = self._readStruct('>d')
        elif field_type == self.TYPE_OBJECT or field_type == self.TYPE_ARRAY:
            res = self._read_and_exec_opcode(ident=ident + 1)
        else:
            raise RuntimeError('Unknown typecode: %s' % field_type)
        log_debug('* %s %s: ' % (field_type, name) + str(res), ident)
        return res

    def _convert_char_to_type(self, type_char):
        typecode = type_char
        if type(type_char) is int:
            typecode = chr(type_char)
        if typecode in self.TYPECODES_LIST:
            return typecode
        raise RuntimeError("Typecode %s (%s) isn't supported." % (type_char, typecode))

    def _add_reference(self, obj):
        self.references.append(obj)

    def _oops_dump_state(self):
        log_error('==Oops state dump' + '=' * 13)
        log_error('References: %s' % str(self.references))
        log_error('Stream seeking back at -16 byte (2nd line is an actual position!):')
        self.object_stream.seek(-16, mode=1)
        the_rest = self.object_stream.read()
        if len(the_rest):
            log_error('Warning!!!!: Stream still has %s bytes left.' % len(the_rest))
            log_error(self._create_hexdump(the_rest))
        log_error('=' * 30)


class JavaObjectMarshaller(JavaObjectConstants):

    def __init__(self, stream=None):
        self.object_stream = stream

    def dump(self, obj):
        self.object_obj = obj
        self.object_stream = StringIO.StringIO()
        self._writeStreamHeader()
        self.writeObject(obj)
        return self.object_stream.getvalue()

    def _writeStreamHeader(self):
        self._writeStruct('>HH', 4, (self.STREAM_MAGIC, self.STREAM_VERSION))

    def writeObject(self, obj):
        log_debug('Writing object of type ' + str(type(obj)))
        if type(obj) is JavaObject:
            self.write_object(obj)
        elif type(obj) is str:
            self.write_blockdata(obj)
        else:
            raise RuntimeError('Object serialization of type %s is not supported.' % str(type(obj)))

    def _writeStruct(self, unpack, length, args):
        ba = struct.pack(unpack, *args)
        self.object_stream.write(ba)

    def _writeString(self, string):
        len = len(string)
        self._writeStruct('>H', 2, (len,))
        self.object_stream.write(string)

    def write_blockdata(self, obj, parent=None):
        self._writeStruct('>B', 1, (self.TC_BLOCKDATA,))
        if type(obj) is str:
            self._writeStruct('>B', 1, (len(obj),))
            self.object_stream.write(obj)

    def write_object(self, obj, parent=None):
        self._writeStruct('>B', 1, (self.TC_OBJECT,))
        self._writeStruct('>B', 1, (self.TC_CLASSDESC,))