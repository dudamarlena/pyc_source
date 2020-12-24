# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/virtualenv/virtualenv.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 106384 bytes
"""Create a "virtual" Python installation"""
import os, sys
if os.environ.get('VIRTUALENV_INTERPRETER_RUNNING'):
    for path in sys.path[:]:
        if os.path.realpath(os.path.dirname(__file__)) == os.path.realpath(path):
            sys.path.remove(path)

import ast, base64, codecs, contextlib, distutils.spawn, distutils.sysconfig, errno, glob, logging, optparse, os, re, shutil, struct, subprocess, sys, tempfile, textwrap, zipfile, zlib
from distutils.util import strtobool
from os.path import join
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

__version__ = '16.7.2'
virtualenv_version = __version__
DEBUG = os.environ.get('_VIRTUALENV_DEBUG', None) == '1'
if sys.version_info < (2, 7):
    print('ERROR: {}'.format(sys.exc_info()[1]))
    print('ERROR: this script requires Python 2.7 or greater.')
    sys.exit(101)
else:
    HERE = os.path.dirname(os.path.abspath(__file__))
    IS_ZIPAPP = os.path.isfile(HERE)
    try:
        basestring
    except NameError:
        basestring = str

    VERSION = ('{}.{}'.format)(*sys.version_info)
    PY_VERSION = ('python{}.{}'.format)(*sys.version_info)
    IS_PYPY = hasattr(sys, 'pypy_version_info')
    IS_WIN = sys.platform == 'win32'
    IS_CYGWIN = sys.platform == 'cygwin'
    IS_DARWIN = sys.platform == 'darwin'
    ABI_FLAGS = getattr(sys, 'abiflags', '')
    USER_DIR = os.path.expanduser('~')
    if IS_WIN:
        DEFAULT_STORAGE_DIR = os.path.join(USER_DIR, 'virtualenv')
    else:
        DEFAULT_STORAGE_DIR = os.path.join(USER_DIR, '.virtualenv')
    DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_STORAGE_DIR, 'virtualenv.ini')
    if IS_PYPY:
        EXPECTED_EXE = 'pypy'
    else:
        EXPECTED_EXE = 'python'
if not IS_WIN:

    def get_installed_pythons():
        return {}


else:
    try:
        import winreg
    except ImportError:
        import _winreg as winreg

    def get_installed_pythons():
        final_exes = dict()
        exes = _get_installed_pythons_for_view('-32', winreg.KEY_WOW64_32KEY)
        exes_64 = _get_installed_pythons_for_view('-64', winreg.KEY_WOW64_64KEY)
        if set(exes.values()) != set(exes_64.values()):
            exes.update(exes_64)
        for version, bitness in sorted(exes):
            exe = exes[(version, bitness)]
            final_exes[version + bitness] = exe
            final_exes[version] = exe
            final_exes[version[0] + bitness] = exe
            final_exes[version[0]] = exe

        return final_exes


    def _get_installed_pythons_for_view(bitness, view):
        exes = dict()
        for key in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            try:
                python_core = winreg.OpenKey(key, 'Software\\Python\\PythonCore', 0, view | winreg.KEY_READ)
            except WindowsError:
                continue

            i = 0
            while True:
                try:
                    version = winreg.EnumKey(python_core, i)
                    i += 1
                    try:
                        at_path = winreg.QueryValue(python_core, '{}\\InstallPath'.format(version))
                    except WindowsError:
                        continue

                    if version.endswith(bitness):
                        version = version[:-len(bitness)]
                    exes[(version, bitness)] = join(at_path, 'python.exe')
                except WindowsError:
                    break

            winreg.CloseKey(python_core)

        return exes


REQUIRED_MODULES = [
 'os',
 'posix',
 'posixpath',
 'nt',
 'ntpath',
 'genericpath',
 'fnmatch',
 'locale',
 'encodings',
 'codecs',
 'stat',
 'UserDict',
 'readline',
 'copy_reg',
 'types',
 're',
 'sre',
 'sre_parse',
 'sre_constants',
 'sre_compile',
 'zlib']
REQUIRED_FILES = [
 'lib-dynload', 'config']
MAJOR, MINOR = sys.version_info[:2]
if MAJOR == 2:
    if MINOR >= 6:
        REQUIRED_MODULES.extend(['warnings', 'linecache', '_abcoll', 'abc'])
    if MINOR >= 7:
        REQUIRED_MODULES.extend(['_weakrefset'])
else:
    if MAJOR == 3:
        REQUIRED_MODULES.extend([
         '_abcoll',
         'warnings',
         'linecache',
         'abc',
         'io',
         '_weakrefset',
         'copyreg',
         'tempfile',
         'random',
         '__future__',
         'collections',
         'keyword',
         'tarfile',
         'shutil',
         'struct',
         'copy',
         'tokenize',
         'token',
         'functools',
         'heapq',
         'bisect',
         'weakref',
         'reprlib'])
        if MINOR >= 2:
            REQUIRED_FILES[-1] = 'config-{}'.format(MAJOR)
        if MINOR >= 3:
            import sysconfig
            platform_dir = sysconfig.get_config_var('PLATDIR')
            REQUIRED_FILES.append(platform_dir)
            REQUIRED_MODULES.extend(['base64', '_dummy_thread', 'hashlib', 'hmac', 'imp', 'importlib', 'rlcompleter'])
        if MINOR >= 4:
            REQUIRED_MODULES.extend(['operator', '_collections_abc', '_bootlocale'])
        if MINOR >= 6:
            REQUIRED_MODULES.extend(['enum'])
if IS_PYPY:
    REQUIRED_MODULES.extend(['traceback', 'linecache'])
    if MAJOR == 3:
        REQUIRED_MODULES.append('_functools')

class Logger(object):
    __doc__ = '\n    Logging object for use in command-line script.  Allows ranges of\n    levels, to avoid some redundancy of displayed information.\n    '
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    NOTIFY = (logging.INFO + logging.WARN) / 2
    WARN = WARNING = logging.WARN
    ERROR = logging.ERROR
    FATAL = logging.FATAL
    LEVELS = [
     DEBUG, INFO, NOTIFY, WARN, ERROR, FATAL]

    def __init__(self, consumers):
        self.consumers = consumers
        self.indent = 0
        self.in_progress = None
        self.in_progress_hanging = False

    def debug(self, msg, *args, **kw):
        (self.log)(self.DEBUG, msg, *args, **kw)

    def info(self, msg, *args, **kw):
        (self.log)(self.INFO, msg, *args, **kw)

    def notify(self, msg, *args, **kw):
        (self.log)(self.NOTIFY, msg, *args, **kw)

    def warn(self, msg, *args, **kw):
        (self.log)(self.WARN, msg, *args, **kw)

    def error(self, msg, *args, **kw):
        (self.log)(self.ERROR, msg, *args, **kw)

    def fatal(self, msg, *args, **kw):
        (self.log)(self.FATAL, msg, *args, **kw)

    def log(self, level, msg, *args, **kw):
        if args:
            if kw:
                raise TypeError('You may give positional or keyword arguments, not both')
        args = args or kw
        rendered = None
        for consumer_level, consumer in self.consumers:
            if self.level_matches(level, consumer_level):
                if self.in_progress_hanging:
                    if consumer in (sys.stdout, sys.stderr):
                        self.in_progress_hanging = False
                        print('')
                        sys.stdout.flush()
                if rendered is None:
                    if args:
                        rendered = msg % args
                    else:
                        rendered = msg
                    rendered = ' ' * self.indent + rendered
                if hasattr(consumer, 'write'):
                    consumer.write(rendered + '\n')
                else:
                    consumer(rendered)

    def start_progress(self, msg):
        if not not self.in_progress:
            raise AssertionError('Tried to start_progress({!r}) while in_progress {!r}'.format(msg, self.in_progress))
        else:
            if self.level_matches(self.NOTIFY, self._stdout_level()):
                print(msg)
                sys.stdout.flush()
                self.in_progress_hanging = True
            else:
                self.in_progress_hanging = False
        self.in_progress = msg

    def end_progress(self, msg='done.'):
        if not self.in_progress:
            raise AssertionError('Tried to end_progress without start_progress')
        else:
            if self.stdout_level_matches(self.NOTIFY):
                if not self.in_progress_hanging:
                    print('...{}{}'.format(self.in_progress, msg))
                    sys.stdout.flush()
                else:
                    print(msg)
                    sys.stdout.flush()
        self.in_progress = None
        self.in_progress_hanging = False

    def show_progress(self):
        """If we are in a progress scope, and no log messages have been
        shown, write out another '.'"""
        if self.in_progress_hanging:
            print('.')
            sys.stdout.flush()

    def stdout_level_matches(self, level):
        """Returns true if a message at this level will go to stdout"""
        return self.level_matches(level, self._stdout_level())

    def _stdout_level(self):
        """Returns the level that stdout runs at"""
        for level, consumer in self.consumers:
            if consumer is sys.stdout:
                return level

        return self.FATAL

    @staticmethod
    def level_matches(level, consumer_level):
        """
        >>> l = Logger([])
        >>> l.level_matches(3, 4)
        False
        >>> l.level_matches(3, 2)
        True
        >>> l.level_matches(slice(None, 3), 3)
        False
        >>> l.level_matches(slice(None, 3), 2)
        True
        >>> l.level_matches(slice(1, 3), 1)
        True
        >>> l.level_matches(slice(2, 3), 1)
        False
        """
        if isinstance(level, slice):
            start, stop = level.start, level.stop
            if start is not None:
                if start > consumer_level:
                    return False
            if stop is not None:
                if stop <= consumer_level:
                    return False
            return True
        else:
            return level >= consumer_level

    @classmethod
    def level_for_integer(cls, level):
        levels = cls.LEVELS
        if level < 0:
            return levels[0]
        else:
            if level >= len(levels):
                return levels[(-1)]
            return levels[level]


logger = Logger([(Logger.LEVELS[(-1)], sys.stdout)])

def mkdir(at_path):
    global logger
    if not os.path.exists(at_path):
        logger.info('Creating %s', at_path)
        os.makedirs(at_path)
    else:
        logger.info('Directory %s already exists', at_path)


def copy_file_or_folder(src, dest, symlink=True):
    if os.path.isdir(src):
        shutil.copytree(src, dest, symlink)
    else:
        shutil.copy2(src, dest)


def copyfile(src, dest, symlink=True):
    if not os.path.exists(src):
        logger.warn('Cannot find file %s (bad symlink)', src)
        return
    else:
        if os.path.exists(dest):
            logger.debug('File %s already exists', dest)
            return
        if not os.path.exists(os.path.dirname(dest)):
            logger.info('Creating parent directories for %s', os.path.dirname(dest))
            os.makedirs(os.path.dirname(dest))
        if symlink and hasattr(os, 'symlink') and not IS_WIN:
            logger.info('Symlinking %s', dest)
            try:
                os.symlink(os.path.realpath(src), dest)
            except (OSError, NotImplementedError):
                logger.info('Symlinking failed, copying to %s', dest)
                copy_file_or_folder(src, dest, symlink)

        else:
            logger.info('Copying to %s', dest)
            copy_file_or_folder(src, dest, symlink)


def writefile(dest, content, overwrite=True):
    if not os.path.exists(dest):
        logger.info('Writing %s', dest)
        with open(dest, 'wb') as (f):
            f.write(content.encode('utf-8'))
        return
    else:
        with open(dest, 'rb') as (f):
            c = f.read()
        if c != content.encode('utf-8'):
            if not overwrite:
                logger.notify('File %s exists with different content; not overwriting', dest)
                return
            logger.notify('Overwriting %s with new content', dest)
            with open(dest, 'wb') as (f):
                f.write(content.encode('utf-8'))
        else:
            logger.info('Content %s already in place', dest)


