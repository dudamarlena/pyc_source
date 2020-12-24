# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case2_6.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case2_6(Case):
    DESCRIPTION = 'Send ping with binary payload of 125 octets, send in octet-wise chops.'
    EXPECTATION = "Pong with payload echo'ed is sent in reply to Ping. Implementations must be TCP clean. Clean close with normal code."

    def onOpen(self):
        payload = b'\xfe' * 125
        self.expected[Case.OK] = [('pong', payload)]
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
        self.p.sendFrame(opcode=9, payload=payload, chopsize=1)
        self.p.closeAfter(2)