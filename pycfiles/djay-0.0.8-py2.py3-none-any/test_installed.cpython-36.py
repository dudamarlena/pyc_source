# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/pkginfo/pkginfo/tests/test_installed.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 5661 bytes
import unittest

class InstalledTests(unittest.TestCase):

    def _getTargetClass(self):
        from pkginfo.installed import Installed
        return Installed

    def _makeOne(self, filename=None, metadata_version=None):
        if metadata_version is not None:
            return self._getTargetClass()(filename, metadata_version)
        else:
            return self._getTargetClass()(filename)

    def test_ctor_w_package_no___file__(self):
        import sys, warnings
        with warnings.catch_warnings(record=True):
            installed = self._makeOne(sys)
            self.assertEqual(installed.package, sys)
            self.assertEqual(installed.package_name, 'sys')
            self.assertEqual(installed.metadata_version, None)

    def test_ctor_w_package(self):
        import pkginfo
        from pkginfo.tests import _checkSample
        from pkginfo.tests import _defaultMetadataVersion
        EXPECTED = _defaultMetadataVersion()
        installed = self._makeOne(pkginfo)
        self.assertEqual(installed.package, pkginfo)
        self.assertEqual(installed.package_name, 'pkginfo')
        self.assertEqual(installed.metadata_version, EXPECTED)
        _checkSample(self, installed)

    def test_ctor_w_no___package___falls_back_to___name__(self):
        import sys, wsgiref, warnings
        with warnings.catch_warnings(record=True):
            installed = self._makeOne(wsgiref)
            self.assertEqual(installed.package, wsgiref)
            self.assertEqual(installed.package_name, 'wsgiref')
            if sys.version_info[:2] >= (3, 3):
                self.assertEqual(installed.metadata_version, None)
            else:
                self.assertEqual(installed.metadata_version, '1.0')

    def test_ctor_w_package_no_PKG_INFO(self):
        import sys, types, warnings
        with warnings.catch_warnings(record=True):
            installed = self._makeOne(types)
            self.assertEqual(installed.package, types)
            self.assertEqual(installed.package_name, 'types')
            if sys.version_info[:2] >= (3, 3):
                self.assertEqual(installed.metadata_version, '2.1')
            else:
                self.assertEqual(installed.metadata_version, None)

    def test_ctor_w_package_and_metadata_version(self):
        import pkginfo
        from pkginfo.tests import _checkSample
        installed = self._makeOne(pkginfo, metadata_version='1.2')
        self.assertEqual(installed.metadata_version, '1.2')
        self.assertEqual(installed.package.__name__, 'pkginfo')
        _checkSample(self, installed)

    def test_ctor_w_name(self):
        import pkginfo
        from pkginfo.tests import _checkSample
        from pkginfo.tests import _defaultMetadataVersion
        EXPECTED = _defaultMetadataVersion()
        installed = self._makeOne('pkginfo')
        self.assertEqual(installed.metadata_version, EXPECTED)
        self.assertEqual(installed.package, pkginfo)
        self.assertEqual(installed.package_name, 'pkginfo')
        _checkSample(self, installed)

    def test_ctor_w_name_and_metadata_version(self):
        import pkginfo
        from pkginfo.tests import _checkSample
        installed = self._makeOne('pkginfo', metadata_version='1.2')
        self.assertEqual(installed.metadata_version, '1.2')
        self.assertEqual(installed.package, pkginfo)
        self.assertEqual(installed.package_name, 'pkginfo')
        _checkSample(self, installed)

    def test_ctor_w_invalid_name(self):
        import warnings
        with warnings.catch_warnings(record=True):
            installed = self._makeOne('nonesuch')
            self.assertEqual(installed.package, None)
            self.assertEqual(installed.package_name, 'nonesuch')
            self.assertEqual(installed.metadata_version, None)

    def test_ctor_w_egg_info_as_file(self):
        import pkginfo.tests.funny
        installed = self._makeOne('pkginfo.tests.funny')
        self.assertEqual(installed.metadata_version, '1.0')
        self.assertEqual(installed.package, pkginfo.tests.funny)
        self.assertEqual(installed.package_name, 'pkginfo.tests.funny')

    def test_namespaced_pkg_installed_via_setuptools(self):
        import os, sys
        where, _ = os.path.split(__file__)
        wonky = os.path.join(where, 'wonky')
        oldpath = sys.path[:]
        try:
            sys.path.append(wonky)
            import namespaced.wonky
            installed = self._makeOne('namespaced.wonky')
            self.assertEqual(installed.metadata_version, '1.0')
            self.assertEqual(installed.package, namespaced.wonky)
            self.assertEqual(installed.package_name, 'namespaced.wonky')
        finally:
            sys.path[:] = oldpath
            sys.modules.pop('namespaced.wonky', None)
            sys.modules.pop('namespaced', None)

    def test_namespaced_pkg_installed_via_pth(self):
        import os, sys
        where, _ = os.path.split(__file__)
        manky = os.path.join(where, 'manky')
        oldpath = sys.path[:]
        try:
            sys.path.append(manky)
            import namespaced.manky
            installed = self._makeOne('namespaced.manky')
            self.assertEqual(installed.metadata_version, '1.0')
            self.assertEqual(installed.package, namespaced.manky)
            self.assertEqual(installed.package_name, 'namespaced.manky')
        finally:
            sys.path[:] = oldpath
            sys.modules.pop('namespaced.manky', None)
            sys.modules.pop('namespaced', None)