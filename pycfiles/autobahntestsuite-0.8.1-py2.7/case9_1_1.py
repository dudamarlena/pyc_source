# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case9_1_1.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case9_1_1(Case):
    DESCRIPTION = 'Send text message message with payload of length 64 * 2**10 (64k).'
    EXPECTATION = "Receive echo'ed text message (with payload as sent)."

    def init(self):
        self.DATALEN = 64 * 1024
        self.PAYLOAD = 'BAsd7&jh23'
        self.WAITSECS = 10
        self.reportTime = True

    def onOpen(self):
        self.p.createWirelog = False
        self.behavior = Case.FAILED
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
        self.result = 'Did not receive message within %d seconds.' % self.WAITSECS
        self.p.sendFrame(opcode=1, payload=self.PAYLOAD, payload_len=self.DATALEN)
        self.p.closeAfter(self.WAITSECS)

    def onMessage(self, msg, binary):
        if binary:
            self.result = 'Expected text message with payload, but got binary.'
        elif len(msg) != self.DATALEN:
            self.result = 'Expected text message with payload of length %d, but got %d.' % (self.DATALEN, len(msg))
        else:
            self.behavior = Case.OK
            self.result = 'Received text message of length %d.' % len(msg)
        self.p.createWirelog = True
        self.p.sendClose(self.p.CLOSE_STATUS_CODE_NORMAL)