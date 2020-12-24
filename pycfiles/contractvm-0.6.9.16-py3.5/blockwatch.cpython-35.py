# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/contractvmd/chain/blockwatch.py
# Compiled at: 2015-12-16 10:04:28
# Size of source mod 2**32: 620 bytes
import time
from .. import config

class BlockWatch:

    def __init__(self, current, backend, notifyHandler):
        self.current_height = current
        self.backend = backend
        self.notify = notifyHandler

    def run(self):
        while True:
            h = self.backend.getLastBlockHeight()
            if h != self.current_height:
                for i in range(self.current_height + 1, h + 1):
                    self.notify(i)
                    self.current_height = i
                    time.sleep(0.1)

            time.sleep(5)