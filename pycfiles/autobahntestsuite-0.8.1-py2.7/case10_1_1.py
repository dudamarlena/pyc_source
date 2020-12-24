# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case10_1_1.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case10_1_1(Case):
    DESCRIPTION = 'Send text message with payload of length 65536 auto-fragmented with <b>autoFragmentSize = 1300</b>.'
    EXPECTATION = "Receive echo'ed text message (with payload as sent and transmitted frame counts as expected). Clean close with normal code."

    def onOpen(self):
        self.payload = '*' * 65536
        self.p.autoFragmentSize = 1300
        self.expected[Case.OK] = [('message', self.payload, False)]
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
        self.p.sendMessage(self.payload)
        self.p.killAfter(10)

    def onConnectionLost(self, failedByMe):
        Case.onConnectionLost(self, failedByMe)
        if self.p.connectionWasOpen:
            frames_expected = {}
            frames_expected[0] = len(self.payload) / self.p.autoFragmentSize
            frames_expected[1] = 1 if len(self.payload) % self.p.autoFragmentSize > 0 else 0
            frames_got = {}
            frames_got[0] = self.p.txFrameStats[0]
            frames_got[1] = self.p.txFrameStats[1]
            if frames_expected == frames_got:
                pass
            else:
                self.behavior = Case.FAILED
                self.result = 'Frames transmitted %s does not match what we expected %s.' % (str(frames_got), str(frames_expected))
        else:
            self.behavior = Case.FAILED
            self.result = 'WebSocket connection was never open'