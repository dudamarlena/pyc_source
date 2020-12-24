# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rgeda/project/repo/webbpsf/astropy_helpers/ah_bootstrap.py
# Compiled at: 2019-07-20 17:47:20
# Size of source mod 2**32: 35654 bytes
"""
This bootstrap module contains code for ensuring that the astropy_helpers
package will be importable by the time the setup.py script runs.  It also
includes some workarounds to ensure that a recent-enough version of setuptools
is being used for the installation.

This module should be the first thing imported in the setup.py of distributions
that make use of the utilities in astropy_helpers.  If the distribution ships
with its own copy of astropy_helpers, this module will first attempt to import
from the shipped copy.  However, it will also check PyPI to see if there are
any bug-fix releases on top of the current version that may be useful to get
past platform-specific bugs that have been fixed.  When running setup.py, use
the ``--offline`` command-line option to disable the auto-upgrade checks.

When this module is imported or otherwise executed it automatically calls a
main function that attempts to read the project's setup.cfg file, which it
checks for a configuration section called ``[ah_bootstrap]`` the presences of
that section, and options therein, determine the next step taken:  If it
contains an option called ``auto_use`` with a value of ``True``, it will
automatically call the main function of this module called
`use_astropy_helpers` (see that function's docstring for full details).
Otherwise no further action is taken and by default the system-installed version
of astropy-helpers will be used (however, ``ah_bootstrap.use_astropy_helpers``
may be called manually from within the setup.py script).

This behavior can also be controlled using the ``--auto-use`` and
``--no-auto-use`` command-line flags. For clarity, an alias for
``--no-auto-use`` is ``--use-system-astropy-helpers``, and we recommend using
the latter if needed.

Additional options in the ``[ah_boostrap]`` section of setup.cfg have the same
names as the arguments to `use_astropy_helpers`, and can be used to configure
the bootstrap script when ``auto_use = True``.

See https://github.com/astropy/astropy-helpers for more details, and for the
latest version of this module.
"""
import contextlib, errno, io, locale, os, re, subprocess as sp, sys
__minimum_python_version__ = (3, 5)
if sys.version_info < __minimum_python_version__:
    print('ERROR: Python {} or later is required by astropy-helpers'.format(__minimum_python_version__))
    sys.exit(1)
try:
    from ConfigParser import ConfigParser, RawConfigParser
except ImportError:
    from configparser import ConfigParser, RawConfigParser

_str_types = (
 str, bytes)
from distutils.version import LooseVersion
try:
    import setuptools
    assert LooseVersion(setuptools.__version__) >= LooseVersion('1.0')
except (ImportError, AssertionError):
    print('ERROR: setuptools 1.0 or later is required by astropy-helpers')
    sys.exit(1)

try:
    import typing
except ImportError:
    pass

try:
    import setuptools.py31compat
except ImportError:
    pass

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot
except:
    pass

import pkg_resources
from setuptools import Distribution
from setuptools.package_index import PackageIndex
from distutils import log
from distutils.debug import DEBUG
DIST_NAME = 'astropy-helpers'
PACKAGE_NAME = 'astropy_helpers'
UPPER_VERSION_EXCLUSIVE = None
DOWNLOAD_IF_NEEDED = True
INDEX_URL = 'https://pypi.python.org/simple'
USE_GIT = True
OFFLINE = False
AUTO_UPGRADE = True
CFG_OPTIONS = [
 (
  'auto_use', bool), ('path', str), ('download_if_needed', bool),
 (
  'index_url', str), ('use_git', bool), ('offline', bool),
 (
  'auto_upgrade', bool)]

