# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_internal/resolution/resolvelib/provider.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 1703 bytes
from pip._vendor.resolvelib.providers import AbstractProvider
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Any, Optional, Sequence, Tuple, Union
    from pip._internal.req.req_install import InstallRequirement
    from .base import Requirement, Candidate
    from .factory import Factory

class PipProvider(AbstractProvider):

    def __init__(self, factory, ignore_dependencies):
        self._factory = factory
        self._ignore_dependencies = ignore_dependencies

    def get_install_requirement(self, c):
        return c.get_install_requirement()

    def identify(self, dependency):
        return dependency.name

    def get_preference(self, resolution, candidates, information):
        return len(candidates)

    def find_matches(self, requirement):
        return requirement.find_matches()

    def is_satisfied_by(self, requirement, candidate):
        return requirement.is_satisfied_by(candidate)

    def get_dependencies(self, candidate):
        if self._ignore_dependencies:
            return []
        return candidate.get_dependencies()