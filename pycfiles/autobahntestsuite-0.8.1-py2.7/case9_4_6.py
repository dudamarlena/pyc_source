# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case9_4_6.py
# Compiled at: 2018-12-17 11:51:20
from case9_4_1 import Case9_4_1

class Case9_4_6(Case9_4_1):
    DESCRIPTION = 'Send fragmented binary message message with message payload of length 4 * 2**20 (4M). Sent out in fragments of 64k.'
    EXPECTATION = "Receive echo'ed binary message (with payload as sent)."

    def init(self):
        self.DATALEN = 4 * 1048576
        self.FRAGSIZE = 64 * 1024
        self.PAYLOAD = '*' * self.DATALEN
        self.WAITSECS = 100
        self.reportTime = True