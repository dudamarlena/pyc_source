# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/assertions_is/uuids.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 471 bytes
from fluentcheck.assertions_is.base_is import IsBase

class __IsUUIDs(IsBase):

    @property
    def uuid1(self) -> 'Is':
        self.check.is_uuid1()
        return self

    @property
    def not_uuid1(self) -> 'Is':
        self.check.is_not_uuid1()
        return self

    @property
    def uuid4(self) -> 'Is':
        self.check.is_uuid4()
        return self

    @property
    def not_uuid4(self) -> 'Is':
        self.check.is_not_uuid4()
        return self