class _Bootstrapper(object):
    __doc__ = '\n    Bootstrapper implementation.  See ``use_astropy_helpers`` for parameter\n    documentation.\n    '

    def __init__(self, path=None, index_url=None, use_git=None, offline=None, download_if_needed=None, auto_upgrade=None):
        if path is None:
            path = PACKAGE_NAME
        else:
            if not isinstance(path, _str_types):
                if not path is False:
                    raise TypeError('path must be a string or False')
            if not isinstance(path, str):
                fs_encoding = sys.getfilesystemencoding()
                path = path.decode(fs_encoding)
            self.path = path
            self.index_url = index_url if index_url is not None else INDEX_URL
            self.offline = offline if offline is not None else OFFLINE
            if self.offline:
                download_if_needed = False
                auto_upgrade = False
            self.download = download_if_needed if download_if_needed is not None else DOWNLOAD_IF_NEEDED
            self.auto_upgrade = auto_upgrade if auto_upgrade is not None else AUTO_UPGRADE
            git_dir_exists = os.path.exists(os.path.join(os.path.dirname(__file__), '.git'))
            if use_git is None:
                use_git = git_dir_exists or False
        self.use_git = use_git if use_git is not None else USE_GIT
        self.is_submodule = False

    @classmethod
    def main(cls, argv=None):
        if argv is None:
            argv = sys.argv
        config = cls.parse_config()
        config.update(cls.parse_command_line(argv))
        auto_use = config.pop('auto_use', False)
        bootstrapper = cls(**config)
        if auto_use:
            bootstrapper.run()
        return bootstrapper

    @classmethod
    def parse_config(cls):
        if not os.path.exists('setup.cfg'):
            return {}
        else:
            cfg = ConfigParser()
            try:
                cfg.read('setup.cfg')
            except Exception as e:
                try:
                    if DEBUG:
                        raise
                    log.error('Error reading setup.cfg: {0!r}\n{1} will not be automatically bootstrapped and package installation may fail.\n{2}'.format(e, PACKAGE_NAME, _err_help_msg))
                    return {}
                finally:
                    e = None
                    del e

            return cfg.has_section('ah_bootstrap') or {}
        config = {}
        for option, type_ in CFG_OPTIONS:
            if not cfg.has_option('ah_bootstrap', option):
                continue
            elif type_ is bool:
                value = cfg.getboolean('ah_bootstrap', option)
            else:
                value = cfg.get('ah_bootstrap', option)
            config[option] = value

        return config

    @classmethod
    def parse_command_line(cls, argv=None):
        if argv is None:
            argv = sys.argv
        config = {}
        if '--no-git' in argv:
            config['use_git'] = False
            argv.remove('--no-git')
        if '--offline' in argv:
            config['offline'] = True
            argv.remove('--offline')
        if '--auto-use' in argv:
            config['auto_use'] = True
            argv.remove('--auto-use')
        if '--no-auto-use' in argv:
            config['auto_use'] = False
            argv.remove('--no-auto-use')
        if '--use-system-astropy-helpers' in argv:
            config['auto_use'] = False
            argv.remove('--use-system-astropy-helpers')
        return config

    def run(self):
        strategies = [
         'local_directory', 'local_file', 'index']
        dist = None
        for key in list(sys.modules):
            try:
                if key == PACKAGE_NAME or key.startswith(PACKAGE_NAME + '.'):
                    del sys.modules[key]
            except AttributeError:
                continue

        self.is_submodule = self._check_submodule()
        for strategy in strategies:
            method = getattr(self, 'get_{0}_dist'.format(strategy))
            dist = method()
            if dist is not None:
                break
        else:
            raise _AHBootstrapSystemExit('No source found for the {0!r} package; {0} must be available and importable as a prerequisite to building or installing this package.'.format(PACKAGE_NAME))

        dist = dist.clone(precedence=(pkg_resources.EGG_DIST))
        try:
            pkg_resources.working_set.add(dist, replace=True)
        except TypeError:
            if dist.key in pkg_resources.working_set.by_key:
                del pkg_resources.working_set.by_key[dist.key]
            pkg_resources.working_set.add(dist)

    @property
    def config(self):
        """
        A `dict` containing the options this `_Bootstrapper` was configured
        with.
        """
        return dict(((optname, getattr(self, optname)) for optname, _ in CFG_OPTIONS if hasattr(self, optname)))

    def get_local_directory_dist(self):
        """
        Handle importing a vendored package from a subdirectory of the source
        distribution.
        """
        if not os.path.isdir(self.path):
            return
        log.info('Attempting to import astropy_helpers from {0} {1!r}'.format('submodule' if self.is_submodule else 'directory', self.path))
        dist = self._directory_import()
        if dist is None:
            log.warn('The requested path {0!r} for importing {1} does not exist, or does not contain a copy of the {1} package.'.format(self.path, PACKAGE_NAME))
        else:
            if self.auto_upgrade:
                if not self.is_submodule:
                    upgrade = self._do_upgrade(dist)
                    if upgrade is not None:
                        dist = upgrade
        return dist

    def get_local_file_dist(self):
        """
        Handle importing from a source archive; this also uses setup_requires
        but points easy_install directly to the source archive.
        """
        if not os.path.isfile(self.path):
            return
        log.info('Attempting to unpack and import astropy_helpers from {0!r}'.format(self.path))
        try:
            dist = self._do_download(find_links=[self.path])
        except Exception as e:
            try:
                if DEBUG:
                    raise
                log.warn('Failed to import {0} from the specified archive {1!r}: {2}'.format(PACKAGE_NAME, self.path, str(e)))
                dist = None
            finally:
                e = None
                del e

        if dist is not None:
            if self.auto_upgrade:
                upgrade = self._do_upgrade(dist)
                if upgrade is not None:
                    dist = upgrade
        return dist

    def get_index_dist(self):
        if not self.download:
            log.warn('Downloading {0!r} disabled.'.format(DIST_NAME))
            return
        log.warn('Downloading {0!r}; run setup.py with the --offline option to force offline installation.'.format(DIST_NAME))
        try:
            dist = self._do_download()
        except Exception as e:
            try:
                if DEBUG:
                    raise
                log.warn('Failed to download and/or install {0!r} from {1!r}:\n{2}'.format(DIST_NAME, self.index_url, str(e)))
                dist = None
            finally:
                e = None
                del e

        return dist

    def _directory_import(self):
        """
        Import astropy_helpers from the given path, which will be added to
        sys.path.

        Must return True if the import succeeded, and False otherwise.
        """
        path = os.path.abspath(self.path)
        ws = pkg_resources.WorkingSet([])
        ws.add_entry(path)
        dist = ws.by_key.get(DIST_NAME)
        if dist is None:
            setup_py = os.path.join(path, 'setup.py')
            if os.path.isfile(setup_py):
                sp.check_output([sys.executable, 'setup.py', 'egg_info'], cwd=path)
                for dist in pkg_resources.find_distributions(path, True):
                    return dist

        return dist

    def _do_download(self, version='', find_links=None):
        if find_links:
            allow_hosts = ''
            index_url = None
        else:
            allow_hosts = None
            index_url = self.index_url

        class _Distribution(Distribution):

            def get_option_dict(self, command_name):
                opts = Distribution.get_option_dict(self, command_name)
                if command_name == 'easy_install':
                    if find_links is not None:
                        opts['find_links'] = (
                         'setup script', find_links)
                    if index_url is not None:
                        opts['index_url'] = (
                         'setup script', index_url)
                    if allow_hosts is not None:
                        opts['allow_hosts'] = (
                         'setup script', allow_hosts)
                return opts

        if version:
            req = '{0}=={1}'.format(DIST_NAME, version)
        else:
            if UPPER_VERSION_EXCLUSIVE is None:
                req = DIST_NAME
            else:
                req = '{0}<{1}'.format(DIST_NAME, UPPER_VERSION_EXCLUSIVE)
        attrs = {'setup_requires': [req]}
        try:
            context = _verbose if DEBUG else _silence
            with context():
                dist = _Distribution(attrs=attrs)
                try:
                    dist.parse_config_files(ignore_option_errors=True)
                    dist.fetch_build_eggs(req)
                except TypeError:
                    pass

            return pkg_resources.working_set.by_key.get(DIST_NAME)
        except Exception as e:
            try:
                if DEBUG:
                    raise
                else:
                    msg = 'Error retrieving {0} from {1}:\n{2}'
                    if find_links:
                        source = find_links[0]
                    else:
                        if index_url != INDEX_URL:
                            source = index_url
                        else:
                            source = 'PyPI'
                raise Exception(msg.format(DIST_NAME, source, repr(e)))
            finally:
                e = None
                del e

    def _do_upgrade(self, dist):
        next_version = _next_version(dist.parsed_version)
        req = pkg_resources.Requirement.parse('{0}>{1},<{2}'.format(DIST_NAME, dist.version, next_version))
        package_index = PackageIndex(index_url=(self.index_url))
        upgrade = package_index.obtain(req)
        if upgrade is not None:
            return self._do_download(version=(upgrade.version))

    def _check_submodule--- This code section failed: ---

 L. 568         0  LOAD_FAST                'self'
                2  LOAD_ATTR                path
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_TRUE     38  'to 38'

 L. 569        10  LOAD_GLOBAL              os
               12  LOAD_ATTR                path
               14  LOAD_METHOD              exists
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                path
               20  CALL_METHOD_1         1  '1 positional argument'
               22  POP_JUMP_IF_FALSE    42  'to 42'
               24  LOAD_GLOBAL              os
               26  LOAD_ATTR                path
               28  LOAD_METHOD              isdir
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                path
               34  CALL_METHOD_1         1  '1 positional argument'
               36  POP_JUMP_IF_TRUE     42  'to 42'
             38_0  COME_FROM             8  '8'

 L. 570        38  LOAD_CONST               False
               40  RETURN_VALUE     
             42_0  COME_FROM            36  '36'
             42_1  COME_FROM            22  '22'

 L. 572        42  LOAD_FAST                'self'
               44  LOAD_ATTR                use_git
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L. 573        48  LOAD_FAST                'self'
               50  LOAD_METHOD              _check_submodule_using_git
               52  CALL_METHOD_0         0  '0 positional arguments'
               54  RETURN_VALUE     
             56_0  COME_FROM            46  '46'

 L. 575        56  LOAD_FAST                'self'
               58  LOAD_METHOD              _check_submodule_no_git
               60  CALL_METHOD_0         0  '0 positional arguments'
               62  RETURN_VALUE     

