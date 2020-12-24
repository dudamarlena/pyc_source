# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case6_3_2.py
# Compiled at: 2018-12-17 11:51:20
from case import Case
from case6_3_1 import Case6_3_1
import binascii

class Case6_3_2(Case6_3_1):
    DESCRIPTION = 'Send invalid UTF-8 text message in fragments of 1 octet, resulting in frames ending on positions which are not code point ends.<br><br>MESSAGE:<br>%s' % binascii.b2a_hex(Case6_3_1.PAYLOAD)
    EXPECTATION = 'The connection is failed immediately, since the payload is not valid UTF-8.'

    def onOpen(self):
        self.expected[Case.OK] = []
        self.expectedClose = {'closedByMe': False, 'closeCode': [
                       self.p.CLOSE_STATUS_CODE_INVALID_PAYLOAD], 
           'requireClean': False, 
           'closedByWrongEndpointIsFatal': True}
        self.p.sendMessage(self.PAYLOAD, isBinary=False, fragmentSize=1)
        self.p.killAfter(1)