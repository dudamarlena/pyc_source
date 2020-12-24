# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rmcgover/src/pushsource/src/pushsource/_impl/model/base.py
# Compiled at: 2020-02-03 23:07:22
# Size of source mod 2**32: 2756 bytes
from .. import compat_attr as attr

@attr.s()
class PushItem(object):
    __doc__ = 'A PushItem represents a single piece of content to be published.\n    This may be an RPM, an advisory, a generic file, and so on.\n    '
    name = attr.ib(type=str)
    state = attr.ib(type=str, default='PENDING')
    src = attr.ib(type=str, default=None)
    dest = attr.ib(type=list, default=(attr.Factory(list)))
    md5sum = attr.ib(type=str, default=None)
    sha256sum = attr.ib(type=str, default=None)
    origin = attr.ib(type=str, default=None)
    build = attr.ib(type=str, default=None)
    signing_key = attr.ib(type=str, default=None)