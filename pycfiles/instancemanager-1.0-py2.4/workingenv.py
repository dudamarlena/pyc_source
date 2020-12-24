# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/instancemanager/workingenv.py
# Compiled at: 2007-12-17 05:32:50
import sys, os, re, shutil, optparse, logging, urllib2, urlparse
try:
    import setuptools, pkg_resources
except ImportError:
    setuptools = pkg_resources = None

import distutils.sysconfig
try:
    import subprocess
except ImportError:
    print 'ERROR: You must have the subprocess module available to use'
    print '       workingenv.py'
    raise

__version__ = '0.6.4'

class BadCommand(Exception):
    __module__ = __name__


ez_setup_url = 'http://peak.telecommunity.com/dist/ez_setup.py'
python_version = '%s.%s' % (sys.version_info[0], sys.version_info[1])
help = 'This script builds a \'working environment\', which is a directory set\nup for isolated installation of Python scripts, libraries, and\napplications.\n\nTo activate an installation, you must add the lib/python directory\nto your $PYTHONPATH; after you do that the import path will be\nadjusted, as will be installation locations.  Or use\n"source bin/activate" in a Bash shell.\n\nThis may be reapplied to update or refresh an existing environment;\nit will by default pick up the settings originally used.\n'

class DefaultTrackingParser(optparse.OptionParser):
    """
    Version of OptionParser that returns an options argument that has
    a ``._set_vars`` attribute, that shows which options were
    explicitly set (not just picked up from defaults)
    """
    __module__ = __name__

    def get_default_values(self):
        values = optparse.OptionParser.get_default_values(self)
        values = DefaultTrackingValues(values)
        return values


class DefaultTrackingValues(optparse.Values):
    __module__ = __name__

    def __init__(self, defaults=None):
        self.__dict__['_set_vars'] = []
        self.__dict__['_defaults_done'] = False
        self.__dict__['_values'] = {}
        if isinstance(defaults, optparse.Values):
            defaults = defaults.__dict__
        optparse.Values.__init__(self, defaults)
        self.__dict__['_defaults_done'] = True

    def __setattr__(self, attr, value):
        if self._defaults_done:
            self._set_vars.append(attr)
        self._values[attr] = value

    def __getattr__(self, attr):
        return self._values[attr]


parser = DefaultTrackingParser(version=__version__, usage='%%prog [OPTIONS] NEW_DIRECTORY\n\n%s' % help)
parser.add_option('-v', '--verbose', action='count', dest='verbose', default=0, help='Be verbose (use multiple times for more effect)')
parser.add_option('-q', '--quiet', action='count', dest='quiet', default=0, help='Be more and more quiet')
parser.add_option('-n', '--simulate', action='store_true', dest='simulate', help='Simulate (just pretend to do things)')
parser.add_option('--force', action='store_false', dest='interactive', default=True, help='Overwrite files without asking')
parser.add_option('-f', '--find-links', action='append', dest='find_links', default=[], metavar='URL', help='Extra locations/URLs where packages can be found (sets up your distutils.cfg for future installs)')
parser.add_option('-Z', '--always-unzip', action='store_true', dest='always_unzip', help="Don't install zipfiles, no matter what (sets up your distutils.cfg for future installs)")
parser.add_option('--home', dest='install_as_home', action='store_true', default=False, help='If given, then packages will be installed with the distutils --home option instead of --prefix.  Zope requires this kind of installation')
parser.add_option('--site-packages', action='store_true', dest='include_site_packages', help='Include the global site-packages (not included by default)')
parser.add_option('--no-extra', action='store_false', dest='install_extra', default=True, help="Don't create non-essential directories (like src/)")
parser.add_option('--env', action='append', dest='envs', metavar='VAR:VALUE', default=[], help='Add the environmental variable assignments to the activate script')
parser.add_option('-r', '--requirements', dest='requirements', action='append', metavar='FILE/URL', help='A file or URL listing requirements that should be installed in the new environment (one requirement per line, optionally with -e for editable packages).  This file can also contain lines starting with -Z, -f, and -r')
parser.add_option('--confirm', dest='confirm', action='store_true', help="Confirm that the requirements have been installed, but don't do anything else (don't set up environment, don't install packages)")
parser.add_option('--cross-platform-activate', dest='cross_platform_activate', action='store_true', help="If given, then both Posix shell files and Windows bat activation scripts will be created (otherwise only the current platform's script will be created)")

