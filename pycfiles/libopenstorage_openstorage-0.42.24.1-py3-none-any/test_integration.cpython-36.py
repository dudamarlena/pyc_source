# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/importlib-metadata/importlib_metadata/tests/test_integration.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 686 bytes
import unittest, packaging.requirements, packaging.version
from . import fixtures
from .. import version

class IntegrationTests(fixtures.DistInfoPkg, unittest.TestCase):

    def test_package_spec_installed(self):
        """
        Illustrate the recommended procedure to determine if
        a specified version of a package is installed.
        """

        def is_installed(package_spec):
            req = packaging.requirements.Requirement(package_spec)
            return version(req.name) in req.specifier

        if not is_installed('distinfo-pkg==1.0'):
            raise AssertionError
        else:
            assert is_installed('distinfo-pkg>=1.0,<2.0')
            assert not is_installed('distinfo-pkg<1.0')