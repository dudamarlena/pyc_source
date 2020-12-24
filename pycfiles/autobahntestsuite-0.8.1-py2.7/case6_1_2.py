# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case6_1_2.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case6_1_2(Case):
    DESCRIPTION = 'Send fragmented text message, 3 fragments each of length 0.'
    EXPECTATION = "A message is echo'ed back to us (with empty payload)."

    def onOpen(self):
        self.expected[Case.OK] = [
         (
          'message', '', False)]
        self.expectedClose = {'closedByMe': True, 'closeCode': [
                       self.p.CLOSE_STATUS_CODE_NORMAL], 
           'requireClean': True}
        self.p.sendFrame(opcode=1, fin=False, payload='')
        self.p.sendFrame(opcode=0, fin=False, payload='')
        self.p.sendFrame(opcode=0, fin=True, payload='')
        self.p.closeAfter(1)