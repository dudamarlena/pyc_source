# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case5_15.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case5_15(Case):
    DESCRIPTION = 'Send text Message fragmented into 2 fragments, then Continuation Frame with FIN = false where there is nothing to continue, then unfragmented Text Message, all sent in one chop.'
    EXPECTATION = 'The connection is failed immediately, since there is no message to continue.'

    def onOpen(self):
        fragments = [
         'fragment1', 'fragment2', 'fragment3', 'fragment4']
        self.expected[Case.OK] = [('message', ('').join(fragments[:2]), False)]
        self.expected[Case.NON_STRICT] = []
        self.expectedClose = {'closedByMe': False, 'closeCode': [self.p.CLOSE_STATUS_CODE_PROTOCOL_ERROR], 'requireClean': False}
        self.p.sendFrame(opcode=1, fin=False, payload=fragments[0])
        self.p.sendFrame(opcode=0, fin=True, payload=fragments[1])
        self.p.sendFrame(opcode=0, fin=False, payload=fragments[2])
        self.p.sendFrame(opcode=1, fin=True, payload=fragments[3])
        self.p.killAfter(1)