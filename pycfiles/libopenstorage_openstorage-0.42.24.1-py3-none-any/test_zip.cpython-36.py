# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/importlib-metadata/importlib_metadata/tests/test_zip.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 2372 bytes
import sys, unittest
from .. import distribution, entry_points, files, PackageNotFoundError, version
try:
    from importlib.resources import path
except ImportError:
    from importlib_resources import path

try:
    from contextlib import ExitStack
except ImportError:
    from contextlib2 import ExitStack

class TestZip(unittest.TestCase):
    root = 'importlib_metadata.tests.data'

    def setUp(self):
        self.resources = ExitStack()
        self.addCleanup(self.resources.close)
        wheel = self.resources.enter_context(path(self.root, 'example-21.12-py3-none-any.whl'))
        sys.path.insert(0, str(wheel))
        self.resources.callback(sys.path.pop, 0)

    def test_zip_version(self):
        self.assertEqual(version('example'), '21.12')

    def test_zip_version_does_not_match(self):
        with self.assertRaises(PackageNotFoundError):
            version('definitely-not-installed')

    def test_zip_entry_points(self):
        scripts = dict(entry_points()['console_scripts'])
        entry_point = scripts['example']
        self.assertEqual(entry_point.value, 'example:main')
        entry_point = scripts['Example']
        self.assertEqual(entry_point.value, 'example:main')

    def test_missing_metadata(self):
        self.assertIsNone(distribution('example').read_text('does not exist'))

    def test_case_insensitive(self):
        self.assertEqual(version('Example'), '21.12')

    def test_files(self):
        for file in files('example'):
            path = str(file.dist.locate_file(file))
            assert '.whl/' in path, path


class TestEgg(TestZip):

    def setUp(self):
        self.resources = ExitStack()
        self.addCleanup(self.resources.close)
        egg = self.resources.enter_context(path(self.root, 'example-21.12-py3.6.egg'))
        sys.path.insert(0, str(egg))
        self.resources.callback(sys.path.pop, 0)

    def test_files(self):
        for file in files('example'):
            path = str(file.dist.locate_file(file))
            assert '.egg/' in path, path