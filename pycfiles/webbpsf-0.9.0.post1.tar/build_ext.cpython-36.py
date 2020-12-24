# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rgeda/project/repo/webbpsf/astropy_helpers/astropy_helpers/commands/build_ext.py
# Compiled at: 2019-07-20 17:47:20
# Size of source mod 2**32: 19715 bytes
import errno, os, re, shlex, shutil, subprocess, sys, textwrap
from distutils import log, ccompiler, sysconfig
from distutils.core import Extension
from distutils.ccompiler import get_default_compiler
from setuptools.command.build_ext import build_ext as SetuptoolsBuildExt
from setuptools.command import build_py
from ..utils import get_numpy_include_path, invalidate_caches, classproperty
from ..version_helpers import get_pkg_version_module

def should_build_with_cython(package, release=None):
    """Returns the previously used Cython version (or 'unknown' if not
    previously built) if Cython should be used to build extension modules from
    pyx files.  If the ``release`` parameter is not specified an attempt is
    made to determine the release flag from `astropy.version`.
    """
    try:
        version_module = __import__((package + '.cython_version'), fromlist=[
         'release', 'cython_version'])
    except ImportError:
        version_module = None

    if release is None:
        if version_module is not None:
            try:
                release = version_module.release
            except AttributeError:
                pass

    try:
        cython_version = version_module.cython_version
    except AttributeError:
        cython_version = 'unknown'

    have_cython = False
    try:
        import Cython
        have_cython = True
    except ImportError:
        pass

    if have_cython:
        if not release or cython_version == 'unknown':
            return cython_version
    return False


_compiler_versions = {}

def get_compiler_version(compiler):
    if compiler in _compiler_versions:
        return _compiler_versions[compiler]
    else:
        flags = [
         '--version', '--Version', '-version', '-Version',
         '-v', '-V']

        def try_get_version(flag):
            process = subprocess.Popen((shlex.split(compiler, posix=('win' not in sys.platform)) + [flag]),
              stdout=(subprocess.PIPE),
              stderr=(subprocess.PIPE))
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                return 'unknown'
            else:
                output = stdout.strip().decode('latin-1')
                if not output:
                    output = stderr.strip().decode('latin-1')
                if not output:
                    output = 'unknown'
                return output

        for flag in flags:
            version = try_get_version(flag)
            if version != 'unknown':
                break

        _compiler_versions[compiler] = version
        return version


