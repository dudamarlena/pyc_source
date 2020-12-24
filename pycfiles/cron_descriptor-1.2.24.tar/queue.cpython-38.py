# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/urllib3/util/queue.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 497 bytes
import collections
from ..packages import six
from packages.six.moves import queue
if six.PY2:
    import Queue as _unused_module_Queue

class LifoQueue(queue.Queue):

    def _init(self, _):
        self.queue = collections.deque()

    def _qsize(self, len=len):
        return len(self.queue)

    def _put(self, item):
        self.queue.append(item)

    def _get(self):
        return self.queue.pop()