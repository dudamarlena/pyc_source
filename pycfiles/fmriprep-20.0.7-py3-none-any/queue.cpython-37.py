# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_vendor/urllib3/util/queue.py
# Compiled at: 2020-05-05 12:41:36
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