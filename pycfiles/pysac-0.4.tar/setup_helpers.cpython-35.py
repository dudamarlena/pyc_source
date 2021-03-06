# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stuart/Git/SWAT/pysac/astropy_helpers/astropy_helpers/setup_helpers.py
# Compiled at: 2015-11-25 06:17:20
# Size of source mod 2**32: 57177 bytes
"""
This module contains a number of utilities for use during
setup/build/packaging that are useful to astropy as a whole.
"""
from __future__ import absolute_import, print_function
import collections, errno, imp, inspect, os, pkgutil, re, shlex, shutil, subprocess, sys, textwrap
from distutils import log, ccompiler, sysconfig
from distutils.cmd import DistutilsOptionError
from distutils.dist import Distribution
from distutils.errors import DistutilsError, DistutilsFileError
from distutils.core import Extension
from distutils.core import Command
from distutils.command.sdist import sdist as DistutilsSdist
from distutils.version import StrictVersion
from setuptools.command.build_ext import build_ext as SetuptoolsBuildExt
from setuptools.command.build_py import build_py as SetuptoolsBuildPy
from setuptools.command.install import install as SetuptoolsInstall
from setuptools.command.install_lib import install_lib as SetuptoolsInstallLib
from setuptools.command.register import register as SetuptoolsRegister
from setuptools import find_packages
from .test_helpers import AstropyTest
from .utils import silence, invalidate_caches, walk_skip_hidden
_module_state = {'adjusted_compiler': False, 
 'registered_commands': None, 
 'have_cython': False, 
 'have_sphinx': False}
try:
    import Cython
    _module_state['have_cython'] = True
except ImportError:
    pass

try:
    import sphinx
    from sphinx.setup_command import BuildDoc as SphinxBuildDoc
    _module_state['have_sphinx'] = True
except ValueError as e:
    if 'unknown locale' in e.args[0]:
        log.warn("Possible misconfiguration of one of the environment variables LC_ALL, LC_CTYPES, LANG, or LANGUAGE.  For an example of how to configure your system's language environment on OSX see http://blog.remibergsma.com/2012/07/10/setting-locales-correctly-on-mac-osx-terminal-application/")
except ImportError:
    pass
except SyntaxError:
    pass

PY3 = sys.version_info[0] >= 3
Distribution.skip_2to3 = []

def adjust_compiler(package):
    """
    This function detects broken compilers and switches to another.  If
    the environment variable CC is explicitly set, or a compiler is
    specified on the commandline, no override is performed -- the purpose
    here is to only override a default compiler.

    The specific compilers with problems are:

        * The default compiler in XCode-4.2, llvm-gcc-4.2,
          segfaults when compiling wcslib.

    The set of broken compilers can be updated by changing the
    compiler_mapping variable.  It is a list of 2-tuples where the
    first in the pair is a regular expression matching the version
    of the broken compiler, and the second is the compiler to change
    to.
    """
    compiler_mapping = [
     (b'i686-apple-darwin[0-9]*-llvm-gcc-4.2', 'clang')]
    if _module_state['adjusted_compiler']:
        return
    _module_state['adjusted_compiler'] = True
    if 'CC' in os.environ:
        c_compiler = os.environ['CC']
        try:
            version = get_compiler_version(c_compiler)
        except OSError:
            msg = textwrap.dedent('\n                    The C compiler set by the CC environment variable:\n\n                        {compiler:s}\n\n                    cannot be found or executed.\n                    '.format(compiler=c_compiler))
            log.warn(msg)
            sys.exit(1)

        for broken, fixed in compiler_mapping:
            if re.match(broken, version):
                msg = textwrap.dedent('Compiler specified by CC environment variable\n                    ({compiler:s}:{version:s}) will fail to compile {pkg:s}.\n                    Please set CC={fixed:s} and try again.\n                    You can do this, for example, by running:\n\n                        CC={fixed:s} python setup.py <command>\n\n                    where <command> is the command you ran.\n                    '.format(compiler=c_compiler, version=version, pkg=package, fixed=fixed))
                log.warn(msg)
                sys.exit(1)

        return
    if get_distutils_build_option('compiler'):
        return
    compiler_type = ccompiler.get_default_compiler()
    if compiler_type == 'unix':
        c_compiler = sysconfig.get_config_var('CC')
        try:
            version = get_compiler_version(c_compiler)
        except OSError:
            msg = textwrap.dedent('\n                    The C compiler used to compile Python {compiler:s}, and\n                    which is normally used to compile C extensions, is not\n                    available. You can explicitly specify which compiler to\n                    use by setting the CC environment variable, for example:\n\n                        CC=gcc python setup.py <command>\n\n                    or if you are using MacOS X, you can try:\n\n                        CC=clang python setup.py <command>\n                    '.format(compiler=c_compiler))
            log.warn(msg)
            sys.exit(1)

        for broken, fixed in compiler_mapping:
            if re.match(broken, version):
                os.environ['CC'] = fixed
                break


