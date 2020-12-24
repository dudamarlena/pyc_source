# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cstruct/__init__.py
# Compiled at: 2018-10-30 18:12:03
__doc__ = 'C-style structs for Python\n\nConvert C struct definitions into Python classes with methods for\nserializing/deserializing.\nThe usage is very simple: create a class subclassing cstruct.CStruct\nand add a C struct definition as a string in the __struct__ field.\nThe C struct definition is parsed at runtime and the struct format string\nis generated. The class offers the method "unpack" for deserializing\na string of bytes into a Python object and the method "pack" for\nserializing the values into a string.\n\nExample:\nThe following program reads the DOS partition information from a disk.\n\n#!/usr/bin/python\nimport cstruct\n\nclass Position(cstruct.CStruct):\n    __byte_order__ = cstruct.LITTLE_ENDIAN\n    __struct__ = """\n        unsigned char head;\n        unsigned char sector;\n        unsigned char cyl;\n    """\n\nclass Partition(cstruct.CStruct):\n    __byte_order__ = cstruct.LITTLE_ENDIAN\n    __struct__ = """\n        unsigned char status;       /* 0x80 - active */\n        struct Position start;\n        unsigned char partition_type;\n        struct Position end;\n        unsigned int start_sect;    /* starting sector counting from 0 */\n        unsigned int sectors;       /* nr of sectors in partition */\n    """\n\n    def print_info(self):\n        print("bootable: %s" % ((self.status & 0x80) and "Y" or "N"))\n        print("partition_type: %02X" % self.partition_type)\n        print("start: head: %X sectory: %X cyl: %X" % (self.start.head, self.start.sector, self.start.cyl))\n        print("end: head: %X sectory: %X cyl: %X" % (self.end.head, self.end.sector, self.end.cyl))\n        print("starting sector: %08X" % self.start_sect)\n        print("size MB: %s" % (self.sectors / 2 / 1024))\n\nclass MBR(cstruct.CStruct):\n    __byte_order__ = cstruct.LITTLE_ENDIAN\n    __struct__ = """\n        char unused[440];\n        unsigned char disk_signature[4];\n        unsigned char usualy_nulls[2];\n        struct Partition partitions[4];\n        char signature[2];\n    """\n\n    def print_info(self):\n        print("disk signature: %s" % "".join(["%02X" % x for x in self.disk_signature]))\n        print("usualy nulls: %s" % "".join(["%02X" % x for x in self.usualy_nulls]))\n        for i, partition in enumerate(self.partitions):\n            print("")\n            print("partition: %s" % i)\n            partition.print_info()\n\ndisk = "mbr"\nf = open(disk, "rb")\nmbr = MBR()\ndata = f.read(len(mbr))\nmbr.unpack(data)\nmbr.print_info()\nf.close()\n\n'
__author__ = 'Andrea Bonomi <andrea.bonomi@gmail.com>'
__license__ = 'MIT'
__version__ = '1.8'
__date__ = '15 August 2013'
import re, struct, sys
__all__ = [
 'LITTLE_ENDIAN',
 'BIG_ENDIAN',
 'CStruct',
 'define',
 'typedef']
LITTLE_ENDIAN = '<'
BIG_ENDIAN = '>'
C_TYPE_TO_FORMAT = {'char': 's', 
   'signed char': 'b', 
   'unsigned char': 'B', 
   'short': 'h', 
   'short int': 'h', 
   'ushort': 'H', 
   'unsigned short': 'H', 
   'unsigned short int': 'H', 
   'int': 'i', 
   'unsigned int': 'I', 
   'long': 'l', 
   'long int': 'l', 
   'unsigned long': 'L', 
   'unsigned long int': 'L', 
   'long long': 'q', 
   'unsigned long long': 'Q', 
   'float': 'f', 
   'double': 'd', 
   'void *': 'P', 
   'int8': 'b', 
   'int8_t': 'b', 
   'uint8': 'B', 
   'uint8_t': 'B', 
   'int16': 'h', 
   'int16_t': 'h', 
   'uint16': 'H', 
   'uint16_t': 'H', 
   'int32': 'i', 
   'int32_t': 'i', 
   'uint32': 'I', 
   'uint32_t': 'I', 
   'int64': 'q', 
   'int64_t': 'q', 
   'uint64': 'Q', 
   'uint64_t': 'Q'}
