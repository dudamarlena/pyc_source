# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case3_2.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case3_2(Case):
    DESCRIPTION = 'Send small text message, then send again with <b>RSV = 2</b>, then send Ping.'
    EXPECTATION = 'Echo for first message is received, but then connection is failed immediately, since RSV must be 0, when no extension defining RSV meaning has been negotiated. The Pong is not received.'

    def onOpen(self):
        payload = 'Hello, world!'
        self.expected[Case.OK] = [('message', payload, False)]
        self.expected[Case.NON_STRICT] = []
        self.expectedClose = {'closedByMe': False, 'closeCode': [self.p.CLOSE_STATUS_CODE_PROTOCOL_ERROR], 'requireClean': False}
        self.p.sendFrame(opcode=1, payload=payload)
        self.p.sendFrame(opcode=1, payload=payload, rsv=2)
        self.p.sendFrame(opcode=9)
        self.p.killAfter(1)