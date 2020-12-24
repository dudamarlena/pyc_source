# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rmcgover/src/pushsource/src/pushsource/_impl/model/base.py
# Compiled at: 2020-02-03 23:07:22
# Size of source mod 2**32: 2756 bytes
from .. import compat_attr as attr

@attr.s()
class PushItem(object):
    """PushItem"""
    name = attr.ib(type=str)
    state = attr.ib(type=str, default='PENDING')
    src = attr.ib(type=str, default=None)
    dest = attr.ib(type=list, default=(attr.Factory(list)))
    md5sum = attr.ib(type=str, default=None)
    sha256sum = attr.ib(type=str, default=None)
    origin = attr.ib(type=str, default=None)
    build = attr.ib(type=str, default=None)
    signing_key = attr.ib(type=str, default=None)