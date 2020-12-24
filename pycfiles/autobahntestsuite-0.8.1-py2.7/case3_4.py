# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case3_4.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case3_4(Case):
    DESCRIPTION = 'Send small text message, then send again with <b>RSV = 4</b>, then send Ping. Octets are sent in octet-wise chops.'
    EXPECTATION = 'Echo for first message is received, but then connection is failed immediately, since RSV must be 0, when no extension defining RSV meaning has been negotiated. The Pong is not received.'

    def onOpen(self):
        payload = 'Hello, world!'
        self.expected[Case.OK] = [('message', payload, False)]
        self.expected[Case.NON_STRICT] = []
        self.expectedClose = {'closedByMe': False, 'closeCode': [self.p.CLOSE_STATUS_CODE_PROTOCOL_ERROR], 'requireClean': False}
        self.p.sendFrame(opcode=1, payload=payload, chopsize=1)
        self.p.sendFrame(opcode=1, payload=payload, rsv=4, chopsize=1)
        self.p.sendFrame(opcode=9, chopsize=1)
        self.p.killAfter(1)