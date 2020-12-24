# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/util/bplist.py
# Compiled at: 2019-02-24 18:45:28
__doc__ = '\nhttp://github.com/farcaller/bplist-python/blob/master/bplist.py\n'
import struct, plistlib
from datetime import datetime, timedelta

class BPListWriter(object):

    def __init__(self, objects):
        self.bplist = ''
        self.objects = objects

    def binary(self):
        """binary -> string

        Generates bplist
        """
        self.data = 'bplist00'
        return self.data

    def write(self, filename):
        """

        Writes bplist to file
        """
        if self.bplist != '':
            pass
        else:
            raise Exception('BPlist not yet generated')


class BPlistReader(object):

    def __init__(self, s):
        self.data = s
        self.objects = []
        self.resolved = {}

    def __unpackIntStruct(self, sz, s):
        """__unpackIntStruct(size, string) -> int

        Unpacks the integer of given size (1, 2 or 4 bytes) from string
        """
        if sz == 1:
            ot = '!B'
        elif sz == 2:
            ot = '!H'
        elif sz == 4:
            ot = '!I'
        elif sz == 8:
            ot = '!Q'
        else:
            raise Exception('int unpack size ' + str(sz) + ' unsupported')
        return struct.unpack(ot, s)[0]

    def __unpackInt(self, offset):
        """__unpackInt(offset) -> int

        Unpacks int field from plist at given offset
        """
        return self.__unpackIntMeta(offset)[1]

    def __unpackIntMeta(self, offset):
        """__unpackIntMeta(offset) -> (size, int)

        Unpacks int field from plist at given offset and returns its size and value
        """
        obj_header = struct.unpack('!B', self.data[offset])[0]
        obj_type, obj_info = obj_header & 240, obj_header & 15
        int_sz = 2 ** obj_info
        return (
         int_sz, self.__unpackIntStruct(int_sz, self.data[offset + 1:offset + 1 + int_sz]))

    def __resolveIntSize(self, obj_info, offset):
        """__resolveIntSize(obj_info, offset) -> (count, offset)

        Calculates count of objref* array entries and returns count and offset to first element
        """
        if obj_info == 15:
            ofs, obj_count = self.__unpackIntMeta(offset + 1)
            objref = offset + 2 + ofs
        else:
            obj_count = obj_info
            objref = offset + 1
        return (obj_count, objref)

    def __unpackFloatStruct(self, sz, s):
        """__unpackFloatStruct(size, string) -> float

        Unpacks the float of given size (4 or 8 bytes) from string
        """
        if sz == 4:
            ot = '!f'
        elif sz == 8:
            ot = '!d'
        else:
            raise Exception('float unpack size ' + str(sz) + ' unsupported')
        return struct.unpack(ot, s)[0]

    def __unpackFloat(self, offset):
        """__unpackFloat(offset) -> float

        Unpacks float field from plist at given offset
        """
        obj_header = struct.unpack('!B', self.data[offset])[0]
        obj_type, obj_info = obj_header & 240, obj_header & 15
        int_sz = 2 ** obj_info
        return (
         int_sz, self.__unpackFloatStruct(int_sz, self.data[offset + 1:offset + 1 + int_sz]))

    def __unpackDate(self, offset):
        td = int(struct.unpack('>d', self.data[offset + 1:offset + 9])[0])
        return datetime(year=2001, month=1, day=1) + timedelta(seconds=td)

    def __unpackItem(self, offset):
        """__unpackItem(offset)

        Unpacks and returns an item from plist
        """
        obj_header = struct.unpack('!B', self.data[offset])[0]
        obj_type, obj_info = obj_header & 240, obj_header & 15
        if obj_type == 0:
            if obj_info == 0:
                return
            if obj_info == 8:
                return False
            if obj_info == 9:
                return True
            if obj_info == 15:
                raise Exception('0x0F Not Implemented')
            else:
                raise Exception('unpack item type ' + str(obj_header) + ' at ' + str(offset) + 'failed')
        elif obj_type == 16:
            return self.__unpackInt(offset)
        if obj_type == 32:
            return self.__unpackFloat(offset)
        else:
            if obj_type == 48:
                return self.__unpackDate(offset)
            if obj_type == 64:
                obj_count, objref = self.__resolveIntSize(obj_info, offset)
                return plistlib.Data(self.data[objref:objref + obj_count])
            if obj_type == 80:
                obj_count, objref = self.__resolveIntSize(obj_info, offset)
                return self.data[objref:objref + obj_count]
            if obj_type == 96:
                obj_count, objref = self.__resolveIntSize(obj_info, offset)
                return self.data[objref:objref + obj_count * 2].decode('utf-16be')
            if obj_type == 128:
                obj_count, objref = self.__resolveIntSize(obj_info, offset)
                return plistlib.Data(self.data[objref:objref + obj_count])
            if obj_type == 160:
                obj_count, objref = self.__resolveIntSize(obj_info, offset)
                arr = []
                for i in range(obj_count):
                    arr.append(self.__unpackIntStruct(self.object_ref_size, self.data[objref + i * self.object_ref_size:objref + i * self.object_ref_size + self.object_ref_size]))

                return arr
            if obj_type == 192:
                raise Exception('0xC0 Not Implemented')
            else:
                if obj_type == 208:
                    obj_count, objref = self.__resolveIntSize(obj_info, offset)
                    keys = []
                    for i in range(obj_count):
                        keys.append(self.__unpackIntStruct(self.object_ref_size, self.data[objref + i * self.object_ref_size:objref + i * self.object_ref_size + self.object_ref_size]))

                    values = []
                    objref += obj_count * self.object_ref_size
                    for i in range(obj_count):
                        values.append(self.__unpackIntStruct(self.object_ref_size, self.data[objref + i * self.object_ref_size:objref + i * self.object_ref_size + self.object_ref_size]))

                    dic = {}
                    for i in range(obj_count):
                        dic[keys[i]] = values[i]

                    return dic
                raise Exception("don't know how to unpack obj type " + hex(obj_type) + ' at ' + str(offset))
            return

    def __resolveObject(self, idx):
        try:
            return self.resolved[idx]
        except KeyError:
            obj = self.objects[idx]
            if type(obj) == list:
                newArr = []
                for i in obj:
                    newArr.append(self.__resolveObject(i))

                self.resolved[idx] = newArr
                return newArr
            if type(obj) == dict:
                newDic = {}
                for k, v in obj.iteritems():
                    rk = self.__resolveObject(k)
                    rv = self.__resolveObject(v)
                    newDic[rk] = rv

                self.resolved[idx] = newDic
                return newDic
            self.resolved[idx] = obj
            return obj

    def parse(self):
        if self.data[:8] != 'bplist00':
            raise Exception('Bad magic')
        self.offset_size, self.object_ref_size, self.number_of_objects, self.top_object, self.table_offset = struct.unpack('!6xBB4xI4xI4xI', self.data[-32:])
        self.offset_table = self.data[self.table_offset:-32]
        self.offsets = []
        ot = self.offset_table
        for i in xrange(self.number_of_objects):
            offset_entry = ot[:self.offset_size]
            ot = ot[self.offset_size:]
            self.offsets.append(self.__unpackIntStruct(self.offset_size, offset_entry))

        self.objects = []
        k = 0
        for i in self.offsets:
            obj = self.__unpackItem(i)
            k += 1
            self.objects.append(obj)

        return self.__resolveObject(self.top_object)

    @classmethod
    def plistWithString(cls, s):
        parser = cls(s)
        return parser.parse()

    @classmethod
    def plistWithFile(cls, f):
        file = open(f, 'rb')
        parser = cls(file.read())
        file.close()
        return parser.parse()