# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/xwot1/REST-Server-Skeleton/virtualenv.py
# Compiled at: 2014-10-01 04:03:08
"""Create a "virtual" Python installation
"""
__version__ = '1.9.1'
virtualenv_version = __version__
import base64, sys, os, codecs, optparse, re, shutil, logging, tempfile, zlib, errno, glob, distutils.sysconfig
from distutils.util import strtobool
import struct, subprocess
if sys.version_info < (2, 5):
    print 'ERROR: %s' % sys.exc_info()[1]
    print 'ERROR: this script requires Python 2.5 or greater.'
    sys.exit(101)
try:
    set
except NameError:
    from sets import Set as set

try:
    basestring
except NameError:
    basestring = str

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

join = os.path.join
py_version = 'python%s.%s' % (sys.version_info[0], sys.version_info[1])
is_jython = sys.platform.startswith('java')
is_pypy = hasattr(sys, 'pypy_version_info')
is_win = sys.platform == 'win32'
is_cygwin = sys.platform == 'cygwin'
is_darwin = sys.platform == 'darwin'
abiflags = getattr(sys, 'abiflags', '')
user_dir = os.path.expanduser('~')
if is_win:
    default_storage_dir = os.path.join(user_dir, 'virtualenv')
else:
    default_storage_dir = os.path.join(user_dir, '.virtualenv')
default_config_file = os.path.join(default_storage_dir, 'virtualenv.ini')
if is_pypy:
    expected_exe = 'pypy'
elif is_jython:
    expected_exe = 'jython'
else:
    expected_exe = 'python'
REQUIRED_MODULES = [
 'os', 'posix', 'posixpath', 'nt', 'ntpath', 'genericpath',
 'fnmatch', 'locale', 'encodings', 'codecs',
 'stat', 'UserDict', 'readline', 'copy_reg', 'types',
 're', 'sre', 'sre_parse', 'sre_constants', 'sre_compile',
 'zlib']
REQUIRED_FILES = [
 'lib-dynload', 'config']
majver, minver = sys.version_info[:2]
if majver == 2:
    if minver >= 6:
        REQUIRED_MODULES.extend(['warnings', 'linecache', '_abcoll', 'abc'])
    if minver >= 7:
        REQUIRED_MODULES.extend(['_weakrefset'])
    if minver <= 3:
        REQUIRED_MODULES.extend(['sets', '__future__'])
elif majver == 3:
    REQUIRED_MODULES.extend(['_abcoll', 'warnings', 'linecache', 'abc', 'io',
     '_weakrefset', 'copyreg', 'tempfile', 'random',
     '__future__', 'collections', 'keyword', 'tarfile',
     'shutil', 'struct', 'copy', 'tokenize', 'token',
     'functools', 'heapq', 'bisect', 'weakref',
     'reprlib'])
    if minver >= 2:
        REQUIRED_FILES[-1] = 'config-%s' % majver
    if minver == 3:
        import sysconfig
        platdir = sysconfig.get_config_var('PLATDIR')
        REQUIRED_FILES.append(platdir)
        REQUIRED_MODULES.extend([
         'base64',
         '_dummy_thread',
         'hashlib',
         'hmac',
         'imp',
         'importlib',
         'rlcompleter'])
if is_pypy:
    REQUIRED_MODULES.extend(['traceback', 'linecache'])

class Logger(object):
    """
    Logging object for use in command-line script.  Allows ranges of
    levels, to avoid some redundancy of displayed information.
    """
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
        return

    def debug(self, msg, *args, **kw):
        self.log(self.DEBUG, msg, *args, **kw)

    def info(self, msg, *args, **kw):
        self.log(self.INFO, msg, *args, **kw)

    def notify(self, msg, *args, **kw):
        self.log(self.NOTIFY, msg, *args, **kw)

    def warn(self, msg, *args, **kw):
        self.log(self.WARN, msg, *args, **kw)

    def error(self, msg, *args, **kw):
        self.log(self.ERROR, msg, *args, **kw)

    def fatal(self, msg, *args, **kw):
        self.log(self.FATAL, msg, *args, **kw)

    def log(self, level, msg, *args, **kw):
        if args:
            if kw:
                raise TypeError('You may give positional or keyword arguments, not both')
        args = args or kw
        rendered = None
        for consumer_level, consumer in self.consumers:
            if self.level_matches(level, consumer_level):
                if self.in_progress_hanging and consumer in (sys.stdout, sys.stderr):
                    self.in_progress_hanging = False
                    sys.stdout.write('\n')
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

        return

    def start_progress(self, msg):
        assert not self.in_progress, 'Tried to start_progress(%r) while in_progress %r' % (
         msg, self.in_progress)
        if self.level_matches(self.NOTIFY, self._stdout_level()):
            sys.stdout.write(msg)
            sys.stdout.flush()
            self.in_progress_hanging = True
        else:
            self.in_progress_hanging = False
        self.in_progress = msg

    def end_progress(self, msg='done.'):
        if not self.in_progress:
            raise AssertionError('Tried to end_progress without start_progress')
            if self.stdout_level_matches(self.NOTIFY):
                self.in_progress_hanging or sys.stdout.write('...' + self.in_progress + msg + '\n')
                sys.stdout.flush()
            else:
                sys.stdout.write(msg + '\n')
                sys.stdout.flush()
        self.in_progress = None
        self.in_progress_hanging = False
        return

    def show_progress(self):
        """If we are in a progress scope, and no log messages have been
        shown, write out another '.'"""
        if self.in_progress_hanging:
            sys.stdout.write('.')
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

    def level_matches(self, level, consumer_level):
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
            if start is not None and start > consumer_level:
                return False
            if stop is not None and stop <= consumer_level:
                return False
            return True
        return level >= consumer_level
        return

    def level_for_integer(cls, level):
        levels = cls.LEVELS
        if level < 0:
            return levels[0]
        if level >= len(levels):
            return levels[(-1)]
        return levels[level]

    level_for_integer = classmethod(level_for_integer)


logger = Logger([(Logger.LEVELS[(-1)], sys.stdout)])

def mkdir(path):
    global logger
    if not os.path.exists(path):
        logger.info('Creating %s', path)
        os.makedirs(path)
    else:
        logger.info('Directory %s already exists', path)


def copyfileordir(src, dest):
    if os.path.isdir(src):
        shutil.copytree(src, dest, True)
    else:
        shutil.copy2(src, dest)


def copyfile(src, dest, symlink=True):
    if not os.path.exists(src):
        logger.warn('Cannot find file %s (bad symlink)', src)
        return
    if os.path.exists(dest):
        logger.debug('File %s already exists', dest)
        return
    if not os.path.exists(os.path.dirname(dest)):
        logger.info('Creating parent directories for %s' % os.path.dirname(dest))
        os.makedirs(os.path.dirname(dest))
    if not os.path.islink(src):
        srcpath = os.path.abspath(src)
    else:
        srcpath = os.readlink(src)
    if symlink and hasattr(os, 'symlink') and not is_win:
        logger.info('Symlinking %s', dest)
        try:
            os.symlink(srcpath, dest)
        except (OSError, NotImplementedError):
            logger.info('Symlinking failed, copying to %s', dest)
            copyfileordir(src, dest)

    else:
        logger.info('Copying to %s', dest)
        copyfileordir(src, dest)


def writefile(dest, content, overwrite=True):
    if not os.path.exists(dest):
        logger.info('Writing %s', dest)
        f = open(dest, 'wb')
        f.write(content.encode('utf-8'))
        f.close()
        return
    f = open(dest, 'rb')
    c = f.read()
    f.close()
    if c != content.encode('utf-8'):
        if not overwrite:
            logger.notify('File %s exists with different content; not overwriting', dest)
            return
        logger.notify('Overwriting %s with new content', dest)
        f = open(dest, 'wb')
        f.write(content.encode('utf-8'))
        f.close()
    else:
        logger.info('Content %s already in place', dest)


def rmtree(dir):
    if os.path.exists(dir):
        logger.notify('Deleting tree %s', dir)
        shutil.rmtree(dir)
    else:
        logger.info('Do not need to delete %s; already gone', dir)


def make_exe(fn):
    if hasattr(os, 'chmod'):
        oldmode = os.stat(fn).st_mode & 4095
        newmode = (oldmode | 365) & 4095
        os.chmod(fn, newmode)
        logger.info('Changed mode of %s to %s', fn, oct(newmode))


def _find_file(filename, dirs):
    for dir in reversed(dirs):
        files = glob.glob(os.path.join(dir, filename))
        if files and os.path.isfile(files[0]):
            return (True, files[0])

    return (
     False, filename)


def _install_req(py_executable, unzip=False, distribute=False, search_dirs=None, never_download=False):
    if search_dirs is None:
        search_dirs = file_search_dirs()
    if not distribute:
        egg_path = 'setuptools-*-py%s.egg' % sys.version[:3]
        found, egg_path = _find_file(egg_path, search_dirs)
        project_name = 'setuptools'
        bootstrap_script = EZ_SETUP_PY
        tgz_path = None
    else:
        egg_path = 'distribute-*-py%s.egg' % sys.version[:3]
        found, egg_path = _find_file(egg_path, search_dirs)
        project_name = 'distribute'
        if found:
            tgz_path = None
            bootstrap_script = DISTRIBUTE_FROM_EGG_PY
        else:
            egg_path = None
            tgz_path = 'distribute-*.tar.gz'
            found, tgz_path = _find_file(tgz_path, search_dirs)
            bootstrap_script = DISTRIBUTE_SETUP_PY
    if is_jython and os._name == 'nt':
        fd, ez_setup = tempfile.mkstemp('.py')
        os.write(fd, bootstrap_script)
        os.close(fd)
        cmd = [py_executable, ez_setup]
    else:
        cmd = [
         py_executable, '-c', bootstrap_script]
    if unzip and egg_path:
        cmd.append('--always-unzip')
    env = {}
    remove_from_env = [
     '__PYVENV_LAUNCHER__']
    if logger.stdout_level_matches(logger.DEBUG) and egg_path:
        cmd.append('-v')
    old_chdir = os.getcwd()
    if egg_path is not None and os.path.exists(egg_path):
        logger.info('Using existing %s egg: %s' % (project_name, egg_path))
        cmd.append(egg_path)
        if os.environ.get('PYTHONPATH'):
            env['PYTHONPATH'] = egg_path + os.path.pathsep + os.environ['PYTHONPATH']
        else:
            env['PYTHONPATH'] = egg_path
    elif tgz_path is not None and os.path.exists(tgz_path):
        logger.info('Using existing %s egg: %s' % (project_name, tgz_path))
        os.chdir(os.path.dirname(tgz_path))
        remove_from_env.append('PYTHONPATH')
    elif never_download:
        logger.fatal("Can't find any local distributions of %s to install and --never-download is set.  Either re-run virtualenv without the --never-download option, or place a %s distribution (%s) in one of these locations: %r" % (
         project_name, project_name,
         egg_path or tgz_path,
         search_dirs))
        sys.exit(1)
    elif egg_path:
        logger.info('No %s egg found; downloading' % project_name)
        cmd.extend(['--always-copy', '-U', project_name])
    else:
        logger.info('No %s tgz found; downloading' % project_name)
    logger.start_progress('Installing %s...' % project_name)
    logger.indent += 2
    cwd = None
    if project_name == 'distribute':
        env['DONT_PATCH_SETUPTOOLS'] = 'true'

    def _filter_ez_setup(line):
        return filter_ez_setup(line, project_name)

    if not os.access(os.getcwd(), os.W_OK):
        cwd = tempfile.mkdtemp()
        if tgz_path is not None and os.path.exists(tgz_path):
            target = os.path.join(cwd, os.path.split(tgz_path)[(-1)])
            shutil.copy(tgz_path, target)
    try:
        call_subprocess(cmd, show_stdout=False, filter_stdout=_filter_ez_setup, extra_env=env, remove_from_env=remove_from_env, cwd=cwd)
    finally:
        logger.indent -= 2
        logger.end_progress()
        if cwd is not None:
            shutil.rmtree(cwd)
        if os.getcwd() != old_chdir:
            os.chdir(old_chdir)
        if is_jython and os._name == 'nt':
            os.remove(ez_setup)

    return