def generate_build_ext_command(packagename, release):
    """
    Creates a custom 'build_ext' command that allows for manipulating some of
    the C extension options at build time.  We use a function to build the
    class since the base class for build_ext may be different depending on
    certain build-time parameters (for example, we may use Cython's build_ext
    instead of the default version in distutils).

    Uses the default distutils.command.build_ext by default.
    """

    class build_ext(SetuptoolsBuildExt):
        package_name = packagename
        is_release = release
        _user_options = SetuptoolsBuildExt.user_options[:]
        _boolean_options = SetuptoolsBuildExt.boolean_options[:]
        _help_options = SetuptoolsBuildExt.help_options[:]
        force_rebuild = False
        _broken_compiler_mapping = [
         ('i686-apple-darwin[0-9]*-llvm-gcc-4.2', 'clang')]

        @classproperty
        def user_options(cls):
            from distutils import core
            if core._setup_distribution is None:
                return cls._user_options
            else:
                return cls._final_class.user_options

        @classproperty
        def boolean_options(cls):
            from distutils import core
            if core._setup_distribution is None:
                return cls._boolean_options
            else:
                return cls._final_class.boolean_options

        @classproperty
        def help_options(cls):
            from distutils import core
            if core._setup_distribution is None:
                return cls._help_options
            else:
                return cls._final_class.help_options

        @classproperty(lazy=True)
        def _final_class(cls):
            uses_cython = should_build_with_cython(cls.package_name, cls.is_release)
            if uses_cython:
                try:
                    from Cython.Distutils.old_build_ext import old_build_ext as base_cls
                except ImportError:
                    from Cython.Distutils import build_ext as base_cls

            else:
                base_cls = SetuptoolsBuildExt

            def merge_options(attr):
                base = getattr(base_cls, attr)
                ours = getattr(cls, '_' + attr)
                all_base = set(opt[0] for opt in base)
                return base + [opt for opt in ours if opt[0] not in all_base]

            boolean_options = base_cls.boolean_options + [opt for opt in cls._boolean_options if opt not in base_cls.boolean_options]
            members = dict(cls.__dict__)
            members.update({'user_options':merge_options('user_options'), 
             'help_options':merge_options('help_options'), 
             'boolean_options':boolean_options, 
             'uses_cython':uses_cython})
            build_ext.__bases__ = (
             base_cls, object)
            return type(cls.__name__, (build_ext,), members)

        def __new__(cls, *args, **kwargs):
            new_cls = super(build_ext, cls._final_class).__new__(cls._final_class)
            (new_cls.__init__)(*args, **kwargs)
            return new_cls

        def finalize_options(self):
            self._adjust_compiler()
            extensions = self.distribution.ext_modules
            if extensions:
                build_py = self.get_finalized_command('build_py')
                package_dir = build_py.get_package_dir(packagename)
                src_path = os.path.relpath(os.path.join(os.path.dirname(__file__), 'src'))
                shutil.copy(os.path.join(src_path, 'compiler.c'), os.path.join(package_dir, '_compiler.c'))
                ext = Extension(self.package_name + '._compiler', [
                 os.path.join(package_dir, '_compiler.c')])
                extensions.insert(0, ext)
            super(build_ext, self).finalize_options()
            if self.uses_cython:
                try:
                    from Cython import __version__ as cython_version
                except ImportError:
                    cython_version = None

                if cython_version is not None:
                    if cython_version != self.uses_cython:
                        self.force_rebuild = True
                        self.uses_cython = cython_version
            if self.force_rebuild:
                self.force = True

        def run(self):
            np_include = get_numpy_include_path()
            for extension in self.extensions:
                if 'numpy' in extension.include_dirs:
                    idx = extension.include_dirs.index('numpy')
                    extension.include_dirs.insert(idx, np_include)
                    extension.include_dirs.remove('numpy')
                self._check_cython_sources(extension)

            super(build_ext, self).run()
            try:
                cython_version = get_pkg_version_module(packagename,
                  fromlist=['cython_version'])[0]
            except (AttributeError, ImportError):
                cython_version = 'unknown'

            if self.uses_cython and self.uses_cython != cython_version:
                build_py = self.get_finalized_command('build_py')
                package_dir = build_py.get_package_dir(packagename)
                cython_py = os.path.join(package_dir, 'cython_version.py')
                with open(cython_py, 'w') as (f):
                    f.write('# Generated file; do not modify\n')
                    f.write('cython_version = {0!r}\n'.format(self.uses_cython))
                if os.path.isdir(self.build_lib):
                    self.copy_file(cython_py, (os.path.join(self.build_lib, cython_py)),
                      preserve_mode=False)
                invalidate_caches()

        def _adjust_compiler(self):
            """
            This function detects broken compilers and switches to another.  If
            the environment variable CC is explicitly set, or a compiler is
            specified on the commandline, no override is performed -- the
            purpose here is to only override a default compiler.

            The specific compilers with problems are:

                * The default compiler in XCode-4.2, llvm-gcc-4.2,
                  segfaults when compiling wcslib.

            The set of broken compilers can be updated by changing the
            compiler_mapping variable.  It is a list of 2-tuples where the
            first in the pair is a regular expression matching the version of
            the broken compiler, and the second is the compiler to change to.
            """
            if 'CC' in os.environ:
                c_compiler = os.environ['CC']
                try:
                    version = get_compiler_version(c_compiler)
                except OSError:
                    msg = textwrap.dedent('\n                        The C compiler set by the CC environment variable:\n\n                            {compiler:s}\n\n                        cannot be found or executed.\n                        '.format(compiler=c_compiler))
                    log.warn(msg)
                    sys.exit(1)

                for broken, fixed in self._broken_compiler_mapping:
                    if re.match(broken, version):
                        msg = textwrap.dedent('Compiler specified by CC environment variable\n                            ({compiler:s}:{version:s}) will fail to compile\n                            {pkg:s}.\n\n                            Please set CC={fixed:s} and try again.\n                            You can do this, for example, by running:\n\n                                CC={fixed:s} python setup.py <command>\n\n                            where <command> is the command you ran.\n                            '.format(compiler=c_compiler, version=version, pkg=(self.package_name),
                          fixed=fixed))
                        log.warn(msg)
                        sys.exit(1)

                return
            else:
                if self.compiler is not None:
                    return
                compiler_type = ccompiler.get_default_compiler()
                if compiler_type == 'unix':
                    c_compiler = sysconfig.get_config_var('CC')
                    try:
                        version = get_compiler_version(c_compiler)
                    except OSError:
                        msg = textwrap.dedent('\n                        The C compiler used to compile Python {compiler:s}, and\n                        which is normally used to compile C extensions, is not\n                        available. You can explicitly specify which compiler to\n                        use by setting the CC environment variable, for example:\n\n                            CC=gcc python setup.py <command>\n\n                        or if you are using MacOS X, you can try:\n\n                            CC=clang python setup.py <command>\n                        '.format(compiler=c_compiler))
                        log.warn(msg)
                        sys.exit(1)

                    for broken, fixed in self._broken_compiler_mapping:
                        if re.match(broken, version):
                            os.environ['CC'] = fixed
                            break

        def _check_cython_sources(self, extension):
            """
            Where relevant, make sure that the .c files associated with .pyx
            modules are present (if building without Cython installed).
            """
            if self.compiler is None:
                compiler = get_default_compiler()
            else:
                compiler = self.compiler
            for jdx, src in enumerate(extension.sources):
                base, ext = os.path.splitext(src)
                pyxfn = base + '.pyx'
                cfn = base + '.c'
                cppfn = base + '.cpp'
                if not os.path.isfile(pyxfn):
                    pass
                else:
                    if self.uses_cython:
                        extension.sources[jdx] = pyxfn
                    else:
                        if os.path.isfile(cfn):
                            extension.sources[jdx] = cfn
                        else:
                            if os.path.isfile(cppfn):
                                extension.sources[jdx] = cppfn
                            else:
                                msg = 'Could not find C/C++ file {0}.(c/cpp) for Cython file {1} when building extension {2}. Cython must be installed to build from a git checkout.'.format(base, pyxfn, extension.name)
                                raise IOError(errno.ENOENT, msg, cfn)
                if compiler == 'unix':
                    extension.extra_compile_args.extend([
                     '-Wp,-w', '-Wno-unused-function'])

    return build_ext