# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/gpapidl/utils.py
# Compiled at: 2020-04-21 12:12:34
# Size of source mod 2**32: 1866 bytes
import struct, sys
from google.protobuf.message import Message
from google.protobuf.json_format import MessageToDict
from . import googleplay_pb2

def parseProtobufObj(obj):
    return MessageToDict(obj, False, False, False)


def readInt(byteArray, start):
    """Read the byte array, starting from *start* position,
    as an 32-bit unsigned integer"""
    return struct.unpack('!L', byteArray[start:][0:4])[0]


def toBigInt(byteArray):
    """Convert the byte array to a BigInteger"""
    array = byteArray[::-1]
    out = 0
    for key, value in enumerate(array):
        decoded = struct.unpack('B', bytes([value]))[0]
        out = out | decoded << key * 8

    return out


def hasPrefetch(obj):
    try:
        return len(obj.preFetch) > 0
    except ValueError:
        return False


def hasListResponse(obj):
    try:
        return obj.HasField('listResponse')
    except ValueError:
        return False


def hasSearchResponse(obj):
    try:
        return obj.HasField('searchResponse')
    except ValueError:
        return False


def hasCluster(obj):
    try:
        return obj.HasField('cluster')
    except ValueError:
        return False


def hasTosContent(tocResponse):
    try:
        return tocResponse.HasField('tosContent')
    except ValueError:
        return False


def hasTosToken(tocResponse):
    try:
        return tocResponse.HasField('tosToken')
    except ValueError:
        return False


def hasCookie(tocResponse):
    try:
        return tocResponse.HasField('cookie')
    except ValueError:
        return False


def hasDoc(obj):
    try:
        existance = obj.HasField('doc')
    except ValueError:
        try:
            existance = len(obj.doc) > 0
        except TypeError:
            existance = False

    return existance