def file_search_dirs():
    here = os.path.dirname(os.path.abspath(__file__))
    dirs = ['.', here,
     join(here, 'virtualenv_support')]
    if os.path.splitext(os.path.dirname(__file__))[0] != 'virtualenv':
        try:
            import virtualenv
        except ImportError:
            pass
        else:
            dirs.append(os.path.join(os.path.dirname(virtualenv.__file__), 'virtualenv_support'))

    return [ d for d in dirs if os.path.isdir(d) ]


def install_setuptools(py_executable, unzip=False, search_dirs=None, never_download=False):
    _install_req(py_executable, unzip, search_dirs=search_dirs, never_download=never_download)


def install_distribute(py_executable, unzip=False, search_dirs=None, never_download=False):
    _install_req(py_executable, unzip, distribute=True, search_dirs=search_dirs, never_download=never_download)


_pip_re = re.compile('^pip-.*(zip|tar.gz|tar.bz2|tgz|tbz)$', re.I)

def install_pip(py_executable, search_dirs=None, never_download=False):
    if search_dirs is None:
        search_dirs = file_search_dirs()
    filenames = []
    for dir in search_dirs:
        filenames.extend([ join(dir, fn) for fn in os.listdir(dir) if _pip_re.search(fn)
                         ])

    filenames = [ (os.path.basename(filename).lower(), i, filename) for i, filename in enumerate(filenames) ]
    filenames.sort()
    filenames = [ filename for basename, i, filename in filenames ]
    if not filenames:
        filename = 'pip'
    else:
        filename = filenames[(-1)]
    easy_install_script = 'easy_install'
    if is_win:
        easy_install_script = 'easy_install-script.py'
    cmd = [
     py_executable, '-x', join(os.path.dirname(py_executable), easy_install_script), filename]
    if is_jython or is_pypy:
        cmd.remove('-x')
    if filename == 'pip':
        if never_download:
            logger.fatal("Can't find any local distributions of pip to install and --never-download is set.  Either re-run virtualenv without the --never-download option, or place a pip source distribution (zip/tar.gz/tar.bz2) in one of these locations: %r" % search_dirs)
            sys.exit(1)
        logger.info('Installing pip from network...')
    else:
        logger.info('Installing existing %s distribution: %s' % (
         os.path.basename(filename), filename))
    logger.start_progress('Installing pip...')
    logger.indent += 2

    def _filter_setup(line):
        return filter_ez_setup(line, 'pip')

    try:
        call_subprocess(cmd, show_stdout=False, filter_stdout=_filter_setup)
    finally:
        logger.indent -= 2
        logger.end_progress()

    return


def filter_ez_setup(line, project_name='setuptools'):
    if not line.strip():
        return Logger.DEBUG
    if project_name == 'distribute':
        for prefix in ('Extracting', 'Now working', 'Installing', 'Before', 'Scanning',
                       'Setuptools', 'Egg', 'Already', 'running', 'writing', 'reading',
                       'installing', 'creating', 'copying', 'byte-compiling', 'removing',
                       'Processing'):
            if line.startswith(prefix):
                return Logger.DEBUG

        return Logger.DEBUG
    for prefix in ['Reading ', 'Best match', 'Processing setuptools', 'Copying setuptools', 'Adding setuptools',
     'Installing ', 'Installed ']:
        if line.startswith(prefix):
            return Logger.DEBUG

    return Logger.INFO


class UpdatingDefaultsHelpFormatter(optparse.IndentedHelpFormatter):
    """
    Custom help formatter for use in ConfigOptionParser that updates
    the defaults before expanding them, allowing them to show up correctly
    in the help listing
    """

    def expand_default(self, option):
        if self.parser is not None:
            self.parser.update_defaults(self.parser.defaults)
        return optparse.IndentedHelpFormatter.expand_default(self, option)


