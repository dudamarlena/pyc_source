# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/clipboard/in_memory.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 1023 bytes
from .base import Clipboard, ClipboardData
from collections import deque
__all__ = ('InMemoryClipboard', )

class InMemoryClipboard(Clipboard):
    __doc__ = '\n    Default clipboard implementation.\n    Just keep the data in memory.\n\n    This implements a kill-ring, for Emacs mode.\n    '

    def __init__(self, data=None, max_size=60):
        if not data is None:
            if not isinstance(data, ClipboardData):
                raise AssertionError
        else:
            assert max_size >= 1
            self.max_size = max_size
            self._ring = deque()
            if data is not None:
                self.set_data(data)

    def set_data(self, data):
        assert isinstance(data, ClipboardData)
        self._ring.appendleft(data)
        while len(self._ring) > self.max_size:
            self._ring.pop()

    def get_data(self):
        if self._ring:
            return self._ring[0]
        else:
            return ClipboardData()

    def rotate(self):
        if self._ring:
            self._ring.append(self._ring.popleft())