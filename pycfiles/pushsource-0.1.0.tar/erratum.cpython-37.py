# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rmcgover/src/pushsource/src/pushsource/_impl/model/erratum.py
# Compiled at: 2020-01-30 23:16:50
# Size of source mod 2**32: 6014 bytes
from .base import PushItem
from .. import compat_attr as attr

@attr.s()
class ErratumReference(object):
    __doc__ = 'A reference within a :meth:`~ErratumPushItem.references` list.'
    href = attr.ib(type=str)
    type = attr.ib(type=str, default='other')
    id = attr.ib(type=str)
    title = attr.ib(type=str)


@attr.s()
class ErratumModule(object):
    __doc__ = 'A module entry within a :meth:`~ErratumPushItem.pkglist`.'
    arch = attr.ib(type=str)
    context = attr.ib(type=str)
    name = attr.ib(type=str)
    stream = attr.ib(type=str)
    version = attr.ib(type=str)


@attr.s()
class ErratumPackage(object):
    __doc__ = 'A package (RPM) entry within a :meth:`~ErratumPushItem.pkglist`.'
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
    __doc__ = 'A collection of packages found within an :meth:`~ErratumPushItem.pkglist`.\n\n    A non-modular advisory typically contains only a single collection, while modular\n    advisories typically contain one collection per module.\n    '
    module = attr.ib(type=ErratumModule, default=None)
    name = attr.ib(type=str)
    short = attr.ib(type=str, default='')
    packages = attr.ib(type=list)


@attr.s()
class ErratumPushItem(PushItem):
    __doc__ = 'A push item representing a single erratum (also known as "advisory").\n\n    Note that many fields on erratum objects which appear to be numeric\n    are instead represented as strings (\'release\' and \'pushcount\' being two\n    examples).\n    '
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
        return '%s: %s' % (self.name, self.title or '<untitled advisory>')