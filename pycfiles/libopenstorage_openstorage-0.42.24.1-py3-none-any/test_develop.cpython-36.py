# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pkginfo/pkginfo/tests/test_develop.py
# Compiled at: 2020-01-10 16:25:33
# Size of source mod 2**32: 831 bytes
import unittest

class DevelopTests(unittest.TestCase):

    def _getTargetClass(self):
        from pkginfo.develop import Develop
        return Develop

    def _makeOne(self, dirname=None):
        return self._getTargetClass()(dirname)

    def test_ctor_w_path(self):
        from pkginfo.tests import _checkSample
        develop = self._makeOne('.')
        _checkSample(self, develop)

    def test_ctor_w_invalid_path(self):
        import warnings
        old_filters = warnings.filters[:]
        warnings.filterwarnings('ignore')
        try:
            develop = self._makeOne('/nonesuch')
            self.assertEqual(develop.metadata_version, None)
            self.assertEqual(develop.name, None)
            self.assertEqual(develop.version, None)
        finally:
            warnings.filters[:] = old_filters