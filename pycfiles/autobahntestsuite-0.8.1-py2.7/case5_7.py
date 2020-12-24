# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case5_7.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case5_7(Case):
    DESCRIPTION = 'Send text Message fragmented into 2 fragments, one ping with payload in-between. Octets are sent in frame-wise chops.'
    EXPECTATION = "A pong is received, then the message is echo'ed back to us."

    def onOpen(self):
        ping_payload = 'ping payload'
        fragments = ['fragment1', 'fragment2']
        self.expected[Case.OK] = [('pong', ping_payload), ('message', ('').join(fragments), False)]
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
        self.p.sendFrame(opcode=1, fin=False, payload=fragments[0], sync=True)
        self.p.sendFrame(opcode=9, fin=True, payload=ping_payload, sync=True)
        self.p.sendFrame(opcode=0, fin=True, payload=fragments[1], sync=True)
        self.p.closeAfter(1)