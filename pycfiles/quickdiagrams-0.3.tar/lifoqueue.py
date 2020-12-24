# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugoruscitti/Aptana Studio 3 Workspace/quickdiagrams/quickdiagrams/gtkclient/lifoqueue.py
# Compiled at: 2011-01-24 11:46:37
from Queue import Queue

class LifoQueue(Queue):
    """Variant of Queue that retrieves most recently added entries first."""

    def _init(self, maxsize):
        self.queue = []
        self.maxsize = maxsize

    def _qsize(self, len=len):
        return len(self.queue)

    def _put(self, item):
        self.queue.append(item)

    def _get(self):
        return self.queue.pop()