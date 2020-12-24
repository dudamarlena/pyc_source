# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/protocols/nefarious.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 593 bytes
__doc__ = '\nnefarious.py: Migration stub to the new P10 protocol module.\n'
from pylinkirc.log import log
from pylinkirc.protocols.p10 import *

class NefariousProtocol(P10Protocol):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        log.warning('(%s) protocols/nefarious.py has been renamed to protocols/p10.py, which now also supports other IRCu variants. Please update your configuration, as this migration stub will be removed in a future version.', self.name)


Class = NefariousProtocol