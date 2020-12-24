# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case5_20.py
# Compiled at: 2018-12-17 11:51:20
from case5_19 import *

class Case5_20(Case5_19):
    DESCRIPTION = 'Same as Case 5.19, but send all frames with SYNC = True.\n   Note, this does not change the octets sent in any way, only how the stream\n   is chopped up on the wire.'
    EXPECTATION = 'Same as Case 5.19. Implementations must be agnostic to how\n   octet stream is chopped up on wire (must be TCP clean).'

    def init(self):
        self.sync = True