# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rmcgover/src/pushsource/src/pushsource/_impl/model/rpm.py
# Compiled at: 2020-01-30 22:31:14
# Size of source mod 2**32: 269 bytes
from .base import PushItem
from .. import compat_attr as attr

@attr.s()
class RpmPushItem(PushItem):
    __doc__ = 'A push item representing a single RPM.'