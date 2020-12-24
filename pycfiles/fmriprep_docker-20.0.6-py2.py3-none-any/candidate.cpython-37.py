# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-hbx1i2h0/pip/pip/_internal/models/candidate.py
# Compiled at: 2020-04-16 14:32:34
# Size of source mod 2**32: 1150 bytes
import pip._vendor.packaging.version as parse_version
from pip._internal.utils.models import KeyBasedCompareMixin
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from pip._vendor.packaging.version import _BaseVersion
    from pip._internal.models.link import Link

class InstallationCandidate(KeyBasedCompareMixin):
    __doc__ = 'Represents a potential "candidate" for installation.\n    '

    def __init__(self, name, version, link):
        self.name = name
        self.version = parse_version(version)
        self.link = link
        super(InstallationCandidate, self).__init__(key=(
         self.name, self.version, self.link),
          defining_class=InstallationCandidate)

    def __repr__(self):
        return '<InstallationCandidate({!r}, {!r}, {!r})>'.format(self.name, self.version, self.link)

    def __str__(self):
        return '{!r} candidate (version {} at {})'.format(self.name, self.version, self.link)