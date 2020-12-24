# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case6_4_1.py
# Compiled at: 2018-12-17 11:51:20
import binascii
from case import Case
from autobahn.websocket.protocol import WebSocketProtocol

class Case6_4_1(Case):
    PAYLOAD1 = 'κόσμε'
    PAYLOAD2 = b'\xf4\x90\x80\x80'
    PAYLOAD3 = 'edited'
    PAYLOAD = PAYLOAD1 + PAYLOAD2 + PAYLOAD3
    DESCRIPTION = 'Send invalid UTF-8 text message in 3 fragments (frames).\nFirst frame payload is valid, then wait, then 2nd frame which contains the payload making the sequence invalid, then wait, then 3rd frame with rest.\nNote that PART1 and PART3 are valid UTF-8 in themselves, PART2 is a 0x110000 encoded as in the UTF-8 integer encoding scheme, but the codepoint is invalid (out of range).\n<br><br>MESSAGE PARTS:<br>\nPART1 = %s<br>\nPART2 = %s<br>\nPART3 = %s<br>\n' % (binascii.b2a_hex(PAYLOAD1), binascii.b2a_hex(PAYLOAD2), binascii.b2a_hex(PAYLOAD3))
    EXPECTATION = 'The first frame is accepted, we expect to timeout on the first wait. The 2nd frame should be rejected immediately (fail fast on UTF-8). If we timeout, we expect the connection is failed at least then, since the complete message payload is not valid UTF-8.'

    def onOpen(self):
        self.expected[Case.OK] = [
         ('timeout', 'A')]
        self.expected[Case.NON_STRICT] = [('timeout', 'A'), ('timeout', 'B')]
        self.expectedClose = {'closedByMe': False, 'closeCode': [
                       self.p.CLOSE_STATUS_CODE_INVALID_PAYLOAD], 
           'requireClean': False, 
           'closedByWrongEndpointIsFatal': True}
        self.p.sendFrame(opcode=1, fin=False, payload=self.PAYLOAD1)
        self.p.continueLater(1, self.part2, 'A')

    def part2(self):
        if self.p.state == WebSocketProtocol.STATE_OPEN:
            self.received.append(('timeout', 'A'))
            self.p.sendFrame(opcode=0, fin=False, payload=self.PAYLOAD2)
            self.p.continueLater(1, self.part3, 'B')

    def part3(self):
        if self.p.state == WebSocketProtocol.STATE_OPEN:
            self.received.append(('timeout', 'B'))
            self.p.sendFrame(opcode=0, fin=True, payload=self.PAYLOAD3)
            self.p.killAfter(1)