def rm_tree(folder):
    if os.path.exists(folder):
        logger.notify('Deleting tree %s', folder)
        shutil.rmtree(folder)
    else:
        logger.info('Do not need to delete %s; already gone', folder)


def make_exe(fn):
    if hasattr(os, 'chmod'):
        old_mode = os.stat(fn).st_mode & 4095
        new_mode = (old_mode | 365) & 4095
        os.chmod(fn, new_mode)
        logger.info('Changed mode of %s to %s', fn, oct(new_mode))


def _find_file(filename, folders):
    for folder in reversed(folders):
        files = glob.glob(os.path.join(folder, filename))
        if files:
            if os.path.isfile(files[0]):
                return (
                 True, files[0])

    return (
     False, filename)


@contextlib.contextmanager
def virtualenv_support_dirs():
    """Context manager yielding either [virtualenv_support_dir] or []"""
    if os.path.isdir(join(HERE, 'virtualenv_support')):
        yield [
         join(HERE, 'virtualenv_support')]
    else:
        if IS_ZIPAPP:
            tmpdir = tempfile.mkdtemp()
            try:
                with zipfile.ZipFile(HERE) as (zipf):
                    for member in zipf.namelist():
                        if os.path.dirname(member) == 'virtualenv_support':
                            zipf.extract(member, tmpdir)

                yield [
                 join(tmpdir, 'virtualenv_support')]
            finally:
                shutil.rmtree(tmpdir)

        else:
            if os.path.splitext(os.path.dirname(__file__))[0] != 'virtualenv':
                try:
                    import virtualenv
                except ImportError:
                    yield []
                else:
                    yield [
                     join(os.path.dirname(virtualenv.__file__), 'virtualenv_support')]
            else:
                yield []


class UpdatingDefaultsHelpFormatter(optparse.IndentedHelpFormatter):
    __doc__ = '\n    Custom help formatter for use in ConfigOptionParser that updates\n    the defaults before expanding them, allowing them to show up correctly\n    in the help listing\n    '

    def expand_default(self, option):
        if self.parser is not None:
            self.parser.update_defaults(self.parser.defaults)
        return optparse.IndentedHelpFormatter.expand_default(self, option)


class ConfigOptionParser(optparse.OptionParser):
    __doc__ = '\n    Custom option parser which updates its defaults by checking the\n    configuration files and environmental variables\n    '

    def __init__(self, *args, **kwargs):
        self.config = ConfigParser.RawConfigParser()
        self.files = self.get_config_files()
        self.config.read(self.files)
        (optparse.OptionParser.__init__)(self, *args, **kwargs)

    @staticmethod
    def get_config_files():
        config_file = os.environ.get('VIRTUALENV_CONFIG_FILE', False)
        if config_file:
            if os.path.exists(config_file):
                return [
                 config_file]
        return [
         DEFAULT_CONFIG_FILE]

    def update_defaults(self, defaults):
        """
        Updates the given defaults with values from the config files and
        the environ. Does a little special handling for certain types of
        options (lists).
        """
        config = {}
        config.update(dict(self.get_config_section('virtualenv')))
        config.update(dict(self.get_environ_vars()))
        for key, val in config.items():
            key = key.replace('_', '-')
            if not key.startswith('--'):
                key = '--{}'.format(key)
            option = self.get_option(key)
            if option is not None:
                if not val:
                    pass
                else:
                    if option.action == 'append':
                        val = val.split()
                    else:
                        option.nargs = 1
                    if option.action == 'store_false':
                        val = not strtobool(val)
                    else:
                        if option.action in ('store_true', 'count'):
                            val = strtobool(val)
                        try:
                            val = option.convert_value(key, val)
                        except optparse.OptionValueError:
                            e = sys.exc_info()[1]
                            print('An error occurred during configuration: {!r}'.format(e))
                            sys.exit(3)

                    defaults[option.dest] = val

        return defaults

    def get_config_section(self, name):
        """
        Get a section of a configuration
        """
        if self.config.has_section(name):
            return self.config.items(name)
        else:
            return []

    def get_environ_vars(self, prefix='VIRTUALENV_'):
        """
        Returns a generator with all environmental vars with prefix VIRTUALENV
        """
        for key, val in os.environ.items():
            if key.startswith(prefix):
                yield (
                 key.replace(prefix, '').lower(), val)

    def get_default_values(self):
        """
        Overriding to make updating the defaults after instantiation of
        the option parser possible, update_defaults() does the dirty work.
        """
        if not self.process_default_values:
            return optparse.Values(self.defaults)
        else:
            defaults = self.update_defaults(self.defaults.copy())
            for option in self._get_all_options():
                default = defaults.get(option.dest)
                if isinstance(default, basestring):
                    opt_str = option.get_opt_string()
                    defaults[option.dest] = option.check_value(opt_str, default)

            return optparse.Values(defaults)


def main():
    global logger
    parser = ConfigOptionParser(version=virtualenv_version,
      usage='%prog [OPTIONS] DEST_DIR',
      formatter=(UpdatingDefaultsHelpFormatter()))
    parser.add_option('-v',
      '--verbose', action='count', dest='verbose', default=(5 if DEBUG else 0), help='Increase verbosity.')
    parser.add_option('-q', '--quiet', action='count', dest='quiet', default=0, help='Decrease verbosity.')
    parser.add_option('-p',
      '--python',
      dest='python',
      metavar='PYTHON_EXE',
      help=('The Python interpreter to use, e.g., --python=python3.5 will use the python3.5 interpreter to create the new environment.  The default is the interpreter that virtualenv was installed with ({})'.format(sys.executable)))
    parser.add_option('--clear',
      dest='clear', action='store_true', help='Clear out the non-root install and start from scratch.')
    parser.set_defaults(system_site_packages=False)
    parser.add_option('--no-site-packages',
      dest='system_site_packages',
      action='store_false',
      help='DEPRECATED. Retained only for backward compatibility. Not having access to global site-packages is now the default behavior.')
    parser.add_option('--system-site-packages',
      dest='system_site_packages',
      action='store_true',
      help='Give the virtual environment access to the global site-packages.')
    parser.add_option('--always-copy',
      dest='symlink',
      action='store_false',
      default=True,
      help='Always copy files rather than symlinking.')
    parser.add_option('--relocatable',
      dest='relocatable',
      action='store_true',
      help='Make an EXISTING virtualenv environment relocatable. This fixes up scripts and makes all .pth files relative.')
    parser.add_option('--no-setuptools',
      dest='no_setuptools',
      action='store_true',
      help='Do not install setuptools in the new virtualenv.')
    parser.add_option('--no-pip', dest='no_pip', action='store_true', help='Do not install pip in the new virtualenv.')
    parser.add_option('--no-wheel',
      dest='no_wheel', action='store_true', help='Do not install wheel in the new virtualenv.')
    parser.add_option('--extra-search-dir',
      dest='search_dirs',
      action='append',
      metavar='DIR',
      default=[],
      help='Directory to look for setuptools/pip distributions in. This option can be used multiple times.')
    parser.add_option('--download',
      dest='download',
      default=True,
      action='store_true',
      help='Download pre-installed packages from PyPI.')
    parser.add_option('--no-download',
      '--never-download',
      dest='download',
      action='store_false',
      help='Do not download pre-installed packages from PyPI.')
    parser.add_option('--prompt', dest='prompt', help='Provides an alternative prompt prefix for this environment.')
    parser.add_option('--setuptools',
      dest='setuptools',
      action='store_true',
      help='DEPRECATED. Retained only for backward compatibility. This option has no effect.')
    parser.add_option('--distribute',
      dest='distribute',
      action='store_true',
      help='DEPRECATED. Retained only for backward compatibility. This option has no effect.')
    parser.add_option('--unzip-setuptools',
      action='store_true',
      help='DEPRECATED.  Retained only for backward compatibility. This option has no effect.')
    if 'extend_parser' in globals():
        extend_parser(parser)
    options, args = parser.parse_args()
    if 'adjust_options' in globals():
        adjust_options(options, args)
    verbosity = options.verbose - options.quiet
    logger = Logger([(Logger.level_for_integer(2 - verbosity), sys.stdout)])

    def should_reinvoke(options):
        """Do we need to reinvoke ourself?"""
        if options.python:
            if not os.environ.get('VIRTUALENV_INTERPRETER_RUNNING'):
                interpreter = resolve_interpreter(options.python)
                if interpreter != sys.executable:
                    return interpreter
        if IS_WIN:
            if getattr(sys, '_base_executable', sys.executable) != sys.executable:
                return sys._base_executable
            if '__PYVENV_LAUNCHER__' in os.environ:
                import _winapi
                del os.environ['__PYVENV_LAUNCHER__']
                return _winapi.GetModuleFileName(0)

    interpreter = should_reinvoke(options)
    if interpreter is None:
        if options.python:
            logger.warn('Already using interpreter {}'.format(sys.executable))
    else:
        env = os.environ.copy()
        logger.notify('Running virtualenv with interpreter {}'.format(interpreter))
        env['VIRTUALENV_INTERPRETER_RUNNING'] = 'true'
        if '__PYVENV_LAUNCHER__' in env:
            del env['__PYVENV_LAUNCHER__']
        file = __file__
    if file.endswith('.pyc'):
        file = file[:-1]
    else:
        if IS_ZIPAPP:
            file = HERE
        sub_process_call = subprocess.Popen(([interpreter, file] + sys.argv[1:]), env=env)
        raise SystemExit(sub_process_call.wait())
    if not args:
        print('You must provide a DEST_DIR')
        parser.print_help()
        sys.exit(2)
    if len(args) > 1:
        print('There must be only one argument: DEST_DIR (you gave {})'.format(' '.join(args)))
        parser.print_help()
        sys.exit(2)
    home_dir = args[0]
    if os.path.exists(home_dir):
        if os.path.isfile(home_dir):
            logger.fatal('ERROR: File already exists and is not a directory.')
            logger.fatal('Please provide a different path or delete the file.')
            sys.exit(3)
    if os.pathsep in home_dir:
        logger.fatal("ERROR: target path contains the operating system path separator '{}'".format(os.pathsep))
        logger.fatal('This is not allowed as would make the activation scripts unusable.'.format(os.pathsep))
        sys.exit(3)
    if os.environ.get('WORKING_ENV'):
        logger.fatal('ERROR: you cannot run virtualenv while in a working env')
        logger.fatal('Please deactivate your working env, then re-run this script')
        sys.exit(3)
    if 'PYTHONHOME' in os.environ:
        logger.warn('PYTHONHOME is set.  You *must* activate the virtualenv before using it')
        del os.environ['PYTHONHOME']
    if options.relocatable:
        make_environment_relocatable(home_dir)
        return
    with virtualenv_support_dirs() as (search_dirs):
        create_environment(home_dir,
          site_packages=(options.system_site_packages),
          clear=(options.clear),
          prompt=(options.prompt),
          search_dirs=(search_dirs + options.search_dirs),
          download=(options.download),
          no_setuptools=(options.no_setuptools),
          no_pip=(options.no_pip),
          no_wheel=(options.no_wheel),
          symlink=(options.symlink))
    if 'after_install' in globals():
        after_install(options, home_dir)


