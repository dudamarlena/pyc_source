# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\protocols\RDP\tpkt.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 181 bytes


class TPKT:

    def __init__(self):
        self.version = None
        self.reserved = None
        self.length = None