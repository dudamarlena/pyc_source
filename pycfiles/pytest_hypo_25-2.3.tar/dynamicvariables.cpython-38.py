# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\utils\dynamicvariables.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 1182 bytes
import threading
from contextlib import contextmanager

class DynamicVariable:

    def __init__(self, default):
        self.default = default
        self.data = threading.local()

    @property
    def value(self):
        return getattr(self.data, 'value', self.default)

    @value.setter
    def value(self, value):
        self.data.value = value

    @contextmanager
    def with_value(self, value):
        old_value = self.value
        try:
            self.data.value = value
            (yield)
        finally:
            self.data.value = old_value