# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case5_16.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case5_16(Case):
    DESCRIPTION = 'Repeated 2x: Continuation Frame with FIN = false (where there is nothing to continue), then text Message fragmented into 2 fragments.'
    EXPECTATION = 'The connection is failed immediately, since there is no message to continue.'

    def onOpen(self):
        self.expected[Case.OK] = []
        self.expectedClose = {'closedByMe': False, 'closeCode': [self.p.CLOSE_STATUS_CODE_PROTOCOL_ERROR], 'requireClean': False}
        for i in xrange(0, 2):
            self.p.sendFrame(opcode=0, fin=False, payload='fragment1')
            self.p.sendFrame(opcode=1, fin=False, payload='fragment2')
            self.p.sendFrame(opcode=0, fin=True, payload='fragment3')

        self.p.killAfter(1)