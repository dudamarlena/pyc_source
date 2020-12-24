# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case9_3_1.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case9_3_1(Case):
    DESCRIPTION = 'Send fragmented text message message with message payload of length 4 * 2**20 (4M). Sent out in fragments of 64.'
    EXPECTATION = "Receive echo'ed text message (with payload as sent)."

    def init(self):
        self.DATALEN = 4 * 1048576
        self.FRAGSIZE = 64
        self.PAYLOAD = '*' * self.DATALEN
        self.WAITSECS = 100
        self.reportTime = True

    def onOpen(self):
        self.p.createWirelog = False
        self.behavior = Case.FAILED
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
        self.result = 'Did not receive message within %d seconds.' % self.WAITSECS
        self.p.sendMessage(payload=self.PAYLOAD, isBinary=False, fragmentSize=self.FRAGSIZE)
        self.p.closeAfter(self.WAITSECS)

    def onMessage(self, payload, isBinary):
        if isBinary:
            self.result = 'Expected text message with payload, but got binary.'
        elif len(payload) != self.DATALEN:
            self.result = 'Expected text message with payload of length %d, but got %d.' % (self.DATALEN, len(payload))
        else:
            self.behavior = Case.OK
            self.result = 'Received text message of length %d.' % len(payload)
        self.p.createWirelog = True
        self.p.sendClose(self.p.CLOSE_STATUS_CODE_NORMAL)