# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case2_11.py
# Compiled at: 2018-12-17 11:51:20
from case2_10 import *

class Case2_11(Case2_10):
    DESCRIPTION = 'Send 10 Pings with payload. Send out octets in octet-wise chops.'
    EXPECTATION = 'Pongs for our Pings with all the payloads. Note: This is not required by the Spec .. but we check for this behaviour anyway. Clean close with normal code.'

    def init(self):
        self.chopsize = 1