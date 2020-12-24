# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case9_6_3.py
# Compiled at: 2018-12-17 11:51:20
from case9_6_1 import Case9_6_1

class Case9_6_3(Case9_6_1):
    DESCRIPTION = 'Send binary message message with payload of length 1 * 2**20 (1M). Sent out data in chops of 256 octets.'
    EXPECTATION = "Receive echo'ed text message (with payload as sent)."

    def setChopSize(self):
        self.chopsize = 256