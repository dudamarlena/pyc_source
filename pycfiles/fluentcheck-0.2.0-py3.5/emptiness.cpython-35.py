# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/assertions_is/emptiness.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 250 bytes
from .base_is import IsBase

class __IsEmptiness(IsBase):

    @property
    def none(self) -> 'Is':
        self.check.is_none()
        return self

    @property
    def not_none(self) -> 'Is':
        self.check.is_not_none()
        return self