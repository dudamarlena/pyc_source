# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/rtorrent/lib/bencode.py
# Compiled at: 2012-04-10 18:00:40
import sys
_py3 = sys.version_info[0] == 3
if _py3:
    _VALID_STRING_TYPES = (str,)
else:
    _VALID_STRING_TYPES = (
     str, unicode)
_TYPE_INT = 1
_TYPE_STRING = 2
_TYPE_LIST = 3
_TYPE_DICTIONARY = 4
_TYPE_END = 5
_TYPE_INVALID = 6

def _gettype(char):
    if not isinstance(char, int):
        char = ord(char)
    if char == 108:
        return _TYPE_LIST
    else:
        if char == 100:
            return _TYPE_DICTIONARY
        if char == 105:
            return _TYPE_INT
        if char == 101:
            return _TYPE_END
        if char >= 48 and char <= 57:
            return _TYPE_STRING
        return _TYPE_INVALID


def _decode_string(data):
    end = 1
    if _py3:
        char = 58
    else:
        char = chr(58)
    while data[end] != char:
        end = end + 1

    strlen = int(data[:end])
    return (data[end + 1:strlen + end + 1], data[strlen + end + 1:])


def _decode_int(data):
    end = 1
    if _py3:
        char = 101
    else:
        char = chr(101)
    while data[end] != char:
        end = end + 1

    return (
     int(data[1:end]), data[end + 1:])


def _decode_list(data):
    x = []
    overflow = data[1:]
    while True:
        if _gettype(overflow[0]) == _TYPE_END:
            return (x, overflow[1:])
        (value, overflow) = _decode(overflow)
        if isinstance(value, bool) or overflow == '':
            return (False, False)
        x.append(value)


def _decode_dict(data):
    x = {}
    overflow = data[1:]
    while True:
        if _gettype(overflow[0]) != _TYPE_STRING:
            return (False, False)
        (key, overflow) = _decode(overflow)
        if key == False or overflow == '':
            return (False, False)
        (value, overflow) = _decode(overflow)
        if isinstance(value, bool) or overflow == '':
            print 'Error parsing value'
            print value
            print overflow
            return (
             False, False)
        key = key.decode()
        x[key] = value
        if _gettype(overflow[0]) == _TYPE_END:
            return (x, overflow[1:])


def _decode(data):
    btype = _gettype(data[0])
    if btype == _TYPE_INT:
        return _decode_int(data)
    else:
        if btype == _TYPE_STRING:
            return _decode_string(data)
        if btype == _TYPE_LIST:
            return _decode_list(data)
        if btype == _TYPE_DICTIONARY:
            return _decode_dict(data)
        return (False, False)


def decode(data):
    (decoded, overflow) = _decode(data)
    return decoded


def _encode_int(data):
    return 'i' + str(data).encode() + 'e'


def _encode_string(data):
    return str(len(data)).encode() + ':' + data


def _encode_list(data):
    elist = 'l'
    for item in data:
        eitem = encode(item)
        if eitem == False:
            return False
        elist += eitem

    return elist + 'e'


def _encode_dict(data):
    edict = 'd'
    keys = []
    for key in data:
        if not isinstance(key, _VALID_STRING_TYPES) and not isinstance(key, bytes):
            return False
        keys.append(key)

    keys.sort()
    for key in keys:
        ekey = encode(key)
        eitem = encode(data[key])
        if ekey == False or eitem == False:
            return False
        edict += ekey + eitem

    return edict + 'e'


def encode(data):
    if isinstance(data, bool):
        return False
    else:
        if isinstance(data, int):
            return _encode_int(data)
        if isinstance(data, bytes):
            return _encode_string(data)
        if isinstance(data, _VALID_STRING_TYPES):
            return _encode_string(data.encode())
        if isinstance(data, list):
            return _encode_list(data)
        if isinstance(data, dict):
            return _encode_dict(data)
        return False