# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rmcgover/src/pushsource/src/pushsource/_impl/model/file.py
# Compiled at: 2020-02-03 23:53:24
# Size of source mod 2**32: 257 bytes
from .base import PushItem
from .. import compat_attr as attr

@attr.s()
class FilePushItem(PushItem):
    __doc__ = 'A push item representing a single generic file.'
    description = attr.ib(type=str)