# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case2_5.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case2_5(Case):
    DESCRIPTION = 'Send ping with binary payload of 126 octets.'
    EXPECTATION = 'Connection is failed immediately (1002/Protocol Error), since control frames are only allowed to have payload up to and including 125 octets..'

    def onOpen(self):
        payload = b'\xfe' * 126
        self.expected[Case.OK] = []
        self.expectedClose = {'closedByMe': False, 'closeCode': [self.p.CLOSE_STATUS_CODE_PROTOCOL_ERROR], 'requireClean': False}
        self.p.sendFrame(opcode=9, payload=payload)
        self.p.killAfter(1)