def call_subprocess(cmd, show_stdout=True, filter_stdout=None, cwd=None, raise_on_return_code=True, extra_env=None, remove_from_env=None, stdin=None):
    cmd_parts = []
    for part in cmd:
        if len(part) > 45:
            part = part[:20] + '...' + part[-20:]
        else:
            if ' ' in part or '\n' in part or '"' in part or "'" in part:
                part = '"{}"'.format(part.replace('"', '\\"'))
            if hasattr(part, 'decode'):
                try:
                    part = part.decode(sys.getdefaultencoding())
                except UnicodeDecodeError:
                    part = part.decode(sys.getfilesystemencoding())

        cmd_parts.append(part)

    cmd_desc = ' '.join(cmd_parts)
    if show_stdout:
        stdout = None
    else:
        stdout = subprocess.PIPE
    logger.debug('Running command {}'.format(cmd_desc))
    if extra_env or remove_from_env:
        env = os.environ.copy()
        if extra_env:
            env.update(extra_env)
    else:
        if remove_from_env:
            for var_name in remove_from_env:
                env.pop(var_name, None)

        else:
            env = None
        try:
            proc = subprocess.Popen(cmd,
              stderr=(subprocess.STDOUT),
              stdin=(None if stdin is None else subprocess.PIPE),
              stdout=stdout,
              cwd=cwd,
              env=env)
        except Exception:
            e = sys.exc_info()[1]
            logger.fatal('Error {} while executing command {}'.format(e, cmd_desc))
            raise

        all_output = []
        if stdout is not None:
            if stdin is not None:
                with proc.stdin:
                    proc.stdin.write(stdin)
            encoding = sys.getdefaultencoding()
            fs_encoding = sys.getfilesystemencoding()
            with proc.stdout as (stdout):
                while 1:
                    line = stdout.readline()
                    try:
                        line = line.decode(encoding)
                    except UnicodeDecodeError:
                        line = line.decode(fs_encoding)

                    if not line:
                        break
                    line = line.rstrip()
                    all_output.append(line)
                    if filter_stdout:
                        level = filter_stdout(line)
                        if isinstance(level, tuple):
                            level, line = level
                        logger.log(level, line)
                        if not logger.stdout_level_matches(level):
                            logger.show_progress()
                    else:
                        logger.info(line)

        else:
            proc.communicate(stdin)
    proc.wait()
    if proc.returncode:
        if raise_on_return_code:
            if all_output:
                logger.notify('Complete output from command {}:'.format(cmd_desc))
                logger.notify('\n'.join(all_output) + '\n----------------------------------------')
            raise OSError('Command {} failed with error code {}'.format(cmd_desc, proc.returncode))
        else:
            logger.warn('Command {} had error code {}'.format(cmd_desc, proc.returncode))
    return all_output


def filter_install_output(line):
    if line.strip().startswith('running'):
        return Logger.INFO
    else:
        return Logger.DEBUG


def find_wheels(projects, search_dirs):
    """Find wheels from which we can import PROJECTS.

    Scan through SEARCH_DIRS for a wheel for each PROJECT in turn. Return
    a list of the first wheel found for each PROJECT
    """
    wheels = []
    for project in projects:
        for dirname in search_dirs:
            files = glob.glob(os.path.join(dirname, '{}-*.whl'.format(project)))
            if files:
                versions = sorted([(
                 tuple(int(i) for i in os.path.basename(f).split('-')[1].split('.')), f) for f in files])
                if project == 'pip':
                    if sys.version_info[0:2] == (3, 4):
                        wheel = next(p for v, p in versions if v <= (19, 1, 1))
                else:
                    wheel = versions[0][1]
                wheels.append(wheel)
                break
        else:
            logger.fatal('Cannot find a wheel for {}'.format(project))

    return wheels


def install_wheel(project_names, py_executable, search_dirs=None, download=False):
    if search_dirs is None:
        search_dirs_context = virtualenv_support_dirs
    else:

        @contextlib.contextmanager
        def search_dirs_context():
            yield search_dirs

    with search_dirs_context() as (search_dirs):
        _install_wheel_with_search_dir(download, project_names, py_executable, search_dirs)


def _install_wheel_with_search_dir(download, project_names, py_executable, search_dirs):
    wheels = find_wheels(['setuptools', 'pip'], search_dirs)
    python_path = os.pathsep.join(wheels)
    try:
        from urlparse import urljoin
        from urllib import pathname2url
    except ImportError:
        from urllib.parse import urljoin
        from urllib.request import pathname2url

    def space_path2url(p):
        if ' ' not in p:
            return p
        else:
            return urljoin('file:', pathname2url(os.path.abspath(p)))

    find_links = ' '.join(space_path2url(d) for d in search_dirs)
    extra_args = [
     '--ignore-installed', '-v']
    if DEBUG:
        extra_args.append('-v')
    config = _pip_config(py_executable, python_path)
    defined_cert = bool(config.get('install.cert') or config.get(':env:.cert') or config.get('global.cert'))
    script = textwrap.dedent('\n        import sys\n        import pkgutil\n        import tempfile\n        import os\n\n        defined_cert = {defined_cert}\n\n        try:\n            from pip._internal import main as _main\n            cert_data = pkgutil.get_data("pip._vendor.certifi", "cacert.pem")\n        except ImportError:\n            from pip import main as _main\n            cert_data = pkgutil.get_data("pip._vendor.requests", "cacert.pem")\n        except IOError:\n            cert_data = None\n\n        if not defined_cert and cert_data is not None:\n            cert_file = tempfile.NamedTemporaryFile(delete=False)\n            cert_file.write(cert_data)\n            cert_file.close()\n        else:\n            cert_file = None\n\n        try:\n            args = ["install"] + [{extra_args}]\n            if cert_file is not None:\n                args += ["--cert", cert_file.name]\n            args += sys.argv[1:]\n\n            sys.exit(_main(args))\n        finally:\n            if cert_file is not None:\n                os.remove(cert_file.name)\n    '.format(defined_cert=defined_cert,
      extra_args=(', '.join(repr(i) for i in extra_args)))).encode('utf8')
    if sys.version_info[0:2] == (3, 4):
        at = project_names.index('pip')
        project_names[at] = 'pip<19.2'
    cmd = [py_executable, '-'] + project_names
    logger.start_progress('Installing {}...'.format(', '.join(project_names)))
    logger.indent += 2
    env = {'PYTHONPATH':python_path, 
     'PIP_FIND_LINKS':find_links, 
     'PIP_USE_WHEEL':'1', 
     'PIP_ONLY_BINARY':':all:', 
     'PIP_USER':'0', 
     'PIP_NO_INPUT':'1'}
    if not download:
        env['PIP_NO_INDEX'] = '1'
    try:
        call_subprocess(cmd, show_stdout=False, extra_env=env, stdin=script)
    finally:
        logger.indent -= 2
        logger.end_progress()


def _pip_config(py_executable, python_path):
    cmd = [
     py_executable, '-m', 'pip', 'config', 'list']
    config = {}
    for line in call_subprocess(cmd,
      show_stdout=False,
      extra_env={'PYTHONPATH': python_path},
      remove_from_env=[
     'PIP_VERBOSE', 'PIP_QUIET'],
      raise_on_return_code=False):
        key, _, value = line.partition('=')
        if value:
            config[key] = ast.literal_eval(value)

    return config


def create_environment(home_dir, site_packages=False, clear=False, prompt=None, search_dirs=None, download=False, no_setuptools=False, no_pip=False, no_wheel=False, symlink=True):
    """
    Creates a new environment in ``home_dir``.

    If ``site_packages`` is true, then the global ``site-packages/``
    directory will be on the path.

    If ``clear`` is true (default False) then the environment will
    first be cleared.
    """
    home_dir, lib_dir, inc_dir, bin_dir = path_locations(home_dir)
    py_executable = os.path.abspath(install_python(home_dir, lib_dir, inc_dir, bin_dir, site_packages=site_packages, clear=clear, symlink=symlink))
    install_distutils(home_dir)
    to_install = []
    if not no_setuptools:
        to_install.append('setuptools')
    if not no_pip:
        to_install.append('pip')
    if not no_wheel:
        to_install.append('wheel')
    if to_install:
        install_wheel(to_install, py_executable, search_dirs, download=download)
    install_activate(home_dir, bin_dir, prompt)
    install_python_config(home_dir, bin_dir, prompt)


def is_executable_file(fpath):
    return os.path.isfile(fpath) and is_executable(fpath)


def path_locations(home_dir, dry_run=False):
    """Return the path locations for the environment (where libraries are,
    where scripts go, etc)"""
    home_dir = os.path.abspath(home_dir)
    lib_dir, inc_dir, bin_dir = (None, None, None)
    if IS_WIN:
        if not dry_run:
            mkdir(home_dir)
        if ' ' in home_dir:
            import ctypes
            get_short_path_name = ctypes.windll.kernel32.GetShortPathNameW
            size = max(len(home_dir) + 1, 256)
            buf = ctypes.create_unicode_buffer(size)
            try:
                u = unicode
            except NameError:
                u = str

            ret = get_short_path_name(u(home_dir), buf, size)
            if not ret:
                print('Error: the path "{}" has a space in it'.format(home_dir))
                print('We could not determine the short pathname for it.')
                print('Exiting.')
                sys.exit(3)
            home_dir = str(buf.value)
        lib_dir = join(home_dir, 'Lib')
        inc_dir = join(home_dir, 'Include')
        bin_dir = join(home_dir, 'Scripts')
    else:
        if IS_PYPY:
            lib_dir = home_dir
            inc_dir = join(home_dir, 'include')
            bin_dir = join(home_dir, 'bin')
        else:
            if not IS_WIN:
                lib_dir = join(home_dir, 'lib', PY_VERSION)
                inc_dir = join(home_dir, 'include', PY_VERSION + ABI_FLAGS)
                bin_dir = join(home_dir, 'bin')
    return (
     home_dir, lib_dir, inc_dir, bin_dir)


def change_prefix(filename, dst_prefix):
    prefixes = [
     sys.prefix]
    if IS_DARWIN:
        prefixes.extend((
         os.path.join('/Library/Python', VERSION, 'site-packages'),
         os.path.join(sys.prefix, 'Extras', 'lib', 'python'),
         os.path.join('~', 'Library', 'Python', VERSION, 'site-packages'),
         os.path.join('~', '.local', 'lib', 'python', VERSION, 'site-packages'),
         os.path.join('~', 'Library', 'Python', VERSION, 'lib', 'python', 'site-packages')))
    if hasattr(sys, 'real_prefix'):
        prefixes.append(sys.real_prefix)
    if hasattr(sys, 'base_prefix'):
        prefixes.append(sys.base_prefix)
    else:
        prefixes = list(map(os.path.expanduser, prefixes))
        prefixes = list(map(os.path.abspath, prefixes))
        prefixes = sorted(prefixes, key=len, reverse=True)
        filename = os.path.abspath(filename)
        if IS_WIN and filename[0] in 'abcdefghijklmnopqrstuvwxyz':
            filename = filename[0].upper() + filename[1:]
        for i, prefix in enumerate(prefixes):
            if IS_WIN and prefix[0] in 'abcdefghijklmnopqrstuvwxyz':
                prefixes[i] = prefix[0].upper() + prefix[1:]

        for src_prefix in prefixes:
            if filename.startswith(src_prefix):
                _, relative_path = filename.split(src_prefix, 1)
                if src_prefix != os.sep:
                    assert relative_path[0] == os.sep
                    relative_path = relative_path[1:]
                return join(dst_prefix, relative_path)

        assert False, 'Filename {} does not start with any of these prefixes: {}'.format(filename, prefixes)


def find_module_filename(modname):
    if sys.version_info < (3, 4):
        import imp
        try:
            file_handler, filepath, _ = imp.find_module(modname)
        except ImportError:
            return
        else:
            if file_handler is not None:
                file_handler.close()
            return filepath
    else:
        import importlib.util
        if sys.version_info < (3, 5):

            def find_spec(modname):
                loader = importlib.find_loader(modname)
                if loader is None:
                    return
                else:
                    return importlib.util.spec_from_loader(modname, loader)

        else:
            find_spec = importlib.util.find_spec
        spec = find_spec(modname)
        if spec is None:
            return
        if not os.path.exists(spec.origin):
            return
        else:
            filepath = spec.origin
            if os.path.basename(filepath) == '__init__.py':
                filepath = os.path.dirname(filepath)
            return filepath


