# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/data_unpacker.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import array, binascii, struct, traceback
from pyogp.lib.base.exc import *
from pyogp.lib.base.datatypes import *
from msgtypes import MsgType, EndianType, sizeof

class DataUnpacker(object):
    __module__ = __name__

    def __init__(self):
        self.unpacker = {}
        self.unpacker[MsgType.MVT_FIXED] = ('<', self.__unpack_fixed)
        self.unpacker[MsgType.MVT_VARIABLE] = ('>', self.__unpack_string)
        self.unpacker[MsgType.MVT_S8] = ('>', 'b')
        self.unpacker[MsgType.MVT_U8] = ('>', 'B')
        self.unpacker[MsgType.MVT_BOOL] = ('>', 'B')
        self.unpacker[MsgType.MVT_LLUUID] = ('>', self.__unpack_uuid)
        self.unpacker[MsgType.MVT_IP_ADDR] = ('>', self.__unpack_string)
        self.unpacker[MsgType.MVT_IP_PORT] = ('>', 'H')
        self.unpacker[MsgType.MVT_U16] = ('<', 'H')
        self.unpacker[MsgType.MVT_U32] = ('<', 'I')
        self.unpacker[MsgType.MVT_U64] = ('<', 'Q')
        self.unpacker[MsgType.MVT_S16] = ('<', 'h')
        self.unpacker[MsgType.MVT_S32] = ('<', 'i')
        self.unpacker[MsgType.MVT_S64] = ('<', 'q')
        self.unpacker[MsgType.MVT_F32] = ('<', 'f')
        self.unpacker[MsgType.MVT_F64] = ('<', 'd')
        self.unpacker[MsgType.MVT_LLVector3] = ('<', self.__unpack_vector3)
        self.unpacker[MsgType.MVT_LLVector3d] = ('<', self.__unpack_vector3d)
        self.unpacker[MsgType.MVT_LLVector4] = ('<', self.__unpack_vector4)
        self.unpacker[MsgType.MVT_LLQuaternion] = ('<', self.__unpack_quat)

    def unpack_data(self, data, data_type, start_index=-1, var_size=-1, endian_type=EndianType.NONE):
        if start_index != -1:
            if var_size != -1:
                data = data[start_index:start_index + var_size]
            else:
                data = data[start_index:start_index + sizeof(data_type)]
        if data_type in self.unpacker:
            unpack_tup = self.unpacker[data_type]
            endian = unpack_tup[0]
            if endian_type != EndianType.NONE:
                endian = endian_type
            unpack = unpack_tup[1]
            if callable(unpack):
                try:
                    return unpack(endian, data, var_size)
                except struct.error, error:
                    traceback.print_exc()
                    raise DataUnpackingError(data, error)

            else:
                try:
                    return struct.unpack(endian + unpack, data)[0]
                except struct.error, error:
                    traceback.print_exc()
                    raise DataUnpackingError(data, error)

        return

    def __unpack_tuple(self, endian, tup, tp, var_size=None):
        size = len(tup) / struct.calcsize(tp)
        return struct.unpack(endian + str(size) + tp, tup)

    def __unpack_vector3(self, endian, vec, var_size=None):
        return Vector3(vec, 0)

    def __unpack_vector3d(self, endian, vec, var_size=None):
        return self.__unpack_tuple(endian, vec, 'd')

    def __unpack_vector4(self, endian, vec, var_size=None):
        return self.__unpack_tuple(endian, vec, 'f')

    def __unpack_quat(self, endian, quat, var_size=None):
        return Quaternion(quat, 0)

    def __unpack_uuid(self, endian, uuid_data, var_size=None):
        return UUID(bytes=uuid_data, offset=0)

    def __unpack_string(self, endian, pack_string, var_size):
        return pack_string

    def __unpack_fixed(self, endian, data, var_size):
        return data