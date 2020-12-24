# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/data_packer.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import struct
from pyogp.lib.base.datatypes import UUID, Vector3, Quaternion
from msgtypes import MsgType, EndianType
from pyogp.lib.base.helpers import Helpers

class DataPacker(object):
    __module__ = __name__

    def __init__(self):
        self.packer = {}
        self.packer[MsgType.MVT_FIXED] = ('>', self.__pack_string)
        self.packer[MsgType.MVT_VARIABLE] = ('>', self.__pack_string)
        self.packer[MsgType.MVT_S8] = ('>', 'b')
        self.packer[MsgType.MVT_U8] = ('>', 'B')
        self.packer[MsgType.MVT_BOOL] = ('>', 'B')
        self.packer[MsgType.MVT_LLUUID] = ('>', self.__pack_uuid)
        self.packer[MsgType.MVT_IP_ADDR] = ('>', self.__pack_string)
        self.packer[MsgType.MVT_IP_PORT] = ('>', 'H')
        self.packer[MsgType.MVT_U16] = ('<', 'H')
        self.packer[MsgType.MVT_U32] = ('<', 'I')
        self.packer[MsgType.MVT_U64] = ('<', 'Q')
        self.packer[MsgType.MVT_S16] = ('<', 'h')
        self.packer[MsgType.MVT_S32] = ('<', 'i')
        self.packer[MsgType.MVT_S64] = ('<', 'q')
        self.packer[MsgType.MVT_F32] = ('<', 'f')
        self.packer[MsgType.MVT_F64] = ('<', 'd')
        self.packer[MsgType.MVT_LLVector3] = ('<', self.__pack_vector3)
        self.packer[MsgType.MVT_LLVector3d] = ('<', self.__pack_vector3d)
        self.packer[MsgType.MVT_LLVector4] = ('<', self.__pack_vector4)
        self.packer[MsgType.MVT_LLQuaternion] = ('<', self.__pack_quat)

    def pack_data(self, data, data_type, endian_type=EndianType.NONE):
        if data_type in self.packer:
            (endian, pack) = self.packer[data_type]
            if endian_type != EndianType.NONE:
                endian = endian_type
            if callable(pack):
                return pack(endian, data)
            else:
                return struct.pack(endian + pack, data)
        return

    def __pack_tuple(self, endian, tup, tp):
        size = len(tup)
        return struct.pack((endian + str(size) + tp), *tup)

    def __pack_vector3(self, endian, vec):
        if isinstance(vec, Vector3):
            vec = vec()
        return self.__pack_tuple(endian, vec, 'f')

    def __pack_vector3d(self, endian, vec):
        return self.__pack_tuple(endian, vec, 'd')

    def __pack_vector4(self, endian, vec):
        return self.__pack_tuple(endian, vec, 'f')

    def __pack_quat(self, endian, quat):
        if isinstance(quat, Quaternion):
            quat = quat()
        vec = Helpers.pack_quaternion_to_vector3(quat)
        return self.__pack_tuple(endian, vec, 'f')

    def __pack_uuid(self, endian, uuid):
        if isinstance(uuid, UUID):
            return uuid.get_bytes()
        else:
            return uuid.bytes

    def __pack_string(self, endian, pack_string):
        """Return the string UTF-8 encoded and null terminated."""
        if pack_string == None:
            return '\x00'
        elif isinstance(pack_string, unicode):
            return pack_string.encode('utf-8') + '\x00'
        else:
            return pack_string + '\x00'
        return