def get_compiler_version(compiler):
    process = subprocess.Popen(shlex.split(compiler) + ['--version'], stdout=subprocess.PIPE)
    output = process.communicate()[0].strip()
    try:
        version = output.split()[0]
    except IndexError:
        return 'unknown'

    return version


def get_dummy_distribution():
    """Returns a distutils Distribution object used to instrument the setup
    environment before calling the actual setup() function.
    """
    if _module_state['registered_commands'] is None:
        raise RuntimeError('astropy_helpers.setup_helpers.register_commands() must be called before using astropy_helpers.setup_helpers.get_dummy_distribution()')
    dist = Distribution({'script_name': os.path.basename(sys.argv[0]), 
     'script_args': sys.argv[1:]})
    dist.cmdclass.update(_module_state['registered_commands'])
    with silence():
        try:
            dist.parse_config_files()
            dist.parse_command_line()
        except (DistutilsError, AttributeError, SystemExit):
            pass

    return dist


def get_distutils_option(option, commands):
    """ Returns the value of the given distutils option.

    Parameters
    ----------
    option : str
        The name of the option

    commands : list of str
        The list of commands on which this option is available

    Returns
    -------
    val : str or None
        the value of the given distutils option. If the option is not set,
        returns None.
    """
    dist = get_dummy_distribution()
    for cmd in commands:
        cmd_opts = dist.command_options.get(cmd)
        if cmd_opts is not None and option in cmd_opts:
            return cmd_opts[option][1]
    else:
        return


def get_distutils_build_option(option):
    """ Returns the value of the given distutils build option.

    Parameters
    ----------
    option : str
        The name of the option

    Returns
    -------
    val : str or None
        The value of the given distutils build option. If the option
        is not set, returns None.
    """
    return get_distutils_option(option, ['build', 'build_ext', 'build_clib'])


def get_distutils_install_option(option):
    """ Returns the value of the given distutils install option.

    Parameters
    ----------
    option : str
        The name of the option

    Returns
    -------
    val : str or None
        The value of the given distutils build option. If the option
        is not set, returns None.
    """
    return get_distutils_option(option, ['install'])


def get_distutils_build_or_install_option(option):
    """ Returns the value of the given distutils build or install option.

    Parameters
    ----------
    option : str
        The name of the option

    Returns
    -------
    val : str or None
        The value of the given distutils build or install option. If the
        option is not set, returns None.
    """
    return get_distutils_option(option, ['build', 'build_ext', 'build_clib',
     'install'])


def get_compiler_option():
    """ Determines the compiler that will be used to build extension modules.

    Returns
    -------
    compiler : str
        The compiler option specificied for the build, build_ext, or build_clib
        command; or the default compiler for the platform if none was
        specified.

    """
    compiler = get_distutils_build_option('compiler')
    if compiler is None:
        return ccompiler.get_default_compiler()
    return compiler


def get_debug_option(packagename):
    """ Determines if the build is in debug mode.

    Returns
    -------
    debug : bool
        True if the current build was started with the debug option, False
        otherwise.

    """
    try:
        current_debug = get_pkg_version_module(packagename, fromlist=[
         'debug'])[0]
    except (ImportError, AttributeError):
        current_debug = None

    dist = get_dummy_distribution()
    if any(cmd in dist.commands for cmd in ['build', 'build_ext']):
        debug = bool(get_distutils_build_option('debug'))
    else:
        debug = bool(current_debug)
    if current_debug is not None and current_debug != debug:
        build_ext_cmd = dist.get_command_class('build_ext')
        build_ext_cmd.force_rebuild = True
    return debug


def get_pkg_version_module(packagename, fromlist=None):
    """Returns the package's .version module generated by
    `astropy_helpers.version_helpers.generate_version_py`.  Raises an
    ImportError if the version module is not found.

    If ``fromlist`` is an iterable, return a tuple of the members of the
    version module corresponding to the member names given in ``fromlist``.
    Raises an `AttributeError` if any of these module members are not found.
    """
    if not fromlist:
        return __import__(packagename + '.version', fromlist=[''])
    else:
        mod = __import__(packagename + '.version', fromlist=fromlist)
        return tuple(getattr(mod, member) for member in fromlist)


def register_commands(package, version, release):
    if _module_state['registered_commands'] is not None:
        return _module_state['registered_commands']
    _module_state['registered_commands'] = registered_commands = {'test': generate_test_command(package), 
     'sdist': DistutilsSdist, 
     'build_ext': generate_build_ext_command(package, release), 
     'build_py': AstropyBuildPy, 
     'install': AstropyInstall, 
     'install_lib': AstropyInstallLib, 
     'register': AstropyRegister}
    if _module_state['have_sphinx']:
        registered_commands['build_sphinx'] = AstropyBuildSphinx
    else:
        registered_commands['build_sphinx'] = FakeBuildSphinx
    for name, cls in registered_commands.items():
        cls.__name__ = name

    for option in [
     ('use-system-libraries', 'Use system libraries whenever possible', True)]:
        add_command_option('build', *option)
        add_command_option('install', *option)

    return registered_commands


