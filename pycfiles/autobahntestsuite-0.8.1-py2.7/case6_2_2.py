# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case6_2_2.py
# Compiled at: 2018-12-17 11:51:20
from case import Case
import binascii

class Case6_2_2(Case):
    PAYLOAD1 = 'Hello-µ@ßöä'
    PAYLOAD2 = 'üàá-UTF-8!!'
    DESCRIPTION = 'Send a valid UTF-8 text message in two fragments, fragmented on UTF-8 code point boundary.<br><br>MESSAGE FRAGMENT 1:<br>%s<br>%s<br><br>MESSAGE FRAGMENT 2:<br>%s<br>%s' % (PAYLOAD1, binascii.b2a_hex(PAYLOAD1), PAYLOAD2, binascii.b2a_hex(PAYLOAD2))
    EXPECTATION = "The message is echo'ed back to us."

    def onOpen(self):
        self.expected[Case.OK] = [
         (
          'message', self.PAYLOAD1 + self.PAYLOAD2, False)]
        self.expectedClose = {'closedByMe': True, 'closeCode': [
                       self.p.CLOSE_STATUS_CODE_NORMAL], 
           'requireClean': True}
        self.p.sendFrame(opcode=1, fin=False, payload=self.PAYLOAD1)
        self.p.sendFrame(opcode=0, fin=True, payload=self.PAYLOAD2)
        self.p.closeAfter(1)