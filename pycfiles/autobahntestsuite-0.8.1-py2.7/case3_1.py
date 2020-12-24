# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case3_1.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case3_1(Case):
    DESCRIPTION = 'Send small text message with <b>RSV = 1</b>.'
    EXPECTATION = 'The connection is failed immediately (1002/protocol error), since RSV must be 0, when no extension defining RSV meaning has been negotiated.'

    def onOpen(self):
        self.expected[Case.OK] = []
        self.expectedClose = {'closedByMe': False, 'closeCode': [
                       self.p.CLOSE_STATUS_CODE_PROTOCOL_ERROR], 
           'requireClean': False}
        self.p.sendFrame(opcode=1, payload='Hello, world!', rsv=1)
        self.p.killAfter(1)