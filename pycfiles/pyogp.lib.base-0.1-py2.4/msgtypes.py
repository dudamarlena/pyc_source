# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/msgtypes.py
# Compiled at: 2010-02-07 17:28:31
"""
Contributors can be viewed at:
http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt 

$LicenseInfo:firstyear=2008&license=apachev2$

Copyright 2009, Linden Research, Inc.

Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0
or in 
    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt

$/LicenseInfo$
"""

class PacketLayout(object):
    __module__ = __name__
    PACKET_ID_LENGTH = 6
    PHL_FLAGS = 0
    PHL_PACKET_ID = 1
    PHL_OFFSET = 5
    PHL_NAME = 6
    MINIMUM_VALID_PACKET_SIZE = PACKET_ID_LENGTH + 1


class EndianType(object):
    __module__ = __name__
    LITTLE = '<'
    BIG = '>'
    NETWORK = '!'
    NONE = ''


class MsgBlockType(object):
    __module__ = __name__
    (MBT_SINGLE, MBT_MULTIPLE, MBT_VARIABLE) = range(3)
    MBT_String_List = [
     'Single', 'Multiple', 'Variable']

    @classmethod
    def MBT_as_string(cls, typenum):
        if typenum == None:
            return 'None'
        return cls.MBT_String_List[typenum]


class PackFlags(object):
    __module__ = __name__
    LL_ZERO_CODE_FLAG = 128
    LL_RELIABLE_FLAG = 64
    LL_RESENT_FLAG = 32
    LL_ACK_FLAG = 16
    LL_NONE = 0


class MsgFrequency(object):
    __module__ = __name__
    FIXED_FREQUENCY_MESSAGE = -1
    LOW_FREQUENCY_MESSAGE = 4
    MEDIUM_FREQUENCY_MESSAGE = 2
    HIGH_FREQUENCY_MESSAGE = 1


class MsgTrust(object):
    __module__ = __name__
    (LL_TRUSTED, LL_NOTRUST) = range(2)


class MsgEncoding(object):
    __module__ = __name__
    (LL_UNENCODED, LL_ZEROCODED) = range(2)


class MsgDeprecation(object):
    __module__ = __name__
    (LL_DEPRECATED, LL_UDPDEPRECATED, LL_UDPBLACKLISTED, LL_NOTDEPRECATED) = range(4)


class MsgType(object):
    __module__ = __name__
    (MVT_FIXED, MVT_VARIABLE, MVT_U8, MVT_U16, MVT_U32, MVT_U64, MVT_S8, MVT_S16, MVT_S32, MVT_S64, MVT_F32, MVT_F64, MVT_LLVector3, MVT_LLVector3d, MVT_LLVector4, MVT_LLQuaternion, MVT_LLUUID, MVT_BOOL, MVT_IP_ADDR, MVT_IP_PORT) = range(20)
    MVT_String_List = [
     'MVT_FIXED', 'MVT_VARIABLE', 'MVT_U8', 'MVT_U16', 'MVT_U32', 'MVT_U64', 'MVT_S8', 'MVT_S16', 'MVT_S32', 'MVT_S64', 'MVT_F32', 'MVT_F64', 'MVT_LLVector3', 'MVT_LLVector3d', 'MVT_LLVector4', 'MVT_LLQuaternion', 'MVT_LLUUID', 'MVT_BOOL', 'MVT_IP_ADDR', 'MVT_IP_PORT']

    @classmethod
    def MVT_as_string(cls, typenum):
        return cls.MVT_String_List[typenum]


def sizeof(var):
    if var == MsgType.MVT_FIXED:
        return -1
    elif var == MsgType.MVT_VARIABLE:
        return -1
    elif var == MsgType.MVT_U8:
        return 1
    elif var == MsgType.MVT_U16:
        return 2
    elif var == MsgType.MVT_U32:
        return 4
    elif var == MsgType.MVT_U64:
        return 8
    elif var == MsgType.MVT_S8:
        return 1
    elif var == MsgType.MVT_S16:
        return 2
    elif var == MsgType.MVT_S32:
        return 4
    elif var == MsgType.MVT_S64:
        return 8
    elif var == MsgType.MVT_F32:
        return 4
    elif var == MsgType.MVT_F64:
        return 8
    elif var == MsgType.MVT_LLVector3:
        return 12
    elif var == MsgType.MVT_LLVector3d:
        return 24
    elif var == MsgType.MVT_LLVector4:
        return 16
    elif var == MsgType.MVT_LLQuaternion:
        return 12
    elif var == MsgType.MVT_LLUUID:
        return 16
    elif var == MsgType.MVT_BOOL:
        return 1
    elif var == MsgType.MVT_IP_ADDR:
        return 4
    elif var == MsgType.MVT_IP_PORT:
        return 2