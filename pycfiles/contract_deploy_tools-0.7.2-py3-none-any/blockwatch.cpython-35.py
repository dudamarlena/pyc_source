# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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