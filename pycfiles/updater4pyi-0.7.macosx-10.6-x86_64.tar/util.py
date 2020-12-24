# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/updater4pyi/util.py
# Compiled at: 2014-12-07 12:49:59
"""
A collection of various utilities.
"""
import sys, os, os.path, re, subprocess, logging, inspect, urllib, datetime
logger = logging.getLogger('updater4pyi')

def ignore_exc(f, exc=(
 Exception,), value_if_exc=None):
    if not isinstance(exc, tuple):
        exc = (
         exc,)
    try:
        return f()
    except exc:
        return value_if_exc


def getbool(x):
    """
    Utility to parse a string representing a boolean value.

    If `x` is already of integer or boolean type (actually, anything castable to an
    integer), then the corresponding boolean convertion is returned. If it is a
    string-like type, then it is matched against something that looks like 't(rue)?', '1',
    'y(es)?' or 'on' (ignoring case), or against something that looks like 'f(alse)?',
    '0', 'n(o)?' or 'off' (also ignoring case). Leading or trailing whitespace is ignored. 
    If the string cannot be parsed, a :py:exc:`ValueError` is raised.
    """
    try:
        return int(x) != 0
    except (TypeError, ValueError):
        pass

    x = str(x)
    m = re.match('^\\s*(t(?:rue)?|1|y(?:es)?|on)\\s*$', x, re.IGNORECASE)
    if m:
        return True
    m = re.match('^\\s*(f(?:alse)?|0|n(?:o)?|off)\\s*$', x, re.IGNORECASE)
    if m:
        return False
    raise ValueError("Can't parse boolean value: %r" % x)


_TIMEDELTA_RX = '(?xi)\n    (?P<num>\\d+)\\s*\n    (?P<unit>\n        y(ears?)?|\n        mon(ths?)?|\n        weeks?|\n        days?|\n        hours?|\n        min(utes?)?|\n        s(ec(onds?)?)?\n    )\n    (,\\s*)?\n    '
_timedelta_units = {'y': datetime.timedelta(days=365, seconds=0, microseconds=0), 'mon': datetime.timedelta(days=30, seconds=0, microseconds=0), 
   'week': datetime.timedelta(days=7, seconds=0, microseconds=0), 
   'day': datetime.timedelta(days=1, seconds=0, microseconds=0), 
   'hour': datetime.timedelta(days=0, seconds=3600, microseconds=0), 
   'min': datetime.timedelta(days=0, seconds=60, microseconds=0), 
   's': datetime.timedelta(days=0, seconds=1, microseconds=0)}

def ensure_timedelta(x):
    if isinstance(x, datetime.timedelta):
        return x
    if isinstance(x, basestring):
        val = datetime.timedelta(0)
        for m in re.finditer(_TIMEDELTA_RX, x):
            thisvallst = [ v for k, v in _timedelta_units.iteritems() if k.lower().startswith(m.group('unit')) ]
            if not thisvallst:
                raise ValueError('Unexpected unit: %s' % m.group('unit'))
            val += int(m.group('num')) * thisvallst[0]

        return val
    try:
        sec = int(x)
        musec = (x - int(x)) * 1000000.0
        return datetime.timedelta(0, sec, musec)
    except ValueError:
        pass

    raise ValueError('Unable to parse timedelta representation: %r' % x)


def ensure_datetime(x):
    if isinstance(x, datetime.datetime):
        return x
    if isinstance(x, basestring):
        try:
            import dateutil.parser
            return dateutil.parser.parse(x)
        except ImportError:
            pass

        for fmt in ('%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S'):
            try:
                return datetime.strptime(x, fmt)
            except ValueError:
                pass

        raise ValueError("Can't parse date/time : %s" % x)
    raise ValueError("Can't parse date/time: unknown type: %r" % x)


def is_macosx():
    return sys.platform.startswith('darwin')


def is_win():
    return sys.platform.startswith('win')


def is_linux():
    return sys.platform.startswith('linux')


def simple_platform():
    if is_macosx():
        return 'macosx'
    else:
        if is_win():
            return 'win'
        if is_linux():
            return 'linux'
        return sys.platform


def bash_quote(x):
    return "'" + x.replace("'", "'\\''") + "'"


def winshell_quote(x):
    return '"' + x.replace('"', '""') + '"'


