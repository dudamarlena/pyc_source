# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case3_6.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case3_6(Case):
    DESCRIPTION = 'Send Ping with <b>RSV = 6</b>.'
    EXPECTATION = 'The connection is failed immediately, since RSV must be 0.'

    def onOpen(self):
        payload = 'Hello, world!'
        self.expected[Case.OK] = []
        self.expectedClose = {'closedByMe': False, 'closeCode': [self.p.CLOSE_STATUS_CODE_PROTOCOL_ERROR], 'requireClean': False}
        self.p.sendFrame(opcode=2, payload=payload, rsv=6)
        self.p.killAfter(1)