STRUCTS = {}
DEFINES = {}
TYPEDEFS = {}

def define(key, value):
    """
    Add a definition that can be used in the C struct
    """
    DEFINES[key] = value


def typedef(type_, alias):
    """
    Define an alias for a data type
    """
    TYPEDEFS[alias] = type_


class CStructMeta(type):

    def __new__(mcs, name, bases, dict):
        __struct__ = dict.get('__struct__', None)
        if __struct__ is not None:
            dict['__fmt__'], dict['__fields__'], dict['__fields_types__'] = mcs.parse_struct(__struct__)
            if '__byte_order__' in dict:
                dict['__fmt__'] = dict['__byte_order__'] + dict['__fmt__']
            for field in dict['__fields__']:
                if field not in dict:
                    dict[field] = None

            dict['__size__'] = struct.calcsize(dict['__fmt__'])
        new_class = type.__new__(mcs, name, bases, dict)
        if __struct__ is not None:
            STRUCTS[name] = new_class
        return new_class

    @staticmethod
    def parse_struct(st):
        fmt = []
        fields = []
        fields_types = {}
        st = st.replace('*/', '*/\n')
        st = ('  ').join(re.split('/\\*.*\\*/', st))
        st = ('\n').join([ s.split('//')[0] for s in st.split('\n') ])
        st = st.replace('\n', ' ')
        for line_s in st.split(';'):
            line_s = line_s.strip()
            if line_s:
                line = line_s.split()
                if len(line) < 2:
                    raise Exception('Error parsing: ' + line_s)
                vtype = line[0].strip()
                if vtype == 'unsigned' or vtype == 'signed' or vtype == 'struct' and len(line) > 2:
                    vtype = vtype + ' ' + line[1].strip()
                    del line[0]
                vname = line[1]
                if vname == 'int' or vname == 'long':
                    vtype = vtype + ' ' + vname
                    del line[0]
                    vname = line[1]
                if vname.startswith('*'):
                    vname = vname[1:]
                    vtype = 'void *'
                vlen = 1
                if '[' in vname:
                    t = vname.split('[')
                    if len(t) != 2:
                        raise Exception('Error parsing: ' + line_s)
                    vname = t[0].strip()
                    vlen = t[1]
                    vlen = vlen.split(']')[0].strip()
                    try:
                        vlen = int(vlen)
                    except:
                        vlen = DEFINES.get(vlen, None)
                        if vlen is None:
                            raise
                        else:
                            vlen = int(vlen)

                while vtype in TYPEDEFS:
                    vtype = TYPEDEFS[vtype]

                if vtype.startswith('struct '):
                    vtype = vtype[7:]
                    t = STRUCTS.get(vtype, None)
                    if t is None:
                        raise Exception('Unknow struct "' + vtype + '"')
                    vtype = t
                    ttype = 'c'
                    vlen = vtype.size * vlen
                else:
                    ttype = C_TYPE_TO_FORMAT.get(vtype, None)
                    if ttype is None:
                        raise Exception('Unknow type "' + vtype + '"')
                fields.append(vname)
                fields_types[vname] = (vtype, vlen)
                if vlen > 1:
                    fmt.append(str(vlen))
                fmt.append(ttype)

        fmt = ('').join(fmt)
        return (
         fmt, fields, fields_types)

    def __len__(cls):
        return cls.__size__

    @property
    def size(cls):
        """ Structure size (in bytes) """
        return cls.__size__


