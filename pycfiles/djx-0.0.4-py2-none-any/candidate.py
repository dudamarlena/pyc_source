# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_internal/models/candidate.py
# Compiled at: 2019-02-14 00:35:06
from pip._vendor.packaging.version import parse as parse_version
from pip._internal.utils.models import KeyBasedCompareMixin
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from pip._vendor.packaging.version import _BaseVersion
    from pip._internal.models.link import Link
    from typing import Any, Union

class InstallationCandidate(KeyBasedCompareMixin):
    """Represents a potential "candidate" for installation.
    """

    def __init__(self, project, version, location):
        self.project = project
        self.version = parse_version(version)
        self.location = location
        super(InstallationCandidate, self).__init__(key=(
         self.project, self.version, self.location), defining_class=InstallationCandidate)

    def __repr__(self):
        return ('<InstallationCandidate({!r}, {!r}, {!r})>').format(self.project, self.version, self.location)