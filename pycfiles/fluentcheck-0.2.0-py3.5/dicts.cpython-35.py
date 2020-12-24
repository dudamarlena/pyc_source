# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/assertions_is/dicts.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 470 bytes
from fluentcheck.assertions_is.base_is import IsBase

class __IsDicts(IsBase):

    @property
    def dict(self) -> 'Is':
        self.check.is_dict()
        return self

    @property
    def not_dict(self) -> 'Is':
        self.check.is_not_dict()
        return self

    def has_keys(self, *keys) -> 'Is':
        self.check.has_keys(*keys)
        return self

    def has_not_keys(self, *keys) -> 'Is':
        self.check.has_not_keys(*keys)
        return self