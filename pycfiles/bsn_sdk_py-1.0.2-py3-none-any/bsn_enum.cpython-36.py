# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\client\bsn_enum.py
# Compiled at: 2020-04-20 02:55:22
# Size of source mod 2**32: 585 bytes
from enum import IntEnum

class AppAlgorithmType(IntEnum):
    """AppAlgorithmType"""
    AppAlgorithmType_Not = 0
    AppAlgorithmType_SM2 = 1
    AppAlgorithmType_R1 = 2
    AppAlgorithmType_K1 = 3


class AppCaType(IntEnum):
    """AppCaType"""
    AppCaType_Not = 0
    AppCaType_Trust = 1
    AppCaType_NoTrust = 2


class ResCode(IntEnum):
    """ResCode"""
    ResCode_Suc = 0
    ResCode_Fail = -1