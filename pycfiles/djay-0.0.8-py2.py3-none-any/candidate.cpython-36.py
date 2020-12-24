# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/pip/pip/_internal/models/candidate.py
# Compiled at: 2019-07-30 18:46:55
# Size of source mod 2**32: 1169 bytes
from pip._vendor.packaging.version import parse as parse_version
from pip._internal.utils.models import KeyBasedCompareMixin
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from pip._vendor.packaging.version import _BaseVersion
    from pip._internal.models.link import Link
    from typing import Any

class InstallationCandidate(KeyBasedCompareMixin):
    __doc__ = 'Represents a potential "candidate" for installation.\n    '

    def __init__(self, project, version, link):
        self.project = project
        self.version = parse_version(version)
        self.link = link
        super(InstallationCandidate, self).__init__(key=(
         self.project, self.version, self.link),
          defining_class=InstallationCandidate)

    def __repr__(self):
        return '<InstallationCandidate({!r}, {!r}, {!r})>'.format(self.project, self.version, self.link)

    def __str__(self):
        return '{!r} candidate (version {} at {})'.format(self.project, self.version, self.link)