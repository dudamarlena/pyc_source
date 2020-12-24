# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pysfm\api\uf_error.py
# Compiled at: 2018-03-02 03:00:04
from pysfm.core.error import *

def UF_GetErrorCode(retCode):
    if retCode is UF_PROTO_RET_SCAN_FAIL:
        return UF_ERR_SCAN_FAIL
    else:
        if retCode is UF_PROTO_RET_NOT_FOUND:
            return UF_ERR_NOT_FOUND
        if retCode is UF_PROTO_RET_NOT_MATCH:
            return UF_ERR_NOT_MATCH
        if retCode is UF_PROTO_RET_TRY_AGAIN:
            return UF_ERR_TRY_AGAIN
        if retCode is UF_PROTO_RET_TIME_OUT:
            return UF_ERR_TIME_OUT
        if retCode is UF_PROTO_RET_MEM_FULL:
            return UF_ERR_MEM_FULL
        if retCode is UF_PROTO_RET_EXIST_ID:
            return UF_ERR_EXIST_ID
        if retCode is UF_PROTO_RET_FINGER_LIMIT:
            return UF_ERR_FINGER_LIMIT
        if retCode is UF_PROTO_RET_UNSUPPORTED:
            return UF_ERR_UNSUPPORTED
        if retCode is UF_PROTO_RET_INVALID_ID:
            return UF_ERR_INVALID_ID
        if retCode is UF_PROTO_RET_TIMEOUT_MATCH:
            return UF_ERR_TIMEOUT_MATCH
        if retCode is UF_PROTO_RET_BUSY:
            return UF_ERR_BUSY
        if retCode is UF_PROTO_RET_CANCELED:
            return UF_ERR_CANCELED
        if retCode is UF_PROTO_RET_DATA_ERROR:
            return UF_ERR_DATA_ERROR
        if retCode is UF_PROTO_RET_EXIST_FINGER:
            return UF_ERR_EXIST_FINGER
        if retCode is UF_PROTO_RET_DURESS_FINGER:
            return UF_ERR_DURESS_FINGER
        if retCode is UF_PROTO_RET_CARD_ERROR:
            return UF_ERR_CARD_ERROR
        if retCode is UF_PROTO_RET_LOCKED:
            return UF_ERR_LOCKED
        if retCode is UF_PROTO_RET_ACCESS_NOT_GRANTED:
            return UF_ERR_ACCESS_NOT_GRANTED
        if retCode is UF_PROTO_RET_EXCEED_ENTRANCE_LIMIT:
            return UF_ERR_EXCEED_ENTRANCE_LIMIT
        if retCode is UF_PROTO_RET_REJECTED_ID:
            return UF_ERR_REJECTED_ID
        if retCode is UF_PROTO_FAKE_DETECTED:
            return UF_ERR_FAKE_DETECTED
        if retCode is UF_PROTO_RET_RECOVERY_MODE:
            return UF_ERR_RECOVERY_MODE
        if retCode is UF_PROTO_RET_NO_SERIAL_NUMBER:
            return UF_ERR_NO_SERIAL_NUMBER
        return UF_ERR_UNKNOWN


if __name__ == '__main__':
    print UF_GetErrorCode(100)