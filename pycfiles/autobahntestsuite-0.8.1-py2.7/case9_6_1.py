# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case9_6_1.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case9_6_1(Case):
    DESCRIPTION = 'Send binary message message with payload of length 1 * 2**20 (1M). Sent out data in chops of 64 octets.'
    EXPECTATION = "Receive echo'ed binary message (with payload as sent)."

    def setChopSize(self):
        self.chopsize = 64

    def init(self):
        self.DATALEN = 1 * 1048576
        self.PAYLOAD = b'\x00\xfe#\xfa\xf0'
        self.WAITSECS = 1000
        self.reportTime = True
        self.setChopSize()

    def onOpen(self):
        self.p.createWirelog = False
        self.behavior = Case.FAILED
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
        self.result = 'Did not receive message within %d seconds.' % self.WAITSECS
        self.p.sendFrame(opcode=2, payload=self.PAYLOAD, payload_len=self.DATALEN, chopsize=self.chopsize)
        self.p.closeAfter(self.WAITSECS)

    def onMessage(self, msg, binary):
        if not binary:
            self.result = 'Expected binary message with payload, but got text.'
        elif len(msg) != self.DATALEN:
            self.result = 'Expected binary message with payload of length %d, but got %d.' % (self.DATALEN, len(msg))
        else:
            self.behavior = Case.OK
            self.result = 'Received binary message of length %d.' % len(msg)
        self.p.createWirelog = True
        self.p.sendClose(self.p.CLOSE_STATUS_CODE_NORMAL)