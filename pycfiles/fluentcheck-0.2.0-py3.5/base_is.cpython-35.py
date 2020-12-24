# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/assertions_is/base_is.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 395 bytes
from typing import Any

class IsBase:
    _IsBase__check = None

    def __init__(self, object_under_test: Any):
        self.object = object_under_test

    def __call__(self, *args, **kwargs):
        return self

    @property
    def check(self):
        if not IsBase._IsBase__check:
            from ..classes import Check
            IsBase._IsBase__check = Check
        return IsBase._IsBase__check(self.object)