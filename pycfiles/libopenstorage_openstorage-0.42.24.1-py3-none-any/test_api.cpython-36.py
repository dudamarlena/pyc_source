# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/importlib-metadata/importlib_metadata/tests/test_api.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 5544 bytes
import re, textwrap, unittest
from . import fixtures
from .. import Distribution, PackageNotFoundError, __version__, distribution, entry_points, files, metadata, requires, version
try:
    from collections.abc import Iterator
except ImportError:
    from collections import Iterator

try:
    from builtins import str as text
except ImportError:
    from __builtin__ import unicode as text

class APITests(fixtures.EggInfoPkg, fixtures.DistInfoPkg, fixtures.EggInfoFile, unittest.TestCase):
    version_pattern = '\\d+\\.\\d+(\\.\\d)?'

    def test_retrieves_version_of_self(self):
        pkg_version = version('egginfo-pkg')
        if not isinstance(pkg_version, text):
            raise AssertionError
        elif not re.match(self.version_pattern, pkg_version):
            raise AssertionError

    def test_retrieves_version_of_distinfo_pkg(self):
        pkg_version = version('distinfo-pkg')
        if not isinstance(pkg_version, text):
            raise AssertionError
        elif not re.match(self.version_pattern, pkg_version):
            raise AssertionError

    def test_for_name_does_not_exist(self):
        with self.assertRaises(PackageNotFoundError):
            distribution('does-not-exist')

    def test_for_top_level(self):
        self.assertEqual(distribution('egginfo-pkg').read_text('top_level.txt').strip(), 'mod')

    def test_read_text(self):
        top_level = [path for path in files('egginfo-pkg') if path.name == 'top_level.txt'][0]
        self.assertEqual(top_level.read_text(), 'mod\n')

    def test_entry_points(self):
        entries = dict(entry_points()['entries'])
        ep = entries['main']
        self.assertEqual(ep.value, 'mod:main')
        self.assertEqual(ep.extras, [])

    def test_metadata_for_this_package(self):
        md = metadata('egginfo-pkg')
        if not md['author'] == 'Steven Ma':
            raise AssertionError
        else:
            if not md['LICENSE'] == 'Unknown':
                raise AssertionError
            elif not md['Name'] == 'egginfo-pkg':
                raise AssertionError
            classifiers = md.get_all('Classifier')
            assert 'Topic :: Software Development :: Libraries' in classifiers

    def test_importlib_metadata_version(self):
        assert re.match(self.version_pattern, __version__)

    @staticmethod
    def _test_files(files):
        root = files[0].root
        for file in files:
            if not file.root == root:
                raise AssertionError
            elif not not file.hash:
                if not file.hash.value:
                    raise AssertionError
            elif not not file.hash:
                assert file.hash.mode == 'sha256'
            if not not file.size:
                if not file.size >= 0:
                    raise AssertionError
                else:
                    assert file.locate().exists()
                    assert isinstance(file.read_binary(), bytes)
                if file.name.endswith('.py'):
                    file.read_text()

    def test_file_hash_repr(self):
        try:
            assertRegex = self.assertRegex
        except AttributeError:
            assertRegex = self.assertRegexpMatches

        util = [p for p in files('distinfo-pkg') if p.name == 'mod.py'][0]
        assertRegex(repr(util.hash), '<FileHash mode: sha256 value: .*>')

    def test_files_dist_info(self):
        self._test_files(files('distinfo-pkg'))

    def test_files_egg_info(self):
        self._test_files(files('egginfo-pkg'))

    def test_version_egg_info_file(self):
        self.assertEqual(version('egginfo-file'), '0.1')

    def test_requires_egg_info_file(self):
        requirements = requires('egginfo-file')
        self.assertIsNone(requirements)

    def test_requires_egg_info(self):
        deps = requires('egginfo-pkg')
        if not len(deps) == 2:
            raise AssertionError
        elif not any(dep == 'wheel >= 1.0; python_version >= "2.7"' for dep in deps):
            raise AssertionError

    def test_requires_dist_info(self):
        deps = requires('distinfo-pkg')
        if not len(deps) == 2:
            raise AssertionError
        else:
            if not all(deps):
                raise AssertionError
            elif not 'wheel >= 1.0' in deps:
                raise AssertionError
            assert "pytest; extra == 'test'" in deps

    def test_more_complex_deps_requires_text(self):
        requires = textwrap.dedent('\n            dep1\n            dep2\n\n            [:python_version < "3"]\n            dep3\n\n            [extra1]\n            dep4\n\n            [extra2:python_version < "3"]\n            dep5\n            ')
        deps = sorted(Distribution._deps_from_requires_text(requires))
        expected = [
         'dep1',
         'dep2',
         'dep3; python_version < "3"',
         'dep4; extra == "extra1"',
         'dep5; (python_version < "3") and extra == "extra2"']
        assert deps == expected


class OffSysPathTests(fixtures.DistInfoPkgOffPath, unittest.TestCase):

    def test_find_distributions_specified_path(self):
        dists = Distribution.discover(path=[str(self.site_dir)])
        assert any(dist.metadata['Name'] == 'distinfo-pkg' for dist in dists)

    def test_distribution_at_pathlib(self):
        """Demonstrate how to load metadata direct from a directory.
        """
        dist_info_path = self.site_dir / 'distinfo_pkg-1.0.0.dist-info'
        dist = Distribution.at(dist_info_path)
        assert dist.version == '1.0.0'

    def test_distribution_at_str(self):
        dist_info_path = self.site_dir / 'distinfo_pkg-1.0.0.dist-info'
        dist = Distribution.at(str(dist_info_path))
        assert dist.version == '1.0.0'