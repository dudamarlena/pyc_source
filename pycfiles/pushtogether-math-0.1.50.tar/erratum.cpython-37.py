# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rmcgover/src/pushsource/src/pushsource/_impl/model/erratum.py
# Compiled at: 2020-01-30 23:16:50
# Size of source mod 2**32: 6014 bytes
from .base import PushItem
from .. import compat_attr as attr

@attr.s()
class ErratumReference(object):
    """ErratumReference"""
    href = attr.ib(type=str)
    type = attr.ib(type=str, default='other')
    id = attr.ib(type=str)
    title = attr.ib(type=str)


@attr.s()
class ErratumModule(object):
    """ErratumModule"""
    arch = attr.ib(type=str)
    context = attr.ib(type=str)
    name = attr.ib(type=str)
    stream = attr.ib(type=str)
    version = attr.ib(type=str)


@attr.s()
class ErratumPackage(object):
    """ErratumPackage"""
    arch = attr.ib(type=str)
    epoch = attr.ib(type=str, default='0')
    filename = attr.ib(type=str)
    name = attr.ib(type=str)
    version = attr.ib(type=str)
    release = attr.ib(type=str)
    src = attr.ib(type=str)
    md5sum = attr.ib(type=str, default=None)
    sha1sum = attr.ib(type=str, default=None)
    sha256sum = attr.ib(type=str, default=None)


@attr.s()
class ErratumPackageCollection(object):
    """ErratumPackageCollection"""
    module = attr.ib(type=ErratumModule, default=None)
    name = attr.ib(type=str)
    short = attr.ib(type=str, default='')
    packages = attr.ib(type=list)


@attr.s()
class ErratumPushItem(PushItem):
    """ErratumPushItem"""
    type = attr.ib(type=str, default='bugfix')
    release = attr.ib(type=str, default='0')
    status = attr.ib(type=str, default='final')
    pushcount = attr.ib(type=str, default='1')
    reboot_suggested = attr.ib(type=bool, default=False)
    references = attr.ib(type=list, default=(attr.Factory(list)))
    pkglist = attr.ib(type=list, default=(attr.Factory(list)))
    from_ = attr.ib(type=str, default=None)
    rights = attr.ib(type=str, default=None)
    title = attr.ib(type=str, default=None)
    description = attr.ib(type=str, default=None)
    version = attr.ib(type=str, default='1')
    updated = attr.ib(type=str, default=None)
    issued = attr.ib(type=str, default=None)
    severity = attr.ib(type=str, default=None)
    summary = attr.ib(type=str, default=None)
    solution = attr.ib(type=str, default=None)
    content_types = attr.ib(type=list, default=(attr.Factory(list)))

    def __str__(self):
        return '%s: %s' % (self.name, self.title or )