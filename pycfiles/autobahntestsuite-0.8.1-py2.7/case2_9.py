# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case2_9.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case2_9(Case):
    DESCRIPTION = 'Send unsolicited pong with payload. Send ping with payload. Verify pong for ping is received.'
    EXPECTATION = "Nothing in reply to own Pong, but Pong with payload echo'ed in reply to Ping. Clean close with normal code."

    def onOpen(self):
        payload = 'ping payload'
        self.expected[Case.OK] = [('pong', payload)]
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
        self.p.sendFrame(opcode=10, payload='unsolicited pong payload')
        self.p.sendFrame(opcode=9, payload=payload)
        self.p.closeAfter(1)