def copy_required_modules(dst_prefix, symlink):
    for modname in REQUIRED_MODULES:
        if modname in sys.builtin_module_names:
            logger.info('Ignoring built-in bootstrap module: %s' % modname)
            continue
        filename = find_module_filename(modname)
        if filename is None:
            logger.info('Cannot import bootstrap module: %s' % modname)
        else:
            if modname == 'readline':
                if IS_DARWIN:
                    if not (IS_PYPY or filename.endswith(join('lib-dynload', 'readline.so'))):
                        dst_filename = join(dst_prefix, 'lib', PY_VERSION, 'readline.so')
                    elif modname == 'readline':
                        if IS_WIN:
                            dst_filename = None
                    else:
                        dst_filename = change_prefix(filename, dst_prefix)
                elif dst_filename is not None:
                    copyfile(filename, dst_filename, symlink)
                if filename.endswith('.pyc'):
                    py_file = filename[:-1]
                    if os.path.exists(py_file):
                        copyfile(py_file, dst_filename[:-1], symlink)


def copy_required_files(src_dir, lib_dir, symlink):
    if not os.path.isdir(src_dir):
        return
    for fn in os.listdir(src_dir):
        bn = os.path.splitext(fn)[0]
        if fn != 'site-packages' and bn in REQUIRED_FILES:
            copyfile(join(src_dir, fn), join(lib_dir, fn), symlink)


def copy_license(prefix, dst_prefix, lib_dir, symlink):
    """Copy the license file so `license()` builtin works"""
    lib64_dir = lib_dir.replace('lib', 'lib64')
    for license_path in (
     os.path.join(prefix, os.path.relpath(lib_dir, dst_prefix), 'LICENSE.txt'),
     os.path.join(prefix, os.path.relpath(lib64_dir, dst_prefix), 'LICENSE.txt'),
     os.path.join(prefix, 'LICENSE.txt'),
     os.path.join(prefix, 'LICENSE')):
        if os.path.exists(license_path):
            dest = subst_path(license_path, prefix, dst_prefix)
            copyfile(license_path, dest, symlink)
            return

    logger.warn('No LICENSE.txt / LICENSE found in source')


def copy_include_dir(include_src, include_dest, symlink):
    """Copy headers from *include_src* to *include_dest* symlinking if required"""
    if not os.path.isdir(include_src):
        return
    else:
        if IS_PYPY:
            for fn in os.listdir(include_src):
                copyfile(join(include_src, fn), join(include_dest, fn), symlink)

        else:
            copyfile(include_src, include_dest, symlink)


def copy_tcltk(src, dest, symlink):
    """ copy tcl/tk libraries on Windows (issue #93) """
    for lib_version in ('8.5', '8.6'):
        for libname in ('tcl', 'tk'):
            src_dir = join(src, 'tcl', libname + lib_version)
            dest_dir = join(dest, 'tcl', libname + lib_version)
            if os.path.exists(src_dir) and not os.path.exists(dest_dir):
                copy_file_or_folder(src_dir, dest_dir, symlink)


def subst_path(prefix_path, prefix, home_dir):
    prefix_path = os.path.normpath(prefix_path)
    prefix = os.path.normpath(prefix)
    home_dir = os.path.normpath(home_dir)
    if not prefix_path.startswith(prefix):
        logger.warn('Path not in prefix %r %r', prefix_path, prefix)
        return
    else:
        return prefix_path.replace(prefix, home_dir, 1)


def install_python(home_dir, lib_dir, inc_dir, bin_dir, site_packages, clear, symlink=True):
    """Install just the base environment, no distutils patches etc"""
    if sys.executable.startswith(bin_dir):
        print('Please use the *system* python to run this script')
        return
    else:
        if clear:
            rm_tree(lib_dir)
            logger.notify('Not deleting %s', bin_dir)
        else:
            if hasattr(sys, 'real_prefix'):
                logger.notify('Using real prefix %r', sys.real_prefix)
                prefix = sys.real_prefix
            else:
                if hasattr(sys, 'base_prefix'):
                    logger.notify('Using base prefix %r', sys.base_prefix)
                    prefix = sys.base_prefix
                else:
                    prefix = sys.prefix
                prefix = os.path.abspath(prefix)
                mkdir(lib_dir)
                fix_lib64(lib_dir, symlink)
                stdlib_dirs = [os.path.dirname(os.__file__)]
                if IS_WIN:
                    stdlib_dirs.append(join(os.path.dirname(stdlib_dirs[0]), 'DLLs'))
                else:
                    if IS_DARWIN:
                        stdlib_dirs.append(join(stdlib_dirs[0], 'site-packages'))
                    else:
                        if hasattr(os, 'symlink'):
                            logger.info('Symlinking Python bootstrap modules')
                        else:
                            logger.info('Copying Python bootstrap modules')
                        logger.indent += 2
                        try:
                            for stdlib_dir in stdlib_dirs:
                                copy_required_files(stdlib_dir, lib_dir, symlink)

                            copy_required_modules(home_dir, symlink)
                            copy_license(prefix, home_dir, lib_dir, symlink)
                        finally:
                            logger.indent -= 2

                        if IS_WIN:
                            copy_tcltk(prefix, home_dir, symlink)
                        mkdir(join(lib_dir, 'site-packages'))
                        import site
                        site_filename = site.__file__
                        if site_filename.endswith('.pyc') or site_filename.endswith('.pyo'):
                            site_filename = site_filename[:-1]
                        elif site_filename.endswith('$py.class'):
                            site_filename = site_filename.replace('$py.class', '.py')
                        else:
                            site_filename_dst = change_prefix(site_filename, home_dir)
                            site_dir = os.path.dirname(site_filename_dst)
                            writefile(site_filename_dst, SITE_PY)
                            writefile(join(site_dir, 'orig-prefix.txt'), prefix)
                            site_packages_filename = join(site_dir, 'no-global-site-packages.txt')
                            if not site_packages:
                                writefile(site_packages_filename, '')
                            if IS_PYPY or IS_WIN:
                                standard_lib_include_dir = join(prefix, 'include')
                            else:
                                standard_lib_include_dir = join(prefix, 'include', PY_VERSION + ABI_FLAGS)
                            if os.path.exists(standard_lib_include_dir):
                                copy_include_dir(standard_lib_include_dir, inc_dir, symlink)
                            else:
                                logger.debug('No include dir %s', standard_lib_include_dir)
                            platform_include_dir = distutils.sysconfig.get_python_inc(plat_specific=1)
                            if platform_include_dir != standard_lib_include_dir:
                                platform_include_dest = distutils.sysconfig.get_python_inc(plat_specific=1, prefix=home_dir)
                                if platform_include_dir == platform_include_dest:
                                    platform_include_dest = subst_path(platform_include_dir, prefix, home_dir)
                                if platform_include_dest:
                                    copy_include_dir(platform_include_dir, platform_include_dest, symlink)
                            if os.path.realpath(sys.exec_prefix) != os.path.realpath(prefix):
                                if not IS_PYPY:
                                    if IS_WIN:
                                        exec_dir = join(sys.exec_prefix, 'lib')
                                    else:
                                        exec_dir = join(sys.exec_prefix, 'lib', PY_VERSION)
                                    copy_required_files(exec_dir, lib_dir, symlink)
                            mkdir(bin_dir)
                            py_executable = join(bin_dir, os.path.basename(sys.executable))
                            if 'Python.framework' in prefix:
                                if os.environ.get('__PYVENV_LAUNCHER__'):
                                    del os.environ['__PYVENV_LAUNCHER__']
                                if re.search('/Python(?:-32|-64)*$', py_executable):
                                    py_executable = os.path.join(os.path.dirname(py_executable), 'python')
                            logger.notify('New %s executable in %s', EXPECTED_EXE, py_executable)
                            pc_build_dir = os.path.dirname(sys.executable)
                            pyd_pth = os.path.join(lib_dir, 'site-packages', 'virtualenv_builddir_pyd.pth')
                            if IS_WIN:
                                if os.path.exists(os.path.join(pc_build_dir, 'build.bat')):
                                    logger.notify('Detected python running from build directory %s', pc_build_dir)
                                    logger.notify('Writing .pth file linking to build directory for *.pyd files')
                                    writefile(pyd_pth, pc_build_dir)
                            if os.path.exists(pyd_pth):
                                logger.info('Deleting %s (not Windows env or not build directory python)', pyd_pth)
                                os.unlink(pyd_pth)
                            if sys.executable != py_executable:
                                executable = sys.executable
                                shutil.copyfile(executable, py_executable)
                                make_exe(py_executable)
                                if IS_WIN or IS_CYGWIN:
                                    python_w = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
                                    if os.path.exists(python_w):
                                        logger.info('Also created pythonw.exe')
                                        shutil.copyfile(python_w, os.path.join(os.path.dirname(py_executable), 'pythonw.exe'))
                                    python_d = os.path.join(os.path.dirname(sys.executable), 'python_d.exe')
                                    python_d_dest = os.path.join(os.path.dirname(py_executable), 'python_d.exe')
                                    if os.path.exists(python_d):
                                        logger.info('Also created python_d.exe')
                                        shutil.copyfile(python_d, python_d_dest)
                                    else:
                                        if os.path.exists(python_d_dest):
                                            logger.info('Removed python_d.exe as it is no longer at the source')
                                            os.unlink(python_d_dest)
                                        if IS_PYPY:
                                            py_executable_dll_s = [
                                             ('libpypy-c.dll', 'libpypy_d-c.dll')]
                                        else:
                                            py_executable_dll_s = [
                                             (
                                              'python{}.dll'.format(sys.version_info[0]), 'python{}_d.dll'.format(sys.version_info[0])),
                                             (
                                              'python{}{}.dll'.format(sys.version_info[0], sys.version_info[1]),
                                              'python{}{}_d.dll'.format(sys.version_info[0], sys.version_info[1]))]
                                    for py_executable_dll, py_executable_dll_d in py_executable_dll_s:
                                        python_dll = os.path.join(os.path.dirname(sys.executable), py_executable_dll)
                                        python_dll_d = os.path.join(os.path.dirname(sys.executable), py_executable_dll_d)
                                        python_dll_d_dest = os.path.join(os.path.dirname(py_executable), py_executable_dll_d)
                                        if os.path.exists(python_dll):
                                            logger.info('Also created %s', py_executable_dll)
                                            shutil.copyfile(python_dll, os.path.join(os.path.dirname(py_executable), py_executable_dll))
                                        if os.path.exists(python_dll_d):
                                            logger.info('Also created %s', py_executable_dll_d)
                                            shutil.copyfile(python_dll_d, python_dll_d_dest)
                                        elif os.path.exists(python_dll_d_dest):
                                            logger.info('Removed %s as the source does not exist', python_dll_d_dest)
                                            os.unlink(python_dll_d_dest)

                                if IS_PYPY:
                                    python_executable = os.path.join(os.path.dirname(py_executable), 'python')
                                    if IS_WIN or IS_CYGWIN:
                                        python_executable += '.exe'
                                    logger.info('Also created executable %s', python_executable)
                                    copyfile(py_executable, python_executable, symlink)
                                    if IS_WIN:
                                        for name in ('libexpat.dll', 'libeay32.dll',
                                                     'ssleay32.dll', 'sqlite3.dll',
                                                     'tcl85.dll', 'tk85.dll'):
                                            src = join(prefix, name)
                                            if os.path.exists(src):
                                                copyfile(src, join(bin_dir, name), symlink)

                                        for d in sys.path:
                                            if d.endswith('lib_pypy'):
                                                break
                                        else:
                                            logger.fatal('Could not find lib_pypy in sys.path')
                                            raise SystemExit(3)

                                        logger.info('Copying lib_pypy')
                                        copyfile(d, os.path.join(home_dir, 'lib_pypy'), symlink)
                            if os.path.splitext(os.path.basename(py_executable))[0] != EXPECTED_EXE:
                                secondary_exe = os.path.join(os.path.dirname(py_executable), EXPECTED_EXE)
                                py_executable_ext = os.path.splitext(py_executable)[1]
                                if py_executable_ext.lower() == '.exe':
                                    secondary_exe += py_executable_ext
                                if os.path.exists(secondary_exe):
                                    logger.warn('Not overwriting existing {} script {} (you must use {})'.format(EXPECTED_EXE, secondary_exe, py_executable))
                                else:
                                    logger.notify('Also creating executable in %s', secondary_exe)
                                    shutil.copyfile(sys.executable, secondary_exe)
                                    make_exe(secondary_exe)
                            if '.framework' in prefix:
                                original_python = None
                                if 'Python.framework' in prefix:
                                    logger.debug('MacOSX Python framework detected')
                                    original_python = os.path.join(prefix, 'Resources/Python.app/Contents/MacOS/Python')
                                if 'EPD' in prefix:
                                    logger.debug('EPD framework detected')
                                    original_python = os.path.join(prefix, 'bin/python')
                                shutil.copy(original_python, py_executable)
                                virtual_lib = os.path.join(home_dir, '.Python')
                                if os.path.exists(virtual_lib):
                                    os.unlink(virtual_lib)
                                copyfile(os.path.join(prefix, 'Python'), virtual_lib, symlink)
                                try:
                                    mach_o_change(py_executable, os.path.join(prefix, 'Python'), '@executable_path/../.Python')
                                except Exception:
                                    e = sys.exc_info()[1]
                                    logger.warn('Could not call mach_o_change: %s. Trying to call install_name_tool instead.', e)
                                    try:
                                        call_subprocess([
                                         'install_name_tool',
                                         '-change',
                                         os.path.join(prefix, 'Python'),
                                         '@executable_path/../.Python',
                                         py_executable])
                                    except Exception:
                                        logger.fatal("Could not call install_name_tool -- you must have Apple's development tools installed")
                                        raise

                            if not IS_WIN:
                                py_exe_version_major = 'python{}'.format(sys.version_info[0])
                                py_exe_version_major_minor = 'python{}.{}'.format(sys.version_info[0], sys.version_info[1])
                                py_exe_no_version = 'python'
                                required_symlinks = [py_exe_no_version, py_exe_version_major, py_exe_version_major_minor]
                                py_executable_base = os.path.basename(py_executable)
                                if py_executable_base in required_symlinks:
                                    required_symlinks.remove(py_executable_base)
                                for pth in required_symlinks:
                                    full_pth = join(bin_dir, pth)
                                    if os.path.exists(full_pth):
                                        os.unlink(full_pth)
                                    if symlink:
                                        os.symlink(py_executable_base, full_pth)
                                    else:
                                        copyfile(py_executable, full_pth, symlink)

                            cmd = [
                             py_executable,
                             '-c',
                             'import sys;out=sys.stdout;getattr(out, "buffer", out).write(sys.prefix.encode("utf-8"))']
                            (logger.info)(*('Testing executable with %s %s "%s"', ), *cmd)
                            try:
                                proc = subprocess.Popen(cmd, stdout=(subprocess.PIPE))
                                proc_stdout, proc_stderr = proc.communicate()
                            except OSError:
                                e = sys.exc_info()[1]
                                if e.errno == errno.EACCES:
                                    logger.fatal('ERROR: The executable {} could not be run: {}'.format(py_executable, e))
                                    sys.exit(100)
                                else:
                                    raise e

                        proc_stdout = proc_stdout.strip().decode('utf-8')
                        proc_stdout = os.path.normcase(os.path.realpath(proc_stdout))
                        norm_home_dir = os.path.normcase(os.path.realpath(home_dir))
                        if hasattr(norm_home_dir, 'decode'):
                            norm_home_dir = norm_home_dir.decode(sys.getfilesystemencoding())
                    if proc_stdout != norm_home_dir:
                        logger.fatal('ERROR: The executable %s is not functioning', py_executable)
                        logger.fatal('ERROR: It thinks sys.prefix is {!r} (should be {!r})'.format(proc_stdout, norm_home_dir))
                        logger.fatal('ERROR: virtualenv is not compatible with this system or executable')
                        if IS_WIN:
                            logger.fatal('Note: some Windows users have reported this error when they installed Python for "Only this user" or have multiple versions of Python installed. Copying the appropriate PythonXX.dll to the virtualenv Scripts/ directory may fix this problem.')
                        sys.exit(100)
                    else:
                        logger.info('Got sys.prefix result: %r', proc_stdout)
                pydistutils = os.path.expanduser('~/.pydistutils.cfg')
                if os.path.exists(pydistutils):
                    logger.notify('Please make sure you remove any previous custom paths from your %s file.', pydistutils)
                fix_local_scheme(home_dir, symlink)
                if site_packages:
                    if os.path.exists(site_packages_filename):
                        logger.info('Deleting %s', site_packages_filename)
                        os.unlink(site_packages_filename)
        return py_executable


