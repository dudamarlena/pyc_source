# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/pip/pip/_internal/distributions/installed.py
# Compiled at: 2020-02-14 17:24:54
# Size of source mod 2**32: 760 bytes
from pip._internal.distributions.base import AbstractDistribution
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Optional
    from pip._vendor.pkg_resources import Distribution
    from pip._internal.index.package_finder import PackageFinder

class InstalledDistribution(AbstractDistribution):
    __doc__ = 'Represents an installed package.\n\n    This does not need any preparation as the required information has already\n    been computed.\n    '

    def get_pkg_resources_distribution(self):
        return self.req.satisfied_by

    def prepare_distribution_metadata(self, finder, build_isolation):
        pass