# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case9_7_X.py
# Compiled at: 2018-12-17 11:51:20
from case import Case
tests = [
 (0, 1000, 60),
 (16, 1000, 60),
 (64, 1000, 60),
 (256, 1000, 120),
 (1024, 1000, 240),
 (4096, 1000, 480)]
Case9_7_X = []
Case9_8_X = []

def __init__(self, protocol):
    Case.__init__(self, protocol)
    self.reportTime = True


def onOpen(self):
    self.p.enableWirelog(False)
    self.behavior = Case.FAILED
    self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
    self.result = 'Case did not finish within %d seconds.' % self.WAITSECS
    self.p.closeAfter(self.WAITSECS)
    self.count = 0
    self.sendOne()


def sendOne(self):
    if self.BINARY:
        self.p.sendFrame(opcode=2, payload=b'\xfe', payload_len=self.LEN)
    else:
        self.p.sendFrame(opcode=1, payload='*', payload_len=self.LEN)
    self.count += 1


def onMessage(self, msg, binary):
    if binary != self.BINARY or len(msg) != self.LEN:
        self.behavior = Case.FAILED
        self.result = "Echo'ed message type or length differs from what I sent (got binary = %s, payload length = %s)." % (binary, len(msg))
        self.p.enableWirelog(True)
        self.p.sendClose(self.p.CLOSE_STATUS_CODE_NORMAL)
    elif self.count < self.COUNT:
        self.sendOne()
    else:
        self.behavior = Case.OK
        self.result = "Ok, received all echo'ed messages in time."
        self.p.enableWirelog(True)
        self.p.sendClose(self.p.CLOSE_STATUS_CODE_NORMAL)


for b in [False, True]:
    i = 1
    for s in tests:
        if b:
            mt = 'binary'
            cc = 'Case9_8_%d'
        else:
            mt = 'text'
            cc = 'Case9_7_%d'
        DESCRIPTION = 'Send %d %s messages of payload size %d to measure implementation/network RTT (round trip time) / latency.' % (s[1], mt, s[0])
        EXPECTATION = "Receive echo'ed %s messages (with payload as sent). Timeout case after %d secs." % (mt, s[2])
        C = type(cc % i, (
         object, Case), {'LEN': s[0], 'COUNT': s[1], 
           'WAITSECS': s[2], 
           'BINARY': b, 
           'DESCRIPTION': '%s' % DESCRIPTION, 
           'EXPECTATION': '%s' % EXPECTATION, 
           '__init__': __init__, 
           'onOpen': onOpen, 
           'onMessage': onMessage, 
           'sendOne': sendOne})
        if b:
            Case9_8_X.append(C)
        else:
            Case9_7_X.append(C)
        i += 1