# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\client\bsn_enum.py
# Compiled at: 2020-04-20 02:55:22
# Size of source mod 2**32: 585 bytes
from enum import IntEnum

class AppAlgorithmType(IntEnum):
    __doc__ = '\n    应用秘钥类型\n    '
    AppAlgorithmType_Not = 0
    AppAlgorithmType_SM2 = 1
    AppAlgorithmType_R1 = 2
    AppAlgorithmType_K1 = 3


class AppCaType(IntEnum):
    __doc__ = '\n    应用秘钥托管类型\n    '
    AppCaType_Not = 0
    AppCaType_Trust = 1
    AppCaType_NoTrust = 2


class ResCode(IntEnum):
    __doc__ = '\n       应用秘钥托管类型\n       '
    ResCode_Suc = 0
    ResCode_Fail = -1