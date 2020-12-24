# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case1_1_6.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case1_1_6(Case):
    DESCRIPTION = 'Send text message message with payload of length 65535.'
    EXPECTATION = "Receive echo'ed text message (with payload as sent). Clean close with normal code."

    def onOpen(self):
        payload = '*' * 65535
        self.expected[Case.OK] = [('message', payload, False)]
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
        self.p.sendFrame(opcode=1, payload=payload)
        self.p.killAfter(10)