class ConfigOptionParser(optparse.OptionParser):
    """
    Custom option parser which updates its defaults by by checking the
    configuration files and environmental variables
    """

    def __init__(self, *args, **kwargs):
        self.config = ConfigParser.RawConfigParser()
        self.files = self.get_config_files()
        self.config.read(self.files)
        optparse.OptionParser.__init__(self, *args, **kwargs)

    def get_config_files(self):
        config_file = os.environ.get('VIRTUALENV_CONFIG_FILE', False)
        if config_file and os.path.exists(config_file):
            return [config_file]
        return [
         default_config_file]

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
                key = '--%s' % key
            option = self.get_option(key)
            if option is not None:
                if not val:
                    continue
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
                        print 'An error occured during configuration: %s' % e
                        sys.exit(3)

                defaults[option.dest] = val

        return defaults

    def get_config_section(self, name):
        """
        Get a section of a configuration
        """
        if self.config.has_section(name):
            return self.config.items(name)
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
        Overridding to make updating the defaults after instantiation of
        the option parser possible, update_defaults() does the dirty work.
        """
        if not self.process_default_values:
            return optparse.Values(self.defaults)
        defaults = self.update_defaults(self.defaults.copy())
        for option in self._get_all_options():
            default = defaults.get(option.dest)
            if isinstance(default, basestring):
                opt_str = option.get_opt_string()
                defaults[option.dest] = option.check_value(opt_str, default)

        return optparse.Values(defaults)


def main():
    global logger
    parser = ConfigOptionParser(version=virtualenv_version, usage='%prog [OPTIONS] DEST_DIR', formatter=UpdatingDefaultsHelpFormatter())
    parser.add_option('-v', '--verbose', action='count', dest='verbose', default=0, help='Increase verbosity')
    parser.add_option('-q', '--quiet', action='count', dest='quiet', default=0, help='Decrease verbosity')
    parser.add_option('-p', '--python', dest='python', metavar='PYTHON_EXE', help='The Python interpreter to use, e.g., --python=python2.5 will use the python2.5 interpreter to create the new environment.  The default is the interpreter that virtualenv was installed with (%s)' % sys.executable)
    parser.add_option('--clear', dest='clear', action='store_true', help='Clear out the non-root install and start from scratch')
    parser.set_defaults(system_site_packages=False)
    parser.add_option('--no-site-packages', dest='system_site_packages', action='store_false', help="Don't give access to the global site-packages dir to the virtual environment (default)")
    parser.add_option('--system-site-packages', dest='system_site_packages', action='store_true', help='Give access to the global site-packages dir to the virtual environment')
    parser.add_option('--unzip-setuptools', dest='unzip_setuptools', action='store_true', help='Unzip Setuptools or Distribute when installing it')
    parser.add_option('--relocatable', dest='relocatable', action='store_true', help='Make an EXISTING virtualenv environment relocatable.  This fixes up scripts and makes all .pth files relative')
    parser.add_option('--distribute', '--use-distribute', dest='use_distribute', action='store_true', help='Use Distribute instead of Setuptools. Set environ variable VIRTUALENV_DISTRIBUTE to make it the default ')
    parser.add_option('--no-setuptools', dest='no_setuptools', action='store_true', help='Do not install distribute/setuptools (or pip) in the new virtualenv.')
    parser.add_option('--no-pip', dest='no_pip', action='store_true', help='Do not install pip in the new virtualenv.')
    parser.add_option('--setuptools', dest='use_distribute', action='store_false', help='Use Setuptools instead of Distribute.  Set environ variable VIRTUALENV_SETUPTOOLS to make it the default ')
    parser.set_defaults(use_distribute=False)
    default_search_dirs = file_search_dirs()
    parser.add_option('--extra-search-dir', dest='search_dirs', action='append', default=default_search_dirs, help='Directory to look for setuptools/distribute/pip distributions in. You can add any number of additional --extra-search-dir paths.')
    parser.add_option('--never-download', dest='never_download', action='store_true', help='Never download anything from the network.  Instead, virtualenv will fail if local distributions of setuptools/distribute/pip are not present.')
    parser.add_option('--prompt', dest='prompt', help='Provides an alternative prompt prefix for this environment')
    if 'extend_parser' in globals():
        extend_parser(parser)
    options, args = parser.parse_args()
    if 'adjust_options' in globals():
        adjust_options(options, args)
    verbosity = options.verbose - options.quiet
    logger = Logger([(Logger.level_for_integer(2 - verbosity), sys.stdout)])
    if options.python and not os.environ.get('VIRTUALENV_INTERPRETER_RUNNING'):
        env = os.environ.copy()
        interpreter = resolve_interpreter(options.python)
        if interpreter == sys.executable:
            logger.warn('Already using interpreter %s' % interpreter)
        else:
            logger.notify('Running virtualenv with interpreter %s' % interpreter)
            env['VIRTUALENV_INTERPRETER_RUNNING'] = 'true'
            file = __file__
            if file.endswith('.pyc'):
                file = file[:-1]
            popen = subprocess.Popen([interpreter, file] + sys.argv[1:], env=env)
            raise SystemExit(popen.wait())
    if majver > 2:
        options.use_distribute = True
    if os.environ.get('PYTHONDONTWRITEBYTECODE') and not options.use_distribute:
        print 'The PYTHONDONTWRITEBYTECODE environment variable is not compatible with setuptools. Either use --distribute or unset PYTHONDONTWRITEBYTECODE.'
        sys.exit(2)
    if not args:
        print 'You must provide a DEST_DIR'
        parser.print_help()
        sys.exit(2)
    if len(args) > 1:
        print 'There must be only one argument: DEST_DIR (you gave %s)' % (' ').join(args)
        parser.print_help()
        sys.exit(2)
    home_dir = args[0]
    if os.environ.get('WORKING_ENV'):
        logger.fatal('ERROR: you cannot run virtualenv while in a workingenv')
        logger.fatal('Please deactivate your workingenv, then re-run this script')
        sys.exit(3)
    if 'PYTHONHOME' in os.environ:
        logger.warn('PYTHONHOME is set.  You *must* activate the virtualenv before using it')
        del os.environ['PYTHONHOME']
    if options.relocatable:
        make_environment_relocatable(home_dir)
        return
    create_environment(home_dir, site_packages=options.system_site_packages, clear=options.clear, unzip_setuptools=options.unzip_setuptools, use_distribute=options.use_distribute, prompt=options.prompt, search_dirs=options.search_dirs, never_download=options.never_download, no_setuptools=options.no_setuptools, no_pip=options.no_pip)
    if 'after_install' in globals():
        after_install(options, home_dir)


def call_subprocess(cmd, show_stdout=True, filter_stdout=None, cwd=None, raise_on_returncode=True, extra_env=None, remove_from_env=None):
    cmd_parts = []
    for part in cmd:
        if len(part) > 45:
            part = part[:20] + '...' + part[-20:]
        if ' ' in part or '\n' in part or '"' in part or "'" in part:
            part = '"%s"' % part.replace('"', '\\"')
        if hasattr(part, 'decode'):
            try:
                part = part.decode(sys.getdefaultencoding())
            except UnicodeDecodeError:
                part = part.decode(sys.getfilesystemencoding())

        cmd_parts.append(part)

    cmd_desc = (' ').join(cmd_parts)
    if show_stdout:
        stdout = None
    else:
        stdout = subprocess.PIPE
    logger.debug('Running command %s' % cmd_desc)
    if extra_env or remove_from_env:
        env = os.environ.copy()
        if extra_env:
            env.update(extra_env)
        if remove_from_env:
            for varname in remove_from_env:
                env.pop(varname, None)

    else:
        env = None
    try:
        proc = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdin=None, stdout=stdout, cwd=cwd, env=env)
    except Exception:
        e = sys.exc_info()[1]
        logger.fatal('Error %s while executing command %s' % (e, cmd_desc))
        raise

    all_output = []
    if stdout is not None:
        stdout = proc.stdout
        encoding = sys.getdefaultencoding()
        fs_encoding = sys.getfilesystemencoding()
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
        proc.communicate()
    proc.wait()
    if proc.returncode:
        if raise_on_returncode:
            if all_output:
                logger.notify('Complete output from command %s:' % cmd_desc)
                logger.notify(('\n').join(all_output) + '\n----------------------------------------')
            raise OSError('Command %s failed with error code %s' % (
             cmd_desc, proc.returncode))
        else:
            logger.warn('Command %s had error code %s' % (
             cmd_desc, proc.returncode))
    return


def create_environment(home_dir, site_packages=False, clear=False, unzip_setuptools=False, use_distribute=False, prompt=None, search_dirs=None, never_download=False, no_setuptools=False, no_pip=False):
    """
    Creates a new environment in ``home_dir``.

    If ``site_packages`` is true, then the global ``site-packages/``
    directory will be on the path.

    If ``clear`` is true (default False) then the environment will
    first be cleared.
    """
    home_dir, lib_dir, inc_dir, bin_dir = path_locations(home_dir)
    py_executable = os.path.abspath(install_python(home_dir, lib_dir, inc_dir, bin_dir, site_packages=site_packages, clear=clear))
    install_distutils(home_dir)
    if not no_setuptools:
        if use_distribute:
            install_distribute(py_executable, unzip=unzip_setuptools, search_dirs=search_dirs, never_download=never_download)
        else:
            install_setuptools(py_executable, unzip=unzip_setuptools, search_dirs=search_dirs, never_download=never_download)
        if not no_pip:
            install_pip(py_executable, search_dirs=search_dirs, never_download=never_download)
    install_activate(home_dir, bin_dir, prompt)


def is_executable_file(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def path_locations(home_dir):
    """Return the path locations for the environment (where libraries are,
    where scripts go, etc)"""
    if is_win:
        mkdir(home_dir)
        if ' ' in home_dir:
            import ctypes
            GetShortPathName = ctypes.windll.kernel32.GetShortPathNameW
            size = max(len(home_dir) + 1, 256)
            buf = ctypes.create_unicode_buffer(size)
            try:
                u = unicode
            except NameError:
                u = str

            ret = GetShortPathName(u(home_dir), buf, size)
            if not ret:
                print 'Error: the path "%s" has a space in it' % home_dir
                print 'We could not determine the short pathname for it.'
                print 'Exiting.'
                sys.exit(3)
            home_dir = str(buf.value)
        lib_dir = join(home_dir, 'Lib')
        inc_dir = join(home_dir, 'Include')
        bin_dir = join(home_dir, 'Scripts')
    if is_jython:
        lib_dir = join(home_dir, 'Lib')
        inc_dir = join(home_dir, 'Include')
        bin_dir = join(home_dir, 'bin')
    elif is_pypy:
        lib_dir = home_dir
        inc_dir = join(home_dir, 'include')
        bin_dir = join(home_dir, 'bin')
    elif not is_win:
        lib_dir = join(home_dir, 'lib', py_version)
        multiarch_exec = '/usr/bin/multiarch-platform'
        if is_executable_file(multiarch_exec):
            p = subprocess.Popen(multiarch_exec, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            inc_dir = join(home_dir, 'include', stdout.strip(), py_version + abiflags)
        else:
            inc_dir = join(home_dir, 'include', py_version + abiflags)
        bin_dir = join(home_dir, 'bin')
    return (
     home_dir, lib_dir, inc_dir, bin_dir)


def change_prefix(filename, dst_prefix):
    prefixes = [
     sys.prefix]
    if is_darwin:
        prefixes.extend((
         os.path.join('/Library/Python', sys.version[:3], 'site-packages'),
         os.path.join(sys.prefix, 'Extras', 'lib', 'python'),
         os.path.join('~', 'Library', 'Python', sys.version[:3], 'site-packages'),
         os.path.join('~', '.local', 'lib', 'python', sys.version[:3], 'site-packages'),
         os.path.join('~', 'Library', 'Python', sys.version[:3], 'lib', 'python', 'site-packages')))
    if hasattr(sys, 'real_prefix'):
        prefixes.append(sys.real_prefix)
    if hasattr(sys, 'base_prefix'):
        prefixes.append(sys.base_prefix)
    prefixes = list(map(os.path.expanduser, prefixes))
    prefixes = list(map(os.path.abspath, prefixes))
    prefixes = sorted(prefixes, key=len, reverse=True)
    filename = os.path.abspath(filename)
    for src_prefix in prefixes:
        if filename.startswith(src_prefix):
            _, relpath = filename.split(src_prefix, 1)
            if src_prefix != os.sep:
                if not relpath[0] == os.sep:
                    raise AssertionError
                    relpath = relpath[1:]
                return join(dst_prefix, relpath)

    assert False, 'Filename %s does not start with any of these prefixes: %s' % (
     filename, prefixes)


def copy_required_modules(dst_prefix):
    import imp
    _prev_sys_path = sys.path
    if os.environ.get('VIRTUALENV_INTERPRETER_RUNNING'):
        sys.path = sys.path[1:]
    try:
        for modname in REQUIRED_MODULES:
            if modname in sys.builtin_module_names:
                logger.info('Ignoring built-in bootstrap module: %s' % modname)
                continue
            try:
                f, filename, _ = imp.find_module(modname)
            except ImportError:
                logger.info('Cannot import bootstrap module: %s' % modname)
            else:
                if f is not None:
                    f.close()
                if modname == 'readline' and sys.platform == 'darwin' and not (is_pypy or filename.endswith(join('lib-dynload', 'readline.so'))):
                    dst_filename = join(dst_prefix, 'lib', 'python%s' % sys.version[:3], 'readline.so')
                else:
                    dst_filename = change_prefix(filename, dst_prefix)
                copyfile(filename, dst_filename)
                if filename.endswith('.pyc'):
                    pyfile = filename[:-1]
                    if os.path.exists(pyfile):
                        copyfile(pyfile, dst_filename[:-1])

    finally:
        sys.path = _prev_sys_path

    return


def subst_path(prefix_path, prefix, home_dir):
    prefix_path = os.path.normpath(prefix_path)
    prefix = os.path.normpath(prefix)
    home_dir = os.path.normpath(home_dir)
    if not prefix_path.startswith(prefix):
        logger.warn('Path not in prefix %r %r', prefix_path, prefix)
        return
    return prefix_path.replace(prefix, home_dir, 1)


def install_python(home_dir, lib_dir, inc_dir, bin_dir, site_packages, clear):
    """Install just the base environment, no distutils patches etc"""
    if sys.executable.startswith(bin_dir):
        print 'Please use the *system* python to run this script'
        return
    else:
        if clear:
            rmtree(lib_dir)
            logger.notify('Not deleting %s', bin_dir)
        if hasattr(sys, 'real_prefix'):
            logger.notify('Using real prefix %r' % sys.real_prefix)
            prefix = sys.real_prefix
        elif hasattr(sys, 'base_prefix'):
            logger.notify('Using base prefix %r' % sys.base_prefix)
            prefix = sys.base_prefix
        else:
            prefix = sys.prefix
        mkdir(lib_dir)
        fix_lib64(lib_dir)
        stdlib_dirs = [os.path.dirname(os.__file__)]
        if is_win:
            stdlib_dirs.append(join(os.path.dirname(stdlib_dirs[0]), 'DLLs'))
        elif is_darwin:
            stdlib_dirs.append(join(stdlib_dirs[0], 'site-packages'))
        if hasattr(os, 'symlink'):
            logger.info('Symlinking Python bootstrap modules')
        else:
            logger.info('Copying Python bootstrap modules')
        logger.indent += 2
        try:
            for stdlib_dir in stdlib_dirs:
                if not os.path.isdir(stdlib_dir):
                    continue
                for fn in os.listdir(stdlib_dir):
                    bn = os.path.splitext(fn)[0]
                    if fn != 'site-packages' and bn in REQUIRED_FILES:
                        copyfile(join(stdlib_dir, fn), join(lib_dir, fn))

            copy_required_modules(home_dir)
        finally:
            logger.indent -= 2

        mkdir(join(lib_dir, 'site-packages'))
        import site
        site_filename = site.__file__
        if site_filename.endswith('.pyc'):
            site_filename = site_filename[:-1]
        elif site_filename.endswith('$py.class'):
            site_filename = site_filename.replace('$py.class', '.py')
        site_filename_dst = change_prefix(site_filename, home_dir)
        site_dir = os.path.dirname(site_filename_dst)
        writefile(site_filename_dst, SITE_PY)
        writefile(join(site_dir, 'orig-prefix.txt'), prefix)
        site_packages_filename = join(site_dir, 'no-global-site-packages.txt')
        if not site_packages:
            writefile(site_packages_filename, '')
        if is_pypy or is_win:
            stdinc_dir = join(prefix, 'include')
        else:
            stdinc_dir = join(prefix, 'include', py_version + abiflags)
        if os.path.exists(stdinc_dir):
            copyfile(stdinc_dir, inc_dir)
        else:
            logger.debug('No include dir %s' % stdinc_dir)
        platinc_dir = distutils.sysconfig.get_python_inc(plat_specific=1)
        if platinc_dir != stdinc_dir:
            platinc_dest = distutils.sysconfig.get_python_inc(plat_specific=1, prefix=home_dir)
            if platinc_dir == platinc_dest:
                platinc_dest = subst_path(platinc_dir, prefix, home_dir)
            if platinc_dest:
                copyfile(platinc_dir, platinc_dest)
        if sys.exec_prefix != prefix and not is_pypy:
            if is_win:
                exec_dir = join(sys.exec_prefix, 'lib')
            else:
                if is_jython:
                    exec_dir = join(sys.exec_prefix, 'Lib')
                else:
                    exec_dir = join(sys.exec_prefix, 'lib', py_version)
                for fn in os.listdir(exec_dir):
                    copyfile(join(exec_dir, fn), join(lib_dir, fn))

        if is_jython:
            for name in ('jython-dev.jar', 'javalib', 'jython.jar'):
                src = join(prefix, name)
                if os.path.exists(src):
                    copyfile(src, join(home_dir, name))

            src = join(prefix, 'registry')
            if os.path.exists(src):
                copyfile(src, join(home_dir, 'registry'), symlink=False)
            copyfile(join(prefix, 'cachedir'), join(home_dir, 'cachedir'), symlink=False)
        mkdir(bin_dir)
        py_executable = join(bin_dir, os.path.basename(sys.executable))
        if 'Python.framework' in prefix:
            if os.environ.get('__PYVENV_LAUNCHER__'):
                os.unsetenv('__PYVENV_LAUNCHER__')
            if re.search('/Python(?:-32|-64)*$', py_executable):
                py_executable = os.path.join(os.path.dirname(py_executable), 'python')
        logger.notify('New %s executable in %s', expected_exe, py_executable)
        pcbuild_dir = os.path.dirname(sys.executable)
        pyd_pth = os.path.join(lib_dir, 'site-packages', 'virtualenv_builddir_pyd.pth')
        if is_win and os.path.exists(os.path.join(pcbuild_dir, 'build.bat')):
            logger.notify('Detected python running from build directory %s', pcbuild_dir)
            logger.notify('Writing .pth file linking to build directory for *.pyd files')
            writefile(pyd_pth, pcbuild_dir)
        else:
            pcbuild_dir = None
            if os.path.exists(pyd_pth):
                logger.info('Deleting %s (not Windows env or not build directory python)' % pyd_pth)
                os.unlink(pyd_pth)
            if sys.executable != py_executable:
                executable = sys.executable
                shutil.copyfile(executable, py_executable)
                make_exe(py_executable)
                if is_win or is_cygwin:
                    pythonw = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
                    if os.path.exists(pythonw):
                        logger.info('Also created pythonw.exe')
                        shutil.copyfile(pythonw, os.path.join(os.path.dirname(py_executable), 'pythonw.exe'))
                    python_d = os.path.join(os.path.dirname(sys.executable), 'python_d.exe')
                    python_d_dest = os.path.join(os.path.dirname(py_executable), 'python_d.exe')
                    if os.path.exists(python_d):
                        logger.info('Also created python_d.exe')
                        shutil.copyfile(python_d, python_d_dest)
                    elif os.path.exists(python_d_dest):
                        logger.info('Removed python_d.exe as it is no longer at the source')
                        os.unlink(python_d_dest)
                    py_executable_dll = 'python%s%s.dll' % (
                     sys.version_info[0], sys.version_info[1])
                    py_executable_dll_d = 'python%s%s_d.dll' % (
                     sys.version_info[0], sys.version_info[1])
                    pythondll = os.path.join(os.path.dirname(sys.executable), py_executable_dll)
                    pythondll_d = os.path.join(os.path.dirname(sys.executable), py_executable_dll_d)
                    pythondll_d_dest = os.path.join(os.path.dirname(py_executable), py_executable_dll_d)
                    if os.path.exists(pythondll):
                        logger.info('Also created %s' % py_executable_dll)
                        shutil.copyfile(pythondll, os.path.join(os.path.dirname(py_executable), py_executable_dll))
                    if os.path.exists(pythondll_d):
                        logger.info('Also created %s' % py_executable_dll_d)
                        shutil.copyfile(pythondll_d, pythondll_d_dest)
                    elif os.path.exists(pythondll_d_dest):
                        logger.info('Removed %s as the source does not exist' % pythondll_d_dest)
                        os.unlink(pythondll_d_dest)
                if is_pypy:
                    python_executable = os.path.join(os.path.dirname(py_executable), 'python')
                    if sys.platform in ('win32', 'cygwin'):
                        python_executable += '.exe'
                    logger.info('Also created executable %s' % python_executable)
                    copyfile(py_executable, python_executable)
                    if is_win:
                        for name in ('libexpat.dll', 'libpypy.dll', 'libpypy-c.dll',
                                     'libeay32.dll', 'ssleay32.dll', 'sqlite.dll'):
                            src = join(prefix, name)
                            if os.path.exists(src):
                                copyfile(src, join(bin_dir, name))

            if os.path.splitext(os.path.basename(py_executable))[0] != expected_exe:
                secondary_exe = os.path.join(os.path.dirname(py_executable), expected_exe)
                py_executable_ext = os.path.splitext(py_executable)[1]
                if py_executable_ext == '.exe':
                    secondary_exe += py_executable_ext
                if os.path.exists(secondary_exe):
                    logger.warn('Not overwriting existing %s script %s (you must use %s)' % (
                     expected_exe, secondary_exe, py_executable))
                else:
                    logger.notify('Also creating executable in %s' % secondary_exe)
                    shutil.copyfile(sys.executable, secondary_exe)
                    make_exe(secondary_exe)
            if '.framework' in prefix:
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
                copyfile(os.path.join(prefix, 'Python'), virtual_lib)
                try:
                    mach_o_change(py_executable, os.path.join(prefix, 'Python'), '@executable_path/../.Python')
                except:
                    e = sys.exc_info()[1]
                    logger.warn('Could not call mach_o_change: %s. Trying to call install_name_tool instead.' % e)
                    try:
                        call_subprocess([
                         'install_name_tool', '-change',
                         os.path.join(prefix, 'Python'),
                         '@executable_path/../.Python',
                         py_executable])
                    except:
                        logger.fatal("Could not call install_name_tool -- you must have Apple's development tools installed")
                        raise

            if not is_win:
                py_exe_version_major = 'python%s' % sys.version_info[0]
                py_exe_version_major_minor = 'python%s.%s' % (
                 sys.version_info[0], sys.version_info[1])
                py_exe_no_version = 'python'
                required_symlinks = [py_exe_no_version, py_exe_version_major,
                 py_exe_version_major_minor]
                py_executable_base = os.path.basename(py_executable)
                if py_executable_base in required_symlinks:
                    required_symlinks.remove(py_executable_base)
                for pth in required_symlinks:
                    full_pth = join(bin_dir, pth)
                    if os.path.exists(full_pth):
                        os.unlink(full_pth)
                    os.symlink(py_executable_base, full_pth)

            if is_win and ' ' in py_executable:
                py_executable = '"%s"' % py_executable
            cmd = [py_executable, '-c', 'import sys;out=sys.stdout;getattr(out, "buffer", out).write(sys.prefix.encode("utf-8"))']
            logger.info('Testing executable with %s %s "%s"' % tuple(cmd))
            try:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                proc_stdout, proc_stderr = proc.communicate()
            except OSError:
                e = sys.exc_info()[1]
                if e.errno == errno.EACCES:
                    logger.fatal('ERROR: The executable %s could not be run: %s' % (py_executable, e))
                    sys.exit(100)
                else:
                    raise e

        proc_stdout = proc_stdout.strip().decode('utf-8')
        proc_stdout = os.path.normcase(os.path.abspath(proc_stdout))
        norm_home_dir = os.path.normcase(os.path.abspath(home_dir))
        if hasattr(norm_home_dir, 'decode'):
            norm_home_dir = norm_home_dir.decode(sys.getfilesystemencoding())
        if proc_stdout != norm_home_dir:
            logger.fatal('ERROR: The executable %s is not functioning' % py_executable)
            logger.fatal('ERROR: It thinks sys.prefix is %r (should be %r)' % (
             proc_stdout, norm_home_dir))
            logger.fatal('ERROR: virtualenv is not compatible with this system or executable')
            if is_win:
                logger.fatal('Note: some Windows users have reported this error when they installed Python for "Only this user" or have multiple versions of Python installed. Copying the appropriate PythonXX.dll to the virtualenv Scripts/ directory may fix this problem.')
            sys.exit(100)
        else:
            logger.info('Got sys.prefix result: %r' % proc_stdout)
        pydistutils = os.path.expanduser('~/.pydistutils.cfg')
        if os.path.exists(pydistutils):
            logger.notify('Please make sure you remove any previous custom paths from your %s file.' % pydistutils)
        fix_local_scheme(home_dir)
        if site_packages:
            if os.path.exists(site_packages_filename):
                logger.info('Deleting %s' % site_packages_filename)
                os.unlink(site_packages_filename)
        return py_executable


def install_activate(home_dir, bin_dir, prompt=None):
    home_dir = os.path.abspath(home_dir)
    if is_win or is_jython and os._name == 'nt':
        files = {'activate.bat': ACTIVATE_BAT, 'deactivate.bat': DEACTIVATE_BAT, 
           'activate.ps1': ACTIVATE_PS}
        drive, tail = os.path.splitdrive(home_dir.replace(os.sep, '/'))
        home_dir_msys = (drive and '/%s%s' or '%s%s') % (drive[:1], tail)
        home_dir_sh = '$(if [ "$OSTYPE" "==" "cygwin" ]; then cygpath -u \'%s\'; else echo \'%s\'; fi;)' % (
         home_dir, home_dir_msys)
        files['activate'] = ACTIVATE_SH.replace('__VIRTUAL_ENV__', home_dir_sh)
    else:
        files = {'activate': ACTIVATE_SH}
        files['activate.fish'] = ACTIVATE_FISH
        files['activate.csh'] = ACTIVATE_CSH
    files['activate_this.py'] = ACTIVATE_THIS
    if hasattr(home_dir, 'decode'):
        home_dir = home_dir.decode(sys.getfilesystemencoding())
    vname = os.path.basename(home_dir)
    for name, content in files.items():
        content = content.replace('__VIRTUAL_PROMPT__', prompt or '')
        content = content.replace('__VIRTUAL_WINPROMPT__', prompt or '(%s)' % vname)
        content = content.replace('__VIRTUAL_ENV__', home_dir)
        content = content.replace('__VIRTUAL_NAME__', vname)
        content = content.replace('__BIN_NAME__', os.path.basename(bin_dir))
        writefile(os.path.join(bin_dir, name), content)


def install_distutils(home_dir):
    distutils_path = change_prefix(distutils.__path__[0], home_dir)
    mkdir(distutils_path)
    home_dir = os.path.abspath(home_dir)
    writefile(os.path.join(distutils_path, '__init__.py'), DISTUTILS_INIT)
    writefile(os.path.join(distutils_path, 'distutils.cfg'), DISTUTILS_CFG, overwrite=False)


def fix_local_scheme(home_dir):
    """
    Platforms that use the "posix_local" install scheme (like Ubuntu with
    Python 2.7) need to be given an additional "local" location, sigh.
    """
    try:
        import sysconfig
    except ImportError:
        pass

    if sysconfig._get_default_scheme() == 'posix_local':
        local_path = os.path.join(home_dir, 'local')
        if not os.path.exists(local_path):
            os.mkdir(local_path)
            for subdir_name in os.listdir(home_dir):
                if subdir_name == 'local':
                    continue
                os.symlink(os.path.abspath(os.path.join(home_dir, subdir_name)), os.path.join(local_path, subdir_name))


def fix_lib64(lib_dir):
    """
    Some platforms (particularly Gentoo on x64) put things in lib64/pythonX.Y
    instead of lib/pythonX.Y.  If this is such a platform we'll just create a
    symlink so lib64 points to lib
    """
    if [ p for p in distutils.sysconfig.get_config_vars().values() if isinstance(p, basestring) and 'lib64' in p
       ]:
        logger.debug('This system uses lib64; symlinking lib64 to lib')
        assert os.path.basename(lib_dir) == 'python%s' % sys.version[:3], 'Unexpected python lib dir: %r' % lib_dir
        lib_parent = os.path.dirname(lib_dir)
        top_level = os.path.dirname(lib_parent)
        lib_dir = os.path.join(top_level, 'lib')
        lib64_link = os.path.join(top_level, 'lib64')
        assert os.path.basename(lib_parent) == 'lib', 'Unexpected parent dir: %r' % lib_parent
        if os.path.lexists(lib64_link):
            return
        os.symlink('lib', lib64_link)


def resolve_interpreter(exe):
    """
    If the executable given isn't an absolute path, search $PATH for the interpreter
    """
    if os.path.abspath(exe) != exe:
        paths = os.environ.get('PATH', '').split(os.pathsep)
        for path in paths:
            if os.path.exists(os.path.join(path, exe)):
                exe = os.path.join(path, exe)
                break

    if not os.path.exists(exe):
        logger.fatal('The executable %s (from --python=%s) does not exist' % (exe, exe))
        raise SystemExit(3)
    if not is_executable(exe):
        logger.fatal('The executable %s (from --python=%s) is not executable' % (exe, exe))
        raise SystemExit(3)
    return exe


def is_executable(exe):
    """Checks a file is executable"""
    return os.access(exe, os.X_OK)


def make_environment_relocatable(home_dir):
    """
    Makes the already-existing environment use relative paths, and takes out
    the #!-based environment selection in scripts.
    """
    home_dir, lib_dir, inc_dir, bin_dir = path_locations(home_dir)
    activate_this = os.path.join(bin_dir, 'activate_this.py')
    if not os.path.exists(activate_this):
        logger.fatal("The environment doesn't have a file %s -- please re-run virtualenv on this environment to update it" % activate_this)
    fixup_scripts(home_dir)
    fixup_pth_and_egg_link(home_dir)


OK_ABS_SCRIPTS = [
 'python', 'python%s' % sys.version[:3],
 'activate', 'activate.bat', 'activate_this.py']

def fixup_scripts(home_dir):
    shebang = '#!%s/bin/python' % os.path.normcase(os.path.abspath(home_dir))
    new_shebang = '#!/usr/bin/env python%s' % sys.version[:3]
    if is_win:
        bin_suffix = 'Scripts'
    else:
        bin_suffix = 'bin'
    bin_dir = os.path.join(home_dir, bin_suffix)
    home_dir, lib_dir, inc_dir, bin_dir = path_locations(home_dir)
    for filename in os.listdir(bin_dir):
        filename = os.path.join(bin_dir, filename)
        if not os.path.isfile(filename):
            continue
        f = open(filename, 'rb')
        try:
            try:
                lines = f.read().decode('utf-8').splitlines()
            except UnicodeDecodeError:
                continue

        finally:
            f.close()

        if not lines:
            logger.warn('Script %s is an empty file' % filename)
            continue
        if not lines[0].strip().startswith(shebang):
            if os.path.basename(filename) in OK_ABS_SCRIPTS:
                logger.debug('Cannot make script %s relative' % filename)
            elif lines[0].strip() == new_shebang:
                logger.info('Script %s has already been made relative' % filename)
            else:
                logger.warn("Script %s cannot be made relative (it's not a normal script that starts with %s)" % (
                 filename, shebang))
            continue
        logger.notify('Making script %s relative' % filename)
        script = relative_script([new_shebang] + lines[1:])
        f = open(filename, 'wb')
        f.write(('\n').join(script).encode('utf-8'))
        f.close()


def relative_script(lines):
    """Return a script that'll work in a relocatable environment."""
    activate = "import os; activate_this=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'activate_this.py'); execfile(activate_this, dict(__file__=activate_this)); del os, activate_this"
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
    for path in sys_path:
        if not path:
            path = '.'
        if not os.path.isdir(path):
            continue
        path = os.path.normcase(os.path.abspath(path))
        if not path.startswith(home_dir):
            logger.debug('Skipping system (non-environment) directory %s' % path)
            continue
        for filename in os.listdir(path):
            filename = os.path.join(path, filename)
            if filename.endswith('.pth'):
                if not os.access(filename, os.W_OK):
                    logger.warn('Cannot write .pth file %s, skipping' % filename)
                else:
                    fixup_pth_file(filename)
            if filename.endswith('.egg-link'):
                if not os.access(filename, os.W_OK):
                    logger.warn('Cannot write .egg-link file %s, skipping' % filename)
                else:
                    fixup_egg_link(filename)

    return


