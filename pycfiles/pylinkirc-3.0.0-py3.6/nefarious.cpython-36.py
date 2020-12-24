# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/protocols/nefarious.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 593 bytes
"""
nefarious.py: Migration stub to the new P10 protocol module.
"""
from pylinkirc.log import log
from pylinkirc.protocols.p10 import *

class NefariousProtocol(P10Protocol):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        log.warning('(%s) protocols/nefarious.py has been renamed to protocols/p10.py, which now also supports other IRCu variants. Please update your configuration, as this migration stub will be removed in a future version.', self.name)


Class = NefariousProtocol