def generate_test_command(package_name):
    """
    Creates a custom 'test' command for the given package which sets the
    command's ``package_name`` class attribute to the name of the package being
    tested.
    """
    return type(package_name.title() + 'Test', (AstropyTest,), {'package_name': package_name})


def generate_build_ext_command(packagename, release):
    """
    Creates a custom 'build_ext' command that allows for manipulating some of
    the C extension options at build time.  We use a function to build the
    class since the base class for build_ext may be different depending on
    certain build-time parameters (for example, we may use Cython's build_ext
    instead of the default version in distutils).

    Uses the default distutils.command.build_ext by default.
    """
    uses_cython = should_build_with_cython(packagename, release)
    if uses_cython:
        from Cython.Distutils import build_ext as basecls
    else:
        basecls = SetuptoolsBuildExt
    attrs = dict(basecls.__dict__)
    orig_run = getattr(basecls, 'run', None)
    orig_finalize = getattr(basecls, 'finalize_options', None)

    def finalize_options(self):
        if self.extensions:
            src_path = os.path.relpath(os.path.join(os.path.dirname(__file__), 'src'))
            shutil.copy2(os.path.join(src_path, 'compiler.c'), os.path.join(self.package_name, '_compiler.c'))
            ext = Extension(self.package_name + '._compiler', [
             os.path.join(self.package_name, '_compiler.c')])
            self.extensions.insert(0, ext)
        if orig_finalize is not None:
            orig_finalize(self)
        if self.uses_cython:
            try:
                from Cython import __version__ as cython_version
            except ImportError:
                cython_version = None

            if cython_version is not None and cython_version != self.uses_cython:
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
            for jdx, src in enumerate(extension.sources):
                if src.endswith('.pyx'):
                    pyxfn = src
                    cfn = src[:-4] + '.c'
                elif src.endswith('.c'):
                    pyxfn = src[:-2] + '.pyx'
                    cfn = src
                if not os.path.isfile(pyxfn):
                    continue
                if self.uses_cython:
                    extension.sources[jdx] = pyxfn
                elif os.path.isfile(cfn):
                    extension.sources[jdx] = cfn
                else:
                    msg = 'Could not find C file {0} for Cython file {1} when building extension {2}. Cython must be installed to build from a git checkout.'.format(cfn, pyxfn, extension.name)
                    raise IOError(errno.ENOENT, msg, cfn)

        if orig_run is not None:
            orig_run(self)
        try:
            cython_version = get_pkg_version_module(packagename, fromlist=['cython_version'])[0]
        except (AttributeError, ImportError):
            cython_version = 'unknown'

        if self.uses_cython and self.uses_cython != cython_version:
            package_dir = os.path.relpath(packagename)
            cython_py = os.path.join(package_dir, 'cython_version.py')
            with open(cython_py, 'w') as (f):
                f.write('# Generated file; do not modify\n')
                f.write('cython_version = {0!r}\n'.format(self.uses_cython))
            if os.path.isdir(self.build_lib):
                self.copy_file(cython_py, os.path.join(self.build_lib, cython_py), preserve_mode=False)
            invalidate_caches()

    attrs['run'] = run
    attrs['finalize_options'] = finalize_options
    attrs['force_rebuild'] = False
    attrs['uses_cython'] = uses_cython
    attrs['package_name'] = packagename
    attrs['user_options'] = basecls.user_options[:]
    attrs['boolean_options'] = basecls.boolean_options[:]
    return type('build_ext', (basecls, object), attrs)


def _get_platlib_dir(cmd):
    plat_specifier = '.{0}-{1}'.format(cmd.plat_name, sys.version[0:3])
    return os.path.join(cmd.build_base, 'lib' + plat_specifier)


class AstropyInstall(SetuptoolsInstall):
    user_options = SetuptoolsInstall.user_options[:]
    boolean_options = SetuptoolsInstall.boolean_options[:]

    def finalize_options(self):
        build_cmd = self.get_finalized_command('build')
        platlib_dir = _get_platlib_dir(build_cmd)
        self.build_lib = platlib_dir
        SetuptoolsInstall.finalize_options(self)


class AstropyInstallLib(SetuptoolsInstallLib):
    user_options = SetuptoolsInstallLib.user_options[:]
    boolean_options = SetuptoolsInstallLib.boolean_options[:]

    def finalize_options(self):
        build_cmd = self.get_finalized_command('build')
        platlib_dir = _get_platlib_dir(build_cmd)
        self.build_dir = platlib_dir
        SetuptoolsInstallLib.finalize_options(self)


