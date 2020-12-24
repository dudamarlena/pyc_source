# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case7_7_X.py
# Compiled at: 2018-12-17 11:51:20
from case import Case
tests = [
 1000, 1001, 1002, 1003, 1007, 1008, 1009, 1010, 1011, 3000, 3999, 4000, 4999]
Case7_7_X = []

def __init__(self, protocol):
    Case.__init__(self, protocol)


def onOpen(self):
    self.expected[Case.OK] = []
    self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL, self.CLOSE_CODE], 'requireClean': True}
    self.p.sendCloseFrame(self.CLOSE_CODE)
    self.p.killAfter(1)


def onConnectionLost(self, failedByMe):
    Case.onConnectionLost(self, failedByMe)
    if self.behaviorClose == Case.WRONG_CODE:
        self.behavior = Case.FAILED
        self.passed = False
        self.result = self.resultClose


i = 1
for s in tests:
    DESCRIPTION = 'Send close with valid close code %d' % s
    EXPECTATION = 'Clean close with normal or echoed code'
    C = type('Case7_7_%d' % i, (
     object, Case), {'CLOSE_CODE': s, 'DESCRIPTION': '%s' % DESCRIPTION, 
       'EXPECTATION': '%s' % EXPECTATION, 
       '__init__': __init__, 
       'onOpen': onOpen, 
       'onConnectionLost': onConnectionLost})
    Case7_7_X.append(C)
    i += 1