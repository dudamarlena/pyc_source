# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case1_2_7.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case1_2_7(Case):
    DESCRIPTION = 'Send binary message message with payload of length 65536.'
    EXPECTATION = "Receive echo'ed binary message (with payload as sent). Clean close with normal code."

    def onOpen(self):
        payload = b'\xfe' * 65536
        self.expected[Case.OK] = [('message', payload, True)]
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
        self.p.sendFrame(opcode=2, payload=payload)
        self.p.killAfter(10)