class AstropyBuildPy(SetuptoolsBuildPy):
    user_options = SetuptoolsBuildPy.user_options[:]
    boolean_options = SetuptoolsBuildPy.boolean_options[:]

    def finalize_options(self):
        build_cmd = self.get_finalized_command('build')
        platlib_dir = _get_platlib_dir(build_cmd)
        build_cmd.build_purelib = platlib_dir
        build_cmd.build_lib = platlib_dir
        self.build_lib = platlib_dir
        SetuptoolsBuildPy.finalize_options(self)

    def run_2to3(self, files, doctests=False):
        skip_2to3 = self.distribution.skip_2to3
        filtered_files = []
        for file in files:
            for package in skip_2to3:
                if file[len(self.build_lib) + 1:].startswith(package):
                    break
            else:
                filtered_files.append(file)

        SetuptoolsBuildPy.run_2to3(self, filtered_files, doctests)

    def run(self):
        SetuptoolsBuildPy.run(self)


def add_command_option(command, name, doc, is_bool=False):
    """
    Add a custom option to a setup command.

    Issues a warning if the option already exists on that command.

    Parameters
    ----------
    command : str
        The name of the command as given on the command line

    name : str
        The name of the build option

    doc : str
        A short description of the option, for the `--help` message

    is_bool : bool, optional
        When `True`, the option is a boolean option and doesn't
        require an associated value.
    """
    dist = get_dummy_distribution()
    cmdcls = dist.get_command_class(command)
    if hasattr(cmdcls, '_astropy_helpers_options') and name in cmdcls._astropy_helpers_options:
        return
    attr = name.replace('-', '_')
    if hasattr(cmdcls, attr):
        raise RuntimeError('{0!r} already has a {1!r} class attribute, barring {2!r} from being usable as a custom option name.'.format(cmdcls, attr, name))
    for idx, cmd in enumerate(cmdcls.user_options):
        if cmd[0] == name:
            log.warn('Overriding existing {0!r} option {1!r}'.format(command, name))
            del cmdcls.user_options[idx]
            if name in cmdcls.boolean_options:
                cmdcls.boolean_options.remove(name)
            break

    cmdcls.user_options.append((name, None, doc))
    if is_bool:
        cmdcls.boolean_options.append(name)
    setattr(cmdcls, attr, None)
    if not hasattr(cmdcls, '_astropy_helpers_options'):
        cmdcls._astropy_helpers_options = set([name])
    else:
        cmdcls._astropy_helpers_options.add(name)


class AstropyRegister(SetuptoolsRegister):
    __doc__ = 'Extends the built in \'register\' command to support a ``--hidden`` option\n    to make the registered version hidden on PyPI by default.\n\n    The result of this is that when a version is registered as "hidden" it can\n    still be downloaded from PyPI, but it does not show up in the list of\n    actively supported versions under http://pypi.python.org/pypi/astropy, and\n    is not set as the most recent version.\n\n    Although this can always be set through the web interface it may be more\n    convenient to be able to specify via the \'register\' command.  Hidden may\n    also be considered a safer default when running the \'register\' command,\n    though this command uses distutils\' normal behavior if the ``--hidden``\n    option is omitted.\n    '
    user_options = SetuptoolsRegister.user_options + [
     ('hidden', None, 'mark this release as hidden on PyPI by default')]
    boolean_options = SetuptoolsRegister.boolean_options + ['hidden']

    def initialize_options(self):
        SetuptoolsRegister.initialize_options(self)
        self.hidden = False

    def build_post_data(self, action):
        data = SetuptoolsRegister.build_post_data(self, action)
        if action == 'submit' and self.hidden:
            data['_pypi_hidden'] = '1'
        return data

    def _set_config(self):
        self.repository = 'pypi'
        SetuptoolsRegister._set_config(self)
        options = self.distribution.get_option_dict('register')
        if 'repository' in options:
            source, value = options['repository']
            self.repository = value