def install_activate(home_dir, bin_dir, prompt=None):
    if IS_WIN:
        files = {'activate.bat':ACTIVATE_BAT, 
         'deactivate.bat':DEACTIVATE_BAT,  'activate.ps1':ACTIVATE_PS}
        drive, tail = os.path.splitdrive(home_dir.replace(os.sep, '/'))
        home_dir_msys = (drive and '/{}{}' or '{}{}').format(drive[:1], tail)
        home_dir_sh = '$(if [ "$OSTYPE" "==" "cygwin" ]; then cygpath -u \'{}\'; else echo \'{}\'; fi;)'.format(home_dir, home_dir_msys)
        files['activate'] = ACTIVATE_SH.replace('__VIRTUAL_ENV__', home_dir_sh)
    else:
        files = {'activate':ACTIVATE_SH,  'activate.fish':ACTIVATE_FISH, 
         'activate.csh':ACTIVATE_CSH, 
         'activate.ps1':ACTIVATE_PS}
    files['activate_this.py'] = ACTIVATE_THIS
    if sys.version_info >= (3, 4):
        files['activate.xsh'] = ACTIVATE_XSH
    install_files(home_dir, bin_dir, prompt, files)


def install_files(home_dir, bin_dir, prompt, files):
    if hasattr(home_dir, 'decode'):
        home_dir = home_dir.decode(sys.getfilesystemencoding())
    virtualenv_name = os.path.basename(home_dir)
    for name, content in files.items():
        content = content.replace('__VIRTUAL_PROMPT__', prompt or '')
        content = content.replace('__VIRTUAL_WINPROMPT__', prompt or '({}) '.format(virtualenv_name))
        content = content.replace('__VIRTUAL_ENV__', home_dir)
        content = content.replace('__VIRTUAL_NAME__', virtualenv_name)
        content = content.replace('__BIN_NAME__', os.path.basename(bin_dir))
        content = content.replace('__PATH_SEP__', os.pathsep)
        writefile(os.path.join(bin_dir, name), content)


def install_python_config(home_dir, bin_dir, prompt=None):
    if IS_WIN:
        files = {}
    else:
        files = {'python-config': PYTHON_CONFIG}
    install_files(home_dir, bin_dir, prompt, files)
    for name, _ in files.items():
        make_exe(os.path.join(bin_dir, name))


def install_distutils(home_dir):
    distutils_path = change_prefix(distutils.__path__[0], home_dir)
    mkdir(distutils_path)
    writefile(os.path.join(distutils_path, '__init__.py'), DISTUTILS_INIT)
    writefile((os.path.join(distutils_path, 'distutils.cfg')), DISTUTILS_CFG, overwrite=False)


def fix_local_scheme(home_dir, symlink=True):
    """
    Platforms that use the "posix_local" install scheme (like Ubuntu with
    Python 2.7) need to be given an additional "local" location, sigh.
    """
    try:
        import sysconfig
    except ImportError:
        pass
    else:
        if sysconfig._get_default_scheme() == 'posix_local':
            local_path = os.path.join(home_dir, 'local')
            if not os.path.exists(local_path):
                os.mkdir(local_path)
                for subdir_name in os.listdir(home_dir):
                    if subdir_name == 'local':
                        pass
                    else:
                        copyfile(os.path.abspath(os.path.join(home_dir, subdir_name)), os.path.join(local_path, subdir_name), symlink)


def fix_lib64(lib_dir, symlink=True):
    """
    Some platforms (particularly Gentoo on x64) put things in lib64/pythonX.Y
    instead of lib/pythonX.Y.  If this is such a platform we'll just create a
    symlink so lib64 points to lib
    """
    if IS_PYPY:
        logger.debug('PyPy detected, skipping lib64 symlinking')
        return
    else:
        if not [p for p in distutils.sysconfig.get_config_vars().values() if isinstance(p, basestring) if 'lib64' in p]:
            return
        else:
            logger.debug('This system uses lib64; symlinking lib64 to lib')
            assert os.path.basename(lib_dir) == PY_VERSION, 'Unexpected python lib dir: {!r}'.format(lib_dir)
            lib_parent = os.path.dirname(lib_dir)
            top_level = os.path.dirname(lib_parent)
            lib_dir = os.path.join(top_level, 'lib')
            lib64_link = os.path.join(top_level, 'lib64')
            assert os.path.basename(lib_parent) == 'lib', 'Unexpected parent dir: {!r}'.format(lib_parent)
            if os.path.lexists(lib64_link):
                return
        if symlink:
            os.symlink('lib', lib64_link)
        else:
            copyfile(lib_dir, lib64_link, symlink=False)


def resolve_interpreter(exe):
    """
    If the executable given isn't an absolute path, search $PATH for the interpreter
    """
    orig_exe = exe
    python_versions = get_installed_pythons()
    if exe in python_versions:
        exe = python_versions[exe]
    if os.path.abspath(exe) != exe:
        exe = distutils.spawn.find_executable(exe) or exe
    if not os.path.exists(exe):
        logger.fatal('The path {} (from --python={}) does not exist'.format(exe, orig_exe))
        raise SystemExit(3)
    if not is_executable(exe):
        logger.fatal('The path {} (from --python={}) is not an executable file'.format(exe, orig_exe))
        raise SystemExit(3)
    return exe


def is_executable(exe):
    """Checks a file is executable"""
    return os.path.isfile(exe) and os.access(exe, os.X_OK)


def make_environment_relocatable(home_dir):
    """
    Makes the already-existing environment use relative paths, and takes out
    the #!-based environment selection in scripts.
    """
    home_dir, lib_dir, inc_dir, bin_dir = path_locations(home_dir)
    activate_this = os.path.join(bin_dir, 'activate_this.py')
    if not os.path.exists(activate_this):
        logger.fatal("The environment doesn't have a file %s -- please re-run virtualenv on this environment to update it", activate_this)
    fixup_scripts(home_dir, bin_dir)
    fixup_pth_and_egg_link(home_dir)


OK_ABS_SCRIPTS = [
 'python',
 PY_VERSION,
 'activate',
 'activate.bat',
 'activate_this.py',
 'activate.fish',
 'activate.csh',
 'activate.xsh']

def fixup_scripts(_, bin_dir):
    if IS_WIN:
        new_shebang_args = (
         '{} /c'.format(os.path.normcase(os.environ.get('COMSPEC', 'cmd.exe'))), '', '.exe')
    else:
        new_shebang_args = (
         '/usr/bin/env', VERSION, '')
    shebang = '#!{}'.format(os.path.normcase(os.path.join(os.path.abspath(bin_dir), 'python{}'.format(new_shebang_args[2]))))
    new_shebang = ('#!{} python{}{}'.format)(*new_shebang_args)
    for filename in os.listdir(bin_dir):
        filename = os.path.join(bin_dir, filename)
        if not os.path.isfile(filename):
            pass
        else:
            with open(filename, 'rb') as (f):
                try:
                    lines = f.read().decode('utf-8').splitlines()
                except UnicodeDecodeError:
                    continue

        if not lines:
            logger.warn('Script %s is an empty file', filename)
        else:
            old_shebang = lines[0].strip()
            old_shebang = old_shebang[0:2] + os.path.normcase(old_shebang[2:])
            if old_shebang.startswith(shebang) or os.path.basename(filename) in OK_ABS_SCRIPTS:
                logger.debug('Cannot make script %s relative', filename)
            elif lines[0].strip() == new_shebang:
                logger.info('Script %s has already been made relative', filename)
            else:
                logger.warn("Script %s cannot be made relative (it's not a normal script that starts with %s)", filename, shebang)
                continue
                logger.notify('Making script %s relative', filename)
                script = relative_script([new_shebang] + lines[1:])
                with open(filename, 'wb') as (f):
                    f.write('\n'.join(script).encode('utf-8'))


