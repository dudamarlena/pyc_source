# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case7_13_1.py
# Compiled at: 2018-12-17 11:51:20
from case import Case

class Case7_13_1(Case):
    DESCRIPTION = 'Send close with close code 5000'
    EXPECTATION = 'Actual events are undefined by the spec.'

    def init(self):
        self.code = 5000
        self.suppressClose = True

    def onConnectionLost(self, failedByMe):
        Case.onConnectionLost(self, failedByMe)
        self.passed = True
        self.behavior = Case.INFORMATIONAL
        self.behaviorClose = Case.INFORMATIONAL
        self.result = 'Actual events are undefined by the spec.'

    def onOpen(self):
        self.payload = b'\xce\xba\xe1\xbd\xb9\xcf\x83\xce\xbc\xce\xb5\xed\xa0\x80edited'
        self.expected[Case.OK] = []
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL, self.code, self.p.CLOSE_STATUS_CODE_PROTOCOL_ERROR], 'requireClean': False}
        self.p.sendCloseFrame(self.code)
        self.p.killAfter(1)