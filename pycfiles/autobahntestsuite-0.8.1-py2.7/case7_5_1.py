# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case7_5_1.py
# Compiled at: 2018-12-17 11:51:20
from case import Case
import binascii

class Case7_5_1(Case):
    DESCRIPTION = 'Send a close frame with invalid UTF8 payload'
    EXPECTATION = 'Clean close with protocol error or invalid utf8 code or dropped TCP.'

    def init(self):
        self.suppressClose = True

    def onConnectionLost(self, failedByMe):
        Case.onConnectionLost(self, failedByMe)
        if self.behaviorClose == Case.WRONG_CODE:
            self.behavior = Case.FAILED
            self.passed = False
            self.result = self.resultClose
        if self.p.localCloseReason:
            self.p.localCloseReason = binascii.b2a_hex(self.p.localCloseReason)
        else:
            self.p.localCloseReason = '?'

    def onOpen(self):
        self.payload = b'\xce\xba\xe1\xbd\xb9\xcf\x83\xce\xbc\xce\xb5\xed\xa0\x80edited'
        self.expected[Case.OK] = []
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_PROTOCOL_ERROR, self.p.CLOSE_STATUS_CODE_INVALID_PAYLOAD], 'requireClean': False}
        self.p.sendCloseFrame(self.p.CLOSE_STATUS_CODE_NORMAL, reasonUtf8=self.payload)
        self.p.killAfter(1)