def relative_script(lines):
    """Return a script that'll work in a relocatable environment."""
    activate = "import os; activate_this=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'activate_this.py'); exec(compile(open(activate_this).read(), activate_this, 'exec'), { '__file__': activate_this}); del os, activate_this"
    activate_at = None
    for idx, line in reversed(list(enumerate(lines))):
        if line.split()[:3] == ['from', '__future__', 'import']:
            activate_at = idx + 1
            break

    if activate_at is None:
        activate_at = 1
    return lines[:activate_at] + ['', activate, ''] + lines[activate_at:]


def fixup_pth_and_egg_link(home_dir, sys_path=None):
    """Makes .pth and .egg-link files use relative paths"""
    home_dir = os.path.normcase(os.path.abspath(home_dir))
    if sys_path is None:
        sys_path = sys.path
    for a_path in sys_path:
        if not a_path:
            a_path = '.'
        if not os.path.isdir(a_path):
            continue
        a_path = os.path.normcase(os.path.abspath(a_path))
        if not a_path.startswith(home_dir):
            logger.debug('Skipping system (non-environment) directory %s', a_path)
        else:
            for filename in os.listdir(a_path):
                filename = os.path.join(a_path, filename)
                if filename.endswith('.pth'):
                    if not os.access(filename, os.W_OK):
                        logger.warn('Cannot write .pth file %s, skipping', filename)
                    else:
                        fixup_pth_file(filename)
                    if filename.endswith('.egg-link'):
                        if not os.access(filename, os.W_OK):
                            logger.warn('Cannot write .egg-link file %s, skipping', filename)
                        else:
                            fixup_egg_link(filename)


def fixup_pth_file(filename):
    lines = []
    with open(filename) as (f):
        prev_lines = f.readlines()
    for line in prev_lines:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('import ') or os.path.abspath(line) != line:
            lines.append(line)
        else:
            new_value = make_relative_path(filename, line)
            if line != new_value:
                logger.debug('Rewriting path {} as {} (in {})'.format(line, new_value, filename))
            lines.append(new_value)

    if lines == prev_lines:
        logger.info('No changes to .pth file %s', filename)
        return
    logger.notify('Making paths in .pth file %s relative', filename)
    with open(filename, 'w') as (f):
        f.write('\n'.join(lines) + '\n')


def fixup_egg_link(filename):
    with open(filename) as (f):
        link = f.readline().strip()
    if os.path.abspath(link) != link:
        logger.debug('Link in %s already relative', filename)
        return
    new_link = make_relative_path(filename, link)
    logger.notify('Rewriting link {} in {} as {}'.format(link, filename, new_link))
    with open(filename, 'w') as (f):
        f.write(new_link)


def make_relative_path(source, dest, dest_is_directory=True):
    """
    Make a filename relative, where the filename is dest, and it is
    being referred to from the filename source.

        >>> make_relative_path('/usr/share/something/a-file.pth',
        ...                    '/usr/share/another-place/src/Directory')
        '../another-place/src/Directory'
        >>> make_relative_path('/usr/share/something/a-file.pth',
        ...                    '/home/user/src/Directory')
        '../../../home/user/src/Directory'
        >>> make_relative_path('/usr/share/a-file.pth', '/usr/share/')
        './'
    """
    source = os.path.dirname(source)
    if not dest_is_directory:
        dest_filename = os.path.basename(dest)
        dest = os.path.dirname(dest)
    else:
        dest_filename = None
    dest = os.path.normpath(os.path.abspath(dest))
    source = os.path.normpath(os.path.abspath(source))
    dest_parts = dest.strip(os.path.sep).split(os.path.sep)
    source_parts = source.strip(os.path.sep).split(os.path.sep)
    while dest_parts and source_parts and dest_parts[0] == source_parts[0]:
        dest_parts.pop(0)
        source_parts.pop(0)

    full_parts = [
     '..'] * len(source_parts) + dest_parts
    if not dest_is_directory:
        if dest_filename is not None:
            full_parts.append(dest_filename)
        return full_parts or './'
    else:
        return os.path.sep.join(full_parts)


FILE_PATH = __file__ if os.path.isabs(__file__) else os.path.join(os.getcwd(), __file__)

def create_bootstrap_script(extra_text, python_version=''):
    """
    Creates a bootstrap script, which is like this script but with
    extend_parser, adjust_options, and after_install hooks.

    This returns a string that (written to disk of course) can be used
    as a bootstrap script with your own customizations.  The script
    will be the standard virtualenv.py script, with your extra text
    added (your extra text should be Python code).

    If you include these functions, they will be called:

    ``extend_parser(optparse_parser)``:
        You can add or remove options from the parser here.

    ``adjust_options(options, args)``:
        You can change options here, or change the args (if you accept
        different kinds of arguments, be sure you modify ``args`` so it is
        only ``[DEST_DIR]``).

    ``after_install(options, home_dir)``:

        After everything is installed, this function is called.  This
        is probably the function you are most likely to use.  An
        example would be::

            def after_install(options, home_dir):
                subprocess.call([join(home_dir, 'bin', 'easy_install'),
                                 'MyPackage'])
                subprocess.call([join(home_dir, 'bin', 'my-package-script'),
                                 'setup', home_dir])

        This example immediately installs a package, and runs a setup
        script from that package.

    If you provide something like ``python_version='2.5'`` then the
    script will start with ``#!/usr/bin/env python2.5`` instead of
    ``#!/usr/bin/env python``.  You can use this when the script must
    be run with a particular Python version.
    """
    filename = FILE_PATH
    if filename.endswith('.pyc'):
        filename = filename[:-1]
    with codecs.open(filename, 'r', encoding='utf-8') as (f):
        content = f.read()
    py_exe = 'python{}'.format(python_version)
    content = '#!/usr/bin/env {}\n# WARNING: This file is generated\n{}'.format(py_exe, content)
    return content.replace('# EXTEND - bootstrap here', extra_text)


def convert(s):
    b = base64.b64decode(s.encode('ascii'))
    return zlib.decompress(b).decode('utf-8')


