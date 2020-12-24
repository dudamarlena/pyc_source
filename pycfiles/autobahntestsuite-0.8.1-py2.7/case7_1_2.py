# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case7_1_2.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case7_1_2(Case):
    DESCRIPTION = 'Send two close frames'
    EXPECTATION = 'Clean close with normal code. Second close frame ignored.'

    def init(self):
        self.suppressClose = True

    def onConnectionLost(self, failedByMe):
        Case.onConnectionLost(self, failedByMe)
        if self.behaviorClose == Case.WRONG_CODE:
            self.behavior = Case.FAILED
            self.passed = False
            self.result = self.resultClose

    def onOpen(self):
        payload = 'Hello World!'
        self.expected[Case.OK] = []
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
        self.p.sendClose(self.p.CLOSE_STATUS_CODE_NORMAL)
        self.p.sendFrame(opcode=8)
        self.p.killAfter(1)