def fixup_pth_file(filename):
    lines = []
    prev_lines = []
    f = open(filename)
    prev_lines = f.readlines()
    f.close()
    for line in prev_lines:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('import ') or os.path.abspath(line) != line:
            lines.append(line)
        else:
            new_value = make_relative_path(filename, line)
            if line != new_value:
                logger.debug('Rewriting path %s as %s (in %s)' % (line, new_value, filename))
            lines.append(new_value)

    if lines == prev_lines:
        logger.info('No changes to .pth file %s' % filename)
        return
    logger.notify('Making paths in .pth file %s relative' % filename)
    f = open(filename, 'w')
    f.write(('\n').join(lines) + '\n')
    f.close()


def fixup_egg_link(filename):
    f = open(filename)
    link = f.readline().strip()
    f.close()
    if os.path.abspath(link) != link:
        logger.debug('Link in %s already relative' % filename)
        return
    new_link = make_relative_path(filename, link)
    logger.notify('Rewriting link %s in %s as %s' % (link, filename, new_link))
    f = open(filename, 'w')
    f.write(new_link)
    f.close()


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
        full_parts.append(dest_filename)
    if not full_parts:
        return './'
    return os.path.sep.join(full_parts)


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
    filename = __file__
    if filename.endswith('.pyc'):
        filename = filename[:-1]
    f = codecs.open(filename, 'r', encoding='utf-8')
    content = f.read()
    f.close()
    py_exe = 'python%s' % python_version
    content = '#!/usr/bin/env %s\n' % py_exe + '## WARNING: This file is generated\n' + content
    return content.replace('##EXTEND##', extra_text)