SITE_PY = convert('\n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\nIWNQ+EMONwZIp5gxI994rJ0KayiC/wegEfUH\n')
ACTIVATE_SH = convert('\neJytVW1P2zAQ/u5fcaQVG9s6VvjGVLQyKoEELWo6JjZQMMmVWEudynYK5eW/75w3kgbYh9EPbe27\ns5977p5zCyah0DAVEcIs0QauEBKNAdwIE4Kj40T5CFdCbnLfiAU36MCHqYpncMV1+IG1YBkn4HMp\nYwMqkSAMBEKhb6IlY0xM4Tc47fu9vnvguaMf4++DzqMDPdr74sDFVzAhSgb0QT+MwTmjw1IY+cXG\ngtO+EnOzA+ftYtsG765vZYG3dOX2NpsKxgIsUML7DbhP7YnUaKAzhfkyiH3Y3QxwsSmTKIKt3fUu\nS31aoNB6xVEAKBdCxXKG0sCCK8GvItS51xpl07mD9v1pf/zRe4QLijOJkhqMShAoWzIAQQ7Qj7gi\nGrkBHkVpOFnzeCLEGx3te6eH48mP/pF30p8c7NB5xAhUKLEfa+o57Ya7U3rg7TxWJnUs97KcG0Gp\nnXj6B5qzycFoeDA6HrwAqbQ3gJWWJrzS9CrIupctaUZ82qQ6jBMqUICG2ivtP+AygDsdfoKbUPgh\nhHyBwOmHTH48m1mzCakGtqfyo6jBfSoJ1cbEcE0IqH3o3zRWdjHn1Hx5qP4M8JNkECcmNxshr/Nj\nao6WIGhbisEPubxGDTekJx7YryVYbdC11GNzQo5BUQCiXxbq6KRUPzyUm79IMaeDsXs4GnaeK0Oa\nZEdRF5cdXSPtlQK73Rcq63YbJXW7zVq63VeLmJsLIJlLYR0MT5/SX7PYuvlEkLEMUJOQrIRxBV4L\nXIymUDisrQDoWFOh/eL2R0bjKbMLpTDCBa9pujIt6nczVkHbczyvsvQ8h+U8VFNiDbERk5lQ80XF\ne9Pz9g6H3rB/PPC8ndytquMS95MgLGG0w2plfU2qLwjLwlqR6epV6SjN2jO9pZr9/qHb3zsaeCfj\n0fHJpNGYq43QsyBdW+Gnoju3T4RmxxCnsNaD2xc6suleOxQjjfWA95c0HFDyGcJ5jfhz53IDasH5\nNKx0tk2+Bcf8D4JOFNrZkEgeCa7zF4SSEOadprmukAdLC1ghq3pUJFl9b9bXV04itdt3g7FsWT5Z\n8yUNHQmdWe7ntL85WTe/yRx8gxn4n/Pvf2bfc3OPavYXWw6XFQ==\n')
ACTIVATE_FISH = convert('\neJytVm1v2zYQ/q5fcZUdyClqGVuHfQgwDGnjIQYSO3DcAMM6yLREWxxo0iMpty7243ekLImy5RQY\nlg+xTd7rc3cPrweLnGlYM05hW2gDKwqFphn+Y2IDSy0LlVJYMTEiqWF7Ymi8ZjpfwtsvzORMAAFV\nCGGF7TkMIDdmdzMa2V86p5zHqdzCNWiqNZPibRz04E6CkMYqAjOQMUVTww9xEKwLgV6kgGRFdM7W\nh2RHTA7DDMKPUuypMhodOkfuwkjQckttIBuwKpASAWhObgT7RsMA8E9T41SOxvpEbfb1hVWqLhqh\nP37400mspXKO8FAZwGx9mR/jeHiU67AW9psfN/3aSBkSFVn5meYSPMHAXngoWG+XUHDpnqPgwOlA\noXRlc4d/wCiIbiKIPovoxGVGqzpbf9H4KxZoz5QpCKdiD1uZUSAiQ+umUMK6NjnFaqot4ZgWikqx\npcLEkfPaQ0ELjOSZfwt7ohhZcaqdFFuDodh8Q4GwJbOHu+RlMl98un1Inm4X92ENcc81l8bu2mDz\nFSvbWq7Rhq7T/K9M64Lq0U/vfwbCDVXY0tYW5Bg8R5xqm5XvQQnQb5Pn++RlPH+ezKYlUGEcQvhZ\nhNfYFDDkBt7XulXZh5uvpfVBu2LnuVzXupRretnQuWajeOydWodCt7Ar7Hfg/X1xP5vezx7HYXAW\nR313Gk198XocbbFXonGYP81nj0+LZIbYzyd3TTy22aru1DD8GxLsJQdzslNyuzNedzxjGNj5FE8P\nwGWKLbl0E5tUFlxdlrZtCefyi2teRbdyj6JyDUvP7rLiQM87XcbtnDmcmw+8iMaKaOoNUKRPfJSz\npI1U1AUjFdswQXjjx3cPXXl7AukZOt/ToJfx9IvaVaJ2WY/SVfXH05d2uUPHPThDIbz5BSIhRYbH\nqrBsQ6NWEfl6WN296Y55d8hk2n3VENiFdP2X5YKIP8R1li7THnwSNlOmFOV0T3wqiwOPPNv5BUE1\nVR4+ECaJ9zNJQmv//2O4/8hsVaRnpILs1nqV+yWh1UR2WdFJOgBbJBf2vfRHSfJhMk2mt49jROKo\nUuO97Dd0srQ9hYdxUH5aUjghm+5QPELrkqe+lfar2PTb7mByPBhuy7PjNuGka2L71s4suZs83354\nGB/nJzw+jB/l7uBGPi2wmbCR2sRQ+yZIGaczeqSh1uT7Q3820y3xTk7AwSN72gqorw0xhX7n1iBP\nR6MUsXub3nFywBXujBSt+1K5MuKT4lMZpMRNRjHcJ9DqHj+zXz2ZydquiO/gL7uU7hTdIcQuOH+L\nEGRLG9/+w9JM1pG0kuaBc2VUTJg1RFf6Sked4jDAXJJUcsy9XG9eebsbc4MrfQ1RhzIMcHiojbjd\nHaFntuLSEoJ5x7NQw1nr2NkOqV3T+g3qIQ54ubrXgp0032bvamC6yP4kaNfx/wIsXsYv\n')
ACTIVATE_CSH = convert('\neJx9VNtO4zAQffdXDKEiUEFhX8t22bJFWqRyEVuQVkKy3Hi6sZQ44Dit+sK379hJittG5KGqPZdz\nfOZyCLNUlbBQGUJelRbmCFWJElbKphCVRWUShLnS5yKxaiksDpIyjaC/MEUO9Lc/YIfwt6ggEVoX\nFkylQVmQymBis7Wz/jJIcRLma5iIpZIIEwXXmSgVfJf+Qs5//suFygZJkf8YMFaiBY2rTGkcxa8s\nZkxkSpQgsWUBsUVi27viD9MJf7l9mj2Pp/xxPPsNByO4gKMjoCSol+Dvot6e3/A9cl6VdmB71ksw\nmIoyvYROnKeHu8dZiARvpMebHe0CeccvoLz9sjY5tq3h5v6lgY5eD4b9yGFFutCSrkzlRMAm554y\nwe3bWhYJqXcIzx5bGYMZLoW2sBRGiXmG5YAFsdsIvhA7rCDiPDhyHtXl2lOQpGhkZtuVCKKH7+ec\nX9/e8/vx3Q3nw00EfWoBxwFWrRTBeSWiE7Apagb0OXRKz7XIEUbQFcMwK7HLOT6OtwlZQo9PIGao\npVrULKj64Ysnt3/G19ObtgkCJrXzF74jRz2MaCnJgtcN5B7wLfK2DedOp4vGydPcet5urq2XBEZv\nDcnQpBZVJt0KUBqEa4YzpS0a3x7odFOm0Dlqe9oEkN8qVUlK01/iKfSa3LRRKmqkBc2vBKFpmyCs\nXG4d2yYyEQZBzIvKOgLN+JDveiVoaXyqedVYOkTrmCRqutrfNVHr6xMFBhh9QD/qNQuGLvq72d03\n3Jy2CtGCf0rca/tp+N4BXqsflKquRr0L2sjmuClOu+/8/NKvTQsNZ3l9ZqxeTew//1a6EA==\n')
ACTIVATE_XSH = convert('\neJyNU11PwjAUfe+vuNY9sIj7ASQ+YCSBRD6i02gIaSq7gyWjXdqyaIz/3XYwVmB+9GFZ78c57T2n\nlNIXKfQa+NJkJTcIeqmywkAqFZSZMlueoygppSRVcgPvrjgyUuYask0hlYEVGqaxAK6B7f8JSTAF\nlmCN2uFqpcMeAbuyFGjxkcglhUwAzzOuUe9SbiWY18H5vm5B6sbgM4qir8jSdCib3t+x59FD/NS/\nZ7N+PKRdoDRskAIXhBsIziqPyFrSf9O9xsPpZDgdD85JD6lz6kPqtwM0RYdx1bnB5Lka2u5cxzML\nvKLWTjZ7mI5n8b8A9rUNjpAiQW3U1gmKFIQ0lXpW1gblEh4xT6EuvGjXtHGFE5ZcwlZotGhKYY4l\nFwZKrjL+lqMmvoXmp4dYhKQV1M7d6yPEv5jNKcqYf1VGbcmZB5x4lRcCfzfvLXaBiCdJ5wj46uD+\nTmg3luR2NGGT/nhgGbpgX48wN7HaYhcUFjlfYrULCTkxWru36jF59rJ9NlJlf7JQde5j11VS+yZr\n0d22eUPaxdycLKMTvqWjR3610emDtgTu36ylcJe83rhv/di/AYN1UZY=\n')
ACTIVATE_BAT = convert('\neJyVk1FLhEAUhd8X/A8XWSkf28dCyMUpBR3FzAiCS+WYwq4TOdXfb0Z3dTJdyCfveO85n8frNXut\nOPCyNFbGqmUCzDxIs3s3REJzB1GrEE3VVJdQsLJuWAEYh97QkaRxlGRwbqxAXp1Uf+RYM32W1LKB\n7Vp2nJC6DReD9m+5qeQ6Wd+a/SN7dlzn9oI7dxsSXJCcoXOskfLgYXdv/j8LnXiM8iGg/RmiZmOr\nbFMSgcebMwGfKhgbBIfnL14X8P7BX3Zs38J3LSoQFdtD3YCVuJlvnfgmj5kfUz+OCLxxqUWoF9zk\nqtYAFyZkBsO9ArzUh/td0ZqP9IskElTFMsnwb4/GqeoLPUlZT5dJvf8Id5hQIONynUSa2G0Wc+m8\nZ+w2w4/Tt2hbYT0hbgOK1I0I4tUw/QOTZfLE\n')
DEACTIVATE_BAT = convert('\neJyFkN0KgkAUhO8X9h0GQapXCIQEDQX/EBO6kso1F9KN3Or1201Si6JzN+fMGT5mxQ61gKgqSijp\nmETup9nGDgo3yi29S90QjmhnEteOYb6AFNjdBC9xvoj9iTUd7lzWkDVrwFuYiZ15JiW8QiskSlbx\nlpUo4sApXtlJGodJhqNQWW7k+Ou831ACNZrC6BeW+eXPNEbfl7OiXr6H/oHZZl4ceXHoToG0nuIM\npk+k4fAba/wd0Pr4P2CqyLeOlJ4iKfkJo6v/iaH9YzfPMEoeMG2RUA==\n')
ACTIVATE_PS = convert('\neJytVW1v2jAQ/p5fcUujFdQm1dRvTJ1GV6YitRQR1mnaJsskB1hK7Mhx0qKJ/75LCCSEUlXT/Aly\nb89z95x9AtOlSGEuIoQ4Sw3MEEJlIFWZDjCEuVYxjJW//AgrlUHApSSrziQIA6HQGJho5cGNAkN5\neuCBd8EDI3Ju0EvSD5Yl5tD53HFkFkXn9lAa1JJHdhdcShQoabiQKTjxSshcBdwIJb1AxTGXodJi\nIWQX/lhA57sWBt1bRRjdr0rjQqtMhqAJpP2DoJXoTze4T0s0kAZaJKYHY/8TAXM6+1Xqn5LH2LXL\nKvhMvC4vrbVlOVX49Hbos3F/egtXLZzxqkLqJdwsdwHXfX/AboYT8veTSBh3TFboTDBVUY6bf7az\nS3vheUU7xlyjNJY1z2RQZIdFpGY86oW47WfnZ/okTLD8Dc5IyRtMjc4KE25bVLR6Sp83JXKuBZ9F\n2GMPdzfscTiZfuvflRW3/sVxUOa9LbvjITv/CcaKSDxWnmAfuNrg+oFKsCJQRlI7DwFumfaYikKW\nC20yHrGEFJeYPYg7x42tQPpabBvr0GBcF/t1LKKBsWzKltNg9NhE00zacgN3oLXS/c38fNopSdvx\nhUQuZIbtIu+OTLE4J+BjNIewsr57nVItkdf9klWoggrG+lBppbkCkazMkixuDJuvDteLtAg6gUym\naEBojRHmXJqd0FKrBlKstwxrcrROzUbRBLdbYrWbXRgbfy1rhE+13va0Be6IVhcOJAjkH2VYi9uy\nmjq32yUvGLsejtiofz9gdAo35g/GjNlw1kiymVorljj4/eu7ARtPHu7H0+0U2819QXWNedt2NZZ9\nvb8UdHWwD7WkbFa3oURTMHAlbandVNfB4NtwNhLshyHdowgB3az0CiQa5+IZjCo/0kWZkqwX0Nq5\nkgC55kJlaYWZ5eU0ruD9Gxe3OC+TOTuSvLuLXTc6iVGK/8abt+gGmS6u54rtOcwyev6UPC0ewTTg\nOqT30Pv/TXAkPrXj7Y7TaT4sB/vj3iGfQ7cL9n5DD5O9vZtr6y9V3o9t\n')
DISTUTILS_INIT = convert('\neJytV21v5DQQ/p5fMaRCJLANcAcSqlghuBdUcRzo6BdUnSI3cXZNs3bO9m679+uZsbOJnWR7fKBS\nu65nPC/PvK7YdUpbUCYR/mSOw/GBaSnkxiTJBaiuUjUHYUAqCwwOQts9a7k8wE7V+5avwCh44FAx\nCXuDnBasgkbIGuyWg7F1K+5Q0LWTzaT9DG7wgdL3oCR0x+64QkaUv9sbC3ccdXjBeMssaG5EzQ0I\nSeJQDkq77I52q+TXyCcawevLx+JYfIRaaF5ZpY8nP7ztSYIEyXYc1uhu0TG7LfobIhm7t6I1Jd0H\nHP8oIbMJe+YFFmXZiJaXZb6CdBCQ5olohudS6R0dslhBDuuZEdnszSA/v0oAf07xKOiQpTcIaxCG\nQQN0rLpnG0TQwucGWNdxpg1FA1H1+IEhHFpVMSsQfWb85dFYvhsF/YS+8NZwr710lpdlIaTh2mbf\nrGDqFFxgdnxgV/D6h2ffukcIBUotDlwbVFQK2Sj4EbLnK/iud8px+TjhRzLcac7acvRpTdSiVawu\nfVpkaTk6PzKmK3irJJ/atoIsRRL9kpw/f/u1fHn97tWLmz/e/Z3nTunoaWwSfmCuFTtWbYXkmFUD\nz9NJMzUgLdF9YRHA7pjmgxByiWvv31RV8Zfa64q/xix449jOOz0JxejH2QB8HwQg8NgeO26SiDIL\nheMpfndxuMFz5p0oKI1H1TGgi6CSwFiX6XgVgUEsBd2WjVa70msKFa56CPOnbZ5I9EnkZZL0jP5M\no1LwR9Tb51ssMfdmX8AL1R1d9Wje8gP2NSw7q8Xd3iKMxGL1cUShLDU/CBeKEo2KZRYh1efkY8U7\nCz+fJL7SWulRWseM6WvzFOBFqQMxScjhoFX0EaGLFSVKpWQjNuSXMEi4MvcCa3Jw4Y4ZbtAWuUl6\n095iBAKrRga0Aw80OjAhqy3c7UVbl/zRwlgZUCtu5BcW7qV6gC3+YpPacOvwxFCZoJc7OVuaFQ84\nU9SDgUuaMVuma2rGvoMRC3Y8rfb92HG6ee1qoNO8EY8YuL4mupbZBnst9eIUhT5/lnonYoyKSu12\nTNbF6EGP2niBDVThcbjwyVG1GJ+RK4tYguqreUODkrXiIy9VRy3ZZIa3zbRC0W68LRAZzfQRQ4xt\nHScmNbyY01XSjHUNt+8jNt6iSMw3aXAgVzybPVkFAc3/m4rZHRZvK+xpuhne5ZOKnz0YB0zUUClm\nLrV9ILGjvsEUSfO48COQi2VYkyfCvBjc4Z++GXgB09sgQ9YQ5MJFoIVOfVaaqyQha2lHKn3huYFP\nKBJb8VIYX/doeTHjSnBr8YkT34eZ07hCWMOimh6LPrMQar8cYTF0yojHdIw37nPavenXpxRHWABc\ns0kXJujs0eKbKdcs4qdgR4yh1Y5dGCJlMdNoC5Y5NgvcbXD9adGIzAEzLy/iKbiszYPA/Wtm8UIJ\nOEGYljt14Bk9z5OYROuXrLMF8zW3ey09W+JX0E+EHPFZSIMwvcYWHucYNtXSb8u4AtCAHRiLmNRn\n1UCevMyoabqBiRt3tcYS9fFZUw/q4UEc/eW8N/X3Tn1YyyEec3NjpSeVWMXJOTNx5tWqcsNwLu5E\nTM5hEMJTTuGZyMPGdQ5N+r7zBJpInqNJjbjGkUbUs+iGTEAt63+Ee2ZVbNMnwacF6yz4AXEZ/Ama\n5RTNk7yefGB+5ESiAtoi/AE9+5LpjemBdfj0Ehf09Lzht5qzCwT9oL00zZZaWjzEWjfEwoU9mMiD\nUbThVzZ34U7fXP+C315S91UcO9rAFLen4fr29OA9WnOyC1c8Zu5xNaLeyNo2WNvPmkCtc2ICqidc\nzmg+LaPu/BXc9srfx9pJbJiSw5NZkgXxWMiyBWpyNjdmeRbmzb+31cHS\n')
DISTUTILS_CFG = convert('\neJxNj00KwkAMhfc9xYNuxe4Ft57AjYiUtDO1wXSmNJnK3N5pdSEEAu8nH6lxHVlRhtDHMPATA4uH\nxJ4EFmGbvfJiicSHFRzUSISMY6hq3GLCRLnIvSTnEefN0FIjw5tF0Hkk9Q5dRunBsVoyFi24aaLg\n9FDOlL0FPGluf4QjcInLlxd6f6rqkgPu/5nHLg0cXCscXoozRrP51DRT3j9QNl99AP53T2Q=\n')
ACTIVATE_THIS = convert('\neJylVE1v2zAMvetXENqh9pZ5wHYL0EMOBdqh64It7RAEhaE4TKzOlgxJ+ULR/15Sdhr341BsOcSW\n9fj4SD5JSjkqgt6ogLDRLqxVhWYDS+ugWDuHJoA2AV3jkP6HQlx7BNxhkdgGTRJK7fOlrjDNHKpF\nkg7g/iSPX/L8ZAhP+w9pJsSEVlAoA3OEtccFbEs0sLdrqNc+8CegTdxpH7RZwXgfSmv6+QdgbCDS\nZ1rn2nxpIjQTUkqh68a6ANYf3rwO+PS+90IEtx8KoN9BqcBdgU2AK1XjmXPWtdtOaZI08h5d0NbE\nnURO+3r/qRWpTIX4AFQTBS64AAgWxqPJOUQaYBjQUxuvFxgLZtBCOyyCdftU0DKnJZxSnVmjQpnR\nypD85LBWc8/P5CAhTQVtUcO0s2YmOZu8PcZ7bLI7q00y66hv4RMcA7IVhqQNGoCUaeabSofkGEz0\nYq6oI68VdYSx5m5uwIOjAp1elQHU3G5eVPhM683Fr8n16DI/u7qJkjkPk6nFom8G6AJqcq2PU//c\nqOKvWiG3l4GlpbE1na1aQ9RYlMpoX4uL3/l4Op4Sf6m8CsElZBYqttk3+3yDzpMFcm2WlqZH2O/T\nyfnPK0ITKmsqFejM1JkPygW/1dR4eac2irB6CU/w1lcsLe+k+V7DYv+5OMp6qefc6X4VnsiwaulY\n6fvJXrN4bKOJ6s/Fyyrg9BTkVptvX2UEtSkJ18b8ZwkcfhTwXrKqJWuHd/+Q3T/IjLWqkHxk7f0B\npW9kFXTaNlwn+TjWSglSwaiMbMRP8l7yTAltE5AOc5VT8FLvDm2KC3F87VnyBzuZrUakdMERXe0P\n7luSN+leWsYF5x/QAQdqeoHC4JZYKrr5+uq6t9mQXT/T8VrWHMRwmoqO9yGTUHF8YN/EHPbFI/bz\n/no=\n')
PYTHON_CONFIG = convert('\neJyNVV1P2zAUfc+v8ODBiSABxlulTipbO6p1LWqBgVhlhcZpPYUkctzSivHfd6+dpGloGH2Ja/ue\ne+65Hz78xNhtf3x90xmw7vCWsRPGLvpDNuz87MKfdKMWSWxZ4ilNpCLZJiuWc66SVFUOZkkcirll\nrfxIBAzOMtImDzSVPBRrekwoX/OZu/0r4lm0DHiG60g86u8sjPw5rCyy86NRkB8QuuBRSqfAKESn\n3orLTCQxE3GYkC9tYp8fk89OSwNsmXgizrhUtnumeSgeo5GbLUMk49Rv+2nK48Cm/qMwfp333J2/\ndVcAGE0CIQHBsgIeEr4Wij0LtWDLzJ9ze5YEvH2WI6CHTAVcSu9ZCsXtgxu81CIvp6/k4eXsdfo7\nPvDCRD75yi41QitfzlcPp1OI7i/1/iQitqnr0iMgQ+A6wa+IKwwdxyk9IiXNAzgquTFU8NIxAVjM\nosm1Zz526e+shQ4hKRVci69nPC3Kw4NQEmkQ65E7OodxorSvxjvpBjQHDmWFIQ1mlmzlS5vedseT\n/mgIEsMJ7Lxz2bLAF9M5xeLEhdbHxpWOw0GdkJApMVBRF1y+a0z3c9WZPAXGFcFrJgCIB+024uad\n0CrzmEoRa3Ub4swNIHPGf7QDV+2uj2OiFWsChgCwjKqN6rp5izpbH6Wc1O1TclQTP/XVwi6anTr1\n1sbubjZLI1+VptPSdCfwnFBrB1jvebrTA9uUhU2/9gad7xPqeFkaQcnnLbCViZK8d7R1kxzFrIJV\n8EaLYmKYpvGVkig+3C5HCXbM1jGCGekiM2pRCVPyRyXYdPf6kcbWEQ36F5V4Gq9N7icNNw+JHwRE\nLTgxRXACpvnQv/PuT0xCCAywY/K4hE6Now2qDwaSE5FB+1agsoUveYDepS83qFcF1NufvULD3fTl\ng6Hgf7WBt6lzMeiyyWVn3P1WVbwaczHmTzE9A5SyItTVgFYyvs/L/fXlaNgbw8v3azT+0eikVlWD\n/vBHbzQumP23uBCjsYdrL9OWARwxs/nuLOzeXbPJTa/Xv6sUmQir5pC1YRLz3eA+CD8Z0XpcW8v9\nMZWF36ryyXXf3yBIz6nzqz8Muyz0m5Qj7OexfYo/Ph3LqvkHUg7AuA==\n')
MH_MAGIC = 4277009102
MH_CIGAM = 3472551422
MH_MAGIC_64 = 4277009103
MH_CIGAM_64 = 3489328638
FAT_MAGIC = 3405691582
BIG_ENDIAN = '>'
LITTLE_ENDIAN = '<'
LC_LOAD_DYLIB = 12
maxint = MAJOR == 3 and getattr(sys, 'maxsize') or getattr(sys, 'maxint')

