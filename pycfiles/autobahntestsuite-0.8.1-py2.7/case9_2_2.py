# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case9_2_2.py
# Compiled at: 2018-12-17 11:51:20
from case9_2_1 import *

class Case9_2_2(Case9_2_1):
    DESCRIPTION = 'Send binary message message with payload of length 256 * 2**10 (256k).'
    EXPECTATION = "Receive echo'ed binary message (with payload as sent)."

    def init(self):
        self.DATALEN = 256 * 1024
        self.PAYLOAD = b'\x00\xfe#\xfa\xf0'
        self.WAITSECS = 10
        self.reportTime = True