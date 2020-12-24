# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case7_1_5.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case7_1_5(Case):
    DESCRIPTION = 'Send message fragment1 followed by close then fragment'
    EXPECTATION = 'Clean close with normal code.'

    def init(self):
        self.suppressClose = True

    def onConnectionLost(self, failedByMe):
        Case.onConnectionLost(self, failedByMe)
        if self.behaviorClose == Case.WRONG_CODE:
            self.behavior = Case.FAILED
            self.passed = False
            self.result = self.resultClose

    def onOpen(self):
        fragments = ['fragment1', 'fragment2']
        self.expected[Case.OK] = []
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
        self.p.sendFrame(opcode=1, fin=False, payload=fragments[0])
        self.p.sendClose(self.p.CLOSE_STATUS_CODE_NORMAL)
        self.p.sendFrame(opcode=0, fin=True, payload=fragments[1])
        self.p.killAfter(1)