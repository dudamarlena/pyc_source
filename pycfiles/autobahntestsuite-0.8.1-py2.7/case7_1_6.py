# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case7_1_6.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case7_1_6(Case):
    DESCRIPTION = 'Send 256K message followed by close then a ping'
    EXPECTATION = 'Case outcome depends on implementation defined close behavior. Message and close frame are sent back to back. If the close frame is processed before the text message write is complete (as can happen in asynchronous processing models) the close frame is processed first and the text message may not be received or may only be partially recieved.'

    def init(self):
        self.suppressClose = True
        self.DATALEN = 256 * 1024
        self.PAYLOAD = 'BAsd7&jh23'

    def onConnectionLost(self, failedByMe):
        Case.onConnectionLost(self, failedByMe)
        self.passed = True
        if self.behavior == Case.OK:
            self.result = 'Text message was processed before close.'
        elif self.behavior == Case.NON_STRICT:
            self.result = 'Close was processed before text message could be returned.'
        self.behavior = Case.INFORMATIONAL
        self.behaviorClose = Case.INFORMATIONAL

    def onOpen(self):
        payload = 'Hello World!'
        self.expected[Case.OK] = [('message', payload, False)]
        self.expected[Case.NON_STRICT] = []
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
        self.p.sendFrame(opcode=1, payload=self.PAYLOAD, payload_len=self.DATALEN)
        self.p.sendFrame(opcode=1, payload=payload)
        self.p.sendClose(self.p.CLOSE_STATUS_CODE_NORMAL)
        self.p.sendFrame(opcode=9)
        self.p.killAfter(1)