class Logger(object):
    """
    Logging object for use in command-line script.  Allows ranges of
    levels, to avoid some redundancy of displayed information.
    """
    __module__ = __name__
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
        self.log(self.WARN, msg, *args, **kw)

    def fatal(self, msg, *args, **kw):
        self.log(self.FATAL, msg, *args, **kw)

    def log(self, level, msg, *args, **kw):
        if args:
            if kw:
                raise TypeError('You may give positional or keyword arguments, not both')
        args = args or kw
        rendered = None
        for (consumer_level, consumer) in self.consumers:
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
        assert not self.in_progress, 'Tried to start_progress(%r) while in_progress %r' % (msg, self.in_progress)
        if self.level_matches(self.NOTIFY, self._stdout_level()):
            sys.stdout.write(msg)
            sys.stdout.flush()
            self.in_progress_hanging = True
        else:
            self.in_progress_hanging = False
        self.in_progress = msg

    def end_progress(self, msg='done.'):
        assert self.in_progress, 'Tried to end_progress without start_progress'
        if self.stdout_level_matches(self.NOTIFY):
            if not self.in_progress_hanging:
                sys.stdout.write('...' + self.in_progress + msg + '\n')
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
        for (level, consumer) in self.consumers:
            if consumer is sys.stdout:
                return level

        return self.FATAL

    def level_matches(self, level, consumer_level):
        """
        >>> l = Logger()
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
            if stop is not None or stop <= consumer_level:
                return False
            return True
        else:
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


class Writer(object):
    """
    File-writing class.  This writes all its files to a
    subdirectory, and respects simulate and interactive
    options.
    """
    __module__ = __name__

    def __init__(self, base_dir, logger, simulate, interactive, python_dir=None):
        self.base_dir = os.path.abspath(base_dir)
        self.simulate = simulate
        self.interactive = interactive
        self.logger = logger
        if python_dir is None:
            python_dir = os.path.join('lib', 'python%s' % python_version)
        self.python_dir = python_dir
        return

    def ensure_dir(self, dir):
        dir = dir.replace('__PYDIR__', self.python_dir)
        if os.path.exists(self.path(dir)):
            self.logger.debug('Directory %s exists', dir)
            return
        self.logger.info('Creating %s', dir)
        if not self.simulate:
            os.makedirs(self.path(dir))

    def ensure_file(self, filename, content, force=False, binary=False):
        """
        Make sure a file exists, with the given content.  If --force
        was given, this will overwrite the file unconditionally;
        otherwise the user is queried (unless ``force=True`` is given
        to override this).  If --simulate was given, this will never
        write the file.
        """
        content = content.replace('__PYDIR__', self.python_dir)
        filename = filename.replace('__PYDIR__', self.python_dir)
        path = self.path(filename)
        if os.path.exists(path):
            c = self.read_file(path, binary=binary)
            if c == content:
                self.logger.debug('File %s already exists (same content)', filename)
                return
            elif self.interactive:
                if self.simulate:
                    self.logger.warn('Would overwrite %s (if confirmed)', filename)
                else:

                    def show_diff():
                        self.show_diff(filename, content, c)

                    if not force:
                        response = self.get_response('Overwrite file %s?' % filename, other_ops=[('d', show_diff)])
                        if not response:
                            return
            else:
                self.logger.warn('Overwriting file %s', filename)
        else:
            self.logger.info('Creating file %s', filename)
        if not self.simulate:
            if binary:
                mode = 'wb'
            else:
                mode = 'w'
            f = open(path, mode)
            f.write(content)
            f.close()

    def show_diff(self, filename, content1, content2):
        from difflib import unified_diff
        u_diff = list(unified_diff(content2.splitlines(), content1.splitlines(), filename))
        print ('\n').join(u_diff)

    def path(self, path):
        return os.path.join(self.base_dir, path)

    def read_file(self, path, binary=False):
        if binary:
            mode = 'rb'
        else:
            mode = 'r'
        f = open(path, mode)
        try:
            c = f.read()
        finally:
            f.close()
        return c

    def add_pythonpath(self):
        """
        Add the working Python path to $PYTHONPATH
        """
        writer_path = os.path.normpath(os.path.abspath(self.path(self.python_dir)))
        cur_path = os.environ.get('PYTHONPATH', None)
        if cur_path is None:
            cur_path = []
        else:
            cur_path = cur_path.split(os.pathsep)
        cur_path = [ os.path.normpath(os.path.abspath(p)) for p in cur_path ]
        if writer_path in cur_path:
            return
        cur_path.insert(0, writer_path)
        os.environ['PYTHONPATH'] = os.pathsep.join(cur_path)
        return

    def get_response(self, msg, default=None, other_ops=()):
        """
        Ask the user about something.  An empty response will return
        default (default=None means an empty response will ask again)
        
        If you give other_ops, it should be a list of [('k', func)], where
        if the user enters 'k' then func will be run (and it will not be
        treated as an answer)
        """
        if default is None:
            prompt = '[y/n'
        elif default:
            prompt = '[Y/n'
        else:
            prompt = '[y/N'
        ops_by_key = {}
        for (key, func) in other_ops:
            prompt += '/' + key
            ops_by_key[key] = func

        prompt += '] '
        while 1:
            response = raw_input(msg + ' ' + prompt).strip().lower()
            if not response:
                if default is None:
                    print 'Please enter Y or N'
                    continue
                return default
            if response[0] in ('y', 'n'):
                return response[0] == 'y'
            if response[0] in ops_by_key:
                ops_by_key[response[0]]()
                continue
            print 'Y or N please'

        return

    def ensure_symlink(self, src, dest):
        src = self.path(src)
        dest = self.path(dest)
        if os.path.exists(dest):
            actual_src = os.path.realpath(dest)
            if os.path.abspath(actual_src) == os.path.abspath(dest):
                self.logger.warn('%s should be a symlink to %s, but is an actual file/directory (leaving as-is)' % (dest, src))
            elif os.path.abspath(actual_src) != os.path.abspath(src):
                self.logger.warn('%s should be symlinked to %s, but is actually symlinked to %s (leaving as-is)' % (dest, src, actual_src))
            else:
                self.logger.debug('%s already symlinked to %s' % (dest, src))
            return
        self.logger.info('Symlinking %s to %s' % (dest, src))
        if not self.simulate:
            os.symlink(src, dest)


basic_layout = [
 '__PYDIR__', '__PYDIR__/distutils', '__PYDIR__/setuptools', 'bin', '.workingenv']
extra_layout = [
 'src']
files_to_write = {}

def call_subprocess(cmd, writer, show_stdout=True, filter_stdout=None, in_workingenv=False, cwd=None, raise_on_returncode=True):
    cmd_parts = []
    for part in cmd:
        if ' ' in part or '\n' in part or '"' in part or "'" in part:
            part = '"%s"' % part.replace('"', '\\"')
        cmd_parts.append(part)

    cmd_desc = (' ').join(cmd_parts)
    if in_workingenv:
        env = os.environ.copy()
        env['PYTHONPATH'] = writer.path(writer.python_dir)
    else:
        env = None
    if show_stdout:
        stdout = None
    else:
        stdout = subprocess.PIPE
    writer.logger.debug('Running command %s' % cmd_desc)
    try:
        proc = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdin=None, stdout=stdout, cwd=cwd, env=env)
    except Exception, e:
        writer.logger.fatal('Error %s while executing command %s' % (e, cmd_desc))
        raise

    if stdout is not None:
        stdout = proc.stdout
        while 1:
            line = stdout.readline()
            if not line:
                break
            line = line.rstrip()
            if filter_stdout:
                level = filter_stdout(line)
                if isinstance(level, tuple):
                    (level, line) = level
                writer.logger.log(level, line)
                if not writer.logger.stdout_level_matches(level):
                    writer.logger.show_progress()
            else:
                writer.logger.info(line)

    else:
        proc.communicate()
    if proc.returncode:
        if raise_on_returncode:
            raise OSError('Command %s failed with error code %s' % (cmd_desc, proc.returncode))
        else:
            writer.logger.warn('Command %s had error code %s' % (cmd_desc, proc.returncode))
    return


def make_working_environment(writer, logger, find_links, always_unzip, include_site_packages, install_extra, force_install_setuptools=True, cross_platform_activate=False, install_as_home=False, envs=()):
    settings = Settings(find_links=find_links, always_unzip=always_unzip, include_site_packages=include_site_packages, install_extra=install_extra, cross_platform_activate=cross_platform_activate, install_as_home=install_as_home, envs=envs)
    make_environment(writer, logger, settings)


def make_environment(writer, logger, settings):
    """
    Create a working environment.  ``writer`` is a ``Writer``
    instance, ``logger`` a ``Logger`` instance.

    ``find_links`` and ``always_unzip`` are used to create
    ``distutils.cfg``, which controls later installations.

    ``include_site_packages``, if true, will cause the environment
    to pick up system-wide packages (besides the standard library).

    ``install_extra``, if true, puts in some directories like
    ``src/``

    ``force_install_setuptools`` will install setuptools even if it is
    already installed elsewhere on the system.  (If it isn't found, it
    will always be installed)

    ``install_as_home`` will install so that distutils will install
    packages like ``--home=WORKINGENV`` was given, not
    ``--prefix=WORKINGENV``

    ``envs`` is a list of ``(var, value)`` of environmental variables
    that should be set when activating this environment.
    """
    if os.path.exists(writer.base_dir):
        logger.notify('Updating working environment in %s' % writer.base_dir)
    else:
        logger.notify('Making working environment in %s' % writer.base_dir)
    layout = basic_layout[:]
    if settings.install_extra:
        layout.extend(extra_layout)
    for dir in layout:
        writer.ensure_dir(dir)

    to_write = files_to_write.copy()
    if not settings.cross_platform_activate:
        if sys.platform == 'win32':
            del to_write['bin/activate']
        else:
            del to_write['bin/activate.bat']
            del to_write['bin/deactivate.bat']
    cfg = distutils_cfg
    if settings.install_as_home:
        prefix_option = 'home = __WORKING__'
    else:
        prefix_option = 'prefix = __WORKING__'
    cfg = cfg.replace('__PREFIX__', prefix_option)
    if settings.find_links:
        first = True
        for find_link in settings.find_links:
            if first:
                find_link = 'find_links = %s' % find_link
                first = False
            else:
                find_link = '             %s' % find_link
            cfg += find_link + '\n'

    if settings.always_unzip:
        cfg += 'zip_ok = false\n'
    to_write[writer.python_dir + '/distutils/distutils.cfg'] = cfg
    install_setuptools(writer, logger)
    add_setuptools_to_path(writer, logger)
    vars = dict(env_name=os.path.basename(writer.base_dir), working_env=os.path.abspath(writer.base_dir), python_version=python_version)
    vars.update(env_assignments(settings.envs))
    for (path, content) in to_write.items():
        content = content % vars
        writer.ensure_file(path, content)

    writer.ensure_file(writer.python_dir + '/site.py', site_py(settings.include_site_packages))
    fix_lib64(writer, logger)
    fix_cli_exe(writer, logger)
    settings.write(writer)


def install_setuptools(writer, logger):
    """
    Install setuptools into a new working environment
    """
    for fn in os.listdir(writer.path(writer.python_dir)):
        if fn.startswith('setuptools-'):
            logger.notify('Setuptools already installed; not updating (remove %s to force installation)' % os.path.join(writer.python_dir, fn))
            return

    if writer.simulate:
        logger.notify('Would have installed local setuptools')
        return
    logger.start_progress('Installing local setuptools...')
    logger.indent += 2
    f_in = urllib2.urlopen(ez_setup_url)
    tmp_dir = os.path.join(writer.path('tmp'))
    tmp_exists = os.path.exists(tmp_dir)
    if not tmp_exists:
        os.mkdir(tmp_dir)
    ez_setup_path = writer.path('tmp/ez_setup.py')
    f_out = open(ez_setup_path, 'w')
    shutil.copyfileobj(f_in, f_out)
    f_in.close()
    f_out.close()
    writer.add_pythonpath()
    site_py = writer.path(os.path.join(writer.python_dir, 'site.py'))
    if os.path.exists(site_py):
        os.unlink(site_py)
    call_subprocess([sys.executable, ez_setup_path, '--always-unzip', '--install-dir', writer.path(writer.python_dir), '--script-dir', writer.path('bin'), '--always-copy', '--upgrade', 'setuptools'], writer, show_stdout=False, filter_stdout=filter_ez_setup)
    os.unlink(ez_setup_path)
    if not tmp_exists:
        os.rmdir(tmp_dir)
    if os.path.exists(site_py):
        os.unlink(site_py)
    easy_install_dir = writer.path('bin')
    for fn in os.listdir(easy_install_dir):
        if fn.startswith('easy_install'):
            fix_easy_install_script(os.path.join(easy_install_dir, fn), logger)

    fix_easy_install_pth(writer, logger)
    logger.indent -= 2
    logger.end_progress()


def filter_ez_setup(line):
    if not line.strip():
        return Logger.DEBUG
    for prefix in ['Reading ', 'Best match', 'Processing setuptools', 'Copying setuptools', 'Adding setuptools', 'Installing ', 'Installed ']:
        if line.startswith(prefix):
            return Logger.DEBUG

    return Logger.INFO


def add_setuptools_to_path(writer, logger):
    setuptools_pth_file = os.path.join(writer.path(writer.python_dir), 'setuptools.pth')
    f = open(setuptools_pth_file)
    setuptools_pth = os.path.join(writer.path(writer.python_dir), f.read().strip())
    f.close()
    sys.path.append(setuptools_pth)


def fix_easy_install_script(filename, logger):
    """
    The easy_install script needs to import setuptools before doing
    the requirement which forces setuptools to be used directly.
    Without importing setuptools, the monkeypatch to keep setuptools
    to stop complaining about site.py won't be installed.
    """
    f = open(filename, 'rb')
    c = f.read()
    f.close()
    if not c.startswith('#!'):
        if not filename.endswith('.exe'):
            logger.warn('Cannot fix import path in script %s' % filename)
        return
    lines = c.splitlines(True)
    if not lines[0].rstrip().endswith('-S'):
        logger.debug('Fixing up path in easy_install because of global setuptools installation')
        lines[0] = lines[0].rstrip() + ' -S\n'
        lines[1:1] = ['import os, sys\n', 'join, dirname, abspath = os.path.join, os.path.dirname, os.path.abspath\n', "site_dirs = [join(dirname(dirname(abspath(__file__))), 'lib', 'python%s.%s' % tuple(sys.version_info[:2])), join(dirname(dirname(abspath(__file__))), 'lib', 'python')]\n", 'sys.path[0:0] = site_dirs\n', 'import site\n', '[site.addsitedir(d) for d in site_dirs]\n']
    for (i, line) in enumerate(lines):
        if line.startswith('from pkg_resources'):
            lines[i:i] = [
             'import setuptools\n']
            break
    else:
        logger.warn('Could not find line "import sys" in %s' % filename)
        return

    logger.info('Fixing easy_install script %s' % filename)
    f = open(filename, 'wb')
    f.write(('').join(lines))
    f.close()


def fix_easy_install_pth(writer, logger):
    """
    easy-install.pth starts with an explicit reference to the
    installed setuptools, which shouldn't be first on the path.
    Because it is already in setuptools.pth, we can simply comment out
    the line in easy-install.pth
    """
    easy_install_pth = os.path.join(writer.python_dir, 'easy-install.pth')
    f = open(writer.path(easy_install_pth))
    lines = f.readlines(True)
    f.close()
    new_lines = []
    for line in lines:
        if not line.startswith('#') and os.path.basename(line).startswith('setuptools-'):
            logger.debug('Commenting out line %r in %s' % (line, easy_install_pth))
            line = '#' + line
        new_lines.append(line)

    new_content = ('').join(new_lines)
    writer.ensure_file(easy_install_pth, new_content, force=True)


def fix_lib64(writer, logger):
    """
    Some platforms (particularly Gentoo on x64) put things in lib64/pythonX.Y
    instead of lib/pythonX.Y.  If this is such a platform we'll just create a
    symlink so lib64 points to lib
    """
    if distutils.sysconfig.get_python_lib(prefix='').startswith('lib64'):
        logger.debug('This system uses lib64; symlinking lib64 to lib')
        writer.ensure_symlink('lib', 'lib64')


def fix_cli_exe(writer, logger):
    """
    Setuptools has the files cli.exe and gui.exe in its egg, but our
    setuptools monkeypatch will keep it from finding these files.  We'll
    simply copy these files to fix that.
    """
    if writer.simulate:
        logger.debug('Would have tried to copy over cli.exe and gui.exe')
        return
    python_path = writer.path(writer.python_dir)
    setuptools_egg = None
    for filename in os.listdir(python_path):
        if filename.lower().startswith('setuptools') and filename.lower().endswith('.egg'):
            setuptools_egg = filename
            break

    if not setuptools_egg:
        logger.error('No setuptools egg found in %r' % python_path)
        return
    for base in ['cli.exe', 'gui.exe']:
        filename = os.path.join(python_path, setuptools_egg, 'setuptools', base)
        if not os.path.exists(filename):
            if sys.platform == 'win32':
                logger.error('No %r file found in the setuptools egg (%r)' % (base, filename))
            continue
        f = open(filename, 'rb')
        c = f.read()
        f.close()
        new_filename = os.path.join(python_path, 'setuptools', base)
        writer.ensure_file(new_filename, c, binary=True)

    return


def read_requirements(logger, requirements):
    """
    Read all the lines from the requirement files, including recursive
    reads.
    """
    lines = []
    req_re = re.compile('^(?:-r|--requirements)\\s+')
    for fn in requirements:
        logger.info('Reading requirement %s' % fn)
        for line in get_lines(fn):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            match = req_re.search(line)
            if match:
                sub_fn = line[match.end():]
                sub_fn = join_filename(fn, sub_fn)
                lines.extend(read_requirements(logger, [sub_fn]))
                continue
            lines.append((line, fn))

    return lines


def join_filename(base, sub, only_req_uri=False):
    if only_req_uri and '#' not in sub:
        return sub
    if re.search('^https?://', base) or re.search('^https?://', sub):
        return urlparse.urljoin(base, sub)
    else:
        base = os.path.dirname(os.path.abspath(base))
        return os.path.join(base, sub)


def parse_requirements(logger, requirement_lines, settings):
    """
    Parse all the lines of requirements.  Can override options.
    Returns a list of requirements to be installed.
    """
    options_re = re.compile('^--?([a-zA-Z0-9_-]*)\\s+')
    plan = []
    for (line, uri) in requirement_lines:
        match = options_re.search(line)
        if match:
            option = match.group(1)
            value = line[match.end():]
            if option in ('f', 'find-links'):
                value = join_filename(uri, value)
                if value not in settings.find_links:
                    settings.find_links.append(value)
            elif option in ('Z', 'always-unzip'):
                settings.always_unzip = True
            elif option in ('e', 'editable'):
                plan.append(('--editable', join_filename(uri, value, only_req_uri=True)))
            else:
                logger.error('Bad option override in requirement: %s' % line)
            continue
        plan.append(join_filename(uri, line, only_req_uri=True))

    return plan


def install_requirements(writer, logger, plan):
    """
    Install all the requirements found in the list of filenames
    """
    writer.add_pythonpath()
    import pkg_resources
    immediate = []
    editable = []
    for req in plan:
        if req[0] == '--editable':
            editable.append(req[1])
        else:
            immediate.append(req)

    if immediate:
        args = (', ').join([ '"%s"' % req.replace('"', '').replace("'", '') for req in immediate ])
        logger.start_progress('Installing %s ...' % (', ').join(immediate))
        logger.indent += 2
        os.chdir(writer.path('.'))
        if not writer.simulate:
            call_subprocess([sys.executable, '-c', 'import setuptools.command.easy_install; setuptools.command.easy_install.main(["-q", %s])' % args], writer, in_workingenv=True, show_stdout=False, filter_stdout=make_filter_easy_install())
        logger.indent -= 2
        logger.end_progress()
    for req in editable:
        logger.debug('Changing to directory %s' % writer.path('src'))
        os.chdir(writer.path('src'))
        req = req.replace('"', '').replace("'", '')
        dist_req = pkg_resources.Requirement.parse(req)
        dir = writer.path(os.path.join('src', dist_req.project_name.lower()))
        dir_exists = os.path.exists(dir)
        if dir_exists:
            logger.info('Package %s already installed in editable form' % req)
        else:
            logger.start_progress('Installing editable %s to %s...' % (req, dir))
            logger.indent += 2
            cmd = [sys.executable, '-c', 'import setuptools.command.easy_install; setuptools.command.easy_install.main(["-q", "-b", ".", "-e", "%s"])' % req]
            call_subprocess(cmd, writer, in_workingenv=True, show_stdout=False, filter_stdout=make_filter_easy_install())
        os.chdir(dir)
        call_subprocess([sys.executable, '-c', 'import setuptools; execfile("setup.py")', 'develop'], writer, in_workingenv=True, show_stdout=False, filter_stdout=make_filter_develop())
        if not dir_exists:
            logger.indent -= 2
            logger.end_progress()


def make_filter_easy_install():
    context = []

    def filter_easy_install(line):
        adjust = 0
        level = Logger.NOTIFY
        prefix = 'Processing dependencies for '
        if line.startswith(prefix):
            requirement = line[len(prefix):].strip()
            context.append(requirement)
            adjust = -2
        prefix = 'Finished installing '
        if line.startswith(prefix):
            requirement = line[len(prefix):].strip()
            if not context or context[(-1)] != requirement:
                if len(context) != 1 or requirement != 'None':
                    print 'Error: Got unexpected "%s%s"' % (prefix, requirement)
                    print '       Context: %s' % context
            context.pop()
        if not line.strip():
            level = Logger.DEBUG
        for regex in ['references __(file|path)__$', '^zip_safe flag not set; analyzing', 'MAY be using inspect.[a-zA-Z0-9_]+$', '^Extracting .*to', '^creating .*\\.egg$']:
            if re.search(regex, line.strip()):
                level = Logger.DEBUG

        indent = len(context) * 2 + adjust
        return (level, ' ' * indent + line)

    return filter_easy_install


def make_filter_develop():
    easy_filter = make_filter_easy_install()

    def filter_develop(line):
        for regex in ['^writing.*egg-info']:
            if re.search(regex, line.strip()):
                return Logger.DEBUG

        return easy_filter(line)

    return filter_develop


def check_requirements(writer, logger, plan):
    """
    Check all the requirements found in the list of filenames
    """
    writer.add_pythonpath()
    import pkg_resources
    for req in plan:
        if '#egg=' in req:
            req = req.split('#egg=')[(-1)]
        try:
            dist = pkg_resources.get_distribution(req)
            logger.notify('Found: %s' % dist)
            logger.info('  in location: %s' % dist.location)
        except pkg_resources.DistributionNotFound:
            logger.warn('Not Found: %s' % req)
        except ValueError, e:
            logger.warn('Cannot confirm %s' % req)


def get_lines(fn_or_url):
    scheme = urlparse.urlparse(fn_or_url)[0]
    if not scheme:
        f = open(fn_or_url)
    else:
        f = urllib2.urlopen(fn_or_url)
    try:
        return f.readlines()
    finally:
        f.close()


def env_assignments(envs):
    """
    Return the shell code to assign an unassign variables, as a
    dictionary of variable substitutions
    """
    vars = {'unix_set_env': [], 'unix_unset_env': [], 'windows_set_env': [], 'windows_unset_env': []}
    for (name, value) in envs:
        vars['unix_set_env'].append('%s="%s"' % (name, value.replace('"', '\\"')))
        vars['unix_set_env'].append('export %s' % name)
        vars['unix_unset_env'].append('unset %s' % name)
        vars['windows_set_env'].append('set %s=%s' % (name, value))
        vars['windows_unset_env'].append('set %s=' % name)

    for (name, value) in vars.items():
        vars[name] = ('\n').join(value)

    return vars


class Settings(object):
    """
    Object to store all the settings for the working environment (this
    does not store transient options like verbosity).
    """
    __module__ = __name__

    def __init__(self, find_links=None, envs=None, always_unzip=True, include_site_packages=False, install_extra=True, cross_platform_activate=False, install_as_home=False, requirements=None):
        self.find_links = find_links or []
        self.envs = envs or []
        self.always_unzip = always_unzip
        self.include_site_packages = include_site_packages
        self.install_extra = install_extra
        self.cross_platform_activate = cross_platform_activate
        self.install_as_home = install_as_home
        self.requirements = requirements or []

    def write(self, writer):
        writer.ensure_file('.workingenv/find_links.txt', ('\n').join(self.find_links), force=True)
        writer.ensure_file('.workingenv/envs.txt', ('\n').join(self.envs), force=True)
        writer.ensure_file('.workingenv/requirements.txt', ('\n').join(self.requirements), force=True)
        settings = []
        settings.append(self.make_setting_line('always_unzip', self.always_unzip))
        settings.append(self.make_setting_line('include_site_packages', self.include_site_packages))
        settings.append(self.make_setting_line('install_extra', self.install_extra))
        settings.append(self.make_setting_line('cross_platform_activate', self.cross_platform_activate))
        settings.append(self.make_setting_line('install_as_home', self.install_as_home))
        writer.ensure_file('.workingenv/settings.txt', ('\n').join(settings) + '\n', force=True)

    def make_setting_line(name, value):
        if value:
            value = 'True'
        else:
            value = 'False'
        return '%s = %s' % (name, value)

    make_setting_line = staticmethod(make_setting_line)

    def read(cls, base_dir):
        dir = os.path.join(base_dir, '.workingenv')
        find_links = cls.read_lines(os.path.join(dir, 'find_links.txt'))
        find_links = cls.unique_lines(find_links)
        envs = cls.read_lines(os.path.join(dir, 'envs.txt'))
        requirements = cls.read_lines(os.path.join(dir, 'requirements.txt'))
        args = dict(always_unzip=False, include_site_packages=False, install_extra=True, cross_platform_activate=False, install_as_home=False)
        for line in cls.read_lines(os.path.join(dir, 'settings.txt')):
            if '=' not in line:
                raise ValueError('Badly formatted line: %r' % line)
            (name, value) = line.split('=', 1)
            name = name.strip()
            value = cls.make_bool(value.strip())
            args[name] = value

        return cls(find_links=find_links, envs=envs, requirements=requirements, **args)

    read = classmethod(read)

    def read_lines(filename):
        if not os.path.exists(filename):
            return []
        f = open(filename)
        result = []
        for line in f:
            if not line.strip() or line.strip().startswith('#'):
                continue
            result.append(line.strip())

        f.close()
        return result

    read_lines = staticmethod(read_lines)

    def unique_lines(lines):
        result = []
        for line in lines:
            if line not in result:
                result.append(line)

        return result

    unique_lines = staticmethod(unique_lines)

    def make_bool(value):
        value = value.strip().lower()
        if value in ('1', 'true', 't', 'yes', 'y', 'on'):
            return True
        elif value in ('0', 'false', 'f', 'no', 'n', 'off'):
            return False
        raise ValueError('Cannot convert to boolean: %r' % value)

    make_bool = staticmethod(make_bool)


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    (options, args) = parser.parse_args(args)
    if not args or len(args) > 1:
        raise BadCommand('You must provide a single output directory')
    output_dir = args[0]
    level = 1
    level += options.verbose
    level -= options.quiet
    if options.simulate and not options.verbose:
        level += 1
    level = Logger.level_for_integer(3 - level)
    logger = Logger([(level, sys.stdout)])
    if options.install_as_home:
        python_dir = os.path.join('lib', 'python')
    else:
        python_dir = os.path.join('lib', 'python%s' % python_version)
    writer = Writer(output_dir, logger, simulate=options.simulate, interactive=options.interactive, python_dir=python_dir)
    envs = []
    for assignment in options.envs:
        if ':' not in assignment:
            raise BadCommand('--env=%s should be --env=VAR:VALUE' % assignment)
        (var, value) = assignment.split(':', 1)
        envs.append((var, value))

    if os.path.exists(os.path.join(output_dir, '.workingenv')):
        logger.info('Reading settings from environment')
        settings = Settings.read(output_dir)
    else:
        settings = Settings()
    for var in options._set_vars:
        setattr(settings, var, getattr(options, var))

    requirements = settings.requirements
    requirement_lines = read_requirements(logger, requirements)
    plan = parse_requirements(logger, requirement_lines, settings)
    if not options.confirm:
        make_environment(writer, logger, settings)
    if options.confirm:
        check_requirements(writer, logger, plan)
        return
    if plan:
        install_requirements(writer, logger, plan)
    return


def site_py(include_site_packages):
    s = '# Duplicating setuptools\' site.py...\ndef __boot():\n    PYTHONPATH = os.environ.get(\'PYTHONPATH\')\n    if PYTHONPATH is None or (sys.platform==\'win32\' and not PYTHONPATH):\n        PYTHONPATH = []\n    else:\n        PYTHONPATH = PYTHONPATH.split(os.pathsep)\n    pic = getattr(sys,\'path_importer_cache\',{})\n    stdpath = sys.path[len(PYTHONPATH):]\n    mydir = os.path.dirname(__file__)\n    known_paths = dict([(makepath(item)[1],1) for item in sys.path]) # 2.2 comp\n\n    oldpos = getattr(sys,\'__egginsert\',0)   # save old insertion position\n    sys.__egginsert = 0                     # and reset the current one\n\n    for item in PYTHONPATH:\n        addsitedir(item)\n        item_site_packages = os.path.join(item, \'site-packages\')\n        if os.path.exists(item_site_packages):\n            addsitedir(item_site_packages)\n\n    sys.__egginsert += oldpos           # restore effective old position\n\n    d,nd = makepath(stdpath[0])\n    insert_at = None\n    new_path = []\n\n    for item in sys.path:\n        p,np = makepath(item)\n\n        if np==nd and insert_at is None:\n            # We\'ve hit the first \'system\' path entry, so added entries go here\n            insert_at = len(new_path)\n\n        if np in known_paths or insert_at is None:\n            new_path.append(item)\n        else:\n            # new path after the insert point, back-insert it\n            new_path.insert(insert_at, item)\n            insert_at += 1\n\n    sys.path[:] = new_path\n    \nimport sys\nimport os\nimport __builtin__\n\ndef makepath(*paths):\n    dir = os.path.abspath(os.path.join(*paths))\n    return dir, os.path.normcase(dir)\n\ndef abs__file__():\n    """Set all module\' __file__ attribute to an absolute path"""\n    for m in sys.modules.values():\n        try:\n            m.__file__ = os.path.abspath(m.__file__)\n        except AttributeError:\n            continue\n\ntry:\n    set\nexcept NameError:\n    class set:\n        def __init__(self, args=()):\n            self.d = {}\n            for v in args:\n                self.d[v] = None\n        def __contains__(self, key):\n            return key in self.d\n        def add(self, key):\n            self.d[key] = None\n\ndef removeduppaths():\n    """ Remove duplicate entries from sys.path along with making them\n    absolute"""\n    # This ensures that the initial path provided by the interpreter contains\n    # only absolute pathnames, even if we\'re running from the build directory.\n    L = []\n    known_paths = set()\n    for dir in sys.path:\n        # Filter out duplicate paths (on case-insensitive file systems also\n        # if they only differ in case); turn relative paths into absolute\n        # paths.\n        dir, dircase = makepath(dir)\n        if not dircase in known_paths:\n            L.append(dir)\n            known_paths.add(dircase)\n    sys.path[:] = L\n    return known_paths\n\ndef _init_pathinfo():\n    """Return a set containing all existing directory entries from sys.path"""\n    d = set()\n    for dir in sys.path:\n        try:\n            if os.path.isdir(dir):\n                dir, dircase = makepath(dir)\n                d.add(dircase)\n        except TypeError:\n            continue\n    return d\n\ndef addpackage(sitedir, name, known_paths, exclude_packages=()):\n    """Add a new path to known_paths by combining sitedir and \'name\' or execute\n    sitedir if it starts with \'import\'"""\n    import fnmatch\n    if known_paths is None:\n        _init_pathinfo()\n        reset = 1\n    else:\n        reset = 0\n    fullname = os.path.join(sitedir, name)\n    try:\n        f = open(fullname, "rU")\n    except IOError:\n        return\n    try:\n        for line in f:\n            if line.startswith("#"):\n                continue\n            found_exclude = False\n            for exclude in exclude_packages:\n                if exclude(line):\n                    found_exclude = True\n                    break\n            if found_exclude:\n                continue\n            if line.startswith("import"):\n                exec line\n                continue\n            line = line.rstrip()\n            dir, dircase = makepath(sitedir, line)\n            if not dircase in known_paths and os.path.exists(dir):\n                sys.path.append(dir)\n                known_paths.add(dircase)\n    finally:\n        f.close()\n    if reset:\n        known_paths = None\n    return known_paths\n\ndef addsitedir(sitedir, known_paths=None, exclude_packages=()):\n    """Add \'sitedir\' argument to sys.path if missing and handle .pth files in\n    \'sitedir\'"""\n    if known_paths is None:\n        known_paths = _init_pathinfo()\n        reset = 1\n    else:\n        reset = 0\n    sitedir, sitedircase = makepath(sitedir)\n    if not sitedircase in known_paths:\n        sys.path.append(sitedir)        # Add path component\n    try:\n        names = os.listdir(sitedir)\n    except os.error:\n        return\n    names.sort()\n    for name in names:\n        if name.endswith(os.extsep + "pth"):\n            addpackage(sitedir, name, known_paths,\n                       exclude_packages=exclude_packages)\n    if reset:\n        known_paths = None\n    return known_paths\n\ndef addsitepackages(known_paths):\n    """Add site-packages (and possibly site-python) to sys.path"""\n    prefixes = [os.path.join(sys.prefix, "local"), sys.prefix]\n    if sys.exec_prefix != sys.prefix:\n        prefixes.append(os.path.join(sys.exec_prefix, "local"))\n    for prefix in prefixes:\n        if prefix:\n            if sys.platform in (\'os2emx\', \'riscos\'):\n                sitedirs = [os.path.join(prefix, "Lib", "site-packages")]\n            elif os.sep == \'/\':\n                sitedirs = [os.path.join(prefix,\n                                         "lib",\n                                         "python" + sys.version[:3],\n                                         "site-packages"),\n                            os.path.join(prefix, "lib", "site-python")]\n                try:\n                    # sys.getobjects only available in --with-pydebug build\n                    sys.getobjects\n                    sitedirs.insert(0, os.path.join(sitedirs[0], \'debug\'))\n                except AttributeError:\n                    pass\n            else:\n                sitedirs = [prefix, os.path.join(prefix, "lib", "site-packages")]\n            if sys.platform == \'darwin\':\n                sitedirs.append( os.path.join(\'/opt/local\', \'lib\', \'python\' + sys.version[:3], \'site-packages\') )\n                # for framework builds *only* we add the standard Apple\n                # locations. Currently only per-user, but /Library and\n                # /Network/Library could be added too\n                if \'Python.framework\' in prefix:\n                    home = os.environ.get(\'HOME\')\n                    if home:\n                        sitedirs.append(\n                            os.path.join(home,\n                                         \'Library\',\n                                         \'Python\',\n                                         sys.version[:3],\n                                         \'site-packages\'))\n            for sitedir in sitedirs:\n                if os.path.isdir(sitedir):\n                    addsitedir(sitedir, known_paths,\n                               exclude_packages=[lambda line: \'setuptools\' in line])\n    return None\n\ndef setquit():\n    """Define new built-ins \'quit\' and \'exit\'.\n    These are simply strings that display a hint on how to exit.\n\n    """\n    if os.sep == \':\':\n        exit = \'Use Cmd-Q to quit.\'\n    elif os.sep == \'\\\\\':\n        exit = \'Use Ctrl-Z plus Return to exit.\'\n    else:\n        exit = \'Use Ctrl-D (i.e. EOF) to exit.\'\n    __builtin__.quit = __builtin__.exit = exit\n\n\nclass _Printer(object):\n    """interactive prompt objects for printing the license text, a list of\n    contributors and the copyright notice."""\n\n    MAXLINES = 23\n\n    def __init__(self, name, data, files=(), dirs=()):\n        self.__name = name\n        self.__data = data\n        self.__files = files\n        self.__dirs = dirs\n        self.__lines = None\n\n    def __setup(self):\n        if self.__lines:\n            return\n        data = None\n        for dir in self.__dirs:\n            for filename in self.__files:\n                filename = os.path.join(dir, filename)\n                try:\n                    fp = file(filename, "rU")\n                    data = fp.read()\n                    fp.close()\n                    break\n                except IOError:\n                    pass\n            if data:\n                break\n        if not data:\n            data = self.__data\n        self.__lines = data.split(\'\\n\')\n        self.__linecnt = len(self.__lines)\n\n    def __repr__(self):\n        self.__setup()\n        if len(self.__lines) <= self.MAXLINES:\n            return "\\n".join(self.__lines)\n        else:\n            return "Type %s() to see the full %s text" % ((self.__name,)*2)\n\n    def __call__(self):\n        self.__setup()\n        prompt = \'Hit Return for more, or q (and Return) to quit: \'\n        lineno = 0\n        while 1:\n            try:\n                for i in range(lineno, lineno + self.MAXLINES):\n                    print self.__lines[i]\n            except IndexError:\n                break\n            else:\n                lineno += self.MAXLINES\n                key = None\n                while key is None:\n                    key = raw_input(prompt)\n                    if key not in (\'\', \'q\'):\n                        key = None\n                if key == \'q\':\n                    break\n\ndef setcopyright():\n    """Set \'copyright\' and \'credits\' in __builtin__"""\n    __builtin__.copyright = _Printer("copyright", sys.copyright)\n    if sys.platform[:4] == \'java\':\n        __builtin__.credits = _Printer(\n            "credits",\n            "Jython is maintained by the Jython developers (www.jython.org).")\n    else:\n        __builtin__.credits = _Printer("credits", """\\\n    Thanks to CWI, CNRI, BeOpen.com, Zope Corporation and a cast of thousands\n    for supporting Python development.  See www.python.org for more information.""")\n    here = os.path.dirname(os.__file__)\n    __builtin__.license = _Printer(\n        "license", "See http://www.python.org/%.3s/license.html" % sys.version,\n        ["LICENSE.txt", "LICENSE"],\n        [os.path.join(here, os.pardir), here, os.curdir])\n\n\nclass _Helper(object):\n    """Define the built-in \'help\'.\n    This is a wrapper around pydoc.help (with a twist).\n\n    """\n\n    def __repr__(self):\n        return "Type help() for interactive help, " \\\n               "or help(object) for help about object."\n    def __call__(self, *args, **kwds):\n        import pydoc\n        return pydoc.help(*args, **kwds)\n\ndef sethelper():\n    __builtin__.help = _Helper()\n\ndef aliasmbcs():\n    """On Windows, some default encodings are not provided by Python,\n    while they are always available as "mbcs" in each locale. Make\n    them usable by aliasing to "mbcs" in such a case."""\n    if sys.platform == \'win32\':\n        import locale, codecs\n        enc = locale.getdefaultlocale()[1]\n        if enc.startswith(\'cp\'):            # "cp***" ?\n            try:\n                codecs.lookup(enc)\n            except LookupError:\n                import encodings\n                encodings._cache[enc] = encodings._unknown\n                encodings.aliases.aliases[enc] = \'mbcs\'\n\ndef setencoding():\n    """Set the string encoding used by the Unicode implementation.  The\n    default is \'ascii\', but if you\'re willing to experiment, you can\n    change this."""\n    encoding = "ascii" # Default value set by _PyUnicode_Init()\n    if 0:\n        # Enable to support locale aware default string encodings.\n        import locale\n        loc = locale.getdefaultlocale()\n        if loc[1]:\n            encoding = loc[1]\n    if 0:\n        # Enable to switch off string to Unicode coercion and implicit\n        # Unicode to string conversion.\n        encoding = "undefined"\n    if encoding != "ascii":\n        # On Non-Unicode builds this will raise an AttributeError...\n        sys.setdefaultencoding(encoding) # Needs Python Unicode build !\n\n\ndef execsitecustomize():\n    """Run custom site specific code, if available."""\n    try:\n        import sitecustomize\n    except ImportError:\n        pass\n\ndef fixup_setuptools():\n    """Make sure our setuptools monkeypatch is in place"""\n    for i in range(len(sys.path)):\n        if sys.path[i].find(\'setuptools\') != -1:\n            path = sys.path[i]\n            del sys.path[i]\n            sys.path.append(path)\n\ndef main():\n    abs__file__()\n    paths_in_sys = removeduppaths()\n    if include_site_packages:\n        paths_in_sys = addsitepackages(paths_in_sys)\n    setquit()\n    setcopyright()\n    sethelper()\n    aliasmbcs()\n    setencoding()\n    execsitecustomize()\n    # Remove sys.setdefaultencoding() so that users cannot change the\n    # encoding after initialization.  The test for presence is needed when\n    # this module is run as a script, because this code is executed twice.\n    if hasattr(sys, "setdefaultencoding"):\n        del sys.setdefaultencoding\n    __boot()\n    fixup_setuptools()\n    \n'
    s += '\n\ninclude_site_packages = %r\n\n' % include_site_packages
    s += '\n\nmain()\n'
    return s


