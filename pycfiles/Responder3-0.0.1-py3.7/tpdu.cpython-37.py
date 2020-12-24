# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\protocols\RDP\tpdu.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 494 bytes
import enum

class X224_TPDU_TYPE(enum.Enum):
    X224_TPDU_CONNECTION_REQUEST = 224
    X224_TPDU_CONNECTION_CONFIRM = 208
    X224_TPDU_DISCONNECT_REQUEST = 128
    X224_TPDU_DATA = 240
    X224_TPDU_ERROR = 112


class TPDU:

    def __init__(self):
        self.LI = None
        self.Code = None
        self.DST_REF = None
        self.SRC_REF = None
        self.Class = None