Parse error at or near `CALL_METHOD_0' instruction at offset 60

    def _check_submodule_using_git(self):
        """
        Check if the given path is a git submodule.  If so, attempt to initialize
        and/or update the submodule if needed.

        This function makes calls to the ``git`` command in subprocesses.  The
        ``_check_submodule_no_git`` option uses pure Python to check if the given
        path looks like a git submodule, but it cannot perform updates.
        """
        cmd = [
         'git', 'submodule', 'status', '--', self.path]
        try:
            log.info('Running `{0}`; use the --no-git option to disable git commands'.format(' '.join(cmd)))
            returncode, stdout, stderr = run_cmd(cmd)
        except _CommandNotFound:
            return False
        else:
            stderr = stderr.strip()
            if returncode != 0:
                if stderr:
                    perl_warning = 'perl: warning: Falling back to the standard locale ("C").'
                    if not stderr.strip().endswith(perl_warning):
                        log.warn('git submodule command failed unexpectedly:\n{0}'.format(stderr))
                        return False
            _git_submodule_status_re = re.compile('^(?P<status>[+-U ])(?P<commit>[0-9a-f]{40}) (?P<submodule>\\S+)( .*)?$')
            m = _git_submodule_status_re.match(stdout)
            if m:
                self._update_submodule(m.group('submodule'), m.group('status'))
                return True
            log.warn('Unexpected output from `git submodule status`:\n{0}\nWill attempt import from {1!r} regardless.'.format(stdout, self.path))
            return False

    def _check_submodule_no_git(self):
        """
        Like ``_check_submodule_using_git``, but simply parses the .gitmodules file
        to determine if the supplied path is a git submodule, and does not exec any
        subprocesses.

        This can only determine if a path is a submodule--it does not perform
        updates, etc.  This function may need to be updated if the format of the
        .gitmodules file is changed between git versions.
        """
        gitmodules_path = os.path.abspath('.gitmodules')
        if not os.path.isfile(gitmodules_path):
            return False
        gitmodules_fileobj = io.StringIO()
        with io.open(gitmodules_path) as (f):
            for line in f:
                line = line.lstrip()
                if line:
                    if line[0] in (':', ';'):
                        continue
                gitmodules_fileobj.write(line)

        gitmodules_fileobj.seek(0)
        cfg = RawConfigParser()
        try:
            cfg.readfp(gitmodules_fileobj)
        except Exception as exc:
            try:
                log.warn('Malformatted .gitmodules file: {0}\n{1} cannot be assumed to be a git submodule.'.format(exc, self.path))
                return False
            finally:
                exc = None
                del exc

        for section in cfg.sections():
            if not cfg.has_option(section, 'path'):
                continue
            submodule_path = cfg.get(section, 'path').rstrip(os.sep)
            if submodule_path == self.path.rstrip(os.sep):
                return True

        return False

    def _update_submodule(self, submodule, status):
        if status == ' ':
            return
        if status == '-':
            if self.offline:
                raise _AHBootstrapSystemExit('Cannot initialize the {0} submodule in --offline mode; this requires being able to clone the submodule from an online repository.'.format(submodule))
            cmd = [
             'update', '--init']
            action = 'Initializing'
        else:
            if status == '+':
                cmd = [
                 'update']
                action = 'Updating'
                if self.offline:
                    cmd.append('--no-fetch')
                else:
                    if status == 'U':
                        raise _AHBootstrapSystemExit('Error: Submodule {0} contains unresolved merge conflicts.  Please complete or abandon any changes in the submodule so that it is in a usable state, then try again.'.format(submodule))
                    else:
                        log.warn('Unknown status {0!r} for git submodule {1!r}.  Will attempt to use the submodule as-is, but try to ensure that the submodule is in a clean state and contains no conflicts or errors.\n{2}'.format(status, submodule, _err_help_msg))
                        return
            else:
                err_msg = None
                cmd = ['git', 'submodule'] + cmd + ['--', submodule]
                log.warn('{0} {1} submodule with: `{2}`'.format(action, submodule, ' '.join(cmd)))
                try:
                    log.info('Running `{0}`; use the --no-git option to disable git commands'.format(' '.join(cmd)))
                    returncode, stdout, stderr = run_cmd(cmd)
                except OSError as e:
                    try:
                        err_msg = str(e)
                    finally:
                        e = None
                        del e

            if returncode != 0:
                err_msg = stderr
            if err_msg is not None:
                log.warn('An unexpected error occurred updating the git submodule {0!r}:\n{1}\n{2}'.format(submodule, err_msg, _err_help_msg))


class _CommandNotFound(OSError):
    __doc__ = '\n    An exception raised when a command run with run_cmd is not found on the\n    system.\n    '


def run_cmd(cmd):
    """
    Run a command in a subprocess, given as a list of command-line
    arguments.

    Returns a ``(returncode, stdout, stderr)`` tuple.
    """
    try:
        p = sp.Popen(cmd, stdout=(sp.PIPE), stderr=(sp.PIPE))
        stdout, stderr = p.communicate()
    except OSError as e:
        try:
            if DEBUG:
                raise
            elif e.errno == errno.ENOENT:
                msg = 'Command not found: `{0}`'.format(' '.join(cmd))
                raise _CommandNotFound(msg, cmd)
            else:
                raise _AHBootstrapSystemExit('An unexpected error occurred when running the `{0}` command:\n{1}'.format(' '.join(cmd), str(e)))
        finally:
            e = None
            del e

    try:
        stdio_encoding = locale.getdefaultlocale()[1] or 'latin1'
    except ValueError:
        stdio_encoding = 'latin1'

    if not isinstance(stdout, str):
        stdout = stdout.decode(stdio_encoding, 'replace')
    if not isinstance(stderr, str):
        stderr = stderr.decode(stdio_encoding, 'replace')
    return (p.returncode, stdout, stderr)


def _next_version(version):
    """
    Given a parsed version from pkg_resources.parse_version, returns a new
    version string with the next minor version.

    Examples
    ========
    >>> _next_version(pkg_resources.parse_version('1.2.3'))
    '1.3.0'
    """
    if hasattr(version, 'base_version'):
        if version.base_version:
            parts = version.base_version.split('.')
        else:
            parts = []
    else:
        parts = []
        for part in version:
            if part.startswith('*'):
                break
            parts.append(part)

    parts = [int(p) for p in parts]
    if len(parts) < 3:
        parts += [0] * (3 - len(parts))
    major, minor, micro = parts[:3]
    return '{0}.{1}.{2}'.format(major, minor + 1, 0)


class _DummyFile(object):
    __doc__ = 'A noop writeable object.'
    errors = ''
    encoding = 'utf-8'

    def write(self, s):
        pass

    def flush(self):
        pass


@contextlib.contextmanager
def _verbose():
    yield


@contextlib.contextmanager
def _silence():
    """A context manager that silences sys.stdout and sys.stderr."""
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = _DummyFile()
    sys.stderr = _DummyFile()
    exception_occurred = False
    try:
        yield
    except:
        exception_occurred = True
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        raise

    if not exception_occurred:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


_err_help_msg = '\nIf the problem persists consider installing astropy_helpers manually using pip\n(`pip install astropy_helpers`) or by manually downloading the source archive,\nextracting it, and installing by running `python setup.py install` from the\nroot of the extracted source code.\n'

class _AHBootstrapSystemExit(SystemExit):

    def __init__(self, *args):
        if not args:
            msg = 'An unknown problem occurred bootstrapping astropy_helpers.'
        else:
            msg = args[0]
        msg += '\n' + _err_help_msg
        (super(_AHBootstrapSystemExit, self).__init__)(msg, *args[1:])


BOOTSTRAPPER = _Bootstrapper.main()

def use_astropy_helpers(**kwargs):
    """
    Ensure that the `astropy_helpers` module is available and is importable.
    This supports automatic submodule initialization if astropy_helpers is
    included in a project as a git submodule, or will download it from PyPI if
    necessary.

    Parameters
    ----------

    path : str or None, optional
        A filesystem path relative to the root of the project's source code
        that should be added to `sys.path` so that `astropy_helpers` can be
        imported from that path.

        If the path is a git submodule it will automatically be initialized
        and/or updated.

        The path may also be to a ``.tar.gz`` archive of the astropy_helpers
        source distribution.  In this case the archive is automatically
        unpacked and made temporarily available on `sys.path` as a ``.egg``
        archive.

        If `None` skip straight to downloading.

    download_if_needed : bool, optional
        If the provided filesystem path is not found an attempt will be made to
        download astropy_helpers from PyPI.  It will then be made temporarily
        available on `sys.path` as a ``.egg`` archive (using the
        ``setup_requires`` feature of setuptools.  If the ``--offline`` option
        is given at the command line the value of this argument is overridden
        to `False`.

    index_url : str, optional
        If provided, use a different URL for the Python package index than the
        main PyPI server.

    use_git : bool, optional
        If `False` no git commands will be used--this effectively disables
        support for git submodules. If the ``--no-git`` option is given at the
        command line the value of this argument is overridden to `False`.

    auto_upgrade : bool, optional
        By default, when installing a package from a non-development source
        distribution ah_boostrap will try to automatically check for patch
        releases to astropy-helpers on PyPI and use the patched version over
        any bundled versions.  Setting this to `False` will disable that
        functionality. If the ``--offline`` option is given at the command line
        the value of this argument is overridden to `False`.

    offline : bool, optional
        If `False` disable all actions that require an internet connection,
        including downloading packages from the package index and fetching
        updates to any git submodule.  Defaults to `True`.
    """
    global BOOTSTRAPPER
    config = BOOTSTRAPPER.config
    (config.update)(**kwargs)
    BOOTSTRAPPER = _Bootstrapper(**config)
    BOOTSTRAPPER.run()