files_to_write['__PYDIR__/distutils/__init__.py'] = 'import os\n\ndirname = os.path.dirname\nlib_dir = dirname(dirname(__file__))\nworking_env = dirname(dirname(lib_dir))\n\n# This way we run first, but distutils still gets imported:\ndistutils_path = os.path.join(os.path.dirname(os.__file__), \'distutils\')\n__path__.insert(0, distutils_path)\nexec open(os.path.join(distutils_path, \'__init__.py\')).read()\n\nimport dist\ndef make_repl(v):\n    if isinstance(v, basestring):\n        return v.replace(\'__WORKING__\', working_env)\n    else:\n        return v\n    \nold_parse_config_files = dist.Distribution.parse_config_files\ndef parse_config_files(self, filenames=None):\n    old_parse_config_files(self, filenames)\n    for d in self.command_options.values():\n        for name, value in d.items():\n            if isinstance(value, list):\n                value = [make_repl(v) for v in value]\n            elif isinstance(value, tuple):\n                value = tuple([make_repl(v) for v in value])\n            elif isinstance(value, basestring):\n                value = make_repl(value)\n            else:\n                print "unknown: %%s=%%r" %% (name, value)\n            d[name] = value\ndist.Distribution.parse_config_files = parse_config_files\n\nold_find_config_files = dist.Distribution.find_config_files\ndef find_config_files(self):\n    found = old_find_config_files(self)\n    system_distutils = os.path.join(distutils_path, \'distutils.cfg\')\n    if os.path.exists(system_distutils):\n        found.insert(0, system_distutils)\n    return found\ndist.Distribution.find_config_files = find_config_files\n'
files_to_write['__PYDIR__/setuptools/__init__.py'] = 'import os, sys\nfrom distutils import log\n# setuptools should be on sys.path already from a .pth file\n\nfor path in sys.path:\n    if \'setuptools\' in path:\n        setuptools_path = os.path.join(path, \'setuptools\')\n        __path__.insert(0, setuptools_path)\n        break\nelse:\n    raise ImportError(\n        \'Cannot find setuptools on sys.path; is setuptools.pth missing?\')\n\nexecfile(os.path.join(setuptools_path, \'__init__.py\'))\nimport setuptools.command.easy_install as easy_install\n\ndef get_script_header(script_text, executable=easy_install.sys_executable,\n                      wininst=False):\n    from distutils.command.build_scripts import first_line_re\n    first, rest = (script_text+\'\\n\').split(\'\\n\',1)\n    match = first_line_re.match(first)\n    options = \'\'\n    if match:\n        script_text = rest\n        options = match.group(1) or \'\'\n        if options:\n            options = \' \'+options\n    if wininst:\n        executable = "python.exe"\n    else:\n        executable = easy_install.nt_quote_arg(executable)\n    if options.find(\'-S\') == -1:\n        options += \' -S\'\n    shbang = "#!%%(executable)s%%(options)s\\n" %% locals()\n    shbang += ("import sys, os\\n"\n               "join, dirname, abspath = os.path.join, os.path.dirname, os.path.abspath\\n"\n               "site_dirs = [join(dirname(dirname(abspath(__file__))), \'lib\', \'python%%s.%%s\' %% tuple(sys.version_info[:2])), join(dirname(dirname(abspath(__file__))), \'lib\', \'python\')]\\n"\n               "sys.path[0:0] = site_dirs\\n"\n               "import site\\n"\n               "[site.addsitedir(d) for d in site_dirs]\\n")\n    return shbang\n\ndef install_site_py(self):\n    # to heck with this, we gots our own site.py and we\'d like\n    # to keep it, thank you\n    pass\n\nold_process_distribution = easy_install.easy_install.process_distribution\n\ndef process_distribution(self, requirement, dist, deps=True, *info):\n    old_process_distribution(self, requirement, dist, deps, *info)\n    log.info(\'Finished installing %%s\', requirement)\n\neasy_install.get_script_header = get_script_header\neasy_install.easy_install.install_site_py = install_site_py\neasy_install.easy_install.process_distribution = process_distribution\n'
distutils_cfg = '[install]\n__PREFIX__\n\n[easy_install]\ninstall_dir = __WORKING__/__PYDIR__\nsite_dirs = __WORKING__/__PYDIR__\nscript_dir = __WORKING__/bin/\nalways_copy = True\n'
files_to_write['bin/activate'] = '# This file must be used with "source bin/activate" *from bash*\n# you cannot run it directly\n\ndeactivate () {\n    if [ -n "$_WE_OLD_WORKING_PATH" ] ; then\n        PATH="$_WE_OLD_WORKING_PATH"\n        export PATH\n        unset _WE_OLD_WORKING_PATH\n    fi\n    if [ -n "$_WE_OLD_PYTHONPATH" ] ; then\n        if [ "$_WE_OLD_PYTHONPATH" = "__none__" ] ; then\n            unset PYTHONPATH\n        else\n            PYTHONPATH="$_WE_OLD_PYTHONPATH"\n        fi\n        export PYTHONPATH\n        unset _WE_OLD_PYTHONPATH\n    fi\n    if [ -n "$_WE_OLD_PS1" ] ; then\n        PS1="$_WE_OLD_PS1"\n        export PS1\n        unset _WE_OLD_PS1\n    fi\n\n\n    unset WORKING_ENV\n    %(unix_unset_env)s\n\n    if [ ! "$1" = "nondestructive" ] ; then\n    # Self destruct!\n        unset deactivate\n    fi\n}\n\n# unset irrelavent variables\ndeactivate nondestructive\n\nexport WORKING_ENV="%(working_env)s"\n\n_WE_OLD_WORKING_PATH="$PATH"\nPATH="$WORKING_ENV/bin:$PATH"\nexport PATH\nexport _WE_OLD_WORKING_PATH\n\n_WE_OLD_PS1="$PS1"\nPS1="(`basename $WORKING_ENV`)$PS1"\nexport PS1\nexport _WE_OLD_PS1\n\nif [ -z "$PYTHONPATH" ] ; then\n    _WE_OLD_PYTHONPATH="__none__"\n    PYTHONPATH="$WORKING_ENV/__PYDIR__"\nelse\n    _WE_OLD_PYTHONPATH="$PYTHONPATH"\n    PYTHONPATH="$WORKING_ENV/__PYDIR__:$PYTHONPATH"\nfi\nexport PYTHONPATH\nexport _WE_OLD_PYTHONPATH\n%(unix_set_env)s\n\n# This should detect bash, which has a hash command that must\n# be called to get it to forget past commands.  Without\n# forgetting past commands the $PATH changes we made may not\n# be respected\nif [ -n "$BASH" ] ; then\n    hash -r\nfi\n\n'
files_to_write['bin/activate.bat'] = '@echo off\nset WORKING_ENV=%(working_env)s\n\nif not defined PROMPT (\n    set PROMPT=$P$G\n)\n\nif defined _WE_OLD_PROMPT (\n    set PROMPT=%%_WE_OLD_PROMPT%%\n)\n\nset _WE_OLD_PROMPT=%%PROMPT%%\nset PROMPT=(%(env_name)s) %%PROMPT%%\n\nif defined _WE_OLD_WORKING_PATH (\n    set PATH=%%_WE_OLD_WORKING_PATH%%\n    goto SKIP1\n)\nset _WE_OLD_WORKING_PATH=%%PATH%%\n\n:SKIP1\nset PATH=%%WORKING_ENV%%\\bin;%%PATH%%\n\nif defined _WE_OLD_PYTHONPATH (\n    if %%_WE_OLD_PYTHONPATH%%+X==__none__+X (\n        set PYTHONPATH=\n        goto SKIP2\n    )\n    set PYTHONPATH=%%_WE_OLD_PYTHONPATH%%\n)\n\n:SKIP2\nif defined PYTHONPATH (\n    set _WE_OLD_PYTHONPATH=%%PYTHONPATH%%\n    set PYTHONPATH=%%WORKING_ENV%%\\__PYDIR__;%%PYTHONPATH%%\n    goto END\n)\nset _WE_OLD_PYTHONPATH=__none__\nset PYTHONPATH=%%WORKING_ENV%%\\__PYDIR__\n%(windows_set_env)s\n\n:END\n'
files_to_write['bin/deactivate.bat'] = '@echo off\n\nif defined _WE_OLD_PROMPT (\n    set PROMPT=%%_WE_OLD_PROMPT%%\n)\nset _WE_OLD_PROMPT=\n\nif defined _WE_OLD_WORKING_PATH (\n    set PATH=%%_WE_OLD_WORKING_PATH%%\n)\nset _WE_OLD_WORKING_PATH=\n\nif defined _WE_OLD_PYTHONPATH (\n    if %%_WE_OLD_PYTHONPATH%%+X==__none__+X (\n        set PYTHONPATH=\n        goto SKIP1\n    )\n    set PYTHONPATH=%%_WE_OLD_PYTHONPATH%%\n)\n\n:SKIP1\nset _WE_OLD_PYTHONPATH=\n%(windows_unset_env)s\n\n:END\n'
if __name__ == '__main__':
    try:
        main()
    except BadCommand, e:
        print e
        sys.exit(2)