def convert(s):
    b = base64.b64decode(s.encode('ascii'))
    return zlib.decompress(b).decode('utf-8')


SITE_PY = convert('\n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\nUM3ckC/Q8aP8VLy+mjYY5MxOtAdgjULwf2RtvCc=\n')
EZ_SETUP_PY = convert('\neJzNWmmP20YS/a5fwSgYSIJlDu9DhrzIJg5gIMgGuYCFPavpc8SYIhWS8li7yH/f181DJDWcJIt8\nWAbOzJDN6qpXVa+qWvr8s+O52ufZbD6f/z3Pq7IqyNEoRXU6VnmelkaSlRVJU1IlWDR7K41zfjIe\nSVYZVW6cSjFcq54WxpGwD+RBLMr6oXk8r41fTmWFBSw9cWFU+6ScySQV6pVqDyHkIAyeFIJVeXE2\nHpNqbyTV2iAZNwjn+gW1oVpb5Ucjl/VOrfzNZjYzcMkiPxji3zt930gOx7yolJa7i5Z63fDWcnVl\nWSF+PUEdgxjlUbBEJsz4KIoSIKi9L6+u1e9YxfPHLM0Jnx2SosiLtZEXGh2SGSStRJGRSnSLLpau\n9aYMq3hulLlBz0Z5Oh7Tc5I9zJSx5Hgs8mORqNfzo3KCxuH+fmzB/b05m/2oYNK4Mr2xkiiM4oTf\nS2UKK5KjNq/xqtby+FAQ3vejqYJh1oBXnsvZV2++/uKnb37c/fzm+x/e/uNbY2vMLTNgtj3vHv30\n/TcKV/VoX1XHze3t8XxMzDq4zLx4uG2Cory9KW/xX7fb7dy4UbuYDb7vNu7dbHbg/o6TikDgf7TH\nFpc3XmJzar88nh3TNcXDw2JjLKLIcRiRsWU7vsUjL6JxHNBQOj4LRMDIYv2MFK+VQsOYRMSzXOH5\nliMpjXwhXGnHnh26PqMTUpyhLn7gh6Ef84gEPJLM86zQIjG3Qid0eBw/L6XTxYMBJOJ2EHOHiiCw\nJXEdEgjfEZ6MnCmL3KEulLo2syQL3TgmgeuHcRz6jPBY+sQK7OhZKZ0ubkQihrs8EIw7juOF0g5j\nGXISBLEkbEKKN9QlcCzPJ44nuCdsQVkYSmG5MSGeCGQo/GelXHBh1CF25EOPiBMmJXW4DX0sl7rU\nZt7TUtgoXqgrHer7bswD+DWUoUd4GNsOBJHYiiYsYuN4gT1ccCAZhNzhjpTC9iwrdgNPOsSb8DSz\nraEyDHA4hPrcJZbjB54fwD/MdiPLIqEVW8+L6bTxQ44X4aOYRlYYOsyPie+SyHNd4nM+iUwtxm/F\ncOEFhEXAMg5ZFPt+6AhfRD7CUdCIhc+LCTptIoFMIkJaAQBymAg824M0B0YC8Alvg1SG2DiUCIIc\ntl2O95FGTiRCSnzqE2jExfNiLp7igRvLmFoQ5jHP8eLQcj0umCOYxZxJT9lDbAKPxZ50qQxJiCh0\nBYtcYVEH7g69mDrPi+mwoZLEjm1ZlMNNHDkBSYJzF44PPCsKJsSMeEZaVuBRGRDi0JBbUAvIeghs\nK7JD5kw5asQzgR3YsSMEc33phQJeswPGA2I7kOqEU1JGPCPtCAQF8uUSoUIcP2YxpEibhzSM5ARb\nsRHPCEvw0Asih8VxRCUNgXRkIXot+Dy0p5ztDp1EqJB2IDmHYb7v217k2SwEf/E4igN/SsqIrahF\nY9u1CSPUdSyAAZ4LpecxH0QR2vJZKZ1FCBKJPQPuSSpdZBSVsRcwC1CB9cRUwHhDiyLF1iB+12Gc\nxix0KJMe6MsJpBMROcVW/tAiIWLJIwvqICERsdIV4HQ/BGHwyA6mPO0PLSISXMUlqoodWrYQADdE\ncfIpQ8EjwRTL+CMfRdyVAQjBY4yQKLQ9BA53Q8oYd7nPJ6QEQ4uQMBGqfGTbASpRFHmhAxGomL4X\nI7WniDMYVTfmB0T6IQW+6B6QDYEFQzzPRYL5ZIobgqFF1JERCX0HxR60S10UaQuu5sKXaCV8d0JK\nOKI7Cz6SMeHMJYHtC9+2faQhWooIFDgZL+GoEpBIxr6HKsDB5ZakQcikLR24AY+cqQwIhxZ5qLEE\nfCvRMiABPdezbVtyEbk2/oVTukSjbshSvZATA5GYo36oEASBR66lGivreSmdRYwSNwI3oOfwIpdZ\nKmYRbQCbobJMloFoaJEdOnYIkoOjY85s3/Jji/gRdQXyPPanPB0PLYLuzLPQzNgKYerFgfCYpMKK\nYCuzpjwdj5gBQYbGDrXVjSIegJ2IEFYA8mKB6031d42UziIp4FpX+MQOqe0wuIn5nk1D1F5UfjFV\nSeJhPWIEaWNLxZrEERzEZMcuKltI/dhBjwMpv816EwHGm3JWFedNPXDtSblPE9rOW+jdZ+ITExg1\n3uo7b9RI1KzFw/66GRfS2H0kaYJuX+xwawmddhnmwbWhBoDVRhuQSKO9r2bGdjyoH6qLJ5gtKowL\nSoR+0dyLT/VdzHftMshpVn627aS8a0XfXeSpC3MXpsHXr9V0UlZcFJjrloMV6porkxoLmvnwBlMY\nwRjGPzOM5Xd5WSY07Y1/GOnw9+Fvq/mVsJvOzMGj1eAvpY/4lFRLp75fwLlFpuGqAR0Nh3pRM15t\nR8PculNrR0kptr2Bbo1JcYdRdZuXJjsV+K0Opu4FLlJy3tr+rHESxsYvTlV+AA4M0+UZo2jGbzuz\neycFaq4/kA/wJYbnj4CKKIAAnjLtSKp9Pc7fN0rfG+U+P6VcTbOkxrovrZ3Ms9OBisKo9qQyMAh3\ngrUsNQFnCl1DYurtlDplXL8ijPsBEPeGGmmXj/uE7dvdBbRWRxO1PGNxu1iZULJG6V5tqeT0jjH2\nohgckDwmmLnpJRIEXyMi6wDXKmc58EgLQfj5oj72eCt76mnY9XbN2YQWUzVaamlUaFUaQPSJBcsz\nXtbYtGocCQJFgQpEVFolVQLXZQ+984za4439eSb0eUJ9NsJrvQBqnioMnzwfUVo2hw2iEabPcor8\nhJ1ErUqdZ8Q4iLIkD6I+4Lgk3f29jpeCJKUwfjiXlTi8+aTwympHZAapcK8+2SBUUYsyXoWgMqY+\n9TDbCNU/H0m5q1kI9m+NxfHDw64QZX4qmCgXimHU9oecn1JRqlOSHoGOH9c5gazjiIMGtuXqwiQq\n5LaXpOnlZYPYKAXbtFuPEu3CAW2SmEBWFNXSWqtNeiTXEHW306v+6Q5tj/l2jWN2mpi3SkbtIBD7\nWNYAIP3wCYbvXmoJqQ9I8+h6h4Foswmu5fyi8evt/EUD1epVI7uvwlDAz/XKL/NMpgmrAM2mz/59\nz/9Ztp//uL9E/0S8L19vb8pVl8ttDuujzPfZkPDnjGSLSqVUlyLgDHV8p3OkOa5T2XLKMoSyaXyX\nCkRIu/xKnsohlcogIAFbWg1lUpQA4lSqdFhAwrl1vfHyp57yC3Mk7332Plt+eSoKSAOd1wJuilHd\nWqFqXWJZmKR4KN9Zd8/XrCd991WCwEzoSdXRb/Pq6xzs3AsUUpazJtvS4ZvrfkK+G6XznXrlc4Ci\nCT//MKiZ/RCti+dTmfpXV1CVz8i4Qen86ok6qTOTXHjeSHNWdxmaEWsbkqo+9NVdw/9p3axZVx3r\nt3Xz98qmuqd2va6ZNZXfX8rgRKnL6wLX1jdVJ1h1IunFiKZuDGtD+6lBgfJBHUTWHvGY1kHbtqBb\no8dPL29KtNM3peqm5/1cGJ1q14EPuf1yoDAzXgy7vpJ8FNB+iy675vlf8iRbtlWhXVqLKwumxOnW\n91sU6LZbVuzTvo68K6tyWYtdbVQyfPExT1QAHQVRJbBVp+ySbUDR6tKhyCFIoVG2KKX5w2CV6q+V\nX4bvqgsrzUdSZEuF88u/7qo/9Gi4siHn8qkov9EhoT4MWYqPIlN/wJwjlJ3tRXpUrdzbOtp67UQX\nKug3VPyrj2uWCooZWH5tgKpm6tYB6ZwJAIlXkIeqmQXpikdFsQQTalnqt/u0rknZnDVbgo2btuWy\nI1TmbTSbs9kSjCg2CmEt5kDYXnVQPBd1rdnDvVCiesyLD82ma+NYF4ycVqT5qE0xhWaJG5CpYhEg\nwHQjrhdA8iUTm8wpRFOA+gaYq7/SiwiK9VXI9Ej3qkfSUbZW2XT1GpoEHaxVoobFphdKhTi+qn8s\nR+3UMDpbGtalrpzrLUalTKdcww8mfuZHkS2vln1ufI8+/vaxSCqQD3wMfHUHDQ7/sFaf9j0q76kO\ngBUqDUGNLC+Kkw6OVIyEab/3w0M11pXQ61tObK/mk7OpuRoGmGrGWK6GGtcsoq2puWI9f6RzwIkH\nprajnqy7lzDfqTlvM6YAbLDRu7A0L8VydUURZbXRQvvPm2rWkhYUTNUvLW3N/sil6vcBkb5ED/Jx\nPVWxLzX37XOfg+oa+wbdUrOqLRBP9cejz5efa47reaDj6iuJlzXPzwx6+Lauu6zhZDAYDLTPVGr0\nxgGWHw4w1By0he0JDWlmrPZqfKQhTlELNM6rF+oA5W6lw/RRLAod1sJQZfx3Q0VZqnAe1Sql9nUN\nwaJThqHuw7IzS6TlsMHvmbbbNWjtdsYWU55lWqa9+NNd/z9B8Jpc1ahLyzwVyNWJabft41FM6l79\nqkcvxCH/qPlWe6L+GoMealE5KlBv+ju8O2q+J7vsJql+HTYrvWGq3+1cz3d/YEbDz2ea+dEgtpmO\n9v85JJ9Ls07w70q5iuan8q5Nt7vhGK7BtlYIfFilqj8cx3SkqCdPR6ja5S8CoFNfa37BZbCldqAO\n8/kPV23RfN0yyhwk+KALUaFOdBGEaJIuAT1/Qt5i+T3aqXn7hRvzeB4OlPP6qzTX3zYxV4vmpPLY\n1ad2hCkv9PyTfmqoFKGnJK1e1ke/EPmgJsWzYuR+FBfN/KN6rfaouBN7AUT33JfuWv2pViwvXbUW\n0tZCXTQXBV1cnnUnx+rdu+bUWbZF9cmTZ9kVu3oErEv0u7n646bY4N8aXIHxoek064as3chE8T2U\ny9Vd97JZwuKudB7VUDGf15NCXaT7wMADGCGrdmLQXxHatnfNB1HVSavuL/uT9E53DLtdE/UdJI2M\ntaFhedW0RC0Ar8bGHkiFaXALPc1SkILtl/P3Wf8rPu+z5bt//Xb3YvXbXLcnq/4Yo9/ucdETjI1C\nrr9klRpCscBn8+skbRmxVhX/f7fRgk3dei/t1R3GMA3kC/20fojRFY82d0+bv3hsYkI27VGneg+A\nGcxocdxuF7udStjdbtF9sJEqiVBT5/BrR5fD9u939h3eefkSYNWp0itfvdzpljubu6fqouaIi0y1\nqL7+C1AkCcw=\n')
DISTRIBUTE_FROM_EGG_PY = convert('\neJw9j8tqAzEMRfcG/4MgmxQyptkGusonZBmGoGTUGYFfWPKE6dfXTkM3gqt7rh47OKP3NMF3SQFW\nLlrRU1zhybpAxoKBlIqcrNnBdRjQP3GTocYfzmNrrCPQPN9iwzpxSQfQhWBi0cL3qtRtYIG/4Mv0\nKApY5hooqrOGQ05FQTaxptF9Fnx16Rq0XofjaE1XGXVxHIWK7j8P8EY/rHndLqQ1a0pe3COFgHFy\nhLLdWkDbi/DeEpCjNb3u/zccT2Ob8gtnwVyI\n')
DISTRIBUTE_SETUP_PY = convert('\n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\n')
ACTIVATE_SH = convert('\neJytVVFvokAQfudXTLEPtTlLeo9tvMSmJpq02hSvl7u2wRUG2QR2DSxSe7n/frOACEVNLlceRHa+\nnfl25pvZDswCnoDPQ4QoTRQsENIEPci4CsBMZBq7CAsuLOYqvmYKTTj3YxnBgiXBudGBjUzBZUJI\nBXEqgCvweIyuCjeG4eF2F5x14bcB9KQiQQWrjSddI1/oQIx6SYYeoFjzWIoIhYI1izlbhJjkKO7D\nM/QEmKfO9O7WeRo/zr4P7pyHwWxkwitcgwpQ5Ej96OX+PmiFwLeVjFUOrNYKaq1Nud3nR2n8nI2m\nk9H0friPTGVsUdptaxGrTEfpNVFEskxpXtUkkCkl1UNF9cgLBkx48J4EXyALuBtAwNYIjF5kcmUU\nabMKmMq1ULoiRbgsDEkTSsKSGFCJ6Z8vY/2xYiSacmtyAfCDdCNTVZoVF8vSTQOoEwSnOrngBkws\nMYGMBMg8/bMBLSYKS7pYEXP0PqT+ZmBT0Xuy+Pplj5yn4aM9nk72JD8/Wi+Gr98sD9eWSMOwkapD\nBbUv91XSvmyVkICt2tmXR4tWmrcUCsjWOpw87YidEC8i0gdTSOFhouJUNxR+4NYBG0MftoCTD9F7\n2rTtxG3oPwY1b2HncYwhrlmj6Wq924xtGDWqfdNxap+OYxplEurnMVo9RWks+rH8qKEtx7kZT5zJ\n4H7oOFclrN6uFe+d+nW2aIUsSgs/42EIPuOhXq+jEo3S6tX6w2ilNkDnIpHCWdEQhFgwj9pkk7FN\nl/y5eQvRSIQ5+TrL05lewxWpt/Lbhes5cJF3mLET1MGhcKCF+40tNWnUulxrpojwDo2sObdje3Bz\nN3QeHqf3D7OjEXMVV8LN3ZlvuzoWHqiUcNKHtwNd0IbvPGKYYM31nPKCgkUILw3KL+Y8l7aO1ArS\nAd37nIU0fCj5NE5gQCuC5sOSu+UdI2NeXg/lFkQIlFpdWVaWZRfvqGiirC9o6liJ9FXGYrSY9mI1\nD/Ncozgn13vJvsznr7DnkJWXsyMH7e42ljdJ+aqNDF1bFnKWFLdj31xtaJYK6EXFgqmV/ymD/ROG\n+n8O9H8f5vsGOWXsL1+1k3g=\n')
ACTIVATE_FISH = convert('\neJyVVWFv2jAQ/c6vuBoqQVWC9nVSNVGVCaS2VC2rNLWVZZILWAs2s52wVvvxsyEJDrjbmgpK7PP5\n3bt3d22YLbmGlGcIq1wbmCPkGhPYcLMEEsGciwGLDS+YwSjlekngLFVyBe73GXSXxqw/DwbuTS8x\nyyKpFr1WG15lDjETQhpQuQBuIOEKY5O9tlppLqxHKSDByjVAPwEy+mXtCq5MzjIUBTCRgEKTKwFG\ngpBqxTLYXgN2myspVigMaYF92tZSowGZJf4mFExxNs9Qb614CgZtmH0BpEOn11f0cXI/+za8pnfD\n2ZjA1sg9zlV/8QvcMhxbNu0QwgYokn/d+n02nt6Opzcjcnx1vXcIoN74O4ymWQXmHURfJw9jenc/\nvbmb0enj6P5+cuVhqlKm3S0u2XRtRbA2QQAhV7VhBF0rsgUX9Ur1rBUXJgVSy8O751k8mzY5OrKH\nRW3eaQhYGTr8hrXO59ALhxQ83mCsDLAid3T72CCSdJhaFE+fXgicXAARUiR2WeVO37gH3oYHzFKo\n9k7CaPZ1UeNwH1tWuXA4uFKYYcEa8vaKqXl7q1UpygMPhFLvlVKyNzsSM3S2km7UBOl4xweUXk5u\n6e3wZmQ9leY1XE/Ili670tr9g/5POBBpGIJXCCF79L1siarl/dbESa8mD8PL61GpzqpzuMS7tqeB\n1YkALrRBloBMbR9yLcVx7frQAgUqR7NZIuzkEu110gbNit1enNs82Rx5utq7Z3prU78HFRgulqNC\nOTwbqJa9vkJFclQgZSjbKeBgSsUtCtt9D8OwAbIVJuewQdfvQRaoFE9wd1TmCuRG7OgJ1bVXGHc7\nz5WDL/WW36v2oi37CyVBak61+yPBA9C1qqGxzKQqZ0oPuocU9hpud0PIp8sDHkXR1HKkNlzjuUWA\na0enFUyzOWZA4yXGP+ZMI3Tdt2OuqU/SO4q64526cPE0A7ZyW2PMbWZiZ5HamIZ2RcCKLXhcDl2b\nvXL+eccQoRzem80mekPDEiyiWK4GWqZmwxQOmPM0eIfgp1P9cqrBsewR2p/DPMtt+pfcYM+Ls2uh\nhALufTAdmGl8B1H3VPd2af8fQAc4PgqjlIBL9cGQqNpXaAwe3LrtVn8AkZTUxg==\n')
ACTIVATE_CSH = convert('\neJx9VG1P2zAQ/u5fcYQKNgTNPtN1WxlIQ4KCUEGaxuQ6yYVYSuzKdhqVX7+zk3bpy5YPUXL3PPfc\nne98DLNCWshliVDV1kGCUFvMoJGugMjq2qQIiVSxSJ1cCofD1BYRnOVGV0CfZ0N2DD91DalQSjsw\ntQLpIJMGU1euvPe7QeJlkKzgWixlhnAt4aoUVsLnLBiy5NtbJWQ5THX1ZciYKKWwkOFaE04dUm6D\nr/zh7pq/3D7Nnid3/HEy+wFHY/gEJydg0aFaQrBFgz1c5DG1IhTs+UZgsBC2GMFBlaeH+8dZXwcW\nVPvCjXdlAvCfQsE7al0+07XjZvrSCUevR5dnkVeKlFYZmUztG4BdzL2u9KyLVabTU0bdfg7a0hgs\ncSmUg6UwUiQl2iHrcbcVGNvPCiLOe7+cRwG13z9qRGgx2z6DHjfm/Op2yqeT+xvOLzs0PTKHDz2V\ntkckFHoQfQRXoGJAj9el0FyJCmEMhzgMS4sB7KPOE2ExoLcSieYwDvR+cP8cg11gKkVJc2wRcm1g\nQhYFlXiTaTfO2ki0fQoiFM4tLuO4aZrhOzqR4dIPcWx17hphMBY+Srwh7RTyN83XOWkcSPh1Pg/k\nTXX/jbJTbMtUmcxZ+/bbqOsy82suFQg/BhdSOTRhMNBHlUarCpU7JzBhmkKmRejKOQzayQe6MWoa\nn1wqWmuh6LZAaHxcdeqIlVLhIBJdO9/kbl0It2oEXQj+eGjJOuvOIR/YGRqvFhttUB2XTvLXYN2H\n37CBdbW2W7j2r2+VsCn0doVWcFG1/4y1VwBjfwAyoZhD\n')
ACTIVATE_BAT = convert('\neJx9UdEKgjAUfW6wfxjiIH+hEDKUFHSKLCMI7kNOEkIf9P9pTJ3OLJ/03HPPPed4Es9XS9qqwqgT\nPbGKKOdXL4aAFS7A4gvAwgijuiKlqOpGlATS2NeMLE+TjJM9RkQ+SmqAXLrBo1LLIeLdiWlD6jZt\nr7VNubWkndkXaxg5GO3UaOOKS6drO3luDDiO5my3iA0YAKGzPRV1ack8cOdhysI0CYzIPzjSiH5X\n0QcvC8Lfaj0emsVKYF2rhL5L3fCkVjV76kShi59NHwDniAHzkgDgqBcwOgTMx+gDQQqXCw==\n')
DEACTIVATE_BAT = convert('\neJxzSE3OyFfIT0vj4ipOLVEI8wwKCXX0iXf1C7Pl4spMU0hJTcvMS01RiPf3cYmHyQYE+fsGhCho\ncCkAAUibEkTEVhWLMlUlLk6QGixStlyaeCyJDPHw9/Pw93VFsQguim4ZXAJoIUw5DhX47XUM8UCx\nEchHtwsohN1bILUgw61c/Vy4AJYPYm4=\n')
ACTIVATE_PS = convert('\n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\nQastYw==\n')
DISTUTILS_INIT = convert('\neJytV1uL4zYUfvevOE0ottuMW9q3gVDa3aUMXXbLMlDKMBiNrSTqOJKRlMxkf33PkXyRbGe7Dw2E\nUXTu37lpxLFV2oIyifAncxmOL0xLIfcG+gv80x9VW6maw7o/CANSWWBwFtqeWMPlGY6qPjV8A0bB\nC4eKSTgZ5LRgFeyErMEeOBhbN+Ipgeizhjtnhkn7DdyjuNLPoCS0l/ayQTG0djwZC08cLXozeMss\naG5EzQ0IScpnWtHSTXuxByV/QCmxE7y+eS0uxWeoheaVVfqSJHiU7Mhhi6gULbOHorshkrEnKxpT\n0n3A8Y8SMpuwZx6aoix3ouFlmW8gHRSkeSJ2g7hU+kiHLDaQw3bmRDaTGfTnty7gPm0FHbIBg9U9\noh1kZzAFLaue2R6htPCtAda2nGlDSUJ4PZBgCJBGVcwKTAMz/vJiLD+Oin5Z5QlvDPdulC6EsiyE\nNFzb7McNTKJzbJqzphx92VKRFY1idenzmq3K0emRcbWBD0ryqc4NZGmKOOOX9Pz5x+/l27tP797c\nf/z0d+4NruGNai8uAM0bfsYaw8itFk8ny41jsfpyO+BWlpqfhcG4yxLdi/0tQqoT4a8Vby382mt8\np7XSo7aWGdPBc+b6utaBmCQ7rQKQoWtAuthQCiold2KfJIPTT8xwg9blPumc+YDZC/wYGdAyHpJk\nvUbHbHWAp5No6pK/WhhLEWrFjUwtPEv1Agf8YmnsuXUQYkeZoHm8ogP16gt2uHoxcEMdf2C6pmbw\nhUMsWGhanboh4IzzmsIpWs134jVPqD/c74bZHdY69UKKSn/+KfVhxLgUlToemayLMYQOqfEC61bh\ncbhwaqoGUzIyZRFHPmau5juaWqwRn3mpWmoEA5nhzS5gog/5jbcFQqOZvmBasZtwYlG93k5GEiyw\nbuHhMWLjDarEGpMGB2LFs5nIJkhp/nUmZneFaRth++lieJtHepIvKgx6PJqIlD9X2j6pG1i9x3pZ\n5bHuCPFiirGHeO7McvoXkz786GaKVzC9DSpnOxJdc4xm6NSVq7lNEnKdVlnpu9BNYoKX2Iq3wvgh\ngGEUM66kK6j4NiyoneuPLSwaCWDxczgaolEWpiMyDVDb7dNuLAbriL8ig8mmeju31oNvQdpnvEPC\n1vAXbWacGRVrGt/uXN/gU0CDDwgooKRrHfTBb1/s9lYZ8ZqOBU0yLvpuP6+K9hLFsvIjeNhBi0KL\nMlOuWRn3FRwx5oHXjl0YImUx0+gLzjGchrgzca026ETmYJzPD+IpuKzNi8AFn048Thd63OdD86M6\n84zE8yQm0VqXdbbgvub2pKVnS76icBGdeTHHXTKspUmr4NYo/furFLKiMdQzFjHJNcdAnMhltBJK\n0/IKX3DVFqvPJ2dLE7bDBkH0l/PJ29074+F0CsGYOxsb7U3myTUncYfXqnLLfa6sJybX4g+hmcjO\nkMRBfA1JellfRRKJcyRpxdS4rIl6FdmQCWjo/o9Qz7yKffoP4JHjOvABcRn4CZIT2RH4jnxmfpVG\nqgLaAvQBNfuO6X0/Ux02nb4FKx3vgP+XnkX0QW9pLy/NsXgdN24dD3LxO2Nwil7Zlc1dqtP3d7/h\nkzp1/+7hGBuY4pk0XD/0Ao/oTe/XGrfyM773aB7iUhgkpy+dwAMalxMP0DrBcsVw/6p25+/hobP9\nGBknrWExDhLJ1bwt1NcCNblaFbMKCyvmX0PeRaQ=\n')
DISTUTILS_CFG = convert('\neJxNj00KwkAMhfc9xYNuxe4Ft57AjYiUtDO1wXSmNJnK3N5pdSEEAu8nH6lxHVlRhtDHMPATA4uH\nxJ4EFmGbvfJiicSHFRzUSISMY6hq3GLCRLnIvSTnEefN0FIjw5tF0Hkk9Q5dRunBsVoyFi24aaLg\n9FDOlL0FPGluf4QjcInLlxd6f6rqkgPu/5nHLg0cXCscXoozRrP51DRT3j9QNl99AP53T2Q=\n')
ACTIVATE_THIS = convert('\neJyNU01v2zAMvetXEB4K21jmDOstQA4dMGCHbeihlyEIDMWmG62yJEiKE//7kXKdpN2KzYBt8euR\nfKSyLPs8wiEo8wh4wqZTGou4V6Hm0wJa1cSiTkJdr8+GsoTRHuCotBayiWqQEYGtMCgfD1KjGYBe\n5a3p0cRKiAe2NtLADikftnDco0ko/SFEVgEZ8aRC5GLux7i3BpSJ6J1H+i7A2CjiHq9z7JRZuuQq\nsiwTIvpxJYCeuWaBpwZdhB+yxy/eWz+ZvVSU8C4E9FFZkyxFsvCT/ZzL8gcz9aXVE14Yyp2M+2W0\ny7n5mp0qN+avKXvbsyyzUqjeWR8hjGE+2iCE1W1tQ82hsCZN9UzlJr+/e/iab8WfqsmPI6pWeUPd\nFrMsd4H/55poeO9n54COhUs+sZNEzNtg/wanpjpuqHJaxs76HtZryI/K3H7KJ/KDIhqcbJ7kI4ar\nXL+sMgXnX0D+Te2Iy5xdP8yueSlQB/x/ED2BTAtyE3K4SYUN6AMNfbO63f4lBW3bUJPbTL+mjSxS\nPyRfJkZRgj+VbFv+EzHFi5pKwUEepa4JslMnwkowSRCXI+m5XvEOvtuBrxHdhLalG0JofYBok6qj\nYdN2dEngUlbC4PG60M1WEN0piu7Nq7on0mgyyUw3iV1etLo6r/81biWdQ9MWHFaePWZYaq+nmp+t\ns3az+sj7eA0jfgPfeoN1\n')
MH_MAGIC = 4277009102
MH_CIGAM = 3472551422
MH_MAGIC_64 = 4277009103
MH_CIGAM_64 = 3489328638
FAT_MAGIC = 3405691582
BIG_ENDIAN = '>'
LITTLE_ENDIAN = '<'
LC_LOAD_DYLIB = 12
maxint = majver == 3 and getattr(sys, 'maxsize') or getattr(sys, 'maxint')