_CStructParent = CStructMeta('_CStructParent', (object,), {})
if sys.version_info < (2, 6):
    EMPTY_BYTES_STRING = str()
    CHAR_ZERO = '\x00'
elif sys.version_info < (3, 0):
    EMPTY_BYTES_STRING = bytes()
    CHAR_ZERO = bytes('\x00')
else:
    EMPTY_BYTES_STRING = bytes()
    CHAR_ZERO = bytes('\x00', 'ascii')

class CStruct(_CStructParent):
    """
    Convert C struct definitions into Python classes.

    __struct__ = definition of the struct in C syntax
    __byte_order__ = (optional) valid values are LITTLE_ENDIAN and BIG_ENDIAN

    The following fields are generated from the C struct definition
    __fmt__ = struct format string
    __size__ = lenght of the structure in bytes
    __fields__ = list of structure fields
    __fields_types__ = dictionary mapping field names to types
    Every fields defined in the structure is added to the class

    """

    def __init__(self, string=None, **kargs):
        if string is not None:
            self.unpack(string)
        else:
            try:
                self.unpack(string)
            except:
                pass

            for key, value in kargs.items():
                setattr(self, key, value)

        return

    def unpack(self, string):
        """
        Unpack the string containing packed C structure data
        """
        if string is None:
            string = CHAR_ZERO * self.__size__
        data = struct.unpack(self.__fmt__, string)
        i = 0
        for field in self.__fields__:
            vtype, vlen = self.__fields_types__[field]
            if vtype == 'char':
                setattr(self, field, data[i])
                i = i + 1
            elif isinstance(vtype, CStructMeta):
                num = int(vlen / vtype.size)
                if num == 1:
                    sub_struct = vtype()
                    sub_struct.unpack(EMPTY_BYTES_STRING.join(data[i:i + sub_struct.size]))
                    setattr(self, field, sub_struct)
                    i = i + sub_struct.size
                else:
                    sub_structs = []
                    for j in range(0, num):
                        sub_struct = vtype()
                        sub_struct.unpack(EMPTY_BYTES_STRING.join(data[i:i + sub_struct.size]))
                        i = i + sub_struct.size
                        sub_structs.append(sub_struct)

                    setattr(self, field, sub_structs)
            elif vlen == 1:
                setattr(self, field, data[i])
                i = i + vlen
            else:
                setattr(self, field, list(data[i:i + vlen]))
                i = i + vlen

        return

    def pack(self):
        """
        Pack the structure data into a string
        """
        data = []
        for field in self.__fields__:
            vtype, vlen = self.__fields_types__[field]
            if vtype == 'char':
                data.append(getattr(self, field))
            elif isinstance(vtype, CStructMeta):
                num = int(vlen / vtype.size)
                if num == 1:
                    v = getattr(self, field, vtype())
                    v = v.pack()
                    if sys.version_info >= (3, 0):
                        v = [ bytes([x]) for x in v ]
                    data.extend(v)
                else:
                    values = getattr(self, field, [])
                    for j in range(0, num):
                        try:
                            v = values[j]
                        except:
                            v = vtype()

                        v = v.pack()
                        if sys.version_info >= (3, 0):
                            v = [ bytes([x]) for x in v ]
                        data.extend(v)

            elif vlen == 1:
                data.append(getattr(self, field))
            else:
                v = getattr(self, field)
                v = v[:vlen] + [0] * (vlen - len(v))
                data.extend(v)

        return struct.pack(self.__fmt__, *data)

    def clear(self):
        self.unpack(None)
        return

    def __len__(self):
        """ Structure size (in bytes) """
        return self.__size__

    @property
    def size(self):
        """ Structure size (in bytes) """
        return self.__size__

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        result = []
        for field in self.__fields__:
            result.append(field + '=' + str(getattr(self, field, None)))

        return type(self).__name__ + '(' + (', ').join(result) + ')'

    def __repr__(self):
        return self.__str__()