def applescript_quote(x):
    return '"' + re.sub('([\\\\"])', '\\\\\\1', x) + '"'


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """

    def base_path():
        try:
            return sys._MEIPASS
        except AttributeError:
            pass

        mainfn = inspect.stack()[(-1)][1]
        return os.path.abspath(os.path.dirname(mainfn))

    return os.path.join(base_path(), relative_path)


def path2url(p):
    x = p
    if os.sep != '/':
        x = x.replace(os.sep, '/')
    x = urllib.pathname2url(x)
    if not x.startswith('///'):
        x = '//' + os.path.abspath(x)
    return 'file:' + x


def locationIsWritable(path):
    if os.path.isdir(path):
        return dirIsWritable(path)
    if os.path.isfile(path):
        return fileIsWritable(path)
    logger.warning('location does not exist: %s', path)
    return False


def fileIsWritable(fn):
    if not is_win():
        return os.access(fn, os.W_OK)
    return dirIsWritable(os.path.dirname(fn))


def dirIsWritable(directory):
    if not is_win():
        return os.access(directory, os.W_OK)
    try:
        tmp_prefix = 'upd4pyi_tmp_write_tester'
        count = 0
        filename = os.path.join(directory, tmp_prefix)
        while os.path.exists(filename):
            filename = '%s.%s.tmp' % (os.path.join(directory, tmp_prefix), count)
            count = count + 1

        with open(filename, 'w') as (f):
            pass
        os.remove(filename)
        return True
    except IOError as e:
        return False


def run_as_admin(argv):
    cmd = []
    if is_macosx():
        cmd = [
         'osascript',
         '-e',
         'do shell script ' + applescript_quote((' ').join([ bash_quote(x) for x in argv ])) + ' with administrator privileges']
    elif is_linux():
        if which('pkexec'):
            cmd = [
             which('pkexec')] + argv
        elif os.environ.get('DISPLAY') and which('gksudo'):
            cmd = [
             which('gksudo')] + argv
        elif os.environ.get('DISPLAY') and which('kdesudo'):
            cmd = [
             which('kdesudo')] + argv
        elif os.environ.get('DISPLAY') and which('xterm'):
            cmd = [
             which('xterm'), '-e', 'sudo'] + argv
        else:
            cmd = [
             which('sudo')] + argv
    else:
        if is_win():
            return _run_as_admin_win(argv)
        logger.error('Platform not recognized for running process as admin: %s', simple_platform())
        raise NotImplementedError
    logger.debug('Running command %r', cmd)
    retcode = subprocess.call(cmd, stdin=None, stdout=None, stderr=None, shell=False)
    if retcode != 0:
        logger.warning('admin subprocess %s failed', argv[0] if argv else None)
    return retcode


def run_win(argv, needs_sudo=False, wait=True, cwd=None):
    """
    Run a process on windows.

    Returns: the exit code of the process if `wait` is `True`, or the PID of the running
    process if `wait` is `False`.
    """
    if os.name != 'nt':
        raise RuntimeError, 'This function is only implemented on Windows.'
    import win32api, win32con, win32event, win32process
    from win32com.shell.shell import ShellExecuteEx
    from win32com.shell import shellcon
    cmd = winshell_quote(argv[0])
    params = (' ').join([ winshell_quote(x) for x in argv[1:] ])
    cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL
    if needs_sudo:
        lpVerb = 'runas'
    else:
        lpVerb = 'open'
    logger.debug('running %s %s', cmd, params)
    optional_args = {}
    if cwd is not None:
        optional_args['lpDirectory'] = cwd
    procInfo = ShellExecuteEx(nShow=showCmd, fMask=shellcon.SEE_MASK_NOCLOSEPROCESS, lpVerb=lpVerb, lpFile=cmd, lpParameters=params, **optional_args)
    if wait:
        procHandle = procInfo['hProcess']
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
        logger.debug('Process handle %s returned code %s', (procHandle, rc))
    else:
        rc = win32process.GetProcessId(procInfo['hProcess'])
    return rc


_component_re = re.compile('(\\d+ | [a-z]+ | \\.| -)', re.VERBOSE)
_replace = {'pre': 'c', 'preview': 'c', '-': 'final-', 'rc': 'c', 'dev': '@'}.get

def _parse_version_parts(s):
    for part in _component_re.split(s):
        part = _replace(part, part)
        if not part or part == '.':
            continue
        if part[:1] in '0123456789':
            yield part.zfill(8)
        else:
            yield '*' + part

    yield '*final'


def parse_version(s):
    """
    Convert a version string to a chronologically-sortable key

    This function is based on code from `setuptools
    <https://bitbucket.org/pypa/setuptools/src/353a4270074435faa7daa2aa0ee480e22e505f53/pkg_resources.py?at=default>`_.
    (I didn't find any license text to copy from that project, but on `PyPI
    <https://pypi.python.org/pypi/setuptools>`_ it states that the license is 'PSF or
    `ZPL <http://opensource.org/licenses/ZPL-2.0>`_'.)

    This is a rough cross between distutils' StrictVersion and LooseVersion;
    if you give it versions that would work with StrictVersion, then it behaves
    the same; otherwise it acts like a slightly-smarter LooseVersion. It is
    *possible* to create pathological version coding schemes that will fool
    this parser, but they should be very rare in practice.

    The returned value will be a tuple of strings.  Numeric portions of the
    version are padded to 8 digits so they will compare numerically, but
    without relying on how numbers compare relative to strings.  Dots are
    dropped, but dashes are retained.  Trailing zeros between alpha segments
    or dashes are suppressed, so that e.g. "2.4.0" is considered the same as
    "2.4". Alphanumeric parts are lower-cased.

    The algorithm assumes that strings like "-" and any alpha string that
    alphabetically follows "final"  represents a "patch level".  So, "2.4-1"
    is assumed to be a branch or patch of "2.4", and therefore "2.4.1" is
    considered newer than "2.4-1", which in turn is newer than "2.4".

    Strings like "a", "b", "c", "alpha", "beta", "candidate" and so on (that
    come before "final" alphabetically) are assumed to be pre-release versions,
    so that the version "2.4" is considered newer than "2.4a1".

    Finally, to handle miscellaneous cases, the strings "pre", "preview", and
    "rc" are treated as if they were "c", i.e. as though they were release
    candidates, and therefore are not as new as a version string that does not
    contain them, and "dev" is replaced with an '@' so that it sorts lower than
    than any other pre-release tag.
    """
    parts = []
    for part in _parse_version_parts(s.lower()):
        if part.startswith('*'):
            if part < '*final':
                while parts and parts[(-1)] == '*final-':
                    parts.pop()

            while parts and parts[(-1)] == '00000000':
                parts.pop()

        parts.append(part)

    return tuple(parts)


_which_cache = {}
_which_cache_first = {}

def which_clear_cache():
    _which_cache.clear()
    _which_cache_first.clear()


def which(name, flags=os.X_OK, usecache=True, firstresult=True):
    """Search PATH for executable files with the given name.

    This function is based on code from
    `twisted <http://twistedmatrix.com/trac/browser/tags/releases/twisted-8.2.0/twisted/python/procutils.py>`_
    (see copyright notice in source code of this function).

    On newer versions of MS-Windows, the PATHEXT environment variable will be
    set to the list of file extensions for files considered executable. This
    will normally include things like ".EXE". This fuction will also find files
    with the given name ending with any of these extensions.

    On MS-Windows the only flag that has any meaning is os.F_OK. Any other
    flags will be ignored.

    @type name: C{str}
    @param name: The name for which to search.

    @type flags: C{int}
    @param flags: Arguments to L{os.access}.

    @rtype: C{list}
    @param: A list of the full paths to files found, in the
    order in which they were found.
    """
    if usecache:
        if firstresult:
            if name in _which_cache_first:
                return _which_cache_first.get(name)
        elif name in _which_cache:
            return _which_cache.get(name)
    result = []
    exts = filter(None, os.environ.get('PATHEXT', '').split(os.pathsep))
    path = os.environ.get('PATH', None)
    if path is None:
        return []
    else:
        for p in os.environ.get('PATH', '').split(os.pathsep):
            p = os.path.join(p, name)
            if os.access(p, flags):
                result.append(p)
            for e in exts:
                pext = p + e
                if os.access(pext, flags):
                    result.append(pext)

            if firstresult and result:
                _which_cache_first[name] = result[0]
                return result[0]

        if usecache and result:
            _which_cache[name] = result
        return result