class FileView(object):
    __doc__ = '\n    A proxy for file-like objects that exposes a given view of a file.\n    Modified from macholib.\n    '

    def __init__(self, file_obj, start=0, size=maxint):
        if isinstance(file_obj, FileView):
            self._file_obj = file_obj._file_obj
        else:
            self._file_obj = file_obj
        self._start = start
        self._end = start + size
        self._pos = 0

    def __repr__(self):
        return '<fileview [{:d}, {:d}] {!r}>'.format(self._start, self._end, self._file_obj)

    def tell(self):
        return self._pos

    def _checkwindow(self, seek_to, op):
        if not self._start <= seek_to <= self._end:
            raise IOError('{} to offset {:d} is outside window [{:d}, {:d}]'.format(op, seek_to, self._start, self._end))

    def seek(self, offset, whence=0):
        seek_to = offset
        if whence == os.SEEK_SET:
            seek_to += self._start
        else:
            if whence == os.SEEK_CUR:
                seek_to += self._start + self._pos
            else:
                if whence == os.SEEK_END:
                    seek_to += self._end
                else:
                    raise IOError('Invalid whence argument to seek: {!r}'.format(whence))
        self._checkwindow(seek_to, 'seek')
        self._file_obj.seek(seek_to)
        self._pos = seek_to - self._start

    def write(self, content):
        here = self._start + self._pos
        self._checkwindow(here, 'write')
        self._checkwindow(here + len(content), 'write')
        self._file_obj.seek(here, os.SEEK_SET)
        self._file_obj.write(content)
        self._pos += len(content)

    def read(self, size=maxint):
        assert size >= 0
        here = self._start + self._pos
        self._checkwindow(here, 'read')
        size = min(size, self._end - here)
        self._file_obj.seek(here, os.SEEK_SET)
        read_bytes = self._file_obj.read(size)
        self._pos += len(read_bytes)
        return read_bytes


def read_data(file, endian, num=1):
    """
    Read a given number of 32-bits unsigned integers from the given file
    with the given endianness.
    """
    res = struct.unpack(endian + 'L' * num, file.read(num * 4))
    if len(res) == 1:
        return res[0]
    else:
        return res


def mach_o_change(at_path, what, value):
    """
    Replace a given name (what) in any LC_LOAD_DYLIB command found in
    the given binary with a new name (value), provided it's shorter.
    """

    def do_macho(file, bits, endian):
        cpu_type, cpu_sub_type, file_type, n_commands, size_of_commands, flags = read_data(file, endian, 6)
        if bits == 64:
            read_data(file, endian)
        for _ in range(n_commands):
            where = file.tell()
            cmd, cmd_size = read_data(file, endian, 2)
            if cmd == LC_LOAD_DYLIB:
                name_offset = read_data(file, endian)
                file.seek(where + name_offset, os.SEEK_SET)
                load = file.read(cmd_size - name_offset).decode()
                load = load[:load.index('\x00')]
                if load == what:
                    file.seek(where + name_offset, os.SEEK_SET)
                    file.write(value.encode() + '\x00'.encode())
            file.seek(where + cmd_size, os.SEEK_SET)

    def do_file(file, offset=0, size=maxint):
        file = FileView(file, offset, size)
        magic = read_data(file, BIG_ENDIAN)
        if magic == FAT_MAGIC:
            n_fat_arch = read_data(file, BIG_ENDIAN)
            for _ in range(n_fat_arch):
                cpu_type, cpu_sub_type, offset, size, align = read_data(file, BIG_ENDIAN, 5)
                do_file(file, offset, size)

        else:
            if magic == MH_MAGIC:
                do_macho(file, 32, BIG_ENDIAN)
            else:
                if magic == MH_CIGAM:
                    do_macho(file, 32, LITTLE_ENDIAN)
                else:
                    if magic == MH_MAGIC_64:
                        do_macho(file, 64, BIG_ENDIAN)
                    elif magic == MH_CIGAM_64:
                        do_macho(file, 64, LITTLE_ENDIAN)

    assert len(what) >= len(value)
    with open(at_path, 'r+b') as (f):
        do_file(f)


if __name__ == '__main__':
    main()