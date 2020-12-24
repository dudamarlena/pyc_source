# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case6_4_2.py
# Compiled at: 2018-12-17 11:51:20
import binascii
from case import Case
from case6_4_1 import Case6_4_1
from autobahn.websocket.protocol import WebSocketProtocol

class Case6_4_2(Case6_4_1):
    DESCRIPTION = 'Same as Case 6.4.1, but in 2nd frame, we send only up to and including the octet making the complete payload invalid.\n<br><br>MESSAGE PARTS:<br>\nPART1 = %s<br>\nPART2 = %s<br>\nPART3 = %s<br>\n' % (binascii.b2a_hex(Case6_4_1.PAYLOAD[:12]), binascii.b2a_hex(Case6_4_1.PAYLOAD[12]), binascii.b2a_hex(Case6_4_1.PAYLOAD[13:]))
    EXPECTATION = 'The first frame is accepted, we expect to timeout on the first wait. The 2nd frame should be rejected immediately (fail fast on UTF-8). If we timeout, we expect the connection is failed at least then, since the complete message payload is not valid UTF-8.'

    def onOpen(self):
        self.expected[Case.OK] = [
         ('timeout', 'A')]
        self.expected[Case.NON_STRICT] = [('timeout', 'A'), ('timeout', 'B')]
        self.expectedClose = {'closedByMe': False, 'closeCode': [
                       self.p.CLOSE_STATUS_CODE_INVALID_PAYLOAD], 
           'requireClean': False, 
           'closedByWrongEndpointIsFatal': True}
        self.p.sendFrame(opcode=1, fin=False, payload=self.PAYLOAD[:12])
        self.p.continueLater(1, self.part2, 'A')

    def part2(self):
        if self.p.state == WebSocketProtocol.STATE_OPEN:
            self.received.append(('timeout', 'A'))
            self.p.sendFrame(opcode=0, fin=False, payload=self.PAYLOAD[12])
            self.p.continueLater(1, self.part3, 'B')

    def part3(self):
        if self.p.state == WebSocketProtocol.STATE_OPEN:
            self.received.append(('timeout', 'B'))
            self.p.sendFrame(opcode=0, fin=True, payload=self.PAYLOAD[13:])
            self.p.killAfter(1)