if _module_state['have_sphinx']:

    class AstropyBuildSphinx(SphinxBuildDoc):
        __doc__ = " A version of the ``build_sphinx`` command that uses the\n        version of Astropy that is built by the setup ``build`` command,\n        rather than whatever is installed on the system - to build docs\n        against the installed version, run ``make html`` in the\n        ``astropy/docs`` directory.\n\n        This also automatically creates the docs/_static directories -\n        this is needed because github won't create the _static dir\n        because it has no tracked files.\n        "
        description = 'Build Sphinx documentation for Astropy environment'
        user_options = SphinxBuildDoc.user_options[:]
        user_options.append(('warnings-returncode', 'w', 'Parses the sphinx output and sets the return code to 1 if there are any warnings. Note that this will cause the sphinx log to only update when it completes, rather than continuously as is normally the case.'))
        user_options.append(('clean-docs', 'l', 'Completely clean previous builds, including automodapi-generated files before building new ones'))
        user_options.append(('no-intersphinx', 'n', 'Skip intersphinx, even if conf.py says to use it'))
        user_options.append(('open-docs-in-browser', 'o', 'Open the docs in a browser (using the webbrowser module) if the build finishes successfully.'))
        boolean_options = SphinxBuildDoc.boolean_options[:]
        boolean_options.append('warnings-returncode')
        boolean_options.append('clean-docs')
        boolean_options.append('no-intersphinx')
        boolean_options.append('open-docs-in-browser')
        _self_iden_rex = re.compile('self\\.([^\\d\\W][\\w]+)', re.UNICODE)

        def initialize_options(self):
            SphinxBuildDoc.initialize_options(self)
            self.clean_docs = False
            self.no_intersphinx = False
            self.open_docs_in_browser = False
            self.warnings_returncode = False

        def finalize_options(self):
            if self.clean_docs:
                dirstorm = [
                 os.path.join(self.source_dir, 'api')]
                if self.build_dir is None:
                    dirstorm.append('docs/_build')
                else:
                    dirstorm.append(self.build_dir)
                for d in dirstorm:
                    if os.path.isdir(d):
                        log.info('Cleaning directory ' + d)
                        shutil.rmtree(d)
                    else:
                        log.info('Not cleaning directory ' + d + ' because not present or not a directory')

            SphinxBuildDoc.finalize_options(self)

        def run(self):
            import webbrowser
            if PY3:
                from urllib.request import pathname2url
            else:
                from urllib import pathname2url
            retcode = None
            if self.build_dir is not None:
                basedir, subdir = os.path.split(self.build_dir)
                if subdir == '':
                    basedir, subdir = os.path.split(basedir)
                staticdir = os.path.join(basedir, '_static')
                if os.path.isfile(staticdir):
                    raise DistutilsOptionError('Attempted to build_sphinx in a location where' + staticdir + 'is a file.  Must be a directory.')
                self.mkpath(staticdir)
            build_cmd = self.reinitialize_command('build')
            build_cmd.inplace = 0
            self.run_command('build')
            build_cmd = self.get_finalized_command('build')
            build_cmd_path = os.path.abspath(build_cmd.build_lib)
            ah_importer = pkgutil.get_importer('astropy_helpers')
            ah_path = os.path.abspath(ah_importer.path)
            subproccode = ''
            try:
                if StrictVersion(sphinx.__version__) >= StrictVersion('1.3b1'):
                    subproccode = 'from __future__ import print_function\n\n'
            except:
                pass

            runlines, runlineno = inspect.getsourcelines(SphinxBuildDoc.run)
            subproccode += textwrap.dedent('\n                from sphinx.setup_command import *\n\n                os.chdir({srcdir!r})\n                sys.path.insert(0, {build_cmd_path!r})\n                sys.path.insert(0, {ah_path!r})\n\n            ').format(build_cmd_path=build_cmd_path, ah_path=ah_path, srcdir=self.source_dir)
            subproccode += textwrap.dedent(''.join(runlines[1:]))
            subproccode = AstropyBuildSphinx._self_iden_rex.split(subproccode)
            for i in range(1, len(subproccode), 2):
                iden = subproccode[i]
                val = getattr(self, iden)
                if iden.endswith('_dir'):
                    subproccode[i] = repr(os.path.abspath(val))
                else:
                    subproccode[i] = repr(val)

            subproccode = ''.join(subproccode)
            if self.no_intersphinx:
                subproccode = subproccode.replace('confoverrides = {}', "confoverrides = {'intersphinx_mapping':{}}")
            log.debug('Starting subprocess of {0} with python code:\n{1}\n[CODE END])'.format(sys.executable, subproccode))
            if self.warnings_returncode:
                proc = subprocess.Popen([sys.executable], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                stdo, stde = proc.communicate(subproccode.encode('utf-8'))
                print(stdo)
                stdolines = stdo.split(b'\n')
                if b'build succeeded.' in stdolines:
                    retcode = 0
                else:
                    retcode = 1
                if retcode != 0:
                    if os.environ.get('TRAVIS', None) == 'true':
                        msg = 'The build_sphinx travis build FAILED because sphinx issued documentation warnings (scroll up to see the warnings).'
                    else:
                        msg = 'build_sphinx returning a non-zero exit code because sphinx issued documentation warnings.'
                    log.warn(msg)
            else:
                proc = subprocess.Popen([sys.executable], stdin=subprocess.PIPE)
                proc.communicate(subproccode.encode('utf-8'))
            if proc.returncode == 0:
                if self.open_docs_in_browser:
                    if self.builder == 'html':
                        absdir = os.path.abspath(self.builder_target_dir)
                        index_path = os.path.join(absdir, 'index.html')
                        fileurl = 'file://' + pathname2url(index_path)
                        webbrowser.open(fileurl)
                    else:
                        log.warn('open-docs-in-browser option was given, but the builder is not html! Ignogring.')
            else:
                log.warn('Sphinx Documentation subprocess failed with return code ' + str(proc.returncode))
            if retcode is not None:
                sys.exit(retcode)


def get_distutils_display_options():
    """ Returns a set of all the distutils display options in their long and
    short forms.  These are the setup.py arguments such as --name or --version
    which print the project's metadata and then exit.

    Returns
    -------
    opts : set
        The long and short form display option arguments, including the - or --
    """
    short_display_opts = set('-' + o[1] for o in Distribution.display_options if o[1])
    long_display_opts = set('--' + o[0] for o in Distribution.display_options)
    short_display_opts.add('-h')
    long_display_opts.add('--help')
    display_commands = set([
     'clean', 'register', 'setopt', 'saveopts', 'egg_info',
     'alias'])
    return short_display_opts.union(long_display_opts.union(display_commands))


def is_distutils_display_option():
    """ Returns True if sys.argv contains any of the distutils display options
    such as --version or --name.
    """
    display_options = get_distutils_display_options()
    return bool(set(sys.argv[1:]).intersection(display_options))


def update_package_files(srcdir, extensions, package_data, packagenames, package_dirs):
    """
    This function is deprecated and maintained for backward compatibility
    with affiliated packages.  Affiliated packages should update their
    setup.py to use `get_package_info` instead.
    """
    info = get_package_info(srcdir)
    extensions.extend(info['ext_modules'])
    package_data.update(info['package_data'])
    packagenames = list(set(packagenames + info['packages']))
    package_dirs.update(info['package_dir'])


def get_package_info(srcdir='.', exclude=()):
    """
    Collates all of the information for building all subpackages
    subpackages and returns a dictionary of keyword arguments that can
    be passed directly to `distutils.setup`.

    The purpose of this function is to allow subpackages to update the
    arguments to the package's ``setup()`` function in its setup.py
    script, rather than having to specify all extensions/package data
    directly in the ``setup.py``.  See Astropy's own
    ``setup.py`` for example usage and the Astropy development docs
    for more details.

    This function obtains that information by iterating through all
    packages in ``srcdir`` and locating a ``setup_package.py`` module.
    This module can contain the following functions:
    ``get_extensions()``, ``get_package_data()``,
    ``get_build_options()``, ``get_external_libraries()``,
    and ``requires_2to3()``.

    Each of those functions take no arguments.

    - ``get_extensions`` returns a list of
      `distutils.extension.Extension` objects.

    - ``get_package_data()`` returns a dict formatted as required by
      the ``package_data`` argument to ``setup()``.

    - ``get_build_options()`` returns a list of tuples describing the
      extra build options to add.

    - ``get_external_libraries()`` returns
      a list of libraries that can optionally be built using external
      dependencies.

    - ``requires_2to3()`` should return `True` when the source code
      requires `2to3` processing to run on Python 3.x.  If
      ``requires_2to3()`` is missing, it is assumed to return `True`.

    """
    ext_modules = []
    packages = []
    package_data = {}
    package_dir = {}
    skip_2to3 = []
    packages = filter_packages(find_packages(srcdir, exclude=exclude))
    for setuppkg in iter_setup_packages(srcdir, packages):
        if hasattr(setuppkg, 'get_build_options'):
            options = setuppkg.get_build_options()
            for option in options:
                add_command_option('build', *option)

        if hasattr(setuppkg, 'get_external_libraries'):
            libraries = setuppkg.get_external_libraries()
            for library in libraries:
                add_external_library(library)

        if hasattr(setuppkg, 'requires_2to3'):
            requires_2to3 = setuppkg.requires_2to3()
        else:
            requires_2to3 = True
        if not requires_2to3:
            skip_2to3.append(os.path.dirname(setuppkg.__file__))

    for setuppkg in iter_setup_packages(srcdir, packages):
        if hasattr(setuppkg, 'get_extensions'):
            ext_modules.extend(setuppkg.get_extensions())
        if hasattr(setuppkg, 'get_package_data'):
            package_data.update(setuppkg.get_package_data())

    ext_modules.extend(get_cython_extensions(srcdir, packages, ext_modules, [
     'numpy']))
    for i, ext in reversed(list(enumerate(ext_modules))):
        if ext.name == 'skip_cython':
            del ext_modules[i]

    if get_compiler_option() == 'msvc':
        for ext in ext_modules:
            ext.extra_link_args.append('/MANIFEST')

    return {'ext_modules': ext_modules, 
     'packages': packages, 
     'package_dir': package_dir, 
     'package_data': package_data, 
     'skip_2to3': skip_2to3}


def iter_setup_packages(srcdir, packages):
    """ A generator that finds and imports all of the ``setup_package.py``
    modules in the source packages.

    Returns
    -------
    modgen : generator
        A generator that yields (modname, mod), where `mod` is the module and
        `modname` is the module name for the ``setup_package.py`` modules.

    """
    for packagename in packages:
        package_parts = packagename.split('.')
        package_path = os.path.join(srcdir, *package_parts)
        setup_package = os.path.relpath(os.path.join(package_path, 'setup_package.py'))
        if os.path.isfile(setup_package):
            module = import_file(setup_package)
            yield module


def iter_pyx_files(package_dir, package_name):
    """
    A generator that yields Cython source files (ending in '.pyx') in the
    source packages.

    Returns
    -------
    pyxgen : generator
        A generator that yields (extmod, fullfn) where `extmod` is the
        full name of the module that the .pyx file would live in based
        on the source directory structure, and `fullfn` is the path to
        the .pyx file.
    """
    for dirpath, dirnames, filenames in walk_skip_hidden(package_dir):
        for fn in filenames:
            if fn.endswith('.pyx'):
                fullfn = os.path.relpath(os.path.join(dirpath, fn))
                extmod = '.'.join([package_name, fn[:-4]])
                yield (extmod, fullfn)

        break


def should_build_with_cython(package, release=None):
    """Returns the previously used Cython version (or 'unknown' if not
    previously built) if Cython should be used to build extension modules from
    pyx files.  If the ``release`` parameter is not specified an attempt is
    made to determine the release flag from `astropy.version`.
    """
    try:
        version_module = __import__(package + '.cython_version', fromlist=[
         'release', 'cython_version'])
    except ImportError:
        version_module = None

    if release is None and version_module is not None:
        try:
            release = version_module.release
        except AttributeError:
            pass

        try:
            cython_version = version_module.cython_version
        except AttributeError:
            cython_version = 'unknown'

        if _module_state['have_cython'] and (not release or cython_version == 'unknown'):
            pass
        return cython_version
    else:
        return False


def get_cython_extensions(srcdir, packages, prevextensions=tuple(), extincludedirs=None):
    """
    Looks for Cython files and generates Extensions if needed.

    Parameters
    ----------
    srcdir : str
        Path to the root of the source directory to search.
    prevextensions : list of `~distutils.core.Extension` objects
        The extensions that are already defined.  Any .pyx files already here
        will be ignored.
    extincludedirs : list of str or None
        Directories to include as the `include_dirs` argument to the generated
        `~distutils.core.Extension` objects.

    Returns
    -------
    exts : list of `~distutils.core.Extension` objects
        The new extensions that are needed to compile all .pyx files (does not
        include any already in `prevextensions`).
    """
    prevsourcepaths = []
    ext_modules = []
    for ext in prevextensions:
        for s in ext.sources:
            if s.endswith(('.pyx', '.c')):
                sourcepath = os.path.realpath(os.path.splitext(s)[0])
                prevsourcepaths.append(sourcepath)

    for package_name in packages:
        package_parts = package_name.split('.')
        package_path = os.path.join(srcdir, *package_parts)
        for extmod, pyxfn in iter_pyx_files(package_path, package_name):
            sourcepath = os.path.realpath(os.path.splitext(pyxfn)[0])
            if sourcepath not in prevsourcepaths:
                ext_modules.append(Extension(extmod, [pyxfn], include_dirs=extincludedirs))

    return ext_modules


def write_if_different(filename, data):
    """ Write `data` to `filename`, if the content of the file is different.

    Parameters
    ----------
    filename : str
        The file name to be written to.
    data : bytes
        The data to be written to `filename`.
    """
    assert isinstance(data, bytes)
    if os.path.exists(filename):
        with open(filename, 'rb') as (fd):
            original_data = fd.read()
    else:
        original_data = None
    if original_data != data:
        with open(filename, 'wb') as (fd):
            fd.write(data)


def get_numpy_include_path():
    """
    Gets the path to the numpy headers.
    """
    if sys.version_info[0] >= 3:
        import builtins
        if hasattr(builtins, '__NUMPY_SETUP__'):
            del builtins.__NUMPY_SETUP__
        import imp, numpy
        imp.reload(numpy)
    else:
        import __builtin__
        if hasattr(__builtin__, '__NUMPY_SETUP__'):
            del __builtin__.__NUMPY_SETUP__
        import numpy
        reload(numpy)
    try:
        numpy_include = numpy.get_include()
    except AttributeError:
        numpy_include = numpy.get_numpy_include()

    return numpy_include


def import_file(filename):
    """
    Imports a module from a single file as if it doesn't belong to a
    particular package.
    """
    with open(filename, 'U') as (fd):
        name = '_'.join(os.path.relpath(os.path.splitext(filename)[0]).split(os.sep)[1:])
        return imp.load_module(name, fd, filename, ('.py', 'U', 1))


class DistutilsExtensionArgs(collections.defaultdict):
    __doc__ = '\n    A special dictionary whose default values are the empty list.\n\n    This is useful for building up a set of arguments for\n    `distutils.Extension` without worrying whether the entry is\n    already present.\n    '

    def __init__(self, *args, **kwargs):

        def default_factory():
            return []

        super(DistutilsExtensionArgs, self).__init__(default_factory, *args, **kwargs)

    def update(self, other):
        for key, val in other.items():
            self[key].extend(val)


def pkg_config(packages, default_libraries, executable='pkg-config'):
    """
    Uses pkg-config to update a set of distutils Extension arguments
    to include the flags necessary to link against the given packages.

    If the pkg-config lookup fails, default_libraries is applied to
    libraries.

    Parameters
    ----------
    packages : list of str
        A list of pkg-config packages to look up.

    default_libraries : list of str
        A list of library names to use if the pkg-config lookup fails.

    Returns
    -------
    config : dict
        A dictionary containing keyword arguments to
        `distutils.Extension`.  These entries include:

        - ``include_dirs``: A list of include directories
        - ``library_dirs``: A list of library directories
        - ``libraries``: A list of libraries
        - ``define_macros``: A list of macro defines
        - ``undef_macros``: A list of macros to undefine
        - ``extra_compile_args``: A list of extra arguments to pass to
          the compiler
    """
    flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries', 
     '-D': 'define_macros', '-U': 'undef_macros'}
    command = ('{0} --libs --cflags {1}'.format(executable, ' '.join(packages)),)
    result = DistutilsExtensionArgs()
    try:
        pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        output = pipe.communicate()[0].strip()
    except subprocess.CalledProcessError as e:
        lines = [
         '{0} failed.  This may cause the build to fail below.'.format(executable),
         '  command: {0}'.format(e.cmd),
         '  returncode: {0}'.format(e.returncode),
         '  output: {0}'.format(e.output)]
        log.warn('\n'.join(lines))
        result['libraries'].extend(default_libraries)
    else:
        if pipe.returncode != 0:
            lines = [
             'pkg-config could not lookup up package(s) {0}.'.format(', '.join(packages)),
             'This may cause the build to fail below.']
            log.warn('\n'.join(lines))
            result['libraries'].extend(default_libraries)
        else:
            for token in output.split():
                arg = token[:2].decode('ascii')
                value = token[2:].decode(sys.getfilesystemencoding())
                if arg in flag_map:
                    if arg == '-D':
                        value = tuple(value.split('=', 1))
                    result[flag_map[arg]].append(value)
                else:
                    result['extra_compile_args'].append(value)

        return result


