# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case6_2_3.py
# Compiled at: 2018-12-17 11:51:20
from case import Case
import binascii

class Case6_2_3(Case):
    PAYLOAD = 'Hello-µ@ßöäüàá-UTF-8!!'
    DESCRIPTION = 'Send a valid UTF-8 text message in fragments of 1 octet, resulting in frames ending on positions which are not code point ends.<br><br>MESSAGE:<br>%s<br>%s' % (PAYLOAD, binascii.b2a_hex(PAYLOAD))
    EXPECTATION = "The message is echo'ed back to us."

    def onOpen(self):
        self.expected[Case.OK] = [
         (
          'message', self.PAYLOAD, False)]
        self.expectedClose = {'closedByMe': True, 'closeCode': [
                       self.p.CLOSE_STATUS_CODE_NORMAL], 
           'requireClean': True}
        self.p.sendMessage(self.PAYLOAD, isBinary=False, fragmentSize=1)
        self.p.closeAfter(1)