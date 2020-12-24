# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case2_3.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case2_3(Case):
    DESCRIPTION = 'Send ping with small binary (non UTF-8) payload.'
    EXPECTATION = "Pong with payload echo'ed is sent in reply to Ping. Clean close with normal code."

    def onOpen(self):
        payload = b'\x00\xff\xfe\xfd\xfc\xfb\x00\xff'
        self.expected[Case.OK] = [
         (
          'pong', payload)]
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
        self.p.sendFrame(opcode=9, payload=payload)
        self.p.closeAfter(1)