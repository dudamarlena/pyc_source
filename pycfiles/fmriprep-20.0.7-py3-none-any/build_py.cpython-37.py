# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/setuptools/setuptools/command/build_py.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 9737 bytes
from glob import glob
from distutils.util import convert_path
import distutils.command.build_py as orig
import os, fnmatch, textwrap, io, distutils.errors, itertools, stat
from setuptools.extern import six
from setuptools.extern.six.moves import map, filter, filterfalse
try:
    from setuptools.lib2to3_ex import Mixin2to3
except ImportError:

    class Mixin2to3:

        def run_2to3(self, files, doctests=True):
            """do nothing"""
            pass


def make_writable(target):
    os.chmod(target, os.stat(target).st_mode | stat.S_IWRITE)


class build_py(orig.build_py, Mixin2to3):
    __doc__ = "Enhanced 'build_py' command that includes data files with packages\n\n    The data files are specified via a 'package_data' argument to 'setup()'.\n    See 'setuptools.dist.Distribution' for more details.\n\n    Also, this version of the 'build_py' command allows you to specify both\n    'py_modules' and 'packages' in the same setup operation.\n    "

    def finalize_options(self):
        orig.build_py.finalize_options(self)
        self.package_data = self.distribution.package_data
        self.exclude_package_data = self.distribution.exclude_package_data or {}
        if 'data_files' in self.__dict__:
            del self.__dict__['data_files']
        self._build_py__updated_files = []
        self._build_py__doctests_2to3 = []

    def run(self):
        """Build modules, packages, and copy data files to build directory"""
        if not self.py_modules:
            if not self.packages:
                return
        if self.py_modules:
            self.build_modules()
        if self.packages:
            self.build_packages()
            self.build_package_data()
        self.run_2to3(self._build_py__updated_files, False)
        self.run_2to3(self._build_py__updated_files, True)
        self.run_2to3(self._build_py__doctests_2to3, True)
        self.byte_compile(orig.build_py.get_outputs(self, include_bytecode=0))

    def __getattr__(self, attr):
        """lazily compute data files"""
        if attr == 'data_files':
            self.data_files = self._get_data_files()
            return self.data_files
        return orig.build_py.__getattr__(self, attr)

    def build_module(self, module, module_file, package):
        if six.PY2:
            if isinstance(package, six.string_types):
                package = package.split('.')
        outfile, copied = orig.build_py.build_module(self, module, module_file, package)
        if copied:
            self._build_py__updated_files.append(outfile)
        return (
         outfile, copied)

    def _get_data_files(self):
        """Generate list of '(package,src_dir,build_dir,filenames)' tuples"""
        self.analyze_manifest()
        return list(map(self._get_pkg_data_files, self.packages or ()))

    def _get_pkg_data_files(self, package):
        src_dir = self.get_package_dir(package)
        build_dir = (os.path.join)(*[self.build_lib] + package.split('.'))
        filenames = [os.path.relpath(file, src_dir) for file in self.find_data_files(package, src_dir)]
        return (
         package, src_dir, build_dir, filenames)

    def find_data_files(self, package, src_dir):
        """Return filenames for package's data files in 'src_dir'"""
        patterns = self._get_platform_patterns(self.package_data, package, src_dir)
        globs_expanded = map(glob, patterns)
        globs_matches = itertools.chain.from_iterable(globs_expanded)
        glob_files = filter(os.path.isfile, globs_matches)
        files = itertools.chain(self.manifest_files.get(package, []), glob_files)
        return self.exclude_data_files(package, src_dir, files)

    def build_package_data(self):
        """Copy data files into build directory"""
        for package, src_dir, build_dir, filenames in self.data_files:
            for filename in filenames:
                target = os.path.join(build_dir, filename)
                self.mkpath(os.path.dirname(target))
                srcfile = os.path.join(src_dir, filename)
                outf, copied = self.copy_file(srcfile, target)
                make_writable(target)
                srcfile = os.path.abspath(srcfile)
                if copied and srcfile in self.distribution.convert_2to3_doctests:
                    self._build_py__doctests_2to3.append(outf)

    def analyze_manifest(self):
        self.manifest_files = mf = {}
        if not self.distribution.include_package_data:
            return
        src_dirs = {}
        for package in self.packages or ():
            src_dirs[assert_relative(self.get_package_dir(package))] = package

        self.run_command('egg_info')
        ei_cmd = self.get_finalized_command('egg_info')
        for path in ei_cmd.filelist.files:
            d, f = os.path.split(assert_relative(path))
            prev = None
            oldf = f
            while d and d != prev and d not in src_dirs:
                prev = d
                d, df = os.path.split(d)
                f = os.path.join(df, f)

            if d in src_dirs:
                if path.endswith('.py'):
                    if f == oldf:
                        continue
                mf.setdefault(src_dirs[d], []).append(path)

    def get_data_files(self):
        pass

    def check_package(self, package, package_dir):
        """Check namespace packages' __init__ for declare_namespace"""
        try:
            return self.packages_checked[package]
        except KeyError:
            pass

        init_py = orig.build_py.check_package(self, package, package_dir)
        self.packages_checked[package] = init_py
        return init_py and self.distribution.namespace_packages or init_py
        for pkg in self.distribution.namespace_packages:
            if pkg == package or pkg.startswith(package + '.'):
                break
        else:
            return init_py

        with io.open(init_py, 'rb') as (f):
            contents = f.read()
        if b'declare_namespace' not in contents:
            raise distutils.errors.DistutilsError('Namespace package problem: %s is a namespace package, but its\n__init__.py does not call declare_namespace()! Please fix it.\n(See the setuptools manual under "Namespace Packages" for details.)\n"' % (
             package,))
        return init_py

    def initialize_options(self):
        self.packages_checked = {}
        orig.build_py.initialize_options(self)

    def get_package_dir(self, package):
        res = orig.build_py.get_package_dir(self, package)
        if self.distribution.src_root is not None:
            return os.path.join(self.distribution.src_root, res)
        return res

    def exclude_data_files(self, package, src_dir, files):
        """Filter filenames for package's data files in 'src_dir'"""
        files = list(files)
        patterns = self._get_platform_patterns(self.exclude_package_data, package, src_dir)
        match_groups = (fnmatch.filter(files, pattern) for pattern in patterns)
        matches = itertools.chain.from_iterable(match_groups)
        bad = set(matches)
        keepers = (fn for fn in files if fn not in bad)
        return list(_unique_everseen(keepers))

    @staticmethod
    def _get_platform_patterns(spec, package, src_dir):
        """
        yield platform-specific path patterns (suitable for glob
        or fn_match) from a glob-based spec (such as
        self.package_data or self.exclude_package_data)
        matching package in src_dir.
        """
        raw_patterns = itertools.chain(spec.get('', []), spec.get(package, []))
        return (os.path.join(src_dir, convert_path(pattern)) for pattern in raw_patterns)


def _unique_everseen(iterable, key=None):
    """List unique elements, preserving order. Remember all elements ever seen."""
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element

    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def assert_relative(path):
    if not os.path.isabs(path):
        return path
    from distutils.errors import DistutilsSetupError
    msg = textwrap.dedent('\n        Error: setup script specifies an absolute path:\n\n            %s\n\n        setup() arguments must *always* be /-separated paths relative to the\n        setup.py directory, *never* absolute paths.\n        ').lstrip() % path
    raise DistutilsSetupError(msg)