# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/context_var/__init__.py
# Compiled at: 2020-03-15 16:14:17
# Size of source mod 2**32: 405 bytes
from contextlib import contextmanager

class ContextVar:
    """ContextVar"""

    def __init__(self, default=None):
        self.values = [default]

    @contextmanager
    def set(self, value):
        self.values.append(value)
        yield
        self.values.pop()

    def get(self):
        return self.values[(-1)]