class fileview(object):
    """
    A proxy for file-like objects that exposes a given view of a file.
    Modified from macholib.
    """

    def __init__(self, fileobj, start=0, size=maxint):
        if isinstance(fileobj, fileview):
            self._fileobj = fileobj._fileobj
        else:
            self._fileobj = fileobj
        self._start = start
        self._end = start + size
        self._pos = 0

    def __repr__(self):
        return '<fileview [%d, %d] %r>' % (
         self._start, self._end, self._fileobj)

    def tell(self):
        return self._pos

    def _checkwindow(self, seekto, op):
        if not self._start <= seekto <= self._end:
            raise IOError('%s to offset %d is outside window [%d, %d]' % (
             op, seekto, self._start, self._end))

    def seek(self, offset, whence=0):
        seekto = offset
        if whence == os.SEEK_SET:
            seekto += self._start
        elif whence == os.SEEK_CUR:
            seekto += self._start + self._pos
        elif whence == os.SEEK_END:
            seekto += self._end
        else:
            raise IOError('Invalid whence argument to seek: %r' % (whence,))
        self._checkwindow(seekto, 'seek')
        self._fileobj.seek(seekto)
        self._pos = seekto - self._start

    def write(self, bytes):
        here = self._start + self._pos
        self._checkwindow(here, 'write')
        self._checkwindow(here + len(bytes), 'write')
        self._fileobj.seek(here, os.SEEK_SET)
        self._fileobj.write(bytes)
        self._pos += len(bytes)

    def read(self, size=maxint):
        assert size >= 0
        here = self._start + self._pos
        self._checkwindow(here, 'read')
        size = min(size, self._end - here)
        self._fileobj.seek(here, os.SEEK_SET)
        bytes = self._fileobj.read(size)
        self._pos += len(bytes)
        return bytes


