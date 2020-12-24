# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zwsun/workspace/python/corunner/corunner/ProcessNode.py
# Compiled at: 2013-10-09 09:39:22
import time, logging
PROCESS_STATUS_NONE = 0
PROCESS_STATUS_STARTED = 1
PROCESS_STATUS_ALIVE = 2
PROCESS_STATUS_DEAD = 3
PROCESS_STATUS_END = 9

class ProcessNode:

    def __init__(self, node, port=22):
        self.logger = logging.getLogger()
        self.node = node
        self.port = port
        self.status = PROCESS_STATUS_NONE
        self.lastAccessTime = time.time()

    def updateStatus(self, status):
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug('Update node %s status %s', self.node, self.toStr(status))
        if status >= self.status or self.status == PROCESS_STATUS_DEAD:
            self.status = status
        self.lastAccessTime = time.time()

    def toStr(self, status):
        if status == 0:
            return 'NONE'
        else:
            if status == 1:
                return 'STARTED'
            if status == 2:
                return 'ALIVE'
            if status == 3:
                return 'DEAD'
            if status == 9:
                return 'END'
            return 'UNKNOWN'