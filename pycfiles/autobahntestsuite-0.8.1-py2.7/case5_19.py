# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case5_19.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case5_19(Case):
    DESCRIPTION = 'A fragmented text message is sent in multiple frames. After\n   sending the first 2 frames of the text message, a Ping is sent. Then we wait 1s,\n   then we send 2 more text fragments, another Ping and then the final text fragment.\n   Everything is legal.'
    EXPECTATION = "The peer immediately answers the first Ping before\n   it has received the last text message fragment. The peer pong's back the Ping's\n   payload exactly, and echo's the payload of the fragmented message back to us."

    def init(self):
        self.sync = False

    def onOpen(self):
        self.fragments = [
         'fragment1', 'fragment2', 'fragment3', 'fragment4', 'fragment5']
        self.pings = ['pongme 1!', 'pongme 2!']
        self.expected[Case.OK] = [
         (
          'pong', self.pings[0]), ('pong', self.pings[1]), ('message', ('').join(self.fragments), False)]
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
        self.p.sendFrame(opcode=1, fin=False, payload=self.fragments[0], sync=self.sync)
        self.p.sendFrame(opcode=0, fin=False, payload=self.fragments[1], sync=self.sync)
        self.p.sendFrame(opcode=9, fin=True, payload=self.pings[0], sync=self.sync)
        self.p.continueLater(1, self.part2)

    def part2(self):
        self.p.sendFrame(opcode=0, fin=False, payload=self.fragments[2], sync=self.sync)
        self.p.sendFrame(opcode=0, fin=False, payload=self.fragments[3], sync=self.sync)
        self.p.sendFrame(opcode=9, fin=True, payload=self.pings[1], sync=self.sync)
        self.p.sendFrame(opcode=0, fin=True, payload=self.fragments[4], sync=self.sync)
        self.p.closeAfter(1)