def add_external_library(library):
    """
    Add a build option for selecting the internal or system copy of a library.

    Parameters
    ----------
    library : str
        The name of the library.  If the library is `foo`, the build
        option will be called `--use-system-foo`.
    """
    for command in ['build', 'build_ext', 'install']:
        add_command_option(command, str('use-system-' + library), 'Use the system {0} library'.format(library), is_bool=True)


def use_system_library(library):
    """
    Returns `True` if the build configuration indicates that the given
    library should use the system copy of the library rather than the
    internal one.

    For the given library `foo`, this will be `True` if
    `--use-system-foo` or `--use-system-libraries` was provided at the
    commandline or in `setup.cfg`.

    Parameters
    ----------
    library : str
        The name of the library

    Returns
    -------
    use_system : bool
        `True` if the build should use the system copy of the library.
    """
    return get_distutils_build_or_install_option('use_system_{0}'.format(library)) or get_distutils_build_or_install_option('use_system_libraries')


def filter_packages(packagenames):
    """
    Removes some packages from the package list that shouldn't be
    installed on the current version of Python.
    """
    if PY3:
        exclude = '_py2'
    else:
        exclude = '_py3'
    return [x for x in packagenames if not x.endswith(exclude)]


class FakeBuildSphinx(Command):
    __doc__ = '\n    A dummy build_sphinx command that is called if Sphinx is not\n    installed and displays a relevant error message\n    '
    user_options = [
     ('fresh-env', 'E', ''),
     ('all-files', 'a', ''),
     ('source-dir=', 's', ''),
     ('build-dir=', None, ''),
     ('config-dir=', 'c', ''),
     ('builder=', 'b', ''),
     ('project=', None, ''),
     ('version=', None, ''),
     ('release=', None, ''),
     ('today=', None, ''),
     ('link-index', 'i', '')]
    user_options.append(('warnings-returncode', 'w', ''))
    user_options.append(('clean-docs', 'l', ''))
    user_options.append(('no-intersphinx', 'n', ''))
    user_options.append(('open-docs-in-browser', 'o', ''))

    def initialize_options(self):
        try:
            raise RuntimeError('Sphinx must be installed for build_sphinx')
        except:
            log.error('error : Sphinx must be installed for build_sphinx')
            sys.exit(1)