# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case7_3_6.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case7_3_6(Case):
    DESCRIPTION = 'Send a close frame with close code and close reason which is too long (124) - total frame payload 126 octets'
    EXPECTATION = 'Clean close with protocol error code or dropped TCP connection.'

    def init(self):
        self.suppressClose = True

    def onConnectionLost(self, failedByMe):
        Case.onConnectionLost(self, failedByMe)
        if self.behaviorClose == Case.WRONG_CODE:
            self.behavior = Case.FAILED
            self.passed = False
            self.result = self.resultClose

    def onOpen(self):
        self.payload = '*' * 124
        self.expected[Case.OK] = []
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_PROTOCOL_ERROR], 'requireClean': False}
        self.p.sendCloseFrame(self.p.CLOSE_STATUS_CODE_NORMAL, reasonUtf8=self.payload)
        self.p.killAfter(1)