# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/importlib-metadata/importlib_metadata/tests/fixtures.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 5004 bytes
from __future__ import unicode_literals
import os, sys, shutil, tempfile, textwrap, contextlib
try:
    from contextlib import ExitStack
except ImportError:
    from contextlib2 import ExitStack

try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib

__metaclass__ = type

@contextlib.contextmanager
def tempdir():
    tmpdir = tempfile.mkdtemp()
    try:
        yield pathlib.Path(tmpdir)
    finally:
        shutil.rmtree(tmpdir)


@contextlib.contextmanager
def save_cwd():
    orig = os.getcwd()
    try:
        yield
    finally:
        os.chdir(orig)


@contextlib.contextmanager
def tempdir_as_cwd():
    with tempdir() as (tmp):
        with save_cwd():
            os.chdir(str(tmp))
            yield tmp


class SiteDir:

    def setUp(self):
        self.fixtures = ExitStack()
        self.addCleanup(self.fixtures.close)
        self.site_dir = self.fixtures.enter_context(tempdir())


class OnSysPath:

    @staticmethod
    @contextlib.contextmanager
    def add_sys_path(dir):
        sys.path[:0] = [str(dir)]
        try:
            yield
        finally:
            sys.path.remove(str(dir))

    def setUp(self):
        super(OnSysPath, self).setUp()
        self.fixtures.enter_context(self.add_sys_path(self.site_dir))


class DistInfoPkg(OnSysPath, SiteDir):
    files = {'distinfo_pkg-1.0.0.dist-info':{'METADATA':"\n                Name: distinfo-pkg\n                Author: Steven Ma\n                Version: 1.0.0\n                Requires-Dist: wheel >= 1.0\n                Requires-Dist: pytest; extra == 'test'\n                ", 
      'RECORD':'mod.py,sha256=abc,20\n', 
      'entry_points.txt':'\n                [entries]\n                main = mod:main\n                ns:sub = mod:main\n            '}, 
     'mod.py':'\n            def main():\n                print("hello world")\n            '}

    def setUp(self):
        super(DistInfoPkg, self).setUp()
        build_files(DistInfoPkg.files, self.site_dir)


class DistInfoPkgOffPath(SiteDir):

    def setUp(self):
        super(DistInfoPkgOffPath, self).setUp()
        build_files(DistInfoPkg.files, self.site_dir)


class EggInfoPkg(OnSysPath, SiteDir):
    files = {'egginfo_pkg.egg-info':{'PKG-INFO':'\n                Name: egginfo-pkg\n                Author: Steven Ma\n                License: Unknown\n                Version: 1.0.0\n                Classifier: Intended Audience :: Developers\n                Classifier: Topic :: Software Development :: Libraries\n                ', 
      'SOURCES.txt':'\n                mod.py\n                egginfo_pkg.egg-info/top_level.txt\n            ', 
      'entry_points.txt':'\n                [entries]\n                main = mod:main\n            ', 
      'requires.txt':'\n                wheel >= 1.0; python_version >= "2.7"\n                [test]\n                pytest\n            ', 
      'top_level.txt':'mod\n'}, 
     'mod.py':'\n            def main():\n                print("hello world")\n            '}

    def setUp(self):
        super(EggInfoPkg, self).setUp()
        build_files((EggInfoPkg.files), prefix=(self.site_dir))


class EggInfoFile(OnSysPath, SiteDir):
    files = {'egginfo_file.egg-info': '\n            Metadata-Version: 1.0\n            Name: egginfo_file\n            Version: 0.1\n            Summary: An example package\n            Home-page: www.example.com\n            Author: Eric Haffa-Vee\n            Author-email: eric@example.coms\n            License: UNKNOWN\n            Description: UNKNOWN\n            Platform: UNKNOWN\n            '}

    def setUp(self):
        super(EggInfoFile, self).setUp()
        build_files((EggInfoFile.files), prefix=(self.site_dir))


def build_files(file_defs, prefix=pathlib.Path()):
    """Build a set of files/directories, as described by the

    file_defs dictionary.  Each key/value pair in the dictionary is
    interpreted as a filename/contents pair.  If the contents value is a
    dictionary, a directory is created, and the dictionary interpreted
    as the files within it, recursively.

    For example:

    {"README.txt": "A README file",
     "foo": {
        "__init__.py": "",
        "bar": {
            "__init__.py": "",
        },
        "baz.py": "# Some code",
     }
    }
    """
    for name, contents in file_defs.items():
        full_name = prefix / name
        if isinstance(contents, dict):
            full_name.mkdir()
            build_files(contents, prefix=full_name)
        elif isinstance(contents, bytes):
            with full_name.open('wb') as (f):
                f.write(contents)
        else:
            with full_name.open('w') as (f):
                f.write(DALS(contents))


def DALS(str):
    """Dedent and left-strip"""
    return textwrap.dedent(str).lstrip()