def read_data(file, endian, num=1):
    """
    Read a given number of 32-bits unsigned integers from the given file
    with the given endianness.
    """
    res = struct.unpack(endian + 'L' * num, file.read(num * 4))
    if len(res) == 1:
        return res[0]
    return res


def mach_o_change(path, what, value):
    """
    Replace a given name (what) in any LC_LOAD_DYLIB command found in
    the given binary with a new name (value), provided it's shorter.
    """

    def do_macho(file, bits, endian):
        cputype, cpusubtype, filetype, ncmds, sizeofcmds, flags = read_data(file, endian, 6)
        if bits == 64:
            read_data(file, endian)
        for n in range(ncmds):
            where = file.tell()
            cmd, cmdsize = read_data(file, endian, 2)
            if cmd == LC_LOAD_DYLIB:
                name_offset = read_data(file, endian)
                file.seek(where + name_offset, os.SEEK_SET)
                load = file.read(cmdsize - name_offset).decode()
                load = load[:load.index('\x00')]
                if load == what:
                    file.seek(where + name_offset, os.SEEK_SET)
                    file.write(value.encode() + ('\x00').encode())
            file.seek(where + cmdsize, os.SEEK_SET)

    def do_file(file, offset=0, size=maxint):
        file = fileview(file, offset, size)
        magic = read_data(file, BIG_ENDIAN)
        if magic == FAT_MAGIC:
            nfat_arch = read_data(file, BIG_ENDIAN)
            for n in range(nfat_arch):
                cputype, cpusubtype, offset, size, align = read_data(file, BIG_ENDIAN, 5)
                do_file(file, offset, size)

        elif magic == MH_MAGIC:
            do_macho(file, 32, BIG_ENDIAN)
        elif magic == MH_CIGAM:
            do_macho(file, 32, LITTLE_ENDIAN)
        elif magic == MH_MAGIC_64:
            do_macho(file, 64, BIG_ENDIAN)
        elif magic == MH_CIGAM_64:
            do_macho(file, 64, LITTLE_ENDIAN)

    assert len(what) >= len(value)
    do_file(open(path, 'r+b'))


if __name__ == '__main__':
    main()