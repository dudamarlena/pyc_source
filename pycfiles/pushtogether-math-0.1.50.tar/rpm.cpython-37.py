# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rmcgover/src/pushsource/src/pushsource/_impl/model/rpm.py
# Compiled at: 2020-01-30 22:31:14
# Size of source mod 2**32: 269 bytes
from .base import PushItem
from .. import compat_attr as attr

@attr.s()
class RpmPushItem(PushItem):
    """RpmPushItem"""
    pass