# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case2_10.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case2_10(Case):
    DESCRIPTION = 'Send 10 Pings with payload.'
    EXPECTATION = 'Pongs for our Pings with all the payloads. Note: This is not required by the Spec .. but we check for this behaviour anyway. Clean close with normal code.'

    def init(self):
        self.chopsize = None
        return

    def onOpen(self):
        self.expected[Case.OK] = []
        for i in xrange(0, 10):
            payload = 'payload-%d' % i
            self.expected[Case.OK].append(('pong', payload))
            self.p.sendFrame(opcode=9, payload=payload, chopsize=self.chopsize)

        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
        self.p.closeAfter(3)