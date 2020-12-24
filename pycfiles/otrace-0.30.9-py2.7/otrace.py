# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/otrace.py
# Compiled at: 2012-08-26 21:10:23
"""An object-oriented debugger for nonlinear tracing

Installation
============

Ensure that ``otrace.py`` is in the python module load path.
(For python 2.6 or earlier, you will also need ``ordereddict.py``.) 

Usage
======

*otrace* may be used as:
   - a tracing tool for debugging web servers and interactive programs
   - a console or dashboard for monitoring production servers
   - a teaching tool for exploring the innards of a program
   - a code patching tool for unit testing

*otrace* does not consume any resources until some tracing action is
initiated. So it can be included in production code without any
performance penalty.
*otrace* works well with detached server processes (*daemons*)
via the GNU `screen <http://www.gnu.org/software/screen>`_
utility that emulates a terminal.
 
*otrace* is meant to be used in conjunction with an *event loop*, which
is usually present in programs that interact with users such as web
servers or GUI applications. *otrace* takes control of the terminal,
and would not work very well with programs that read user input
directly from the terminal (or standard input).

To use *otrace*, simply ``import otrace`` and instantiate the class ``otrace.OShell``,
which provides a unix-like shell interface to interact with a running
program via the terminal.

Here is a simple server example::

     import BaseHTTPServer
     from SimpleHTTPServer import SimpleHTTPRequestHandler
     from otrace import OShell, traceassert

     http_server = BaseHTTPServer.HTTPServer(("", 8888), SimpleHTTPRequestHandler)
     oshell = OShell(locals_dict=locals(), globals_dict=globals(),
                     new_thread=True, allow_unsafe=True, init_file="server.trc")
     try:
         oshell.loop()
         http_server.serve_forever()   # Main event loop
     except KeyboardInterrupt:
         oshell.shutdown()

*Usage notes:*

 - If you run in *oshell* in its own daemon thread as shown above, use
   the ^C sequence to abort the main thread, and call ``OShell.shutdown``
   from main thread to cleanup terminal I/O etc.

 - If you run *oshell* in the main thread and the event loop in a
   separate thread, ^C will abort and cleanup *oshell*. You may need to
   shutdown the event loop cleanly after that.

 - Install the python ``readline`` module to enable *TAB* command completion.

 - To start a detached server (daemon) process, use the command:
      ``screen -d -m -S <screen_name> <executable> <argument1> ...``
   To attach a terminal to this process, use:
      ``screen -r <screen_name>``

 - By default, *otrace* logs to the ``logging`` module. Subclass
   ``TraceCallback``, overriding the methods ``callback`` and ``returnback``
   to implement your own logging  (see ``DefaultCallback`` for a simple example)

Synopsis
=========

*otrace* uses a *Virtual Directory Shell Interface* which maps all the
objects in a a running python program to a virtual filesystem mounted in
the directory ``/osh`` (sort of like the unix ``/proc`` filesystem, if you are
familiar with it). Each module, class, method, function, and variable in the global namespace
is mapped to a virtual file within this directory.
For example, a class ``TestClass`` in the ``globals()`` dictionary can be accessed as::

   /osh/globals/TestClass

and a method ``test_method`` can be accessed as::

   /osh/globals/TestClass/test_method

and so on.

*otrace* provides a unix shell-like interface, *oshell*, with commands
such as ``cd``, ``ls``, ``view``, and ``edit`` that can be used navigate, view,
and edit the virtual files. Editing a function or method
"`monkey patches <http://en.wikipedia.org/wiki/Monkey_patch>`_"  it,
allowing the insertion of ``print`` statements etc. in the running program.

The ``trace`` command allows dynamic tracing of function or method invocations,
return values, and exceptions. This is accomplished by
dynamically *decorating* (or *wrapping*) the function to be traced.
When a trace condition is satisfied, the function-wrapper saves *context information*, such as
arguments and return values, in a newly created virtual directory in::

    /osh/recent/*

These *trace context* directories can be navigated just like
``/osh/globals/*``. (If there are too many trace contexts, the oldest
ones are deleted, unless they have been explicitly *saved*.)

*oshell* allows standard unix shell commands to be interspersed with
*oshell*-specific commands. The path of the "current working directory"
determines which of the these two types of commands will be executed. 
If the current working directory is not in ``/osh/*``, the command is
treated as a standard unix shell command (except for ``cd``, which is
always handled by *oshell*.)

Credits
========

*otrace* was developed as part of the `Mindmeldr <http://mindmeldr.com>`_ project, which is aimed at improving classroom interaction.

*otrace* was inspired by the following:
 - the tracing module `echo.py <http://wordaligned.org/articles/echo>`_ written by Thomas Guest <tag@wordaligned.org>. This nifty little program uses decorators to trace function calls.

 - the python ``dir()`` function, which treats objects as directories. If objects are directories, then shouldn't we be able to inspect them using the familiar ``cd`` and ``ls`` unix shell commands?

 - the unix `proc <http://en.wikipedia.org/wiki/Procfs>`_ filesystem, which cleverly maps non-file data to a filesystem interface mounted at ``/proc``

 - the movie `Being John Malkovich <http://en.wikipedia.org/wiki/Being_John_Malkovich>`_ (think of ``/osh`` as the portal to the "mind" of a running program)

License
=========
*otrace* is distributed as open source under the `BSD-license <http://www.opensource.org/licenses/bsd-license.php>`_.

"""
from __future__ import with_statement
import cgi, cgitb, codeop, collections, copy, cPickle, datetime, functools, hashlib, hmac, inspect, logging, logging.handlers, os, os.path, pprint, Queue, random, re, select, shlex, sqlite3, StringIO, struct, subprocess, sys, tempfile, threading, time, traceback, types, urllib, weakref
Banner_messages = []
try:
    import termios
    Term_attr = termios.tcgetattr(sys.stdin.fileno())
except Exception:
    Term_attr = None

try:
    import readline
    if readline.__doc__ and 'libedit' in readline.__doc__:
        readline.parse_and_bind('bind ^I rl_complete')
except Exception:
    readline = None
    mod_name = 'pyreadline' if sys.platform.startswith('win') else 'readline'
    Banner_messages.append("  Please install '%s' module for TAB completion (e.g. 'easy_install %s')" % (mod_name, mod_name))

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

try:
    from collections import MutableMapping
except ImportError:
    from UserDict import DictMixin as MutableMapping

OTRACE_VERSION = '0.30.9'
__all__ = [
 'OTrace', 'OShell', 'OTraceException']
EXEC_TIMEOUT = 10
REPEAT_COUNT = 10000
PATH_SEP = '/'
BACKSLASH = '\\'
ENTITY_CHAR = ':'
BASE_DIR = 'osh'
BASE_OFFSET = 1
BASE1_OFFSET = 2
BASE2_OFFSET = 3
TRACE_OFFSET = 6
MAX_PICKLE_CHECK_DEPTH = 3
MAX_PICKLE_DATA_LENGTH = 10000
ALL_DIR = 'all'
BROWSER_DIR = 'browser'
DATABASE_DIR = 'db'
GLOBALS_DIR = 'globals'
LOCALS_DIR = 'locals'
PATCHES_DIR = 'patches'
PICKLED_DIR = 'pickled'
RECENT_DIR = 'recent'
SAVED_DIR = 'saved'
WEB_DIR = 'web'
LAZY_DIRS = [
 DATABASE_DIR, PICKLED_DIR]
DIR_LIST = [
 ALL_DIR, BROWSER_DIR, DATABASE_DIR, GLOBALS_DIR, LOCALS_DIR, PATCHES_DIR, PICKLED_DIR, RECENT_DIR, SAVED_DIR, WEB_DIR]
OT_DIRS = set(DIR_LIST)
DIR_PREFIX = dict((dir_name, PATH_SEP + BASE_DIR + PATH_SEP + dir_name + PATH_SEP) for dir_name in DIR_LIST)
BREAK_ACTIONS = [
 'break', 'ipdb', 'pdb']
TRACE_ACTIONS = BREAK_ACTIONS + ['hold', 'tag']
TRACE_INFO = '__trc'
DOWN_STACK = '__down'
UP_STACK = '__up'
SHOW_HIDDEN = set(['__call__', TRACE_INFO, DOWN_STACK, UP_STACK])
IGNORE_FUNCNAMES = set(['otrace_function_call', 'otrace_wrapped'])
ASSIGNMENT_RE = re.compile('\\s*[a-zA-Z][a-zA-Z0-9_\\.]*\\s*=[^=]')
EXEC_PREFIX = '!'
NEWCONTEXT_PREFIX = '~~'
GLOBALS_PREFIX = '~~g'
WORKDIR_PREFIX = '~~w'
TRACE_ID_PREFIX = '~'
TRACE_ID_SEP = ':'
TRACE_LABEL_PREFIX = ':'
TRACE_LOG_PREFIX = 'log:'
CLEAR_SCREEN_SEQUENCE = '\x1b[H\x1b[J'
ALT_SCREEN_ONSEQ = '\x1b[?1049h'
ALT_SCREEN_OFFSEQ = '\x1b[?1049l'
INAME = 0
ISUBDIR = 1
FILE_EXTENSIONS = {'css': 'css', 'htm': 'html', 'html': 'html', 'js': 'javascript', 'py': 'python', 'xml': 'xml'}
DOC_URL = 'http://info.mindmeldr.com/code/otrace'
DEFAULT_BANNER = "  ***otrace object shell (v%s)*** (type 'help' for info)" % OTRACE_VERSION
Help_params = OrderedDict()
Help_params['allow_xml'] = 'Allow output markup for display in browser (if supported)'
Help_params['append_traceback'] = 'Append traceback information to exceptions'
Help_params['assert_context'] = 'No. of lines of context retrieved for traceassert (0 for efficiency)'
Help_params['auto_lock'] = 'Automatically lock after specified idle time (in seconds), if password is set'
Help_params['deep_copy'] = "Create deep copies of arguments and local variables for 'snapshots'"
Help_params['editor'] = 'Editor to use for editing patches or viewing source'
Help_params['exec_lock'] = 'Execute code within re-entrant lock'
Help_params['log_format'] = 'Format for log messages'
Help_params['log_level'] = 'Logging level (10=>DEBUG, 20=>INFO, 30=>WARNING ...; see logging module)'
Help_params['log_remote'] = 'IP address or domain (:port) for remote logging (default port: 9020)'
Help_params['log_truncate'] = 'No. of characters to display for log messages (default: 72)'
Help_params['max_recent'] = 'Maximum number of entries to keep in /osh/recent'
Help_params['osh_bin'] = 'Path to prepend to $PATH to use custom commands'
Help_params['password'] = 'Encrypted access password (use otrace.encrypt_password to create it)'
Help_params['pickle_file'] = 'Name of file to save pickled trace contexts'
Help_params['pretty_print'] = 'Use pprint.pformat rather than print to display expressions'
Help_params['repeat_interval'] = 'Command repeat interval (sec)'
Help_params['safe_mode'] = 'Safe mode (disable code modification and execution)'
Help_params['save_tags'] = 'Automatically save all tag contexts'
Help_params['trace_active'] = 'Activate tracing (can be used to force/suppress tracing)'
Help_params['trace_related'] = 'Automatically trace calls related to tagged objects'
Help_params['unpickle_file'] = 'Name of file to read pickled trace contexts from'
Set_params = {}
Set_params['allow_xml'] = True
Set_params['append_traceback'] = False
Set_params['assert_context'] = 0
Set_params['auto_lock'] = 0
Set_params['deep_copy'] = False
Set_params['editor'] = ''
Set_params['exec_lock'] = False
Set_params['log_format'] = None
Set_params['log_level'] = None
Set_params['log_remote'] = None
Set_params['log_truncate'] = None
Set_params['max_recent'] = 10
Set_params['osh_bin'] = ''
Set_params['password'] = ''
Set_params['pickle_file'] = ''
Set_params['pretty_print'] = False
Set_params['repeat_interval'] = 0.2
Set_params['safe_mode'] = True
Set_params['save_tags'] = False
Set_params['trace_active'] = None
Set_params['trace_related'] = False
Set_params['unpickle_file'] = None
Trace_rlock = threading.RLock()
Pickle_rlock = threading.RLock()
if sys.version_info[0] < 3:

    def encode(s):
        return s


    def decode(s):
        return s


else:

    def encode(s):
        return s.encode('utf-8')


    def decode(s):
        return s.decode('utf-8')


def encrypt_password(password, salt=None, hexdigits=16):
    """Encrypt password, returning encrypted password prefixed with salt,
    which defaults to a random value
    """
    if not salt:
        salt = '%015d' % random.randrange(0, 1000000000000000)
    elif ':' in salt:
        raise Exception('Colon not allowed in salt')
    encrypted = hmac.new(encode(salt), encode(password), digestmod=hashlib.sha256).hexdigest()[:hexdigits]
    return salt + ':' + encrypted


def verify_password(password, encrypted_password):
    salt, sep, _ = encrypted_password.partition(':')
    if not salt:
        raise Exception('No salt in encrypted password')
    return encrypted_password == encrypt_password(password, salt=salt)


class OSDirectory(object):

    def __init__(self, path=None):
        self.path = path


class AltHandler(Exception):
    pass


def is_absolute_path(path):
    if path.startswith(PATH_SEP):
        return True
    if os.sep == BACKSLASH and re.match('[a-zA-Z]:', path):
        return True
    return False


def os_path(path):
    """Convert unix-style path to OS path"""
    if os.sep == BACKSLASH:
        if path.startswith(PATH_SEP):
            comps = path[1:].split(PATH_SEP)
            comps[0] = 'c:\\' + comps[0]
        else:
            comps = path.split(PATH_SEP)
        path = os.path.join(*comps)
    return path


def expanduser(filepath):
    if filepath.startswith(GLOBALS_PREFIX):
        filepath = DIR_PREFIX[GLOBALS_DIR][:-1] + filepath[len(GLOBALS_PREFIX):]
    elif filepath.startswith(WORKDIR_PREFIX):
        dir_path = OShell.instance and OShell.instance.work_dir or os.getcwd()
        filepath = dir_path + filepath[len(WORKDIR_PREFIX):]
    elif filepath.startswith(NEWCONTEXT_PREFIX):
        return PATH_SEP + PATH_SEP.join(OTrace.recent_pathnames)
    return os.path.expanduser(filepath)


def expandpath(filepath):
    """Return expanded filepath (absolute path or assumed relative to work directory)"""
    return expanduser(filepath if is_absolute_path(filepath) or filepath.startswith(NEWCONTEXT_PREFIX) or filepath.startswith('~') else WORKDIR_PREFIX + PATH_SEP + filepath)


def otrace_pformat(*args, **kwargs):
    if Set_params['pretty_print']:
        return ('\n').join(pprint.pformat(arg, **kwargs) for arg in args)
    else:
        return (' ').join(str(arg) for arg in args)


def de_indent(lines):
    """Remove global indentation"""
    out_lines = []
    indent = None
    for line in lines:
        temline = line.lstrip()
        if indent is None and temline and not temline.startswith('#') and not temline.startswith('@'):
            indent = len(line) - len(temline)
        if indent and len(line) - len(temline) >= indent:
            out_lines.append(line[indent:])
        elif not temline.startswith('@'):
            out_lines.append(line)

    return out_lines


def pythonize(args):
    """Convert shell-style space-separated, unquoted arguments to
     python-style comma-separated, quoted arguments"""
    arg_list = []
    for arg in args:
        if '=' in arg:
            kw, sep, arg = arg.partition('=')
            prefix = kw + sep
        else:
            prefix = ''
        if arg and (arg.isdigit() or arg[0] in '+-' and arg[1:].isdigit()):
            arg_list.append(prefix + arg)
        else:
            arg_list.append(prefix + repr(arg))

    return (', ').join(arg_list)


def strip_compare_op(prop_name):
    """Return (stripped_prop_name, compare_op) for suffixed property names of the form "arg1!=", "arg2<" etc."""
    cmp_op = ''
    if prop_name.endswith('='):
        cmp_op = '='
        prop_name = prop_name[:-1]
    if prop_name[(-1)] in ('=', '!', '<', '>'):
        cmp_op = prop_name[(-1)] + cmp_op
        prop_name = prop_name[:-1]
    if not cmp_op or cmp_op == '=':
        cmp_op = '=='
    return (prop_name.strip(), cmp_op)


def compare(value1, op_str, value2):
    """Return True or False for comparison using operator."""
    return op_str == '==' and value1 == value2 or op_str == '!=' and value1 != value2 or op_str == '<=' and value1 <= value2 or op_str == '>=' and value1 >= value2 or op_str == '<' and value1 < value2 or op_str == '>' and value1 > value2


def match_parse(match_str, delimiter=','):
    """Parse match dict components of the form: var1.comp1==value1,var2!=value2,... where values with commas/spaces must be quoted."""
    match_dict = {}
    invalid_tokens = []
    lex = shlex.shlex(match_str, None, True)
    lex.whitespace = delimiter
    lex.whitespace_split = True
    while True:
        token = lex.get_token()
        if token is None:
            break
        if not token:
            continue
        re_match = re.match('^([\\w\\.]+)(==|!=|<=|>=|<|>)(.+)$', token)
        if not re_match:
            invalid_tokens.append(token)
            continue
        value = re_match.group(3)
        if value and (value[0].isdigit() or value[0] in '+-' and value[1:2].isdigit()):
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = long(value)
            except Exception:
                invalid_tokens.append(token)
                value = None

        elif value in ('True', 'False'):
            value = value == 'True'
        elif value == 'None':
            value = None
        match_dict[re_match.group(1) + re_match.group(2)] = value

    if invalid_tokens and re.search('[=<>]', match_str):
        raise Exception('Invalid match components: ' + (',').join(invalid_tokens))
    return match_dict


def get_obj_properties(value, full_path=None):
    """Return (python_mime_type, command) for object value"""
    opts = ''
    if full_path and OShell.instance:
        if len(full_path) > BASE_OFFSET and full_path[BASE_OFFSET] in OShell.instance.lazy_dirs:
            base_subdir = full_path[BASE_OFFSET]
            if len(full_path) == BASE1_OFFSET + OShell.instance.lazy_dirs[base_subdir].root_depth:
                return ('object', 'cdls')
            opts += ' -v'
    if value is None or isinstance(value, (basestring, bool, complex, float, int, list, tuple)):
        return ('value', 'pr')
    if inspect.isfunction(value) or inspect.ismethod(value):
        return ('function', 'view -i')
    return ('object', 'cdls' + opts)
    return


def format_traceback(exc_info=None):
    """Return string describing exception."""
    try:
        etype, value, tb = exc_info if exc_info else sys.exc_info()
        tblist = traceback.extract_tb(tb)
        del tblist[:1]
        fmtlist = traceback.format_list(tblist)
        if fmtlist:
            fmtlist.insert(0, 'Traceback (most recent call last):\n')
        fmtlist[(len(fmtlist)):] = traceback.format_exception_only(etype, value)
    finally:
        tblist = tb = None

    return ('').join(fmtlist)


def get_naked_function(method):
    """Return function object associated with a method."""
    if inspect.isfunction(method):
        return method
    else:
        return getattr(method, '__func__', None)


def ismethod_or_function(method):
    return inspect.isfunction(get_naked_function(method))


def get_method_type(parent_cls, method):
    """Return 'instancemethod'/'classmethod'/'staticmethod' """
    attr_value = parent_cls.__dict__[method.__name__]
    if inspect.isfunction(attr_value):
        return 'instancemethod'
    return type(attr_value).__name__


class OTraceException(Exception):
    pass


class TraceDict(dict):

    def has_trc(self, trace_attr):
        """Returns True if self[TRACE_INFO] has attribute."""
        return TRACE_INFO in self and trace_attr in self[TRACE_INFO]

    def get_trc(self, trace_attr, default=None):
        """Return self[TRACE_INFO][trace_attr] or default."""
        if TRACE_INFO in self:
            return self[TRACE_INFO].get(trace_attr, default)
        else:
            return default

    def set_trc(self, trace_attr, value):
        """Set self[TRACE_INFO][trace_attr] to value."""
        if TRACE_INFO not in self:
            self[TRACE_INFO] = {}
        self[TRACE_INFO][trace_attr] = value


class MappingDict(MutableMapping):
    pass


class ObjectDict(MappingDict):
    """Wrapper to make an object appear like a dict."""

    def __init__(self, obj):
        self._obj = obj

    def copy(self):
        return ObjectDict(self._obj)

    def keys(self):
        return dir(self._obj)

    def __contains__(self, key):
        return hasattr(self._obj, key)

    def __getitem__(self, key):
        if not hasattr(self._obj, key):
            raise KeyError(key)
        return getattr(self._obj, key)

    def __iter__(self):
        return self.keys().__iter__

    def __len__(self):
        return len(self.keys())

    def __setitem__(self, key, value):
        setattr(self._obj, key, value)

    def __delitem__(self, key):
        if not hasattr(self._obj, key):
            raise KeyError(key)
        delattr(self._obj, key)


class ListDict(MappingDict):
    """Wrapper to make a list/tuple appear like a dict."""

    def __init__(self, lst):
        self._lst = lst

    def copy(self):
        return ListDict(self._lst)

    def keys(self):
        return [ str(x) for x in range(len(self._lst)) ]

    def __contains__(self, key):
        try:
            key = int(key)
        except Exception:
            return False

        return key >= 0 and key < len(self._lst)

    def __getitem__(self, key):
        if not self.__contains__(key):
            raise KeyError(key)
        return self._lst[int(key)]

    def __iter__(self):
        for x in self.keys():
            yield x

    def __len__(self):
        return len(self._lst)

    def __setitem__(self, key, value):
        if not self.__contains__(key):
            raise KeyError(key)
        self._lst[int(key)] = value

    def __delitem__(self, key):
        if not self.__contains__(key):
            raise KeyError(key)
        del self._lst[int(key)]


class LineList(list):

    def __str__(self):
        s = [ str(x) for x in self ]
        return ('').join((x if x.endswith('\n') else x + '\n') for x in s)


def setTerminalEcho(enabled):
    if not Term_attr:
        return
    fd = sys.stdin.fileno()
    iflag, oflag, cflag, lflag, ispeed, ospeed, cc = termios.tcgetattr(fd)
    if enabled:
        lflag |= termios.ECHO
    else:
        lflag &= ~termios.ECHO
    new_attr = [
     iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
    termios.tcsetattr(fd, termios.TCSANOW, new_attr)


def getTerminalSize():
    """Return (lines:int, cols:int)"""
    if not Term_attr:
        return (25, 80)

    def ioctl_GWINSZ(fd):
        import fcntl
        return struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))

    for fd in (0, 1, 2):
        try:
            return ioctl_GWINSZ(fd)
        except Exception:
            pass

    try:
        fd = os.open(os.ctermid(), os.O_RDONLY)
        try:
            return ioctl_GWINSZ(fd)
        finally:
            os.close(fd)

    except Exception:
        pass

    try:
        return tuple(int(os.getenv(var)) for var in ('LINES', 'COLUMNS'))
    except Exception:
        pass

    return (25, 80)


def read_password(prompt='Password:'):
    """Read password, with no echo, from stdin"""
    setTerminalEcho(False)
    try:
        password = raw_input(prompt)
    except ValueError:
        raise EOFError

    sys.stdout.write('\n')
    setTerminalEcho(True)
    return password


def check_for_hold(self_arg):
    """Return callable function if self_arg has a hold, else return None."""
    return getattr(self_arg, OTrace.hold_attr, None)


def resume_from_hold(self_arg):
    if hasattr(self_arg, OTrace.resume_attr):
        callback = getattr(self_arg, OTrace.resume_attr)
        delattr(self_arg, OTrace.resume_attr)
        if callback:
            try:
                callback()
                return True
            except Exception:
                return False

    return False


class TraceInterpreter(object):
    """Class to execute code interactively using argument values as the local context."""

    def __init__(self):
        self.compile = codeop.CommandCompiler()

    def evaluate(self, expression, locals_dict={}, globals_dict={}, print_out=False):
        """ Evaluate expression; return output string, if print_out is True.

        Returns tuple (out_str, err_str), with err_str == "" for successful execution,
                                          and err_str == None for incomplete expression
        """
        _stdout = StringIO.StringIO()
        _stderr = StringIO.StringIO()
        locals_dict['_stdout'] = _stdout
        locals_dict['_stderr'] = _stderr
        prefix = 'print >>_stdout, ' if print_out else ''
        result = self.exec_source(prefix + expression, locals_dict=locals_dict, globals_dict=globals_dict)
        del locals_dict['_stdout']
        del locals_dict['_stderr']
        out_str = _stdout.getvalue()
        err_str = _stderr.getvalue()
        _stdout.close()
        _stderr.close()
        if result is None:
            return ('<Incomplete Expression>', None)
        else:
            return (
             out_str, err_str + result)

    def exec_source(self, source, filename='<input>', symbol='single', locals_dict={}, globals_dict={}):
        """Execute source code.

        Returns None if code is incomplete,
        null string on successful execution of code,
        or a string describing a syntax error or other exeception.
        All exceptions, excepting for SystemExit, are caught.
        """
        try:
            code = self.compile(source, filename, symbol)
        except (OverflowError, SyntaxError, ValueError):
            etype, value, last_traceback = sys.exc_info()
            return ('.').join(traceback.format_exception_only(etype, value))

        if code is None:
            return
        else:
            try:
                if globals_dict is locals_dict:
                    exec code in locals_dict
                else:
                    exec code in globals_dict, locals_dict
                return ''
            except SystemExit:
                raise
            except Exception:
                return format_traceback()

            return


class TraceConsole(object):
    """Console for trace interpreter (similar to code.interact).
    
    Runs in separate thread (as a daemon)
    """
    prompt1 = '> '
    prompt2 = '... '

    def __init__(self, globals_dict={}, locals_dict={}, banner=DEFAULT_BANNER, echo_callback=None, db_interface=None, web_interface=None, no_input=False, new_thread=False, _stdin=sys.stdin, _stdout=sys.stdout, _stderr=sys.stderr):
        """Create console instance.

        If echo_callback is specified, it should be a callable,
        and it will be called with stdout and stderr string data to echo output.
        If new_thread, a new (daemon) thread is created for TraceConsole,
        else TraceConsole runs in current thread, blocking it.
        """
        self.globals_dict = globals_dict
        self.locals_dict = locals_dict
        self.banner = banner
        self.echo_callback = echo_callback
        self.lazy_dirs = {PICKLED_DIR: PickleInterface}
        if db_interface:
            self.lazy_dirs[DATABASE_DIR] = db_interface
        self.web_interface = web_interface
        self.no_input = no_input
        self.thread = threading.Thread(target=self.run) if new_thread and not no_input else None
        if self.thread:
            self.thread.setDaemon(True)
        self.queue = None
        self.expect_run = False
        self._stdin = _stdin
        self._stdout = _stdout
        self._stderr = _stderr
        self.interpreter = TraceInterpreter()
        self.resetbuffer()
        self.feed_lines = []
        self.last_input_time = 0
        self.set_repeat(None)
        self.repeat_alt_screen = 0
        self.reading_stdin = False
        self.suspend_input = False
        self.shutting_down = False
        return

    def set_repeat(self, line=None):
        if line and Set_params['repeat_interval']:
            self.repeat_line = line
            self.repeat_count = REPEAT_COUNT
            self.repeat_interval = Set_params['repeat_interval']
        else:
            self.repeat_line = None
            self.repeat_count = 0
            self.repeat_interval = None
        return

    def has_trc(self, trace_attr):
        """ Return True if self.locals_dict[TRACE_INFO] has attribute."""
        return self.locals_dict and TRACE_INFO in self.locals_dict and trace_attr in self.locals_dict[TRACE_INFO]

    def get_trc(self, trace_attr, default=None):
        """ Return self.locals_dict[TRACE_INFO][trace_attr] or default."""
        if self.locals_dict and TRACE_INFO in self.locals_dict:
            return self.locals_dict[TRACE_INFO].get(trace_attr, default)
        else:
            return default

    def set_trc(self, trace_attr, value):
        """ Set self.locals_dict[TRACE_INFO][trace_attr] to value."""
        if TRACE_INFO not in self.locals_dict:
            self.locals_dict[TRACE_INFO] = {}
        self.locals_dict[TRACE_INFO][trace_attr] = value

    def loop(self, wait_to_run=False):
        """Start trace input loop.
        If wait_to_run, block until run command is issued in oshell.
        (wait_to_run requires new_thread or no_input)
        If not no_input, block until shutdown.
        """
        if wait_to_run:
            if not (self.thread or self.no_input):
                raise AssertionError
                self.queue = Queue.Queue()
                self.expect_run = True
            if self.thread:
                self.thread.start()
            else:
                self.run()
            return wait_to_run or None
        else:
            while not self.shutting_down:
                try:
                    run_args = self.queue.get(block=True, timeout=1)
                except Queue.Empty:
                    run_args = None

                if run_args:
                    self.expect_run = False
                    try:
                        try:
                            retval = run_args[0](run_args[1])
                            run_msg = 'Run completed'
                        except Exception as excp:
                            run_msg = 'Error in completed run\n' + format_traceback()

                    finally:
                        self.expect_run = True

                    OTrace.callback_handler.logmessage(None, run_msg)

            return

    def run(self):
        self.reading_stdin = not self.no_input
        self.display_banner()
        self.interact()

    def display_banner(self):
        banner = self.banner
        for msg in Banner_messages:
            banner += '\n' + msg

        banner += '\n  ^C to terminate program'
        self.std_output('%s\n' % str(banner))

    def resetbuffer(self):
        self.buffer = []

    @classmethod
    def invoke_debugger(cls, action='pdb'):
        if cls.instance:
            cls.instance.suspend_input = True
        if action == 'ipdb':
            try:
                import ipdb
                ipdb.set_trace()
            except ImportError:
                import pdb
                pdb.set_trace()

        else:
            import pdb
            pdb.set_trace()
        if cls.instance:
            cls.instance.suspend_input = False

    def interact(self):
        more = False
        noprompt = False
        while not self.shutting_down:
            try:
                if noprompt or self.repeat_interval:
                    prompt = ''
                else:
                    if more:
                        prompt = self.prompt2
                    else:
                        prompt = self.prompt1
                    try:
                        line = self.get_feed_line(prompt, echo=True)
                        if line is None:
                            if self.no_input:
                                return
                            if self.suspend_input:
                                self.std_output('***OShell suspended for pdb\n')
                                while self.suspend_input:
                                    time.sleep(1)

                            line = self.std_input(prompt, timeout=self.repeat_interval)
                            if self.repeat_interval:
                                if line is not None:
                                    self.set_repeat(None)
                                else:
                                    line = self.repeat_line
                                    self.repeat_count -= 1
                                    if self.repeat_count <= 0:
                                        self.set_repeat(None)
                            if line is None:
                                continue
                    except EOFError:
                        self.std_output('\n')
                        break

                    try:
                        noprompt, more, out_str, err_str = self.parse_out(line, more, echo=True)
                    except Exception:
                        self.err_output(format_traceback())

            except KeyboardInterrupt:
                if not self.thread:
                    raise
                self.resetbuffer()
                more = False
                self.std_output('\nKeyboardInterrupt: Type Control-D to quit\n')

        self.shutdown()
        return

    def get_feed_line(self, prompt='', echo=False):
        """Return next feed line, or None, echoing it if need be"""
        if not self.feed_lines:
            return None
        else:
            line = self.feed_lines.pop(0)
            if line and line[(-1)] == '\n':
                line = line[:-1]
            if line and line[(-1)] == '\r':
                line = line[:-1]
            if line.startswith('noecho '):
                line = line[len('noecho '):]
            elif echo:
                self.std_output(prompt + line + '\n')
            return line

    def parse_out(self, line, more=False, echo=False):
        """Parse line and optionally echo execution result,
        returning (noprompt, more, out_str, err_str)
        """
        out_str, err_str = self.parse(line, batch=bool(self.repeat_interval))
        if out_str == '_NoPrompt_':
            noprompt = True
            out_str = None
        else:
            noprompt = False
            if self.repeat_interval:
                if err_str:
                    self.set_repeat(None)
                elif out_str:
                    out_str = CLEAR_SCREEN_SEQUENCE + out_str
                    if self.repeat_alt_screen == 1:
                        self.repeat_alt_screen = 2
                        out_str = ALT_SCREEN_ONSEQ + out_str
            elif self.repeat_alt_screen == 2:
                self.repeat_alt_screen = 0
                out_str = ALT_SCREEN_OFFSEQ + out_str
            more = err_str is None
            if echo and out_str and not more:
                if out_str[(-1)] == '\n':
                    self.std_output(out_str)
                else:
                    self.std_output(out_str + '\n')
        if echo and err_str:
            self.err_output(err_str + '\n')
        return (noprompt, more, out_str, err_str)

    def stuff_lines(self, lines):
        """Accept list of lines for processing as input (skipping lines starting with '#')"""
        self.feed_lines += [ line for line in lines if line.strip() and line.strip()[0] != '#' ]

    def close(self):
        """Closes console input (thread-safe)."""
        if not self.reading_stdin:
            return
        try:
            self._stdin.close()
        except Exception:
            pass

    def shutdown(self):
        if self.shutting_down:
            return
        self.shutting_down = True
        if self.thread:
            if self.thread.isAlive():
                try:
                    self.thread._Thread__stop()
                    print >> sys.stderr, 'Killed TraceConsole thread'
                except Exception:
                    pass

            if Term_attr:
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, Term_attr)

    def switch_screen(self, logtype=''):
        """Return (prefix, suffix) escape sequences for alt screen switching"""
        if logtype != 'trace':
            if self.repeat_alt_screen == 2:
                return (ALT_SCREEN_OFFSEQ, ALT_SCREEN_ONSEQ)
            else:
                return ('', '')

        if self.repeat_interval:
            self.set_repeat(None)
        if self.repeat_alt_screen == 2:
            self.repeat_alt_screen = 0
            return (
             ALT_SCREEN_OFFSEQ, '')
        else:
            return ('', '')
            return

    def parse(self, line):
        return self.push(line)

    def push(self, line, batch=False):
        """Execute command line.

        The line should not have a trailing newline; it may have internal newlines.
        Returns (out_str, err_str)
        If batch, a complete line of non-interactive expression is evaluated,
        without outputting to stdout.
        If not batch, output is sent to stdout.
        out_str is None if not batch, else it contains the evaluated expression output.
        err_str is None if code is incomplete,
                is null string on successful execution of code,
                or a string describing a syntax error or other exeception.
        """
        if not Set_params['exec_lock']:
            return self.push_aux(line, batch=batch)
        with Trace_rlock:
            return self.push_aux(line, batch=batch)

    def push_aux(self, line, batch=False):
        if batch:
            self.resetbuffer()
            out_str, err_str = self.interpreter.evaluate(line, locals_dict=self.locals_dict, globals_dict=self.globals_dict, print_out=True)
        else:
            self.buffer.append(line)
            source = ('\n').join(self.buffer)
            out_str = None
            err_str = self.interpreter.exec_source(source, locals_dict=self.locals_dict, globals_dict=self.globals_dict)
            if err_str is not None:
                self.resetbuffer()
        return (
         out_str, err_str)

    def std_output(self, data, flush=False):
        self._stdout.write(data)
        if self.echo_callback:
            self.echo_callback(data)
        if flush:
            self._stdout.flush()

    def err_output(self, data, flush=False):
        self._stderr.write(data)
        if self.echo_callback:
            self.echo_callback(data)
        if flush:
            self._stderr.flush()

    def std_input(self, prompt='', timeout=None):
        """Override for a different input source.
        If not timeout and sys.stdin, use raw_input, else use select.
        Returns None on timeout and raises EOFError on close
        """
        if Set_params['auto_lock'] and not timeout:
            timeout = Set_params['auto_lock']
        if not timeout and self._stdin is sys.stdin:
            try:
                input_data = raw_input(prompt)
            except ValueError:
                raise EOFError

            self.last_input_time = time.time()
            return input_data
        else:
            if prompt:
                self._stdout.write(prompt)
                self._stdout.flush()
            read_list, _, _ = select.select([self._stdin], [], [], timeout)
            if read_list:
                self.last_input_time = time.time()
                return self._stdin.readline()
            if Set_params['password'] and Set_params['auto_lock'] and time.time() - self.last_input_time > Set_params['auto_lock']:
                return 'lock\n'
            return
            return


class OShell(TraceConsole):
    """Object-oriented shell
    """
    html_fmt = '<span class="gterm-link" data-gtermuri="%s" data-gtermmime="%s" data-gtermcmd="%s">%s</span>'
    commands = {'alias': 'alias name command <arg\\*> <arg\\1>... # Define alias name for command\n\nalias name                            # Display alias for name\nalias name ""                         # Clear alias for name\n', 
       'cd': 'cd [path]                 # Change current working directory to "path"\n\nSpecial paths: ".."=>parent, "/"=>root, "~"=>home, "~~"=>most recent trace,\n               "~~g"=>/osh/globals, "~~w"=>work directory\nIf current directory is /osh/*, user input is interpreted as oshell commands.\nIf current directory is not /osh/*, user input is interpreted as unix shell commands.\n\nIf no path is specified, current default path is used, as determined below:\nIf in a trace context (/osh/recent/*), the default path is the topmost directory of the trace context.\nIf in /osh/*, the default path is /osh/globals.\nIf not in /osh/*, the default path is the user\'s home directory (~).\n', 
       'cdls': 'cdls [pathname]           # cd to "pathname" and list "files" (cd+ls)', 
       'del': 'del [trace_id1..]         # Delete trace context', 
       'dn': 'dn                        # Command alias to move one level down in stack frames in a trace context (to a newer frame)', 
       'edit': 'edit [-f] (filename|class[.method]) [< readfile]  # Edit/patch file/method/function\n\nNames of patched methods are saved is /osh/patches.\nSpecify "-f" option to modify already patched code.\nIf readfile is specified for input redirection, read text from file to patch code.\n', 
       'exec': 'exec python_code          # Execute python code (also ' + EXEC_PREFIX + '<python_code>) ', 
       'help': 'help [command|*]          # Display help information\n\nhelp *                    # Help info on all commands\nhelp command              # Help info on command\n', 
       'lock': 'lock                      # Lock terminal until password is entered', 
       'ls': 'ls [-acflmtv] [-(.|..|.baseclass)] [pathname1|*]   # List pathname values (or all pathnames in current "directory")\n\npathname can be omitted or include simple shell wildcard patterns (e.g., "*", "abc*", ...)\n-a List special attributes of the form __*__\n-c List classes\n-f List function/method names\n-l "Long listing" => name=value ...\n-m List modules\n-t Order trace context listing by time\n-v List variables\n\n-.  Exclude attributes of current class\n-.. Exclude attributes of parent class\n-<baseclass> Exclude attributes of baseclass\n', 
       'popd': 'popd [-a]                 # Pop directory stack and revert to previous directory', 
       'pr': 'pr python_expression      # Print value of expression (DEFAULT COMMAND)\n\nThe command prefix "pr" may be omitted, and is assumed by default.\n', 
       'pushd': 'pushd [path]              # Push current directory into stack and cd to path', 
       'pwd': 'pwd [-a]                  # Print current working "directory"\n\n-a Print all paths in stack; top first\n', 
       'quit': 'quit                      # Quit shell', 
       'repeat': 'repeat command            # Repeat command till new user input is received', 
       'resume': 'resume [trace_id1..]      # Resume from breakpoint', 
       'rm': 'rm [-r] [pathname1..]     # Delete entities corresponding to pathnames (if supported)\n\n-r   recursive remove all child entities\n', 
       'run': 'run function [arg1 ...]   # Run function in main thread with optional string list argument\n', 
       'save': 'save [trace_id1..]        # Save current or specified trace context\n\nThe trace context is saved to /osh/saved\n', 
       'set': 'set [parameter [value]]   # Set (or display) parameter\n\nset                       # Display all parameter values\nset parameter             # Display current value of parameter\nset parameter ""          # Clear parameter value\n\nPARAMETERS', 
       'source': 'source filename           # Read commands from file', 
       'swapd': 'swapd                     # Swap current work dir with top of directory stack', 
       'tag': 'tag [(object|.) [tag_str|id|time]]    # Tag object for tracing (default tag: id(object))', 
       'trace': "trace [-a (break|ipdb|pdb|hold|tag)] [-c call|return|all|tag|comma_sep_arg_match_conditions] [-n +/-count] ([class.][method]|db_key|*)   # Enable tracing for class/method/key on matching condition\n\n-a break|ipdb|pdb|hold|tag   Action to be taken when trace condition is satisfied:\n     break => stop until resume command\n     ipdb => start ipdb\n     pdb => start pdb\n     hold => asynchronously hold this request (if supported)\n     tag => tag self argument on method return using a string describing matched trace conditions\n-c call|return|all|tag|comma_sep_arg_match_conditions   Condition to match for tracing:\n     call => before function call,\n     return => after function return,\n     all => before call and and after return,\n     tagged[argname] => match if any (or argname) argument has a tag\n     argname1.comp1==value1,argname2!=value2,... => on argument value match (values with commas/spaces must be quoted; the special argument name 'return' may also be used)\n-n +/-count   If count > 0, stop tracing after count matches; if count > 0, start tracing after -count matches\n", 
       'unpatch': 'unpatch class[.method]|* [> savefile]  # Unpatch method (and save patch to file)\n\nIn directory /osh/patches, "unpatch *" will unpatch all currently patched methods.\n', 
       'unpickle': 'unpickle filename [field=value]        # Read pickled trace contexts from file ', 
       'untag': 'untag [object|.]          # Untag object', 
       'untrace': 'untrace ([class.][method]|*|all)  # Disable tracing for class/method', 
       'up': 'up                        # Command alias to move one level up in stack frames in a trace context (to an older frame)', 
       'view': 'view [-d] [-i] [class/method/file]  # Display source/doc using editor for objects/traces/files\n\n-d  Display docstring only\n-i  Display output inline, i.e., without using an editor.\n'}
    instance = None

    def __new__(cls, *args, **kwargs):
        cls.instance = super(OShell, cls).__new__(cls)
        return cls.instance

    def __init__--- This code section failed: ---

 L.1445         0  LOAD_FAST             6  'work_dir'
                3  UNARY_NOT        
                4  POP_JUMP_IF_TRUE     28  'to 28'
                7  LOAD_GLOBAL           0  'is_absolute_path'
               10  LOAD_FAST             6  'work_dir'
               13  CALL_FUNCTION_1       1  None
               16  POP_JUMP_IF_TRUE     28  'to 28'
               19  LOAD_ASSERT              AssertionError
               22  LOAD_CONST               'work_dir must be an absolute path'
               25  RAISE_VARARGS_2       2  None

 L.1447        28  LOAD_GLOBAL           2  'super'
               31  LOAD_GLOBAL           3  'OShell'
               34  LOAD_FAST             0  'self'
               37  CALL_FUNCTION_2       2  None
               40  LOAD_ATTR             4  '__init__'
               43  LOAD_CONST               'globals_dict'
               46  LOAD_FAST             1  'globals_dict'
               49  LOAD_CONST               'locals_dict'
               52  LOAD_FAST             2  'locals_dict'
               55  LOAD_CONST               'banner'

 L.1448        58  LOAD_FAST             8  'banner'
               61  LOAD_CONST               'echo_callback'
               64  LOAD_FAST            11  'echo_callback'
               67  LOAD_CONST               'db_interface'

 L.1449        70  LOAD_FAST            12  'db_interface'
               73  LOAD_CONST               'web_interface'
               76  LOAD_FAST            13  'web_interface'
               79  LOAD_CONST               'no_input'

 L.1450        82  LOAD_FAST             9  'no_input'
               85  LOAD_CONST               'new_thread'
               88  LOAD_FAST            10  'new_thread'
               91  LOAD_CONST               '_stdin'

 L.1451        94  LOAD_FAST            16  '_stdin'
               97  LOAD_CONST               '_stdout'
              100  LOAD_FAST            17  '_stdout'
              103  LOAD_CONST               '_stderr'
              106  LOAD_FAST            18  '_stderr'
              109  CALL_FUNCTION_2816  2816  None
              112  POP_TOP          

 L.1452       113  LOAD_FAST             3  'init_func'
              116  LOAD_FAST             0  'self'
              119  STORE_ATTR            5  'init_func'

 L.1453       122  LOAD_FAST             4  'init_file'
              125  LOAD_FAST             0  'self'
              128  STORE_ATTR            6  'init_file'

 L.1454       131  LOAD_FAST             5  'allow_unsafe'
              134  LOAD_FAST             0  'self'
              137  STORE_ATTR            7  'allow_unsafe'

 L.1455       140  LOAD_FAST             6  'work_dir'
              143  LOAD_FAST             0  'self'
              146  STORE_ATTR            8  'work_dir'

 L.1456       149  LOAD_FAST             7  'add_env'
              152  LOAD_FAST             0  'self'
              155  STORE_ATTR            9  'add_env'

 L.1458       158  LOAD_FAST            14  'hold_wrapper'
              161  POP_JUMP_IF_FALSE   176  'to 176'

 L.1459       164  LOAD_FAST            14  'hold_wrapper'
              167  LOAD_GLOBAL          10  'OTrace'
              170  STORE_ATTR           11  'hold_wrapper'
              173  JUMP_FORWARD          0  'to 176'
            176_0  COME_FROM           173  '173'

 L.1461       176  LOAD_FAST            15  'eventloop_callback'
              179  POP_JUMP_IF_FALSE   194  'to 194'

 L.1462       182  LOAD_FAST            15  'eventloop_callback'
              185  LOAD_GLOBAL          10  'OTrace'
              188  STORE_ATTR           12  'eventloop_callback'
              191  JUMP_FORWARD          0  'to 194'
            194_0  COME_FROM           191  '191'

 L.1464       194  LOAD_FAST             1  'globals_dict'
              197  LOAD_GLOBAL          10  'OTrace'
              200  LOAD_ATTR            13  'base_context'
              203  LOAD_GLOBAL          14  'GLOBALS_DIR'
              206  STORE_SUBSCR     

 L.1465       207  LOAD_FAST             2  'locals_dict'
              210  LOAD_GLOBAL          10  'OTrace'
              213  LOAD_ATTR            13  'base_context'
              216  LOAD_GLOBAL          15  'LOCALS_DIR'
              219  STORE_SUBSCR     

 L.1466       220  BUILD_MAP_0           0  None
              223  LOAD_GLOBAL          10  'OTrace'
              226  LOAD_ATTR            13  'base_context'
              229  LOAD_GLOBAL          16  'PICKLED_DIR'
              232  STORE_SUBSCR     

 L.1468       233  LOAD_GLOBAL          17  'Queue'
              236  LOAD_ATTR            17  'Queue'
              239  CALL_FUNCTION_0       0  None
              242  LOAD_FAST             0  'self'
              245  STORE_ATTR           18  'break_queue'

 L.1469       248  LOAD_GLOBAL          19  'OrderedDict'
              251  CALL_FUNCTION_0       0  None
              254  LOAD_FAST             0  'self'
              257  STORE_ATTR           20  'break_events'

 L.1471       260  BUILD_MAP_10         10  None

 L.1472       263  LOAD_CONST               'cd'
              266  LOAD_GLOBAL          21  'ENTITY_CHAR'
              269  BUILD_LIST_2          2 
              272  LOAD_CONST               'cde'
              275  STORE_MAP        

 L.1473       276  LOAD_CONST               'cd'
              279  LOAD_GLOBAL          22  'TRACE_INFO'
              282  BUILD_LIST_2          2 
              285  LOAD_CONST               'cdt'
              288  STORE_MAP        

 L.1474       289  LOAD_CONST               'cd'
              292  LOAD_GLOBAL          23  'DOWN_STACK'
              295  BUILD_LIST_2          2 
              298  LOAD_CONST               'dn'
              301  STORE_MAP        

 L.1475       302  LOAD_CONST               'cd'
              305  LOAD_GLOBAL          23  'DOWN_STACK'
              308  LOAD_CONST               ';'
              311  LOAD_CONST               'view'
              314  LOAD_CONST               '-i'
              317  BUILD_LIST_5          5 
              320  LOAD_CONST               'dv'
              323  STORE_MAP        

 L.1476       324  LOAD_CONST               'view'
              327  LOAD_CONST               '-d'
              330  LOAD_CONST               '-i'
              333  BUILD_LIST_3          3 
              336  LOAD_CONST               'doc'
              339  STORE_MAP        

 L.1477       340  LOAD_CONST               'exec'
              343  LOAD_CONST               'import'
              346  LOAD_CONST               'os'
              349  LOAD_CONST               ';'
              352  LOAD_CONST               'import'
              355  LOAD_CONST               'signal'
              358  LOAD_CONST               ';'
              361  LOAD_CONST               'os.kill(os.getpid(),signal.SIGINT)'
              364  BUILD_LIST_8          8 
              367  LOAD_CONST               'interrupt'
              370  STORE_MAP        

 L.1478       371  LOAD_CONST               'ls'
              374  LOAD_CONST               '-C'
              377  BUILD_LIST_2          2 
              380  LOAD_CONST               'ls'
              383  STORE_MAP        

 L.1479       384  LOAD_CONST               'view'
              387  LOAD_CONST               '-i'
              390  BUILD_LIST_2          2 
              393  LOAD_CONST               'show'
              396  STORE_MAP        

 L.1480       397  LOAD_CONST               'cd'
              400  LOAD_GLOBAL          24  'UP_STACK'
              403  BUILD_LIST_2          2 
              406  LOAD_CONST               'up'
              409  STORE_MAP        

 L.1481       410  LOAD_CONST               'cd'
              413  LOAD_GLOBAL          24  'UP_STACK'
              416  LOAD_CONST               ';'
              419  LOAD_CONST               'view'
              422  LOAD_CONST               '-i'
              425  BUILD_LIST_5          5 
              428  LOAD_CONST               'uv'
              431  STORE_MAP        
              432  LOAD_FAST             0  'self'
              435  STORE_ATTR           25  'aliases'

 L.1486       438  LOAD_GLOBAL          26  'BASE_DIR'
              441  LOAD_GLOBAL          10  'OTrace'
              444  LOAD_ATTR            13  'base_context'
              447  BUILD_TUPLE_2         2 

 L.1487       450  LOAD_GLOBAL          14  'GLOBALS_DIR'
              453  LOAD_FAST             1  'globals_dict'
              456  BUILD_TUPLE_2         2 
              459  BUILD_LIST_2          2 
              462  LOAD_FAST             0  'self'
              465  STORE_ATTR           27  'cur_fullpath'

 L.1489       468  BUILD_LIST_0          0 
              471  LOAD_FAST             0  'self'
              474  STORE_ATTR           28  'dir_stack'

 L.1490       477  BUILD_LIST_0          0 
              480  LOAD_FAST             0  'self'
              483  STORE_ATTR           29  '_completion_list'

 L.1492       486  LOAD_FAST             0  'self'
              489  LOAD_ATTR            30  'update_terminal_size'
              492  CALL_FUNCTION_0       0  None
              495  POP_TOP          

 L.1493       496  LOAD_GLOBAL          31  'readline'
              499  POP_JUMP_IF_FALSE   534  'to 534'

 L.1494       502  LOAD_GLOBAL          31  'readline'
              505  LOAD_ATTR            32  'set_completer'
              508  LOAD_FAST             0  'self'
              511  LOAD_ATTR            33  'completer'
              514  CALL_FUNCTION_1       1  None
              517  POP_TOP          

 L.1495       518  LOAD_GLOBAL          31  'readline'
              521  LOAD_ATTR            34  'parse_and_bind'
              524  LOAD_CONST               'tab: complete'
              527  CALL_FUNCTION_1       1  None
              530  POP_TOP          
              531  JUMP_FORWARD          0  'to 534'
            534_0  COME_FROM           531  '531'

Parse error at or near `JUMP_FORWARD' instruction at offset 531

    def loop(self, wait_to_run=False):
        """Start input loop for OShell."""
        super(OShell, self).loop(wait_to_run=wait_to_run)

    def run(self):
        if self.init_func:
            self.init_func(self)
        db_interface = self.lazy_dirs.get(DATABASE_DIR)
        if db_interface:
            OTrace.set_database_root(db_interface.get_root_tree())
            db_interface.set_access_hook(OTrace.access_hook)
        if self.web_interface:
            OTrace.set_web_root(self.web_interface.get_root_tree())
            self.web_interface.set_web_hook(OTrace.web_hook)
        if self.init_file:
            filename = expandpath(self.init_file)
            if os.path.exists(filename):
                self.stuff_lines(["source '%s'\n" % filename])
        super(OShell, self).run()

    def get_prompt(self):
        """Return (prompt, cur_dir_path)."""
        return (
         self.prompt1, self.make_path_str())

    def get_main_module(self):
        return sys.modules[self.globals_dict['__name__']]

    def in_base_dir(self):
        return bool(self.cur_fullpath and self.cur_fullpath[0][INAME] == BASE_DIR)

    def get_base_subdir(self):
        if self.in_base_dir() and len(self.cur_fullpath) > BASE_OFFSET:
            return self.cur_fullpath[BASE_OFFSET][INAME]
        return ''

    def get_leaf_dir(self):
        if not self.cur_fullpath:
            return ''
        return self.cur_fullpath[(-1)][INAME]

    def get_leaf_dict(self):
        if not self.cur_fullpath:
            return None
        else:
            return self.cur_fullpath[(-1)][ISUBDIR]

    def get_cur_value(self):
        """ Return value corresponding to current directory
        """
        if len(self.cur_fullpath) > BASE2_OFFSET - 1:
            return self.get_subdir(self.cur_fullpath[(-2)][ISUBDIR], [self.cur_fullpath[(-1)][INAME]], value=True)
        else:
            if len(self.cur_fullpath) == BASE2_OFFSET - 1 and self.get_base_subdir() == GLOBALS_DIR:
                return self.get_main_module()
            else:
                return

            return

    def get_parent_value(self):
        """ Return value corresponding to parent of current directory
        """
        if len(self.cur_fullpath) > BASE2_OFFSET:
            return self.get_subdir(self.cur_fullpath[(-3)][ISUBDIR], [self.cur_fullpath[(-2)][INAME]], value=True)
        else:
            if len(self.cur_fullpath) == BASE2_OFFSET and self.get_base_subdir() == GLOBALS_DIR:
                return self.get_main_module()
            else:
                return

            return

    def get_context_path(self):
        if len(self.cur_fullpath) >= TRACE_OFFSET and self.get_base_subdir() in (RECENT_DIR, SAVED_DIR):
            return self.cur_fullpath[:TRACE_OFFSET]
        if len(self.cur_fullpath) >= BASE2_OFFSET and self.get_base_subdir() == ALL_DIR:
            return self.cur_fullpath[:BASE2_OFFSET]
        return []

    def get_db_root_path(self):
        base_subdir = self.get_base_subdir()
        if base_subdir in self.lazy_dirs and len(self.cur_fullpath) >= self.lazy_dirs[base_subdir].root_depth + BASE1_OFFSET:
            return self.cur_fullpath[:self.lazy_dirs[base_subdir].root_depth + BASE1_OFFSET]
        return []

    def get_web_path(self):
        if self.web_interface and len(self.cur_fullpath) > BASE1_OFFSET and self.get_base_subdir() == WEB_DIR:
            return [ x[0] for x in self.cur_fullpath[BASE1_OFFSET:] ]
        return []

    def make_path_str(self, path=None, relative=False):
        """Creates path string from single or tuple components"""
        if path is None:
            path = self.cur_fullpath
        if not path:
            return PATH_SEP
        else:
            if isinstance(path[0], (list, tuple)):
                path_str = PATH_SEP.join(str(x[INAME]) for x in path)
            else:
                path_str = PATH_SEP.join(str(x) for x in path)
            if relative:
                return path_str
            return PATH_SEP + path_str

    def read_file(self, filename):
        """Reads and executes commands from file.
        Returns null string on success, or error
        """
        try:
            with open(os_path(filename), 'r') as (f):
                self.stuff_lines(f.readlines())
            return ''
        except Exception:
            return "Error in reading from '%s'" % filename

    def update_terminal_size(self):
        tty_size = getTerminalSize()
        if not tty_size:
            tty_size = (24, 80)
        self.tty_width = tty_size[1]

    def completer(self, text, state, line=None, all=False):
        """Handle TAB completion: text is the partial "filename"; return completion list.
        """
        if not readline:
            return []
        if state > 0:
            if state < len(self._completion_list):
                return self._completion_list[state]
            else:
                return

        if line is None:
            line = readline.get_line_buffer()
        if line.startswith(EXEC_PREFIX):
            line = 'exec ' + line[len(EXEC_PREFIX):]
        comps = shlex.split(line)
        if comps:
            if comps[0] in self.commands or comps[0] in self.aliases:
                cmd = comps[0]
            else:
                cmd = 'pr'
                line = cmd + ' ' + line
                comps = [cmd] + comps
        else:
            cmd = ''
        prefix = expanduser(comps[(-1)]) if comps else ''
        preline = line[:len(line) - len(text)].strip()
        if cmd in self.aliases:
            actual_cmd = self.aliases[cmd][0]
        else:
            actual_cmd = cmd
        if not preline:
            cmd_keys = self.commands.keys()
            cmd_keys.sort()
            self._completion_list = [ s for s in cmd_keys if s and s.startswith(text) ]
        elif cmd == 'set' and len(comps) == 2:
            tem_list = [ key for key in Set_params if key.startswith(prefix) ]
            tem_list.sort()
            self._completion_list = [ x[len(prefix) - len(text):] for x in tem_list ]
        elif PATH_SEP not in prefix and prefix.find('..') == -1 and self.get_base_subdir() in (GLOBALS_DIR, LOCALS_DIR):
            path_list = (prefix + '*').split('.')
            tem_list = self.path_matches(self.cur_fullpath, path_list, delimiter='.', completion=True)
            self._completion_list = [ x[len(prefix) - len(text):] for x in tem_list ]
        else:
            path_list = (prefix + '*').split(PATH_SEP)
            if is_absolute_path(prefix):
                offset = 1
                path_list = path_list[1:]
                cur_fullpath = []
            else:
                offset = 0
                cur_fullpath = self.cur_fullpath
            tem_list = self.path_matches(cur_fullpath, path_list, completion=True)
            self._completion_list = [ x[1:] if is_absolute_path(x) else x[len(prefix) - len(text) - offset:] for x in tem_list ]
            self._completion_list = [ x.replace(' ', '\\ ') for x in self._completion_list ]
        if all:
            return self._completion_list
        else:
            if state < len(self._completion_list):
                return self._completion_list[state]
            else:
                return

            return

    def full_path_comps(self, new_dir):
        """ Given new path (absolute or relative), returns list of full path components
        """
        if not new_dir:
            return new_dir
        new_path = new_dir.split(PATH_SEP)
        if not new_path[(-1)]:
            new_path = new_path[-1:]
        if not new_path[0]:
            new_path = new_path[1:]
        else:
            cur_path = [ comp[INAME] for comp in self.cur_fullpath ]
            while cur_path and new_path and new_path[0] in ('.', '..'):
                if new_path[0] == '..':
                    cur_path = cur_path[:-1]
                new_path = new_path[1:]

            new_path = cur_path + new_path
        return new_path

    def get_rel_dir(self, new_dir):
        """ Given new absolute path, returns relative path
        """
        cur_path = [ comp[INAME] for comp in self.cur_fullpath ]
        if not new_dir:
            return PATH_SEP + PATH_SEP.join(cur_path)
        if not is_absolute_path(new_dir):
            return new_dir
        full_path = self.full_path_comps(new_dir)
        nmatch = 0
        while nmatch < min(len(cur_path), len(full_path)):
            if cur_path[nmatch] != full_path[nmatch]:
                break
            nmatch += 1

        new_path = ['..'] * max(0, len(cur_path) - nmatch)
        if nmatch < len(full_path):
            new_path += full_path[nmatch:]
        return PATH_SEP.join(new_path)

    def entity_path_comps(self, full_path):
        indx = full_path.index(ENTITY_CHAR)
        key_comps = full_path[:indx]
        sub_comps = full_path[indx + 1:]
        base_subdir = full_path[BASE_OFFSET]
        if base_subdir in self.lazy_dirs:
            entity_key = self.lazy_dirs[base_subdir].key_from_path(key_comps[BASE1_OFFSET:])
        else:
            entity_key = None
        return (
         key_comps, sub_comps, entity_key)

    def get_default_dir(self):
        if self.in_base_dir():
            context_path = self.get_context_path()
            db_root_path = self.get_db_root_path()
            if context_path:
                default_dir = context_path
            elif db_root_path:
                default_dir = db_root_path
            else:
                default_dir = [
                 (
                  BASE_DIR, OTrace.base_context),
                 (
                  GLOBALS_DIR, OTrace.base_context[GLOBALS_DIR])]
        else:
            default_dir = []
            dir_path = os.path.expanduser('~')
            pathnames = dir_path.split(PATH_SEP)[1:]
            for j, name in enumerate(pathnames):
                sub_path = pathnames[:j + 1]
                subdir = self.get_subdir('root', path_list=sub_path)
                default_dir.append((name, subdir))

        return default_dir[:]

    def change_workdir(self, workdir=None):
        """Changes working directory, returning null string on success,
        or error message string
        """
        if workdir:
            workdir = workdir.strip()
        tail_path = ''
        if not workdir:
            self.cur_fullpath = self.get_default_dir()
        elif workdir == PATH_SEP:
            self.cur_fullpath = []
        elif workdir == PATH_SEP + BASE_DIR:
            self.cur_fullpath = [(BASE_DIR, OTrace.base_context)]
        else:
            path_list = workdir.split(PATH_SEP)
            if not path_list[0]:
                if len(path_list) > 1 and path_list[1] == BASE_DIR:
                    path_list.pop(0)
                    self.cur_fullpath = [(BASE_DIR, OTrace.base_context)]
                else:
                    self.cur_fullpath = []
            elif path_list[0] == BASE_DIR and not self.cur_fullpath:
                self.cur_fullpath = [(BASE_DIR, OTrace.base_context)]
            elif path_list[0] == '.':
                pass
            elif path_list[0] == '..':
                if self.cur_fullpath:
                    self.cur_fullpath.pop()
            else:
                matches = self.path_matches(self.cur_fullpath, path_list=path_list[0:1])
                if not matches:
                    return "Failed to change to directory '%s'" % path_list[0]
                if len(matches) > 1:
                    return "Ambiguous directory change '%s'" % path_list[0]
                subdir = self.get_subdir(self.locals_dict, [matches[0]])
                if subdir is None:
                    return "Stale directory '%s'" % matches[0]
                self.cur_fullpath.append((matches[0], subdir))
            tail_path = PATH_SEP.join(path_list[1:])
        if self.in_base_dir():
            if len(self.cur_fullpath) > BASE_OFFSET:
                self.locals_dict = self.get_leaf_dict()
            else:
                self.locals_dict = OTrace.base_context
        elif self.cur_fullpath:
            self.locals_dict = self.get_leaf_dict()
        else:
            self.locals_dict = self.get_subdir('root')
        if tail_path:
            return self.change_workdir(tail_path)
        else:
            return ''
            return

    def update_prompt(self):
        if not self.cur_fullpath:
            self.prompt1 = '/> '
        elif len(self.cur_fullpath) == TRACE_OFFSET and self.get_base_subdir() in (RECENT_DIR, SAVED_DIR):
            class_prefix = self.cur_fullpath[BASE2_OFFSET][INAME]
            time_suffix = self.cur_fullpath[(BASE2_OFFSET + 2)][INAME][7:]
            if '.' in class_prefix:
                class_prefix = class_prefix[:class_prefix.find('.')]
            self.prompt1 = '%s..%s> ' % (class_prefix, time_suffix)
        else:
            prompt = self.get_leaf_dir()
            if prompt in (UP_STACK, DOWN_STACK) and self.has_trc('funcname'):
                prompt = self.get_trc('funcname')
            if self.get_web_path() and len(self.cur_fullpath) > BASE1_OFFSET:
                self.prompt1 = 'web..%s> ' % (prompt,)
            elif self.in_base_dir() and len(self.cur_fullpath) > BASE1_OFFSET:
                self.prompt1 = '%s..%s> ' % (BASE_DIR, prompt)
            else:
                self.prompt1 = '%s> ' % (prompt,)
        if self.break_events:
            self.prompt1 = 'BRK:' + self.prompt1

    def get_subdir(self, cur_dir='base', path_list=[], value=False):
        """Returns dictionary corresponding to subdirectory, or None, if unable to do so
        If value==True, return value corresponding to path, instead.
        """
        if value and not path_list:
            return cur_dir
        else:
            if cur_dir is None:
                cur_dir = {}
            else:
                if cur_dir == 'base':
                    cur_dir = OTrace.base_context
                else:
                    if cur_dir == 'root' or isinstance(cur_dir, OSDirectory):
                        dir_path = PATH_SEP if cur_dir == 'root' else cur_dir.path
                        cur_dir = dict((subdir_name, OSDirectory(dir_path + PATH_SEP + subdir_name)) for subdir_name in os.listdir(dir_path))
                        if dir_path == PATH_SEP:
                            cur_dir[BASE_DIR] = OTrace.base_context
                    elif isinstance(cur_dir, (list, tuple)):
                        cur_dir = ListDict(cur_dir)
                    elif isinstance(cur_dir, dict):
                        if 0 and any(isinstance(key, basestring) and (PATH_SEP in key or ' ' in key) for key in cur_dir):
                            cur_dir = dict((key.replace(PATH_SEP, '%').replace(' ', '_') if isinstance(key, basestring) else key, value) for key, value in cur_dir.items())
                    elif not isinstance(cur_dir, (MappingDict, weakref.WeakValueDictionary)):
                        cur_dir = ObjectDict(cur_dir)
                    if not path_list:
                        return cur_dir
                sub_dir = None
                if path_list[0] in cur_dir:
                    try:
                        sub_dir = cur_dir[path_list[0]]
                    except Exception:
                        return

                elif path_list[0].isdigit() and int(path_list[0]) in cur_dir:
                    try:
                        sub_dir = cur_dir[int(path_list[0])]
                    except Exception:
                        return

                if sub_dir is None:
                    return
            return self.get_subdir(sub_dir, path_list[1:], value=value)

    def path_matches(self, cur_fullpath, path_list, delimiter=PATH_SEP, sort=True, absolute=False, completion=False):
        """Returns list of matching paths (including simple wildcards)
        for specified context
        """
        if cur_fullpath:
            locals_dict = cur_fullpath[(-1)][ISUBDIR]
        else:
            locals_dict = self.get_subdir('root')
        if not path_list:
            matches = locals_dict.keys()
            matches.sort()
            if absolute:
                matches = [ delimiter + x for x in matches ]
            return matches
        if path_list[0] == '.':
            return self.path_matches(cur_fullpath, path_list[1:], delimiter=delimiter, sort=sort, absolute=absolute, completion=completion)
        if path_list[0] == GLOBALS_PREFIX:
            matches = self.path_matches([(BASE_DIR, OTrace.base_context),
             (
              GLOBALS_DIR, OTrace.base_context[GLOBALS_DIR])], path_list[1:], delimiter=delimiter, sort=sort, absolute=absolute, completion=completion)
            return [ GLOBALS_PREFIX + delimiter + x for x in matches ]
        if path_list[0] == '..':
            if cur_fullpath:
                new_path_list = [ x[INAME] for x in cur_fullpath[:-1] ] + path_list[1:]
                parent_prefix = delimiter + delimiter.join(x[INAME] for x in cur_fullpath[:-1]) if len(cur_fullpath) > 1 else ''
            else:
                new_path_list = path_list[1:]
                parent_prefix = ''
            matches = self.path_matches([], new_path_list, delimiter=delimiter, sort=sort, absolute=True, completion=completion)
            if completion:
                return [ '..' + x[len(parent_prefix):] for x in matches ]
            return matches
        matches = []
        for key in locals_dict.keys():
            first_dir = path_list[0]
            matched = first_dir == key or first_dir.isdigit() and int(first_dir) == key
            if not matched and ('?' in first_dir or '*' in first_dir or '[' in first_dir):
                try:
                    pattern = first_dir.replace('+', '\\+').replace('.', '\\.').replace('?', '.?').replace('*', '.*')
                    matchobj = re.match(pattern, key)
                    if matchobj and matchobj.group() == key:
                        matched = True
                except Exception:
                    pass

            if matched:
                if len(path_list) == 1:
                    matches.append(key)
                else:
                    subdir = self.get_subdir(locals_dict, [key])
                    if not subdir and not completion:
                        matches.append(delimiter.join([key] + path_list[1:]))
                    elif subdir:
                        new_path = cur_fullpath[:]
                        new_path.append((key, subdir))
                        inner_matches = self.path_matches(new_path, path_list[1:], delimiter=delimiter, sort=sort, completion=completion)
                        for inner_match in inner_matches:
                            if inner_match.startswith(delimiter):
                                matches.append(inner_match)
                            else:
                                matches.append(key + delimiter + inner_match)

        matches.sort()
        if absolute:
            matches = [ x if x.startswith(delimiter) else delimiter + x for x in matches ]
        return matches

    def shutdown(self):
        for event in self.break_events.values():
            event.set()

        super(OShell, self).shutdown()

    def line_wrap(self, str_list, html_attrs=None, pre_count=0):
        """Format a list of strings so that they are laid out in tabular form.
        If pre_count, the first pre_count entries always appear in a separate line
        """
        if not str_list:
            return ''
        str_list = [ str(s) for s in str_list ]
        nstr = len(str_list)
        max_width = min(self.tty_width // 2 - 1, max([ len(s) for s in str_list ]))
        ncols = self.tty_width // (max_width + 1)
        text_fmt = '%-' + str(max_width) + 's'
        formatted = []
        for j, value in enumerate(str_list):
            if html_attrs:
                uri, mime, command = html_attrs[value]
                s = str(value)
                fmt_value = self.html_fmt % (uri, mime, command, s)
                if len(s) < max_width:
                    fmt_value += ' ' * (max_width - len(s))
            else:
                fmt_value = text_fmt % value
            jdel = j - pre_count
            if pre_count and j == pre_count or jdel > 0 and not jdel % ncols:
                formatted.append('\n')
            elif j:
                formatted.append(' ')
            formatted.append(fmt_value)

        return ('').join(formatted)

    def execute(self, line, here_doc=None):
        """ Execute single oshell command and return (out_str, err_str)
            here_doc contains optional input string.
        """
        out_str, err_str = ('', '')
        try:
            out_str, err_str = self.parse(line, batch=True, here_doc=here_doc)
            return self.exec_feedlines(out_str, err_str)
        except Exception:
            return (
             out_str, err_str + format_traceback())

    def exec_feedlines(self, out_str='', err_str=''):
        try:
            while True:
                line = self.get_feed_line()
                if line is None:
                    break
                noprompt, more, out_str2, err_str2 = self.parse_out(line)
                out_str += out_str2
                err_str += err_str2

        except Exception:
            self.feed_lines = []
            err_str += format_traceback()

        return (
         out_str, err_str)

    def parse(self, line, batch=False, here_doc=None):
        """Parse command line and execute command, returning (out_str, err_str) like self.push
            here_doc contains optional input.
        """
        cmd_opts = type('Bunch', (object,), dict(batch=batch, here_doc=here_doc, redirect_in=None, redirect_out=None, edit_force=False, view_inline=False, view_docstr=False))
        self.update_terminal_size()
        while not self.break_queue.empty():
            trace_id, event = self.break_queue.get()
            if trace_id in self.break_events:
                self.break_events[trace_id].set()
            self.break_events[trace_id] = event

        if not line.strip():
            return ('', '')
        if line.strip() == 'lock':
            if not Set_params['password']:
                while True:
                    password = read_password('Set password: ').strip()
                    if not password:
                        return ('', 'Lock cancelled')
                    if password == read_password('Confirm password: ').strip():
                        Set_params['password'] = encrypt_password(password)
                        break

            while True:
                try:
                    password = read_password('Enter password to unlock: ').strip()
                    if verify_password(password, Set_params['password']):
                        break
                except:
                    self.shutdown()
                    return ('', 'Shutting down...')

            return ('', '')
        if line.lstrip().startswith('repeat '):
            line = line.lstrip()[len('repeat '):]
            if line:
                self.set_repeat(line)
                if not self.repeat_alt_screen:
                    self.repeat_alt_screen = 1
        if line.startswith(EXEC_PREFIX):
            cmd = 'exec'
            rem_line = line[len(EXEC_PREFIX):].lstrip()
            comps = shlex.split(rem_line.strip())
        else:
            comps = shlex.split(line.strip())
            if comps and (comps[0] in self.commands or comps[0] in self.aliases):
                cmd = comps.pop(0)
                rem_line = line.lstrip()[len(cmd):].lstrip()
            else:
                cmd = 'pr'
                rem_line = line
        if cmd in self.aliases:
            new_comps = []
            clear_comps = False
            for arg in self.aliases[cmd]:
                if '\\**' in arg:
                    arg = arg.replace('\\**', pythonize(comps))
                    clear_comps = True
                else:
                    if '\\*' in arg:
                        arg = arg.replace('\\*', (' ').join(comps))
                        clear_comps = True
                    for j, comp in enumerate(comps):
                        s = '\\' + str(j + 1)
                        if s in arg:
                            arg = arg.replace(s, comp)
                            clear_comps = True

                new_comps.append(arg)

            if not new_comps:
                return ('', 'Error in alias: ' + cmd)
            if clear_comps:
                comps = []
                rem_line = ''
            cmd = new_comps.pop(0)
            if new_comps:
                rem_line = (' ').join(new_comps) + ' ' + rem_line
            line = cmd + ' ' + rem_line
            comps = new_comps + comps
        out_str = ''
        err_str = ''
        if cmd == 'quit':
            err_str = 'Shutting down...'
            self.shutdown()
            return (
             out_str, err_str)
        else:
            if cmd == 'help':
                cmd_keys = self.commands.keys()
                cmd_keys.sort()
                if not comps:
                    out_str = 'Commands:\n%s\n\nIf you omit the command, "pr" is assumed.\nUse TAB key for command completion.\nType "help <command>" or "help *" for more info\n\nSee %s for documentation\n\n' % (self.line_wrap(cmd_keys), DOC_URL)
                elif comps[0] in self.commands:
                    out_str = self.commands[comps[0]]
                    if comps[0] == 'set':
                        for name, value in Help_params.iteritems():
                            out_str += '\n%-17s %s' % (name + ':', value)

                else:
                    out_str = ('\n').join([ self.commands[k].partition('\n')[0] for k in cmd_keys ]) + '\n\nUse otrace.traceassert(<condition>,label=..,action=..) to trace assertions\n\nSee %s for documentation\n\n' % DOC_URL
                return (out_str, err_str)
            else:
                if cmd == 'alias':
                    if not comps:
                        aliases = self.aliases.items()
                        aliases.sort()
                        out_str = ('\n').join([ name + ' ' + (' ').join(value) for name, value in aliases ])
                    elif len(comps) < 2:
                        if comps[0] in self.aliases:
                            out_str = (' ').join(self.aliases[comps[0]])
                        else:
                            err_str = 'No such alias: %s' % comps[0]
                    elif comps[1]:
                        self.aliases[comps[0]] = comps[1:]
                    elif comps[0] in self.aliases:
                        del self.aliases[comps[0]]
                    return (out_str, err_str)
                if cmd in ('cd', 'cdls', 'pushd', 'popd', 'swapd'):
                    opts = []
                    while comps and comps[0].startswith('-'):
                        opts.append(comps.pop(0))

                    follow_up_cmd = ''
                    if cmd == 'cdls':
                        follow_up_cmd = 'ls'
                        line = follow_up_cmd + ' ' + rem_line
                    if cmd == 'popd':
                        if not self.dir_stack:
                            return ('', 'Nothing to pop')
                        if opts == ['-a']:
                            new_dir = self.dir_stack[0]
                            self.dir_stack = []
                        else:
                            new_dir = self.dir_stack.pop()
                    elif cmd == 'swapd':
                        if not self.dir_stack:
                            return ('', 'Nothing to swap')
                        new_dir = self.dir_stack[(-1)]
                        self.dir_stack[-1] = self.make_path_str()
                    elif cmd in ('cd', 'cdls', 'pushd'):
                        if cmd == 'pushd':
                            self.dir_stack.append(self.make_path_str())
                        if not comps:
                            new_dir = None
                        else:
                            new_dir = comps.pop(0)
                    if new_dir is not None:
                        if ';' in new_dir:
                            new_dir, sep, tail = new_dir.partition(';')
                            if tail:
                                follow_up_cmd = tail
                            elif comps:
                                follow_up_cmd = comps.pop(0)
                        elif comps and comps[0].startswith(';'):
                            comp = comps.pop(0)
                            if comp[1:]:
                                follow_up_cmd = comp[1:]
                            elif comps:
                                follow_up_cmd = comps.pop(0)
                        new_dir = expanduser(new_dir)
                        if new_dir.startswith(TRACE_ID_PREFIX):
                            trace_id = new_dir[len(TRACE_ID_PREFIX):]
                            if not trace_id:
                                new_dir = None
                            else:
                                new_dir = PATH_SEP + PATH_SEP.join([BASE_DIR, RECENT_DIR] + ContextDict.split_trace_id(trace_id))
                    if new_dir and PATH_SEP not in new_dir and new_dir.find('..') == -1 and self.get_base_subdir() in (GLOBALS_DIR, LOCALS_DIR):
                        new_dir = new_dir.replace('.', PATH_SEP)
                    out_str, err_str = self.cmd_cd(new_dir)
                    self.update_prompt()
                    if follow_up_cmd:
                        cmd = follow_up_cmd
                        comps = opts + comps
                        rem_line = (' ').join(comps)
                    else:
                        return (
                         out_str, err_str)
                if cmd in ('edit', 'unpatch', 'view'):
                    while comps:
                        if comps[0] == '-d':
                            cmd_opts.view_docstr = True
                        elif comps[0] == '-f':
                            cmd_opts.edit_force = True
                        elif comps[0] == '-i':
                            cmd_opts.view_inline = True
                        else:
                            break
                        comps.pop(0)

                    if comps:
                        comp0 = comps.pop(0)
                        while comps:
                            if comp0.endswith('<') or comp0.endswith('>') or comps[0].startswith('<') or comps[0].startswith('>'):
                                comp0 += comps.pop(0)
                            else:
                                break

                        while True:
                            if comp0.find('<') > comp0.find('>'):
                                comp0, sep, cmd_opts.redirect_in = comp0.rpartition('<')
                                continue
                            if comp0.find('>') > comp0.find('<'):
                                comp0, sep, cmd_opts.redirect_out = comp0.rpartition('>')
                                continue
                            break

                        comp0 = expanduser(comp0)
                        if not is_absolute_path(comp0):
                            path_list = comp0.split(PATH_SEP)
                            matches = self.path_matches(self.cur_fullpath, path_list=path_list)
                            if not matches:
                                if cmd != 'edit' and not self.in_base_dir():
                                    return ('', "File '%s' not found" % comp0)
                            elif len(matches) == 1:
                                comp0 = matches[0]
                            else:
                                return (
                                 '', 'Cannot edit/view multiples files: %s' % comp0)
                        if cmd == 'edit' and cmd_opts.redirect_in == '' and cmd_opts.here_doc is None:
                            return ('', 'Expecting here_doc input for editing %s' % comp0)
                        comps = [comp0] + comps
                    if cmd != 'unpatch':
                        try:
                            return self.edit_view(cmd, comps, inline=cmd_opts.view_inline, here_doc=cmd_opts.here_doc)
                        except AltHandler:
                            pass

                elif not self.in_base_dir():
                    return self.cmd_shell(line)
                if cmd == 'pwd':
                    cwd = self.make_path_str()
                    if comps and comps[0] == '-a':
                        return (('\n').join([cwd] + [ x for x in reversed(self.dir_stack) ]), err_str)
                    return (cwd, err_str)
                else:
                    if self.get_web_path() and len(self.get_web_path()) >= self.web_interface.root_depth:
                        if Set_params['safe_mode']:
                            return ('', 'Javascript console disabled in safe mode; set safe_mode False')
                        try:
                            self.web_interface.send_command(self.get_web_path(), line)
                            return ('_NoPrompt_', None)
                        except Exception as excp:
                            return (
                             '', "Error in command execution '%s': %s" % (line, excp))

                    if cmd == 'trace':
                        return self.cmd_trace(cmd, comps, line, rem_line)
                    if cmd == 'untrace':
                        return self.cmd_untrace(cmd, comps, line, rem_line)
                    if cmd in ('edit', 'unpatch'):
                        return self.cmd_edit_unpatch(cmd, comps, line, rem_line, cmd_opts)
                    if cmd == 'source':
                        if not comps:
                            err_str = 'No filename to read!'
                        else:
                            filename = expanduser(comps[0])
                            if not is_absolute_path(filename):
                                return (out_str, 'Must specify absolute pathname for input file %s' % filename)
                            if not os.path.exists(filename):
                                return (out_str, 'Input file %s not found' % filename)
                            err_str = self.read_file(filename)
                        return (out_str, err_str)
                    if cmd in ('resume', 'save', 'del'):
                        return self.cmd_del_resume_save(cmd, comps, line, rem_line)
                    if cmd in ('ls', 'rm'):
                        return self.cmd_lsrm(cmd, comps, line, rem_line)
                    if cmd == 'run':
                        return self.cmd_run(cmd, comps, line, rem_line)
                    if cmd == 'set':
                        return self.cmd_set(cmd, comps, line, rem_line)
                    if cmd == 'view':
                        return self.cmd_view(cmd, comps, line, rem_line, cmd_opts)
                    if cmd in ('tag', 'untag'):
                        return self.cmd_tag_untag(cmd, comps, line, rem_line)
                    if cmd == 'unpickle':
                        return self.cmd_unpickle(cmd, comps, line, rem_line)
                    if cmd == 'pr':
                        return self.cmd_pr(cmd, comps, line, rem_line, cmd_opts)
                    if cmd == 'exec':
                        return self.cmd_exec(cmd, comps, line, rem_line, cmd_opts)
                return (out_str, "Unrecognized command '%s'" % cmd)

            return (out_str, err_str)

    def cmd_shell(self, line):
        """Execute shell command, returning (out_str, err_str)"""
        out_str, err_str = ('', '')
        try:
            env = os.environ.copy()
            env.update(self.add_env)
            osh_bin = Set_params['osh_bin']
            if osh_bin:
                osh_bin = expanduser(osh_bin)
                if not is_absolute_path(osh_bin):
                    osh_bin = os.path.join(os.getcwd(), os_path(osh_bin))
                prev_path = env.get('PATH')
                if prev_path:
                    env['PATH'] = osh_bin + ':' + prev_path
                else:
                    env['PATH'] = osh_bin
            exec_context = {'queue': Queue.Queue()}

            def execute_in_thread():
                try:
                    exec_context['proc'] = subprocess.Popen(['/bin/bash', '-l', '-c', line], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.make_path_str(), env=env)
                    exec_context['queue'].put(exec_context['proc'].communicate())
                except Exception as excp:
                    exec_context['queue'].put(('', "ERROR in executing '%s': %s" % (line, excp)))

            if Term_attr:
                save_attr = termios.tcgetattr(sys.stdin.fileno())
            thrd = threading.Thread(target=execute_in_thread)
            thrd.start()
            try:
                return exec_context['queue'].get(True, EXEC_TIMEOUT)
            except Queue.Empty:
                exec_context['proc'].kill()
                if Term_attr:
                    termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, save_attr)
                return (
                 '', "Timed out command execution '%s'" % (line,))

        except Exception as excp:
            return (
             '', "Error in command execution '%s': %s" % (line, excp))

    def cmd_view(self, cmd, comps, line, rem_line, cmd_opts):
        """View, returning (out_str, err_str)"""
        out_str, err_str = ('', '')
        obj_path = self.make_path_str()
        obj_value = None
        if not comps or comps[0] == '.':
            if not self.in_base_dir():
                return ('', 'No object to display')
            if self.has_trc('frame'):
                self.locals_dict['_stdout'] = self._stdout
                out_str, err_str = self.push('print >>_stdout, "%%s:%%s %%s\\n" %% %s["frame"][:3], "".join(%s["frame"][3])' % (TRACE_INFO, TRACE_INFO))
                del self.locals_dict['_stdout']
                return (
                 out_str, err_str)
            if self.has_trc('func'):
                obj_value = self.get_trc('func')
            else:
                obj_value = self.get_cur_value()
        else:
            comp0 = comps.pop(0)
            if is_absolute_path(comp0):
                if comp0 == PATH_SEP + BASE_DIR:
                    return ('', 'Cannot edit/view %s' % comp0)
                if not comp0.startswith(PATH_SEP + BASE_DIR + PATH_SEP):
                    raise Exception('Internal error; cannot view %s' % comp0)
                obj_path = comp0
                tem_path = comp0[len(PATH_SEP + BASE_DIR + PATH_SEP):].replace(PATH_SEP, '.').split('.')
                obj_value = self.get_subdir('base', tem_path, value=True)
            else:
                if not self.in_base_dir():
                    raise Exception('Internal error; cannot view %s' % comp0)
                obj_path = obj_path + PATH_SEP + comp0
                tem_path = comp0.replace(PATH_SEP, '.').split('.')
                obj_value = self.get_subdir(self.locals_dict, tem_path, value=True)
        if not obj_value:
            return (out_str, 'No object to display source for')
        else:
            if not (inspect.ismodule(obj_value) or inspect.isclass(obj_value) or inspect.ismethod(obj_value) or inspect.isfunction(obj_value)):
                if hasattr(obj_value, '__class__'):
                    obj_value = getattr(obj_value, '__class__')
            try:
                if cmd_opts.view_docstr:
                    doc = inspect.getdoc(obj_value)
                    lines = doc.split('\n') if doc else []
                else:
                    lines, start_line = OTrace.getsourcelines(obj_value)
                content = ('').join(de_indent(lines))
            except Exception as excp:
                return (
                 out_str, 'Unable to display source for %s:\n %s' % (obj_path, excp))

            if cmd_opts.view_inline:
                return (content, err_str)
            if cmd_opts.redirect_out:
                filename = expanduser(cmd_opts.redirect_out)
                if not is_absolute_path(filename):
                    return (out_str, 'Must specify absolute pathname for output file %s' % filename)
                try:
                    with open(os_path(filename), 'w') as (f):
                        f.write(content)
                    return ('', '')
                except Exception as excp:
                    return (
                     out_str, 'Error in saving view output: ' + str(excp))

            OTrace.callback_handler.editback(content, filepath=obj_path, filetype='python', editor=Set_params['editor'], modify=False)
            return (out_str, err_str)

    def cmd_edit_unpatch(self, cmd, comps, line, rem_line, cmd_opts):
        """Edit/unpatch, returning (out_str, err_str)"""
        out_str, err_str = ('', '')
        if Set_params['safe_mode']:
            return (out_str, 'Patching/unpatching not permitted in safe mode; set safe_mode False')
        else:
            patch_name = None
            parent_obj = None
            if comps and comps[0].startswith(DIR_PREFIX[GLOBALS_DIR]):
                comp = comps.pop(0)
                tem_name = comp[len(DIR_PREFIX[GLOBALS_DIR]):]
                path_list = tem_name.replace(PATH_SEP, '.').split('.')
                patch_name = ('.').join(path_list)
                old_obj = self.get_subdir(self.globals_dict, path_list, value=True)
                if len(path_list) > 1:
                    parent_obj = self.get_subdir(self.globals_dict, path_list[:-1], value=True)
                else:
                    parent_obj = self.get_main_module()
            else:
                if self.get_base_subdir() not in (GLOBALS_DIR, PATCHES_DIR):
                    return (out_str, 'Patching only works in subdirectory of globals/patches')
                if not comps:
                    old_obj = self.get_cur_value()
                    if self.get_base_subdir() == PATCHES_DIR:
                        patch_name = self.get_leaf_dir()
                        parent_obj = None
                    else:
                        patch_name = ('.').join(x[INAME] for x in self.cur_fullpath[BASE1_OFFSET:])
                        parent_obj = self.get_parent_value()
                else:
                    objname = comps.pop(0)
                    obj_path_comps = objname.replace(PATH_SEP, '.').split('.')
                    patch_name = ('.').join([ x[INAME] for x in self.cur_fullpath[BASE1_OFFSET:] ] + obj_path_comps)
                    if self.get_base_subdir() == PATCHES_DIR:
                        old_obj = self.get_subdir(self.locals_dict, [objname], value=True)
                        parent_obj = None
                    else:
                        old_obj = self.get_subdir(self.locals_dict, obj_path_comps, value=True)
                        if len(obj_path_comps) == 1:
                            parent_obj = self.get_cur_value()
                        else:
                            parent_obj = self.get_subdir(self.locals_dict, obj_path_comps[:-1], value=True)
                    basename = patch_name.split('.')[(-1)]
                    if not old_obj and not parent_obj and not (cmd == 'unpatch' and patch_name == '*'):
                        return (out_str, 'Invalid patch class/method: ' + str(patch_name))
                if cmd == 'edit':
                    if inspect.isclass(old_obj):
                        return ('', 'Class patching not yet implemented; patch methods individually')
                    if cmd_opts.redirect_in:
                        filename = expanduser(cmd_opts.redirect_in)
                        if not is_absolute_path(filename):
                            return (out_str, 'Must specify absolute pathname for input file %s' % filename)
                        try:
                            with open(os_path(filename), 'r') as (patchf):
                                mod_content = patchf.read()
                        except Exception as excp:
                            return (
                             out_str, "Error in reading from '%s': %s" % (filename, excp))

                    else:
                        if cmd_opts.here_doc is not None:
                            mod_content = cmd_opts.here_doc
                        else:
                            try:
                                lines, start_line = OTrace.getsourcelines(old_obj)
                            except IOError:
                                return (
                                 out_str, 'Error: source not found; specify source filename')
                            except Exception as excp:
                                return (
                                 out_str, 'Error in accessing source: %s' % excp)

                            if not start_line and not cmd_opts.edit_force:
                                return (out_str, "Error: specify '-f' option to force editing of patched file")
                            content = ('').join(de_indent(lines))
                            mod_content, err_str = OTrace.callback_handler.editback(content, filepath=DIR_PREFIX[GLOBALS_DIR] + patch_name, filetype='python', editor=Set_params['editor'], modify=True)
                            if mod_content is None and err_str is None:
                                return ('_NoPrompt_', None)
                            if err_str:
                                return (out_str, err_str)
                            if mod_content == content:
                                return (
                                 out_str, 'No changes')
                        tem_lines = mod_content.split('\n')
                        mod_lines = [ x + '\n' for x in tem_lines[:-1] ]
                        if tem_lines[(-1)]:
                            mod_lines.append(tem_lines[(-1)])
                        module_name = old_obj.__module__ if old_obj else parent_obj.__module__
                        module_obj = sys.modules[module_name]
                        patch_locals = {}
                        out_str, err_str = self.interpreter.evaluate(mod_content, locals_dict=patch_locals, globals_dict=module_obj.__dict__, print_out=False)
                        if err_str:
                            return (out_str, err_str)
                    if not old_obj or ismethod_or_function(old_obj):
                        if len(patch_locals) != 1 or patch_locals.keys()[0] != basename:
                            return (out_str, "Error: patch file must contain only 'def %s', but found %s" % (basename, patch_locals))
                        func = patch_locals.values()[0]
                        out_str += 'Patched ' + patch_name + ':'
                        patched_obj = OTrace.monkey_patch(func, old_obj, parent_obj, repatch=cmd_opts.edit_force, source=mod_lines)
                        if patched_obj:
                            OTrace.base_context[PATCHES_DIR][patch_name] = patched_obj
                        else:
                            out_str += '-FAILED'
                    else:
                        OTrace.base_context[PATCHES_DIR][patch_name] = old_obj
                        out_str += 'Patched ' + patch_name + ':'
                        for method_name, func in patch_locals.iteritems():
                            method_obj = getattr(old_obj, method_name, None)
                            out_str += ' ' + method_name
                            if not OTrace.monkey_patch(func, method_obj, old_obj, repatch=cmd_opts.edit_force):
                                out_str += '-FAILED'

                else:
                    if patch_name == '*' and self.get_base_subdir() == PATCHES_DIR:
                        unpatch_items = OTrace.base_context[PATCHES_DIR].items()
                    else:
                        unpatch_items = [
                         (
                          patch_name, old_obj)]
                    if len(unpatch_items) == 1 and cmd_opts.redirect_out:
                        filename = expanduser(cmd_opts.redirect_out)
                        if not is_absolute_path(filename):
                            return (out_str, 'Must specify absolute pathname for output file %s' % filename)
                        try:
                            lines, start_line = OTrace.getsourcelines(unpatch_items[0][1])
                        except IOError:
                            return (
                             out_str, 'Error: patch source not found for saving')
                        except Exception as excp:
                            return (
                             out_str, 'Error in saving patch: %s' % excp)

                        try:
                            with open(os_path(filename), 'w') as (f):
                                f.write(('').join(lines))
                        except Exception as excp:
                            return (
                             out_str, 'Error in saving patch source: ' + str(excp))

                    out_str = 'Unpatching'
                    for patch_name, unpatch_obj in unpatch_items:
                        if ismethod_or_function(unpatch_obj):
                            if OTrace.monkey_unpatch(unpatch_obj):
                                out_str += ' ' + patch_name
                            else:
                                return (
                                 out_str, 'Unpatching failed for %s' % patch_name)
                        else:
                            out_str += ' ' + patch_name + ':'
                            for name, method_obj in inspect.getmembers(unpatch_obj, ismethod_or_function):
                                if OTrace.monkey_unpatch(method_obj):
                                    out_str += ' ' + method_obj.__name__

                            try:
                                del OTrace.base_context[PATCHES_DIR][patch_name]
                            except Exception:
                                pass

            return (
             out_str, err_str)

    def cmd_untrace(self, cmd, comps, line, rem_line):
        """Terminate tracing, returning (out_str, err_str)"""
        out_str, err_str = ('', '')
        trace_name = ''
        if comps:
            trace_name = comps[0]
            parent_obj = None
            if trace_name in ('all', '*') or trace_name[0] == TRACE_LABEL_PREFIX or trace_name.startswith(TRACE_LOG_PREFIX):
                trace_value = trace_name
            else:
                path_list = trace_name.split('.')
                trace_value = self.get_subdir(self.locals_dict, path_list, value=True)
                if len(path_list) > 1:
                    parent_obj = self.get_subdir(self.locals_dict, path_list[:-1], value=True)
                else:
                    parent_obj = self.get_cur_value()
                if trace_value is None:
                    return (out_str, 'Invalid class/method for untracing: ' + str(trace_name))
            with Trace_rlock:
                if inspect.isclass(trace_value):
                    OTrace.trace_entity(trace_value, unwrap=True)
                elif inspect.isclass(parent_obj):
                    OTrace.trace_method(parent_obj, trace_value, unwrap=True)
                elif inspect.ismodule(parent_obj):
                    OTrace.trace_modulefunction(parent_obj, trace_value, unwrap=True)
                elif not isinstance(trace_value, basestring):
                    return (out_str, 'Cannot untrace %s' % trace_value)
                fullname = OTrace.remove_trace(trace_name, parent=parent_obj)
                out_str = 'untraced %s' % fullname
        return (
         out_str, err_str)

    def cmd_trace(self, cmd, comps, line, rem_line):
        """Initiate tracing, returning (out_str, err_str)"""
        out_str, err_str = ('', '')
        trace_name = ''
        trace_call = False
        trace_return = False
        match_tag = ''
        argmatch = {}
        access_type = ''
        fullname = ''
        trace_condition = None
        break_action = None
        break_count = 0
        while comps and comps[0].startswith('-'):
            comp = comps.pop(0)
            if comp in ('-a', '-c', '-n') and not comps:
                return (out_str, 'Missing argument for option %s' % comp)
            if comp == '-a':
                if comps[0] in TRACE_ACTIONS:
                    break_action = comps.pop(0)
                else:
                    return (
                     out_str, 'Expected one of %s for option %s' % (comp, TRACE_ACTIONS))
            elif comp == '-c':
                trace_condition = comps.pop(0)
            elif comp == '-n':
                if comps[0].isdigit() or comps[0][1:].isdigit() and comps[0][0] in '+-':
                    break_count = int(comps.pop(0))
                else:
                    return (
                     out_str, 'Expected integer argument for option %s' % comp)
            else:
                return (
                 out_str, 'Invalid option %s' % comp)

        if not comps:
            keys = OTrace.trace_names.keys()
            keys.sort()
            out_str = ('\n').join(str(OTrace.trace_names[k]) for k in keys)
        else:
            trace_name = comps.pop(0)
            trace_value = None
            tracing_key = False
            parent_obj = None
            if trace_name.startswith(DIR_PREFIX[GLOBALS_DIR]):
                tem_name = trace_name[len(DIR_PREFIX[GLOBALS_DIR]):]
                path_list = tem_name.replace(PATH_SEP, '.').split('.')
                trace_value = self.get_subdir(self.globals_dict, path_list, value=True)
                if len(path_list) > 1:
                    parent_obj = self.get_subdir(self.globals_dict, path_list[:-1], value=True)
                else:
                    parent_obj = self.get_main_module()
            else:
                if trace_name.startswith(DIR_PREFIX[DATABASE_DIR]):
                    tracing_key = True
                    trace_value = trace_name[len(DIR_PREFIX[DATABASE_DIR]):] + PATH_SEP
                else:
                    if trace_name == '*' or trace_name[0] == TRACE_LABEL_PREFIX or trace_name.startswith(TRACE_LOG_PREFIX):
                        trace_value = trace_name
                    elif self.get_base_subdir() == DATABASE_DIR:
                        tracing_key = True
                        full_path = self.full_path_comps(trace_name)
                        trace_value = PATH_SEP + PATH_SEP.join(full_path[1:])
                    else:
                        path_list = trace_name.replace(PATH_SEP, '.').split('.')
                        trace_value = self.get_subdir(self.locals_dict, path_list, value=True)
                        parent_obj = None
                        if inspect.ismethod(trace_value):
                            method_self = getattr(trace_value, '__self__', None)
                            if method_self:
                                if inspect.isclass(method_self):
                                    parent_obj = method_self
                                else:
                                    parent_obj = getattr(method_self, '__class__', None)
                        if not parent_obj:
                            if self.get_base_subdir() != GLOBALS_DIR:
                                return (out_str, 'Must be in subdirectory of globals to trace')
                            if len(path_list) > 1:
                                parent_obj = self.get_subdir(self.locals_dict, path_list[:-1], value=True)
                            else:
                                parent_obj = self.get_cur_value()
                    if comps:
                        return (out_str, 'Multiple objects in trace command not yet implemented: %s' % comps)
                if trace_value is None:
                    return (out_str, 'Invalid class/method/key for tracing: ' + str(trace_name))
            if trace_condition:
                try:
                    argmatch = match_parse(trace_condition)
                except Exception:
                    return (
                     out_str, 'Invalid trace arg/attr match: ' + trace_condition)

                if argmatch:
                    pass
                elif tracing_key:
                    if trace_condition in ('get', 'put', 'delete', 'modify', 'all'):
                        access_type = trace_condition
                    else:
                        return (
                         out_str, 'Invalid trace access type: ' + trace_condition)
                elif trace_condition.startswith('tagged'):
                    match_tag = trace_condition[6:] if len(trace_condition) > 6 else '*'
                elif trace_condition == 'call':
                    trace_call = True
                elif trace_condition == 'return':
                    trace_return = True
                elif trace_condition == 'all':
                    trace_call = True
                    trace_return = True
                else:
                    return (
                     out_str, 'Invalid trace condition ' + trace_condition)
            if break_action == 'tag':
                trace_call = False
                trace_return = True
            if tracing_key:
                if not access_type:
                    access_type = 'modify'
                key_path = trace_value.split(PATH_SEP)
                if ENTITY_CHAR in key_path or DATABASE_DIR not in self.lazy_dirs:
                    return (out_str, 'Invalid trace key')
                key = self.lazy_dirs[DATABASE_DIR].key_from_path(key_path)
                if not key:
                    return (out_str, 'Invalid trace key: ' + trace_value)
                trace_value = str(key)
            with Trace_rlock:
                if inspect.isclass(trace_value):
                    OTrace.trace_entity(trace_value)
                elif inspect.isclass(parent_obj) and (inspect.ismethod(trace_value) or inspect.isfunction(trace_value)):
                    OTrace.trace_method(parent_obj, trace_value)
                elif inspect.ismodule(parent_obj) and inspect.isfunction(trace_value):
                    OTrace.trace_modulefunction(parent_obj, trace_value)
                elif not isinstance(trace_value, basestring):
                    return (out_str, 'Cannot trace %s' % type(trace_value))
                fullname = OTrace.add_trace(trace_value, parent=parent_obj, argmatch=argmatch, trace_call=trace_call, trace_return=trace_return, break_count=break_count, break_action=break_action, match_tag=match_tag, access_type=access_type)
                out_str = 'Tracing ' + str(OTrace.trace_names[fullname])
        return (
         out_str, err_str)

    def cmd_del_resume_save(self, cmd, comps, line, rem_line):
        """Delete/resume/save, returning (out_str, err_str)"""
        out_str, err_str = ('', '')
        trace_ids = []
        if not comps:
            if self.has_trc('id'):
                trace_ids = [
                 self.get_trc('id')]
        else:
            if len(self.cur_fullpath) == BASE1_OFFSET and self.get_base_subdir() == ALL_DIR:
                for comp in comps:
                    trace_ids += self.path_matches(self.cur_fullpath, [comp])

            if not trace_ids:
                err_str = 'No match for trace_id'
            for trace_id in trace_ids:
                if cmd == 'resume':
                    with Trace_rlock:
                        event = self.break_events.get(trace_id)
                        if event:
                            event.set()
                            del self.break_events[trace_id]
                            out_str = 'Resuming ' + trace_id
                            OTrace.remove_break_point(trace_id)
                        else:
                            context = OTrace.base_context[ALL_DIR].get(trace_id)
                            if context and context.get_trc('context') == 'holds':
                                self_arg = context.get('self')
                                if hasattr(self_arg, OTrace.resume_attr):
                                    resume_from_hold(self_arg)
                                else:
                                    err_str = 'Unable to resume from hold for ' + trace_id
                                OTrace.remove_break_point(trace_id)
                            else:
                                err_str = 'Unable to resume ' + trace_id
                    self.change_workdir(PATH_SEP + BASE_DIR + PATH_SEP + GLOBALS_DIR)
                    self.update_prompt()
                elif cmd == 'save':
                    with Trace_rlock:
                        context = OTrace.base_context[ALL_DIR].get(trace_id)
                        if context is not None:
                            OTrace.base_context[SAVED_DIR].add_context(context, trace_id)
                        else:
                            err_str = "Unable to save context '%s'" % trace_id
                elif cmd == 'del':
                    with Trace_rlock:
                        try:
                            del OTrace.base_context[ALL_DIR][trace_id]
                        except Exception:
                            pass

                        OTrace.base_context[SAVED_DIR].remove_context(trace_id)

        return (
         out_str, err_str)

    def cmd_lsrm(self, cmd, comps, line, rem_line):
        """'List' directory or 'remove' entries, returning (out_str, err_str)"""
        out_str, err_str = ('', '')
        recursive = False
        base_class = None
        time_sort_key = None
        ls_show = set()
        show_attr = False
        show_long = False
        if cmd == 'rm':
            if Set_params['safe_mode']:
                return (out_str, 'rm: deletion not permitted in safe mode; set safe_mode False')
            if not self.lazy_dirs:
                return (out_str, 'rm: no database connected')
            if comps and comps[0] == '-r':
                recursive = True
                comps.pop(0)
        else:
            if cmd == 'ls':
                while comps and comps[0].startswith('-'):
                    comp = comps.pop(0)
                    if comp.startswith('-.'):
                        base_name = comp[2:]
                        if base_name[:1].isalpha():
                            path_list = base_name.split('.')
                            value = self.get_subdir(self.locals_dict, path_list, value=True)
                            if not value:
                                value = self.get_subdir(self.globals_dict, path_list, value=True)
                            if inspect.isclass(value):
                                base_class = value
                        else:
                            cur_value = self.get_cur_value()
                            if cur_value is None:
                                cur_class = self.locals_dict.get('__class__', None)
                            elif inspect.isclass(cur_value):
                                cur_class = cur_value
                            else:
                                cur_class = getattr(cur_value, '__class__', None)
                            if not base_name:
                                base_class = cur_class
                            elif cur_class:
                                mro_classes = inspect.getmro(cur_class)
                                base_class = mro_classes[min(len(base_name), len(mro_classes) - 1)]
                    else:
                        for opt in comp[1:]:
                            if opt == 'a':
                                show_attr = True
                            elif opt == 'c':
                                ls_show.add('class')
                            elif opt == 'f':
                                ls_show.add('function')
                            elif opt == 'l':
                                show_long = True
                            elif opt == 'm':
                                ls_show.add('module')
                            elif opt == 't':
                                if self.get_base_subdir() in (ALL_DIR, RECENT_DIR, SAVED_DIR):
                                    time_sort_key = lambda x: ContextDict.split_trace_id(os.path.split(x)[1])[3]
                            elif opt == 'v':
                                ls_show.add('variable')

            globals_or_locals = self.get_base_subdir() in (GLOBALS_DIR, LOCALS_DIR)
            if not comps:
                if cmd == 'rm':
                    return (out_str, 'rm: specify entities to delete')
                matches = self.locals_dict.keys()
            else:
                matches = []
                for comp in comps:
                    if comp == PATH_SEP:
                        matches += [PATH_SEP]
                    elif comp == '.':
                        matches += self.make_path_str()
                    else:
                        comp_dir = expanduser(comp)
                        fullpath = self.cur_fullpath
                        absolute = is_absolute_path(comp_dir)
                        if absolute:
                            comp_dir = comp_dir[1:]
                            fullpath = []
                        elif PATH_SEP not in comp_dir and comp_dir.find('..') == -1 and globals_or_locals:
                            comp_dir = comp_dir.replace('.', PATH_SEP)
                        assert comp_dir
                        path_list = comp_dir.split(PATH_SEP)
                        comp_matches = self.path_matches(fullpath, path_list, absolute=absolute)
                        if not comp_matches and ENTITY_CHAR in path_list:
                            comp_matches = [comp_dir]
                        matches += comp_matches

        if base_class:
            matches = [ attr for attr in matches if not hasattr(base_class, attr) ]
        if not show_attr:
            matches = [ attr for attr in matches if attr in SHOW_HIDDEN or not (attr.startswith('__') and attr.endswith('__')) ]
        if not matches and comps:
            return (out_str, "no matches '%s'" % (line.strip(),))
        else:
            if time_sort_key:
                try:
                    matches.sort(key=time_sort_key)
                except Exception:
                    matches.sort()

            else:
                matches.sort()
            if cmd == 'ls':
                _, cur_dir_path = self.get_prompt()
                max_width = min(self.tty_width // 3 - 1, max([ len(key) for key in matches ]) if matches else 2)
                fmt = '%-' + str(max_width) + 's'
                path_attrs = OrderedDict()
                pre_count = 0
                if not show_long and len(self.cur_fullpath) > 1 and Set_params['allow_xml'] and OTrace.html_wrapper:
                    parent_path = self.make_path_str(self.cur_fullpath[:-1])
                    default_path = self.make_path_str(self.get_default_dir())
                    path_attrs['..'] = ['file://' + urllib.quote(parent_path), 'x-python/object', 'cdls']
                    path_attrs['.'] = ['file://' + urllib.quote(cur_dir_path), 'x-python/object', 'cdls']
                    path_attrs['~~'] = ['file://' + urllib.quote(default_path), 'x-python/object', 'cdls']
                    pre_count = len(path_attrs)
                out_list = []
                for j, dir_path in enumerate(matches):
                    if is_absolute_path(dir_path):
                        path_list = dir_path[1:].split(PATH_SEP)[BASE_OFFSET:]
                        locals_dict = OTrace.base_context
                    else:
                        if dir_path and PATH_SEP not in dir_path and dir_path.find('..') == -1 and globals_or_locals:
                            dir_path = dir_path.replace('.', PATH_SEP)
                        path_list = dir_path.split(PATH_SEP)
                        locals_dict = self.locals_dict
                    full_path = self.full_path_comps(dir_path)
                    if ENTITY_CHAR in path_list:
                        key_comps, sub_comps, entity_key = self.entity_path_comps(full_path)
                        if entity_key and full_path[BASE_OFFSET] in self.lazy_dirs:
                            entity = self.lazy_dirs[full_path[BASE_OFFSET]].get_entity(entity_key)
                            path_list = sub_comps
                            if isinstance(entity, dict):
                                locals_dict = entity
                            elif entity:
                                locals_dict = ObjectDict(entity)
                            else:
                                locals_dict = {}
                    if not base_class or not hasattr(base_class, path_list[(-1)]):
                        value = self.get_subdir(locals_dict, path_list, value=True)
                        if inspect.isclass(value):
                            value_type = 'class'
                        elif inspect.isfunction(value) or inspect.ismethod(value):
                            value_type = 'function'
                        elif inspect.ismodule(value):
                            value_type = 'module'
                        else:
                            value_type = 'variable'
                        if ls_show and value_type not in ls_show:
                            continue
                        if isinstance(value, (dict, weakref.WeakValueDictionary)):
                            value_str = '{%s}' % ((', ').join(map(str, value.keys())),)
                        elif isinstance(value, LineList):
                            value_str = '[%s]' % (value,)
                        elif isinstance(value, (list, tuple)):
                            value_str = '[%s]' % ((', ').join(map(str, value)),)
                        else:
                            value_str = repr(value)
                        mime, command = get_obj_properties(value, full_path=full_path)
                        markup = ['file://' + urllib.quote(cur_dir_path + PATH_SEP + dir_path), 'x-python/' + mime, command]
                        path_attrs[dir_path] = markup
                        if show_long:
                            if Set_params['allow_xml'] and OTrace.html_wrapper:
                                s = str(dir_path)
                                fmt_value = self.html_fmt % tuple(markup + [s])
                                if len(s) < max_width:
                                    fmt_value += ' ' * (max_width - len(s))
                                out_list.append(fmt_value + ' = ' + cgi.escape(value_str) + '\n')
                            else:
                                fmt_value = fmt % dir_path
                                out_list.append(fmt_value + ' = ' + value_str + '\n')
                            if not (j + 1) % 5:
                                out_list.append('\n')

                if show_long:
                    out_str = ('').join(out_list)
                elif Set_params['allow_xml'] and OTrace.html_wrapper:
                    out_str = self.line_wrap(path_attrs.keys(), html_attrs=path_attrs, pre_count=pre_count)
                else:
                    out_str = self.line_wrap(path_attrs.keys())
                if Set_params['allow_xml'] and OTrace.html_wrapper:
                    out_str = OTrace.html_wrapper.wrap('<pre>' + out_str + '</pre>')
                return (out_str, err_str)
            out_list = []
            delete_lists = collections.defaultdict(list)
            for j, dir_path in enumerate(matches):
                full_path = self.full_path_comps(dir_path)
                base_subdir = full_path[BASE_OFFSET]
                if len(full_path) < BASE2_OFFSET or base_subdir not in self.lazy_dirs or ENTITY_CHAR in full_path:
                    err_str += 'Invalid path: ' + dir_path + ' '
                else:
                    entity_key = self.lazy_dirs[base_subdir].key_from_path(full_path[BASE1_OFFSET:])
                    if not entity_key:
                        err_str += 'Invalid path: ' + dir_path + ' '
                    else:
                        delete_lists[base_subdir].append(entity_key)

            if not err_str and delete_lists:
                for base_subdir, key_list in delete_lists.items():
                    deleted_keys = self.lazy_dirs[base_subdir].delete_entities(key_list, recursive=recursive)
                    out_list += 'Deleted %s keys' % len(deleted_keys)

            out_str = ('').join(out_list)
            return (out_str, err_str)

    def cmd_run(self, cmd, comps, line, rem_line):
        """Run function in main thread"""
        out_str, err_str = ('', '')
        if not self.expect_run:
            return (out_str, "Already running task; 'interrupt' it or wait for it to complete")
        if not self.queue:
            return (out_str, 'Cannot run function unless otrace is in separate thread')
        if not comps:
            return (out_str, 'Must specify function to run')
        func_name = comps.pop(0)
        path_list = func_name.replace(PATH_SEP, '.').split('.')
        run_func = self.get_subdir(self.locals_dict, path_list, value=True)
        if not callable(run_func):
            return (out_str, '%s of type %s is not callable' % (func_name, type(run_func)))
        self.queue.put((run_func, comps))
        return (out_str, 'Running %s' % func_name)

    def cmd_set(self, cmd, comps, line, rem_line):
        """Set or display parameters, returning (out_str, err_str)"""
        out_str, err_str = ('', '')
        if len(comps) > 1:
            try:
                name, value = comps[0:2]
                if value == 'None':
                    value = None
                if name not in Help_params:
                    return ('', 'Invalid parameter: ' + name)
                if name == 'log_format':
                    OTrace.callback_handler.logformat(value.replace('+', ' '))
                elif name == 'log_level':
                    OTrace.callback_handler.loglevel(int(value))
                elif name == 'log_remote':
                    OTrace.callback_handler.remote_log(value, remove=not value)
                elif name == 'log_truncate':
                    OTrace.callback_handler.tracelen(int(value))
                elif name == 'pickle_file':
                    if PickleInterface.write_connection:
                        PickleInterface.write_connection.close()
                        PickleInterface.write_connection = None
                    if value:
                        PickleInterface.create_pickle_db(expandpath(value))
                elif name == 'unpickle_file':
                    pass
                elif name == 'trace_active':
                    OTrace.trace_active = bool(value)
                else:
                    param_type = type(Set_params[name])
                    if param_type is bool:
                        value = value.lower() == 'true'
                    else:
                        value = param_type(value)
                    if name == 'safe_mode' and not self.allow_unsafe and not value:
                        return ('', 'Switching to unsafe mode not permitted')
                    if name == 'password' and ':' not in value:
                        return ('', 'No salt in encrypted password; SET PASSWORD FAILED')
                    Set_params[name] = value
            except Exception as excp:
                return (
                 out_str, 'Error in setting parameter %s: %s' % (name, excp))

            return ('%s = %s' % (name, value), '')
        else:
            names = []
            if not comps:
                names = Help_params.keys()
            else:
                if len(comps) == 1 and comps[0] in Help_params:
                    names = [
                     comps[0]]
                for name in names:
                    if name == 'log_format':
                        value = OTrace.callback_handler.logformat().replace(' ', '+')
                    elif name == 'log_level':
                        value = OTrace.callback_handler.loglevel()
                    elif name == 'log_remote':
                        value = OTrace.callback_handler.remote_log()
                    elif name == 'log_truncate':
                        value = OTrace.callback_handler.tracelen()
                    elif name == 'pickle_file':
                        value = PickleInterface.write_file
                    elif name == 'unpickle_file':
                        value = PickleInterface.read_file
                    elif name == 'trace_active':
                        value = OTrace.trace_active
                    else:
                        value = Set_params[name]
                    out_str += '%s = %s\n' % (name, value)

            return (
             out_str, err_str)
            return

    def cmd_cd(self, new_dir):
        """cd to new_dir, returning (out_str, err_str)"""
        out_str, err_str = ('', '')
        cur_path = [ comp[INAME] for comp in self.cur_fullpath ]
        if new_dir == ENTITY_CHAR and ENTITY_CHAR not in self.locals_dict and ENTITY_CHAR in cur_path:
            key_comps, sub_comps, entity_key = self.entity_path_comps(self.full_path_comps(new_dir))
            entity_dir = PATH_SEP.join(['..'] * (len(cur_path) - len(key_comps) - 1))
            if entity_dir:
                err_str = self.change_workdir(entity_dir)
                if err_str:
                    return (out_str, err_str)
        elif new_dir and len(cur_path) > BASE_OFFSET and cur_path[BASE_OFFSET] in self.lazy_dirs:
            base_subdir = cur_path[BASE_OFFSET]
            lazy_interface = self.lazy_dirs[base_subdir]
            root_depth = lazy_interface.root_depth
            sub_dir = new_dir
            new_path = self.full_path_comps(new_dir)
            if len(new_path) > BASE_OFFSET and new_path[BASE_OFFSET] == base_subdir:
                if len(new_path) > root_depth + BASE_OFFSET and (is_absolute_path(new_dir) or len(cur_path) <= root_depth + BASE_OFFSET or new_path[(root_depth + BASE_OFFSET)] != cur_path[(root_depth + BASE_OFFSET)]):
                    db_dir = PATH_SEP.join(['..'] * (len(new_path) - (root_depth + BASE1_OFFSET)))
                    sub_dir = PATH_SEP.join(new_path[root_depth + BASE1_OFFSET:])
                    if db_dir:
                        err_str = self.change_workdir(db_dir)
                        if err_str:
                            return (out_str, err_str)
                    root_key = lazy_interface.key_from_path(new_path[BASE1_OFFSET:root_depth + BASE1_OFFSET])
                    locals_dict = lazy_interface.get_child_tree(root_key)
                    for j in xrange(BASE1_OFFSET, root_depth + BASE1_OFFSET):
                        locals_dict = locals_dict[new_path[j]]

                    self.locals_dict = locals_dict
                    self.cur_fullpath.append((new_path[(root_depth + BASE_OFFSET)], self.locals_dict))
                if ENTITY_CHAR in new_path:
                    key_comps, sub_comps, entity_key = self.entity_path_comps(new_path)
                    if not entity_key:
                        return (out_str, 'Invalid key')
                    if len(self.cur_fullpath) < len(key_comps) + 1 or self.cur_fullpath[:len(key_comps) + 1] != key_comps + [ENTITY_CHAR]:
                        sub_dir = PATH_SEP.join(sub_comps)
                        key_dir = self.get_rel_dir(PATH_SEP + PATH_SEP.join(key_comps))
                        if key_dir:
                            err_str = self.change_workdir(key_dir)
                            if err_str:
                                return (out_str, err_str)
                        entity = lazy_interface.get_entity(entity_key)
                        if isinstance(entity, dict):
                            self.locals_dict = entity
                        elif entity:
                            self.locals_dict = ObjectDict(entity)
                        else:
                            self.locals_dict = {}
                        self.cur_fullpath.append((ENTITY_CHAR, self.locals_dict))
            if sub_dir:
                err_str = self.change_workdir(sub_dir)
                if err_str:
                    return (out_str, err_str)
        else:
            err_str = self.change_workdir(new_dir)
            if err_str:
                return (out_str, err_str)
        return (
         out_str, err_str)

    def cmd_tag_untag(self, cmd, comps, line, rem_line):
        """Tag/untag object, returning (out_str, err_str)"""
        out_str, err_str = ('', '')
        if not self.cur_fullpath:
            return (out_str, err_str)
        else:
            value = None
            if not comps or comps[0] == '.':
                if self.has_trc('frame'):
                    if 'self' in self.locals_dict:
                        value = self.locals_dict['self']
                    else:
                        return (
                         out_str, 'No self object to %s in trace context' % cmd)
                else:
                    value = self.get_cur_value()
            else:
                full_path_list = comps[0].split('.')
                value = self.get_subdir(self.locals_dict, full_path_list, value=True)
            try:
                if cmd == 'tag':
                    if len(comps) > 1:
                        tag = comps[1]
                    else:
                        tag = 'id'
                    OTrace.tag(value, tag)
                else:
                    OTrace.untag(value)
            except Exception as excp:
                return (
                 out_str, 'Error in %s: %s' % (cmd, excp))

            return (
             out_str, err_str)

    def cmd_unpickle(self, cmd, comps, line, rem_line):
        """Unpickle file, returning (out_str, err_str)"""
        out_str, err_str = ('', '')
        if not comps:
            return (out_str, 'Please specify filename')
        else:
            filename = expandpath(comps.pop(0))
            filters = {}
            while comps:
                comp = comps.pop(0)
                field, sep, value = comp.partition('=')
                if sep:
                    filters[str(field)] = value

            try:
                PickleInterface.open_pickle_db(filename)
                keys = PickleInterface.read_keys_pickle_db(**filters)
                for key in keys:
                    dirs = ContextDict.split_trace_id(key)
                    context = OTrace.base_context[PICKLED_DIR]
                    for cdir in dirs:
                        if cdir not in context:
                            context[cdir] = {}
                        context = context[cdir]

                    context[ENTITY_CHAR] = None

            except Exception as excp:
                err_str = 'Error in unpickling from %s: %s' % (filename, excp)
                raise

            return (
             out_str, err_str)

    def cmd_pr(self, cmd, comps, line, rem_line, cmd_opts):
        """Print expression, returning (out_str, err_str)"""
        out_str, err_str = ('', '')
        if len(comps) == 1 and comps[0].startswith(PATH_SEP + BASE_DIR + PATH_SEP):
            tem_path = comps[0][len(PATH_SEP + BASE_DIR + PATH_SEP):].replace(PATH_SEP, '.').split('.')
            obj_value = self.get_subdir('base', tem_path, value=True)
            try:
                out_str = str(obj_value)
            except Exception as excp:
                err_str = str(excp)

            return (out_str, err_str)
        if '\n' in rem_line or '\r' in rem_line:
            err_str = 'Line breaks are not permitted in expressions'
        elif Set_params['safe_mode'] and ('(' in rem_line or re.search('[^=]=[^=]', rem_line)):
            err_str = 'Open parenthesis and assignment operator are not permitted in expressions in safe mode; set safe_mode False'
        else:
            if rem_line.lstrip().startswith('import ') or ASSIGNMENT_RE.match(rem_line):
                return (out_str, "Use 'exec' or '!' to execute import or assignment statements")
            if Set_params['pretty_print']:
                self.locals_dict['_otrace_pformat'] = otrace_pformat
                pr_command = '_otrace_pformat(' + rem_line + ', width=%d)' % self.tty_width
                out_str, err_str = self.push(pr_command, batch=True)
                del self.locals_dict['_otrace_pformat']
            elif cmd_opts.batch:
                out_str, err_str = self.push(rem_line, batch=True)
            else:
                self.locals_dict['_otrace_stdout'] = self._stdout
                self.locals_dict['_otrace_value'] = self.get_cur_value()
                if sys.version_info[0] < 3:
                    pr_command = 'print >>_otrace_stdout, ' + rem_line
                else:
                    pr_command = 'print(' + rem_line + ', file=_otrace_stdout)'
                out_str, err_str = self.push(pr_command)
                del self.locals_dict['_otrace_value']
                del self.locals_dict['_otrace_stdout']
            if err_str and re.search('[^=]=[^=]', rem_line):
                err_str += "\n Looks like a python assignment statement; try prefixing with 'exec' or '!'"
        return (
         out_str, err_str)

    def cmd_exec(self, cmd, comps, line, rem_line, cmd_opts):
        """Execute statement, returning (out_str, err_str)"""
        out_str, err_str = ('', '')
        if Set_params['safe_mode']:
            out_str, err_str = ('', 'Code execution not permitted in safe mode; set safe_mode False')
        else:
            out_str, err_str = self.push(rem_line, batch=False)
            out_str = out_str or ''
        return (
         out_str, err_str)

    def edit_view(self, cmd, comps, inline=False, here_doc=None):
        """Handle edit/view of files, returning (out_str, err_str) or raising AltHandler"""
        out_str, err_str = ('', '')
        if not comps:
            if self.in_base_dir():
                raise AltHandler()
            else:
                return ('', 'Must specify filename to edit/view')
        comps = comps[:]
        comp0 = comps[0]
        if is_absolute_path(comp0):
            if comp0 == PATH_SEP + BASE_DIR or comp0.startswith(PATH_SEP + BASE_DIR + PATH_SEP):
                raise AltHandler()
            filepath = comp0
        else:
            if self.in_base_dir():
                raise AltHandler()
            filepath = self.make_path_str() + PATH_SEP + comp0
        content = None
        if os.path.exists(filepath):
            try:
                with open(os_path(filepath), 'r') as (f):
                    content = f.read()
            except Exception as excp:
                return (
                 out_str, "Error in reading from '%s': %s" % (filepath, excp))

        basename, extension = os.path.splitext(filepath)
        if extension:
            filetype = FILE_EXTENSIONS.get(extension[1:].lower(), '')
        else:
            filetype = ''
        if cmd == 'view':
            if content is None:
                return ('', 'File %s not found' % filepath)
            else:
                if inline:
                    return (
                     content, err_str)
                OTrace.callback_handler.editback(content, filepath=filepath, filetype=filetype, editor=Set_params['editor'])
                return (out_str, err_str)

        if here_doc is None:
            mod_content, err_str = OTrace.callback_handler.editback(content, filepath=filepath, filetype=filetype, editor=Set_params['editor'], modify=True)
            if mod_content is None and err_str is None:
                return ('_NoPrompt_', None)
            if err_str:
                return (out_str, err_str)
        else:
            mod_content = here_doc
        if mod_content == content:
            return (
             out_str, 'No changes')
        else:
            try:
                with open(os_path(filepath), 'w') as (f):
                    f.write(mod_content)
            except Exception as excp:
                return (
                 out_str, "Error in saving file '%s': %s" % (filepath, excp))

            return ('', '')


class TraceOpts(object):
    """Trace match options
    """

    def __init__(self, trace_name, argmatch={}, break_count=-1, trace_call=False, trace_return=False, break_action=None, match_tag='', access_type=''):
        self.trace_name = trace_name
        self.argmatch = argmatch
        self.break_count = break_count
        self.trace_call = trace_call
        self.trace_return = trace_return
        self.break_action = break_action
        self.match_tag = match_tag
        self.access_type = access_type

    def __str__(self):
        if self.match_tag:
            taglabel = 'tagged' if self.match_tag == '*' else 'tagged' + self.match_tag
        else:
            taglabel = ''
        condition = self.argmatch or self.access_type or (taglabel if taglabel else 'all' if self.trace_call and self.trace_return else 'call' if self.trace_call else 'return' if self.trace_return else '')
        options = ''
        if self.break_action:
            options = options + '-a %s ' % self.break_action
        if condition:
            options = options + '-c %s ' % condition
        if self.break_count:
            options = options + '-n %d ' % self.break_count
        return '%s%s' % (options, self.trace_name)


class ContextDict(dict):
    """Dictionary for saving trace contexts
    """
    context_types = {'as': 'asserts', 'br': 'breaks', 'db': 'dbaccess', 'ex': 'exceptions', 'hd': 'holds', 'tg': 'tags', 'tr': 'traces'}

    def __init__(self, dirname=''):
        super(ContextDict, self).__init__()
        self.dirname = dirname
        self.trace_ids = collections.defaultdict(list)

    @classmethod
    def make_trace_id(cls, context_type, fullmethodname, id_label, trace_timestamp):
        """Creates trace_id, and return (trace_id, context_id)
        """
        ctype = 'un'
        for cshort, clong in cls.context_types.items():
            if context_type == clong:
                ctype = cshort

        if id_label:
            context_id = ctype + '-' + id_label
        else:
            context_id = ctype
        fullmethodname = fullmethodname.replace(TRACE_ID_SEP, '..')
        context_id = context_id.replace(TRACE_ID_SEP, '..')
        return (
         TRACE_ID_SEP.join((fullmethodname, context_id, trace_timestamp)), context_id)

    @classmethod
    def split_trace_id(cls, trace_id):
        fullmethodname, context_id, trace_timestamp = trace_id.split(TRACE_ID_SEP)
        ctype, sep, id_label = context_id.partition('-')
        if ctype not in cls.context_types:
            context_type = 'unknown'
        else:
            context_type = cls.context_types[ctype]
        return [context_type, fullmethodname, context_id, trace_timestamp]

    def remove_context(self, trace_id, keep_holds=False):
        """ Remove context (called from add_context, with RLock; should not block otrace thread)
        """
        with Trace_rlock:
            context_type, fullmethodname, context_id, trace_timestamp = self.split_trace_id(trace_id)
            if context_type == 'holds':
                try:
                    context = self[context_type][fullmethodname][context_id][trace_timestamp]
                    self_arg = context['self']
                    if self_arg and getattr(self_arg, OTrace.resume_attr, None):
                        if keep_holds:
                            return
                        resume_from_hold(self_arg)
                except Exception:
                    pass

            context_trace_ids = self.trace_ids[context_type]
            try:
                indx = context_trace_ids.index(trace_id)
                if indx >= 0:
                    del context_trace_ids[indx]
            except Exception:
                pass

            try:
                del self[context_type][fullmethodname][context_id][trace_timestamp]
                if not self[context_type][fullmethodname][context_id]:
                    del self[context_type][fullmethodname][context_id]
                    if not self[context_type][fullmethodname]:
                        del self[context_type][fullmethodname]
            except Exception:
                pass

        return

    def add_context(self, new_context, trace_id):
        """Adds context
        """
        with Trace_rlock:
            context_type, fullmethodname, context_id, trace_timestamp = self.split_trace_id(trace_id)
            context_trace_ids = self.trace_ids[context_type]
            context_trace_ids.append(trace_id)
            maxdir = 'max_' + self.dirname
            if Set_params.get(maxdir) and len(context_trace_ids) > Set_params[maxdir]:
                if context_type != 'breaks':
                    self.remove_context(context_trace_ids[0])
            if context_type not in self:
                self[context_type] = {}
            if fullmethodname not in self[context_type]:
                self[context_type][fullmethodname] = {}
            if context_id not in self[context_type][fullmethodname]:
                self[context_type][fullmethodname][context_id] = {}
            self[context_type][fullmethodname][context_id][trace_timestamp] = new_context
            return trace_id


class TraceCallback(object):
    """ Override this class to control logging of callbacks etc
    """

    def __init__(self, log_level=logging.ERROR, trace_len=0, logger=None, log_handler=None):
        self.log_level = log_level
        self.trace_len = trace_len
        self.remote_host = None
        self.logger = logger
        if not self.logger:
            self.logger = logging.getLogger('')
            self.logger.propagate = 0
        if not self.logger.handlers and not log_handler:
            log_handler = CallbackLogHandler()
        if log_handler:
            log_handler.setLevel(level=logging.WARNING)
            log_handler.setFormatter(logging.Formatter(fmt='%(name).4s%(levelname).1s %(message)s'))
            self.logger.addHandler(log_handler)
        return

    def loglevel(self, level=None):
        """ Set/return logging level
        Override this method, if need be.
        """
        if level is None:
            return self.logger.getEffectiveLevel()
        else:
            self.logger.setLevel(level)
            return level

    def tracelen(self, trace_len=None):
        """ Set trace message length, if not None.
        Return current trace message length
        """
        if trace_len is not None:
            self.trace_len = trace_len
        return self.trace_len

    def logformat(self, fmt=None):
        return ''

    def logmessage(self, log_level, msg, exc_info=None, logtype='', plaintext=''):
        if logtype or log_level is None or log_level >= self.log_level:
            if OShell.instance:
                prefix, suffix = OShell.instance.switch_screen(logtype)
            else:
                prefix, suffix = ('', '')
            sys.stderr.write(prefix + (plaintext or msg) + '\n' + suffix)
        return

    def remote_log(self, host=None, remove=False):
        """ Set host (:port) for remote logging. If host is omitted, return current remote host.
        If remove, remove current remote host.
        """
        if remove:
            self.remote_host = None
            for handler in self.logger.handlers:
                if isinstance(handler, logging.handlers.SocketHandler):
                    self.logger.removeHandler(handler)
                    handler.close()

            self.logger.addHandler(logging.StreamHandler())
            return
        else:
            if not host:
                return self.remote_host
            self.remote_host = host
            addr, sep, port = host.partition(':')
            if port:
                port = int(port)
            else:
                port = logging.handlers.DEFAULT_TCP_LOGGING_PORT
            for handler in self.logger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    self.logger.removeHandler(handler)
                    handler.close()

            self.logger.addHandler(logging.handlers.SocketHandler(addr, port))
            return

    def display_log(self, msg, trace_id='', prefix='', logtype='trace'):
        """Display log message, with message prefixed by trace_id or prefix"""
        log_level = self.log_level
        plaintext = ''
        if trace_id:
            if Set_params['allow_xml'] and OTrace.html_wrapper:
                subpath_names = ContextDict.split_trace_id(trace_id)
                markup = ['file:///' + PATH_SEP.join([BASE_DIR, RECENT_DIR] + subpath_names), 'x-python/object', 'cdls']
                plaintext = trace_id + ' ' + msg
                prefix = OShell.html_fmt % tuple(markup + [cgi.escape(trace_id)])
                msg = cgi.escape(msg)
            else:
                prefix = trace_id.replace('%', PATH_SEP)
            msg = prefix + ' ' + msg
            log_level += 10
            if trace_id.startswith('breaks') or trace_id.startswith('holds'):
                log_level += 10
        elif prefix:
            msg = prefix + ': ' + msg
            if Set_params['allow_xml'] and OTrace.html_wrapper:
                plaintext = msg
                msg = cgi.escape(msg)
        if Set_params['allow_xml'] and OTrace.html_wrapper:
            pass
        elif self.trace_len:
            msg = msg[:self.trace_len]
        self.logmessage(log_level, msg, logtype=logtype, plaintext=plaintext)

    def callback(self, trace_id, methodtype, modulename, classname, func_name, arg_val_pairs=[], nameless_args_list=[], retro=False):
        """ Handle function call trace.
        Override this method, if need be.
        """
        arg_vals_str = []
        for arg, val in arg_val_pairs:
            if isinstance(val, type):
                valstr = val.__name__
            else:
                valstr = str(val)
            arg_vals_str.append(arg + '=' + valstr)

        arg_vals_str += map(repr, nameless_args_list)
        call_str = (', ').join(arg_vals_str)
        if retro:
            func_name += '*'
        self.display_log(call_str, trace_id=trace_id, prefix='%s.%s' % (classname, func_name))

    def returnback(self, trace_id, methodtype, modulename, classname, func_name, result):
        """ Handle function return trace.
        Override this method, if need be.
        """
        return_str = 'return %s' % (str(result),)
        self.display_log(return_str, trace_id=trace_id, prefix='%s.%s' % (classname, func_name))

    def accessback(self, trace_id, op_type, key_str, entity):
        """ Handle database access callback
        Override this method, if need be.
        """
        msg = 'access %s %s' % (op_type, key_str)
        self.display_log(msg, trace_id=trace_id)

    def editback(self, content, filepath='', filetype='', editor='', modify=False):
        """ Create temp file with content, and display using editor.
        If not modify, return (content, None) after displaying content.
        On successful modification, returns (modified_content, "").
        On error, returns (None, err_str).
        File is deleted before returning.
        If implementing delayed modification, returns (None, None);
        subsequent command can provide modified data through stdin "here" document.
        """
        if not editor:
            editor = 'vi'
        tempname = None
        try:
            try:
                funit, tempname = tempfile.mkstemp(suffix='.py', text=True)
                try:
                    try:
                        os.write(funit, content)
                    except Exception as excp:
                        return (
                         None, 'Error in writing to temp file %s: %s' % (tempname, excp))

                finally:
                    os.close(funit)

                ret_code = subprocess.call([editor, tempname])
                if ret_code:
                    return (None, 'Error in editing %s (%s): %s' % (filepath, tempname, ret_code))
            except Exception as excp:
                return (
                 None, 'Error in editing %s (%s): %s' % (filepath, tempname, ret_code))

            if not modify:
                return (content, None)
            try:
                with open(os_path(tempname), 'r') as (tempf):
                    return (
                     tempf.read(), '')
            except Exception as excp:
                return (
                 None, "Error in reading temp file '%s': %s" % (tempname, excp))

        finally:
            if tempname:
                try:
                    os.remove(tempname)
                except Exception:
                    pass

        return


class DefaultCallback(TraceCallback):
    """ Simple default callback implementation
    """

    def logmessage(self, log_level, msg, exc_info=None, logtype='', plaintext=''):
        if log_level is None or log_level >= self.log_level:
            super(DefaultCallback, self).logmessage(None, msg, exc_info=exc_info, logtype=logtype, plaintext=plaintext)
        return


class CallbackLogHandler(logging.Handler):

    def __init__(self):
        self.recursion_lock = set()
        logging.Handler.__init__(self)

    def emit(self, record):
        if OTrace.callback_handler:
            try:
                thread_name = threading.currentThread().getName()
            except Exception:
                thread_name = ''

            if thread_name in self.recursion_lock:
                return
            self.recursion_lock.add(thread_name)
            try:
                try:
                    msg = self.format(record)
                    OTrace.callback_handler.logmessage(None, msg)
                except Exception:
                    self.handleError(record)

            finally:
                self.recursion_lock.discard(thread_name)

        return

    def flush(self):
        pass


class HtmlWrapper(object):
    """ Wrapper for HTML output
    """

    def wrap(self, html, msg_type=''):
        return html


class FunctionInfo(object):
    """ Return object containing information about a function"""

    def __init__(self, function, classname='', modulename='', methodtype=''):
        self.fn = function
        self.classname = classname
        self.modulename = modulename
        self.methodtype = methodtype
        func_code = function.func_code
        func_defaults = function.func_defaults
        argcount = func_code.co_argcount
        self.argnames = func_code.co_varnames[:argcount]
        if func_defaults:
            self.argdefs = dict(zip(self.argnames[-len(func_defaults):], func_defaults))
        else:
            self.argdefs = {}


class OTrace(object):
    """Object tracing class.
    All methods are class methods
    Class cannot be instantiated.
    """
    class_trace_attr = '_otrace_class_trace'
    orig_function_attr = '_otrace_orig_function'
    unpatched_function_attr = '_otrace_unpatched_function'
    patch_parent_attr = '_otrace_patch_parent'
    patch_source_attr = '_otrace_patch_source'
    orig_generator_name_attr = '_otrace_orig_generator_name'
    hold_attr = '_otrace_hold'
    resume_attr = '_otrace_resume'
    trace_tag_attr = '_otrace_tag'
    interpreter = TraceInterpreter()
    callback_handler = DefaultCallback()
    hold_wrapper = None
    eventloop_callback = None
    html_wrapper = None
    default_context = {'__name__': '__otrace__', '__doc__': None, '_trace_id': None, 
       '_trace_related': {}}
    base_context = {ALL_DIR: weakref.WeakValueDictionary(), GLOBALS_DIR: {}, LOCALS_DIR: {}, PATCHES_DIR: {}, RECENT_DIR: ContextDict(dirname=RECENT_DIR), 
       SAVED_DIR: ContextDict(dirname=SAVED_DIR)}
    prev_timestamp = [
     None]
    recent_pathnames = [
     BASE_DIR, GLOBALS_DIR]
    recent_trace_id = [None]
    recent_trace_context = [None]
    trace_id_set = set()
    trace_log_set = set()
    trace_names = {}
    trace_keys = {}
    trace_all = False
    trace_active = False

    def __new__(cls, *args, **kwargs):
        raise OTraceException('Class cannot be instantiated')

    @classmethod
    def setup(cls, start_path=[
 BASE_DIR, GLOBALS_DIR], callback_handler=None, hold_wrapper=None, eventloop_callback=None):
        cls.recent_pathnames = start_path
        if callback_handler:
            cls.callback_handler = callback_handler
        if hold_wrapper:
            cls.hold_wrapper = hold_wrapper
        if eventloop_callback:
            cls.eventloop_callback = eventloop_callback

    @classmethod
    def class_method_names(cls, method, parent=None):
        """Analyzes method and returns tuple (classname, methodname)
        Raises OTraceException on failure
        """
        classname = ''
        methodname = ''
        if isinstance(method, str):
            if '.' in method:
                classname, methodname = method.split('.')
            else:
                methodname = method
        elif inspect.isclass(method):
            classname = method.__name__
        elif inspect.isclass(parent):
            methodname = method.__name__
            classname = parent.__name__
        elif inspect.isfunction(method):
            methodname = method.__name__
        elif hasattr(method, '__name__'):
            methodname = method.__name__
        else:
            raise OTraceException('add_trace: Cannot trace object ' + str(method))
        return (classname, methodname)

    @classmethod
    def set_database_root(cls, root_tree):
        cls.base_context[DATABASE_DIR] = root_tree

    @classmethod
    def set_web_root(cls, root_tree):
        cls.base_context[WEB_DIR] = root_tree

    @classmethod
    def add_trace(cls, method=None, parent=None, argmatch={}, break_count=-1, trace_call=False, trace_return=False, break_action=None, match_tag='', access_type=''):
        """To trace all, method = "*"
        To list all methods traced, method = None
        To trace class, method="classname." or classname
        To trace method of any class, method=".methodname"
        To trace bound method method ="classname.methodname" or self.methodname
        To trace function, method = "functionname" or functionname
        argmatch = {"arg1": "value1", "self.arg2": "value2", "arg3":{"entry31": "value31", "entry32","value32"},
        "arg4!=": "value4", "return": "retvalue"}
        Returns full name of method traced, or null string
        If neither trace_call nor trace_return are specified, only exceptions are traced.
        To trace entity keys, trace /kind:name/... get/put/delete/modify/all
        """
        with Trace_rlock:
            if not method:
                trace_names_list = cls.trace_names.keys() + cls.trace_keys.keys()
                trace_names_list.sort()
                if cls.trace_all:
                    trace_names_list.insert(0, '*')
                return trace_names_list
            cls.trace_active = True
            if argmatch:
                ret_match = [ key == 'return' or key.startswith('return.') for key in argmatch ]
                if any(ret_match):
                    trace_return = True
                if break_action != 'tag' and not all(ret_match):
                    trace_call = True
            if method == '*':
                cls.trace_all = True
                return '*'
            if isinstance(method, basestring) and method.startswith(PATH_SEP):
                cls.trace_keys[method] = TraceOpts(method, argmatch=argmatch, break_count=break_count, access_type=access_type, break_action=break_action)
                return method
            if isinstance(method, basestring) and method[0] == TRACE_LABEL_PREFIX:
                fullname = method
            elif isinstance(method, basestring) and method.startswith(TRACE_LOG_PREFIX):
                fullname = method
                cls.trace_log_set.add(fullname)
            else:
                if not isinstance(argmatch, dict):
                    raise OTraceException('add_trace: argmatch must be a dict instance')
                classname, methodname = cls.class_method_names(method, parent)
                fullname = methodname if not classname else classname + '.' + methodname
            trace_opts = TraceOpts(fullname, argmatch=argmatch, break_count=break_count, trace_call=trace_call, trace_return=trace_return, break_action=break_action, match_tag=match_tag)
            cls.trace_names[fullname] = trace_opts
        return fullname

    @classmethod
    def remove_trace(cls, method=None, parent=None):
        """To remove all traces, specify method = "all".
        Returns full name of method untraced, or null string
        """
        if not method:
            raise OTraceException("Specify name to untrace or 'all'")
        if method == 'all':
            cls.clear_trace()
            return 'all tracing'
        with Trace_rlock:
            untrace_name = ''
            retvalue = ''
            if method == '*':
                cls.trace_all = False
                retvalue = '*'
            elif method.startswith(PATH_SEP):
                try:
                    del cls.trace_keys[method]
                    retvalue = method
                except Exception:
                    pass

            elif isinstance(method, basestring) and method[0] == TRACE_LABEL_PREFIX:
                untrace_name = method
            elif isinstance(method, basestring) and method.startswith(TRACE_LOG_PREFIX):
                untrace_name = method
                cls.trace_log_set.discard(untrace_name)
            else:
                try:
                    classname, methodname = cls.class_method_names(method, parent)
                    untrace_name = methodname if not classname else classname + '.' + methodname
                except Exception:
                    pass

            if untrace_name:
                try:
                    del cls.trace_names[untrace_name]
                except Exception:
                    pass

            if not cls.trace_id_set and not cls.trace_all and not cls.trace_names and not cls.trace_keys:
                cls.trace_active = False
            return retvalue or untrace_name

    @classmethod
    def make_tag(cls, obj, tag=''):
        if not tag or tag == 'id':
            return '0x%x' % id(obj)
        else:
            if tag == 'time':
                return cls.get_timestamp()
            return tag

    @classmethod
    def set_tag(cls, obj, trace_tag):
        setattr(obj, cls.trace_tag_attr, trace_tag)

    @classmethod
    def get_tag(cls, obj):
        return getattr(obj, cls.trace_tag_attr, None)

    @classmethod
    def remove_tag(cls, obj):
        with Trace_rlock:
            deleted_value = getattr(obj, cls.trace_tag_attr, None)
            delattr(obj, cls.trace_tag_attr)
            return deleted_value
        return

    @classmethod
    def track_trace_id(cls, trace_id=''):
        with Trace_rlock:
            if trace_id:
                cls.trace_id_set.add(trace_id)
            else:
                cls.trace_id_set.clear()
            if not cls.trace_id_set and not cls.trace_all and cls.trace_names and not cls.trace_keys:
                cls.trace_active = False

    @classmethod
    def clear_trace(cls):
        """Clear all tracing
        """
        with Trace_rlock:
            cls.trace_active = False
            cls.trace_all = False
            cls.trace_id_set.clear()
            cls.trace_names.clear()
            cls.trace_keys.clear()

    @classmethod
    def break_flow(cls, trace_id, action='break'):
        if action == 'break':
            break_event = threading.Event()
            OShell.instance.break_queue.put((trace_id, break_event))
            break_event.wait()
        else:
            OShell.invoke_debugger(action)

    @classmethod
    def tracereturn(cls, return_value):
        """Handles tracing of return values
        """
        if not cls.trace_active:
            return
        frameobj, filename, lineno, function, code_context, index = inspect.stack(context=0)[1]
        args, varargs, varkw, locals_dict = inspect.getargvalues(frameobj)
        try:
            locals_dict = locals_dict.copy()
            if 'self' in locals_dict:
                try:
                    setattr(locals_dict['self'], '_trace_' + function + '_locals', str(locals_dict))
                except Exception:
                    pass

            return return_value
        finally:
            del frameobj
            del args
            del varargs
            del varkw
            del locals_dict

    @classmethod
    def traceassert(cls, condition, label='', action=None):
        """Trace assertions.
        If not tracing, simply acts like "assert condition, label".
        If action=="break", break execution if condition is False.
        If action=="ipdb" or "pdb", invokes ipdb/pdb if condition is False.
        If action=="hold", returns a callable object that accepts a single argument, callback,
          wrapped in a hold_wrapper.
          The callable object will schedule an immediate callback in the event loop if condition is True,
          but delays the callback until the "resume" command, if condition is False.
        """
        if condition:
            if action == 'hold' and cls.hold_wrapper:
                return cls.hold_wrapper(schedule_callback)
            return
        if not (cls.trace_active or condition):
            raise AssertionError, label
            return
        frame_records = inspect.stack(context=Set_params['assert_context'])[1:]
        frameobj, filename, lineno, funcname, code_context, index = frame_records[0]
        frame_records.reverse()
        argvalues = inspect.getargvalues(frameobj)
        args, varargs, varkw, caller_locals_dict = argvalues
        try:
            fullmethodname = funcname
            methodtype = ''
            classname = ''
            modulename = ''
            self_arg = caller_locals_dict.get('self')
            if self_arg:
                try:
                    classname = self_arg.__class__.__name__
                    if classname:
                        fullmethodname = classname + '.' + funcname
                        methodtype = 'instancemethod'
                except Exception:
                    pass

            locals_dict = cls.traverse_framestack(frame_records, copy_locals=bool(Set_params['assert_context']))
            locals_dict.set_trc('argstr', inspect.formatargvalues(*argvalues))
            if action == 'break':
                context_type = 'breaks'
            else:
                if action == 'hold':
                    context_type = 'holds'
                else:
                    context_type = 'asserts'
                trace_context, trace_id = cls.create_context(fullmethodname, self_arg, locals_dict, id_label=label, context_type=context_type)
                cls.callback_handler.callback(trace_id, methodtype, modulename, classname, funcname)
                if action == 'hold':
                    return check_for_hold(self_arg)
            if action in BREAK_ACTIONS:
                cls.break_flow(trace_id, action=action)
        finally:
            del frame_records
            del frameobj
            del argvalues
            del args
            del varargs
            del varkw
            del caller_locals_dict

        try:
            del locals_dict
        except Exception:
            pass

        return

    @classmethod
    def untag(cls, obj):
        """Removes tag from object
        """
        return cls.remove_tag(obj)

    @classmethod
    def tag(cls, obj, tag, **kwargs):
        """ Tags object, where tag = "id" (default), "time", or any other string.
        kwargs are additional variables (dict) to save in the tag context
        """
        if not isinstance(obj, object):
            raise Exception('Only instances of object can be tagged')
        self_arg = obj
        trace_tag = cls.make_tag(self_arg, tag=tag)
        locals_dict = {}
        if kwargs:
            locals_dict.update(kwargs)
        locals_dict['self'] = self_arg
        methodtype = ''
        classname = obj.__class__.__name__
        function = ''
        modulename = ''
        fullmethodname = classname
        context_type = 'tags'
        trace_context, trace_id = cls.create_context(fullmethodname, self_arg, locals_dict, id_label=trace_tag, context_type=context_type)
        cls.set_tag(self_arg, trace_id)
        cls.callback_handler.callback(trace_id, methodtype, modulename, classname, function)
        return trace_id

    @classmethod
    def get_timestamp(cls):
        with Trace_rlock:
            TRACE_TIMESTAMP_FORMAT = '%y%m%d-%H-%M-%S'
            utctime = datetime.datetime.utcnow()
            short_timestamp = utctime.strftime(TRACE_TIMESTAMP_FORMAT)
            long_timestamp = short_timestamp + '.%06d' % (utctime.microsecond // 1000,)
            if not cls.prev_timestamp[0]:
                trace_timestamp = short_timestamp
            elif long_timestamp.startswith(cls.prev_timestamp[0]):
                prev_len = len(cls.prev_timestamp[0])
                if prev_len > len(short_timestamp):
                    trace_timestamp = long_timestamp[:prev_len + 1]
                else:
                    trace_timestamp = long_timestamp[:prev_len + 2]
            else:
                for j, ch in enumerate(cls.prev_timestamp[0]):
                    if ch != long_timestamp[j]:
                        slen = max(j + 1, len(short_timestamp))
                        trace_timestamp = long_timestamp[:slen]
                        break

            cls.prev_timestamp[0] = trace_timestamp
            return trace_timestamp

    @classmethod
    def create_context(cls, fullmethodname, self_arg, locals_dict, id_label='', context_type='traces', excp=None, exc_info=None):
        """Creates new context (locals_dict) and returns (trace_id, trace_context)
        """
        trace_id, context_id = ContextDict.make_trace_id(context_type, fullmethodname, id_label, cls.get_timestamp())
        new_context_path = [BASE_DIR, RECENT_DIR] + ContextDict.split_trace_id(trace_id)
        if self_arg is not None:
            if context_type == 'holds' and cls.hold_wrapper:
                try:
                    setattr(self_arg, cls.hold_attr, cls.hold_wrapper(HoldHandler(self_arg, PATH_SEP + PATH_SEP.join(new_context_path))))
                except Exception:
                    pass

        new_context = TraceDict(locals_dict)
        new_context.set_trc('id', trace_id)
        new_context.set_trc('thread', threading.currentThread().getName())
        new_context.set_trc('context', context_type)
        new_context.set_trc('related', {})
        new_context['__name__'] = '__console__'
        new_context['__doc__'] = None
        if Set_params['append_traceback'] and excp and not isinstance(excp, StopIteration):
            excp_str = excp.args[0] if excp.args and isinstance(excp.args[0], basestring) else ''
            iappend = excp_str.find('\n')
            if iappend < 0:
                iappend = len(excp_str)
                excp_str += '\n'
            pre_str, post_str = excp_str[:iappend + 1], excp_str[iappend + 1:]
            if post_str.startswith(TRACE_ID_PREFIX):
                tb_str = ''
                j = post_str.find('\n')
                if j > 0:
                    prev_trace_id = post_str[len(TRACE_ID_PREFIX):j]
                    post_str = post_str[j + 1:]
                    new_context[TRACE_ID_PREFIX + prev_trace_id] = None
            else:
                tb_str = ('').join(format_traceback(exc_info)) if exc_info else ''
            new_excp_str = pre_str + TRACE_ID_PREFIX + trace_id + '\n' + tb_str + post_str
            new_context.set_trc('exception', new_excp_str)
            if excp.args:
                excp.args = tuple([new_excp_str] + list(excp.args[1:]))
            else:
                excp.args = (
                 new_excp_str,)
        with Trace_rlock:
            cls.base_context[RECENT_DIR].add_context(new_context, trace_id)
            cls.base_context[ALL_DIR][trace_id] = new_context
            if context_type == 'tags' and Set_params['save_tags']:
                cls.base_context[SAVED_DIR].add_context(new_context, trace_id)
            del cls.recent_pathnames[:]
            cls.recent_pathnames += new_context_path
            cls.recent_trace_id[0] = trace_id
            cls.recent_trace_context[0] = new_context
            if PickleInterface.write_connection:
                PickleInterface.write_pickle_db(trace_id, new_context)
            return (
             new_context, trace_id)
        return

    @classmethod
    def remove_break_point(cls, trace_id):
        with Trace_rlock:
            subpath_names = [
             RECENT_DIR] + ContextDict.split_trace_id(trace_id)
            if subpath_names == cls.recent_pathnames[BASE_OFFSET:]:
                del cls.recent_pathnames[:]
                cls.recent_pathnames += [BASE_DIR, GLOBALS_DIR]
            cls.base_context[RECENT_DIR].remove_context(trace_id)

    @classmethod
    def evaluate_in_context(cls, expression, trace_id=None, globals_dict={}, print_out=False):
        """ Evaluate expression; return output string, if print_out is True,
        Use the argument variables associated with trace_id as the context.
        If trace_id is None, use last trace context.
        If trace_id is not recognized, or is set to null string, the default context is used.
        Returns tuple (out_str, err_str)
        """
        context = None
        if trace_id is None:
            recent_traces = cls.base_context[RECENT_DIR].get('traces')
            if recent_traces:
                trace_id = recent_traces.keys()[0]
                context = cls.base_context[RECENT_DIR]['traces'][trace_id]
        else:
            context = cls.base_context[ALL_DIR].get(trace_id)
        if not context:
            context = cls.default_context
        out_str, err_str = cls.interpreter.evaluate(expression, locals_dict=context, globals_dict=globals_dict, print_out=print_out)
        if err_str is None:
            err_str = out_str
            out_str = ''
        return (
         out_str, err_str)

    @classmethod
    def traverse_framestack(cls, frame_records, exc_info=None, copy_locals=False):
        """Traverses frame stack and initializes locals_dict for each frame,
        and returns the final locals_dict
        (for an exception, this would be for the frame where exception occurred)
        """
        prev_locals_dict = None
        framestack = []
        for j, frame_record in enumerate(frame_records):
            frameobj, srcfile, linenum, funcname, lines, index = frame_record
            if funcname in IGNORE_FUNCNAMES:
                continue
            if copy_locals or j + 1 == len(frame_records):
                args, varargs, varkw, locals_dict = inspect.getargvalues(frameobj)
                locals_dict = TraceDict(cls.copy_or_not(locals_dict, split=True))
                locals_dict.set_trc('argvalues', (args, varargs, varkw))
            else:
                locals_dict = TraceDict({})
            locals_dict.set_trc('frame', (srcfile, linenum, funcname, lines))
            locals_dict.set_trc('funcname', funcname)
            if prev_locals_dict is not None:
                locals_dict[UP_STACK] = prev_locals_dict
                prev_locals_dict[DOWN_STACK] = locals_dict
            prev_locals_dict = locals_dict
            framestack.append(locals_dict.get_trc('frame'))

        locals_dict.set_trc('framestack', LineList(framestack))
        locals_dict.set_trc('where', ('-->').join([ x[2] for x in framestack ]))
        if exc_info:
            locals_dict.set_trc('exc_stack', ('').join(traceback.format_exception(*exc_info)))
            try:
                if Set_params['allow_xml'] and cls.html_wrapper:
                    locals_dict.set_trc('exc_context', cls.html_wrapper.wrap(cgitb.html(exc_info, 5)))
                else:
                    locals_dict.set_trc('exc_context', cgitb.text(exc_info, 5))
            except Exception as excp:
                pass

        return locals_dict

    @classmethod
    def check_trace_match(cls, fn, fullmethodname, self_arg, arg_dict, trace_dict=None, break_action=None, on_return=False, return_value=None, match_tag=''):
        """ Trace dict example:
        {"arg1": "value1", "self.arg2": "value2", "arg3":{"entry31": "value31", "entry32","value32"},
        "arg4!=": "value4", "return": "retvalue"}
        Returns triplet tuple (trace_context, trace_id, related_id)
        trace_context: None, or dict if a trace condition was matched
        trace_id: Trace ID for matched condition (including classname prefix)
        related_id: If no trace match, relate to tag match (or null string, if none)

        If break_action == "tag", a tag "trace_id" is returned on successful match, and
        no new context id is created.
        """
        if isinstance(trace_dict, dict):
            if not on_return and trace_dict and all(key == 'return' or key.startswith('return.') for key in trace_dict):
                return (None, '', '')
            trace_matched = True
            matched_list = []
            if match_tag:
                if match_tag == '*':
                    check_args = arg_dict.items()
                else:
                    check_args = [(match_tag, arg_dict[match_tag])] if match_tag in arg_dict else []
                trace_matched = False
                for arg_name, arg_value in check_args:
                    trace_tag = getattr(arg_value, cls.trace_tag_attr, None)
                    if trace_tag:
                        trace_matched = True
                        matched_list = ['tagged%s;%s' % (arg_name, trace_tag.split(':')[1])]
                        break

            else:
                if not trace_dict:
                    pass
                else:
                    for trace_name, trace_value in trace_dict.items():
                        trace_name, cmp_op = strip_compare_op(trace_name)
                        arg_name, sep, prop_name = trace_name.partition('.')
                        if arg_name == 'return':
                            if on_return:
                                actual_value = return_value
                            else:
                                continue
                        else:
                            if arg_name not in arg_dict:
                                continue
                            actual_value = arg_dict[arg_name]
                            if prop_name:
                                if not hasattr(actual_value, prop_name):
                                    continue
                                actual_value = getattr(actual_value, prop_name)
                        if isinstance(actual_value, dict) and isinstance(trace_value, dict):
                            for inner_key, inner_value in trace_value:
                                if inner_key in actual_value:
                                    if compare(actual_value[inner_key], cmp_op, inner_value):
                                        matched_list.append('%s.%s%s%s' % (trace_name, inner_key, cmp_op, inner_value))
                                    else:
                                        trace_matched = False
                                        break

                            if not trace_matched:
                                break
                        elif compare(actual_value, cmp_op, trace_value):
                            matched_list.append('%s%s%s' % (trace_name, cmp_op, trace_value))
                        else:
                            trace_matched = False
                            break

                if trace_matched:
                    matched_list.sort()
                    id_label = (',').join(matched_list).replace(':', ';')
                    if break_action == 'tag':
                        id_label += ';0x%x' % id(self_arg)
                        return (
                         None, id_label, '')
                    if not id_label:
                        id_label = 'return' if on_return else 'call'
                    if break_action == 'break':
                        context_type = 'breaks'
                    elif break_action == 'hold':
                        context_type = 'holds'
                    else:
                        context_type = 'traces'
                    locals_dict = TraceDict(cls.copy_or_not(arg_dict, split=True))
                    locals_dict.set_trc('stack', LineList(traceback.format_stack()[:-3]))
                    locals_dict.set_trc('func', fn)
                    trace_context, trace_id = cls.create_context(fullmethodname, self_arg, locals_dict, id_label=id_label, context_type=context_type)
                    return (
                     trace_context, trace_id, '')
        related_id = ''
        if Set_params['trace_related']:
            if on_return:
                if hasattr(return_value, cls.trace_tag_attr):
                    related_id = getattr(return_value, cls.trace_tag_attr)
            else:
                for arg_name, arg_value in arg_dict.items():
                    if hasattr(arg_value, cls.trace_tag_attr):
                        with Trace_rlock:
                            related_id = getattr(arg_value, cls.trace_tag_attr)
                            related_context = cls.base_context['tags'].get(related_id)
                            if related_context and self_arg and '__class__' in self_arg:
                                related_context.get_trc('related')[self_arg.__class__.__name__] = self_arg
                        break

        return (
         None, '', related_id)

    @classmethod
    def copy_or_not(cls, obj, split=False, keep_self=True):
        """Return deepcopy of obj if deep_copy parameter is set and obj has attribute
        __deepcopy__ or is a (dict,list,set,tuple) else just return obj
        If split, process list or dict values individually and re-group them,
        creating at atleast a shallow copy of the list/dict in the process.
        If keep_self (default), keep original self, and store copy as self_copy
        """
        if not Set_params['deep_copy']:
            return obj
        if not split:
            if hasattr(obj, '__deepcopy__') or isinstance(obj, (dict, list, set, tuple)):
                return copy.deepcopy(obj)
            else:
                return obj

        if isinstance(obj, list):
            return map(cls.copy_or_not, obj)
        if isinstance(obj, dict):
            obj_copy = dict(zip(obj.keys(), map(cls.copy_or_not, obj.values())))
            if keep_self and 'self' in obj and obj_copy['self'] is not obj['self']:
                obj_copy['self_copy'] = obj_copy['self']
                obj_copy['self'] = obj['self']
            return obj_copy
        raise Exception('Unable to split %s' % type(obj))

    @classmethod
    def otrace_function_call(cls, info, *args, **kwargs):
        """Auxiliary method used by wrapper in trace_function
        """
        if not cls.trace_active:
            return info.fn(*args, **kwargs)
        else:
            argcount = len(info.argnames)
            args_pairs = zip(info.argnames, args)
            kwargs_pairs = kwargs.items()
            defaulted_pairs = [ (x, info.argdefs[x]) for x in info.argnames[argcount - len(info.argdefs):argcount] if x not in kwargs
                              ]
            info.arg_val_pairs = args_pairs + kwargs_pairs + defaulted_pairs
            info.nameless_args_list = args[argcount:]
            info.arg_dict = OrderedDict(info.arg_val_pairs)
            if info.methodtype == 'instancemethod' and argcount:
                info.self_arg = info.arg_val_pairs[0][1]
            else:
                info.self_arg = None
            if not info.classname:
                info.fullname = info.fn.__name__ if 1 else info.classname + '.' + info.fn.__name__
                with Trace_rlock:
                    trace_opts = cls.trace_names.get(info.fullname)
                    class_match = False
                    if not trace_opts:
                        if info.classname:
                            trace_opts = cls.trace_names.get('.' + info.fn.__name__)
                            if not trace_opts:
                                trace_opts = cls.trace_names.get(info.classname + '.')
                                if trace_opts:
                                    class_match = True
                info.name_matched = False
                info.return_match_dict = None
                info.trace_context, info.trace_id, info.related_id = (None, None, None)
                trace_call, trace_return, break_action, match_tag = (False, False, None, '')
                if cls.trace_all:
                    info.name_matched = True
                if trace_opts:
                    trace_call = trace_opts.trace_call
                    break_action = trace_opts.break_action
                    match_tag = trace_opts.match_tag
                    if not trace_opts.argmatch and not match_tag and break_action != 'tag':
                        info.name_matched = True
                    if trace_opts.trace_return:
                        if break_action == 'tag':
                            info.return_match_dict = trace_opts.argmatch
                        elif class_match:
                            info.return_match_dict = trace_opts.argmatch
                        elif trace_opts.argmatch:
                            ret_argmatch = [ (key, value) for key, value in trace_opts.argmatch.items() if key == 'return' or key.startswith('return.') ]
                            if ret_argmatch:
                                info.return_match_dict = dict(ret_argmatch)
                    if match_tag or not class_match and trace_opts.trace_call:
                        info.trace_context, info.trace_id, info.related_id = cls.check_trace_match(info.fn, info.fullname, info.self_arg, info.arg_dict, trace_dict=trace_opts.argmatch, break_action=break_action, match_tag=match_tag)
                        if info.trace_context:
                            with Trace_rlock:
                                if trace_opts.break_count < 0:
                                    trace_opts.break_count += 1
                                    info.trace_context, info.trace_id, info.related_id = (None,
                                                                                          None,
                                                                                          None)
                                elif trace_opts.break_count > 0:
                                    trace_opts.break_count -= 1
                                    if trace_opts.break_count == 0:
                                        cls.remove_trace(trace_opts.trace_name)
                info.call_display = (info.name_matched or info.trace_context or info.related_id) and (trace_call or match_tag)
                if info.call_display:
                    cls.callback_handler.callback(info.trace_id, info.methodtype, info.modulename, info.classname, info.fn.__name__, info.arg_val_pairs, info.nameless_args_list)
                    if break_action in BREAK_ACTIONS:
                        cls.break_flow(info.trace_id, action=break_action)
                return_value = trace_opts or info.fn(*args, **kwargs)
                if isinstance(return_value, types.GeneratorType):
                    return return_value
            else:
                try:
                    return_value = info.fn(*args, **kwargs)
                    if isinstance(return_value, types.GeneratorType):
                        wrapped_gen = cls.trace_generator(info, trace_opts, return_value)
                        try:
                            code_obj = getattr(return_value, 'gi_code', None)
                            frame_obj = getattr(return_value, 'gi_frame', None)
                            if not code_obj and frame_obj and hasattr(frame_obj, 'f_code'):
                                code_obj = frame_obj.f_code
                            if code_obj:
                                gen_name = getattr(code_obj, 'co_name', '') + ':' + getattr(code_obj, 'co_filename', '') + ':*'
                                setattr(wrapped_gen, cls.orig_generator_name_attr, gen_name)
                        except Exception:
                            pass

                        if info.call_display and break_action == 'hold' and cls.hold_wrapper and info.self_arg is not None:
                            try:
                                context_path = [
                                 BASE_DIR, RECENT_DIR] + list(ContextDict.split_trace_id(info.trace_id))
                                async_handler = cls.hold_wrapper(HoldHandler(info.self_arg, PATH_SEP + PATH_SEP.join(context_path), resume_value=wrapped_gen))
                                setattr(info.self_arg, cls.hold_attr, async_handler)
                                return async_handler
                            except Exception:
                                pass

                        else:
                            return wrapped_gen
                except StopIteration:
                    raise
                except Exception as excp:
                    try:
                        raise
                    finally:
                        id_label = getattr(excp, '__name__', None)
                        if not id_label and hasattr(excp, '__class__'):
                            id_label = excp.__class__.__name__
                        exc_info = sys.exc_info()
                        innerframe_records = inspect.trace()
                        outerframe_records = inspect.getouterframes(innerframe_records[0][0])
                        outerframe_records.reverse()
                        frame_records = outerframe_records + innerframe_records[1:]
                        try:
                            try:
                                locals_dict = cls.traverse_framestack(frame_records, exc_info, copy_locals=True)
                                dummy_context, trace_id = cls.create_context(info.fullname, info.self_arg, locals_dict, id_label=id_label, context_type='exceptions', excp=excp, exc_info=exc_info)
                                cls.callback_handler.callback(trace_id, info.methodtype, info.modulename, info.classname, info.fn.__name__)
                            except Exception:
                                pass

                        finally:
                            del innerframe_records
                            del outerframe_records
                            del frame_records

                        try:
                            del locals_dict
                            del dummy_context
                        except Exception:
                            pass

            return cls.trace_return_value(info, trace_opts, False, return_value)

    @classmethod
    def trace_return_value(cls, info, trace_opts, trampoline_return, return_value):
        trace_call, trace_return, break_action, match_tag = (
         False, False, None, False)
        if trace_opts:
            trace_return = trace_opts.trace_return
            break_action = trace_opts.break_action
            match_tag = trace_opts.match_tag
        if match_tag or not info.trace_context and info.return_match_dict and info.self_arg:
            info.trace_context, info.trace_id, info.related_id = cls.check_trace_match(info.fn, info.fullname, info.self_arg, info.arg_dict, trace_dict=info.return_match_dict, break_action=break_action, on_return=True, return_value=return_value, match_tag=match_tag)
        if info.trace_context:
            info.trace_context.set_trc('return_value', return_value)
        return_display = (info.name_matched or info.trace_context or info.related_id) and (trace_return or match_tag and not info.call_display)
        if break_action == 'tag':
            if info.trace_id and info.self_arg:
                cls.tag(info.self_arg, info.trace_id, **info.arg_dict)
        elif return_display:
            if not info.call_display:
                cls.callback_handler.callback(info.trace_id, info.methodtype, info.modulename, info.classname, info.fn.__name__, info.arg_val_pairs, info.nameless_args_list, retro=True)
                if info.trace_context:
                    with Trace_rlock:
                        if trace_opts and trace_opts.break_count < 0:
                            trace_opts.break_count += 1
                            info.trace_context, info.trace_id, info.related_id = (None,
                                                                                  None,
                                                                                  None)
                        elif trace_opts and trace_opts.break_count > 0:
                            trace_opts.break_count -= 1
                            if trace_opts.break_count == 0:
                                cls.remove_trace(trace_opts.trace_name)
            cls.callback_handler.returnback(info.trace_id, info.methodtype, info.modulename, info.classname, info.fn.__name__, return_value)
            if break_action in BREAK_ACTIONS:
                cls.break_flow(info.trace_id, action=break_action)
            elif break_action == 'hold' and trampoline_return and cls.hold_wrapper and info.self_arg is not None:
                try:
                    context_path = [
                     BASE_DIR, RECENT_DIR] + ContextDict.split_trace_id(info.trace_id)
                    async_handler = cls.hold_wrapper(HoldHandler(info.self_arg, PATH_SEP + PATH_SEP.join(context_path), resume_value=return_value))
                    setattr(info.self_arg, cls.hold_attr, async_handler)
                    return async_handler
                except Exception:
                    pass

        return return_value

    @classmethod
    def trace_generator(cls, info, trace_opts, gen):
        send_value = None
        exception_flag = False
        while True:
            try:
                if exception_flag:
                    yield_value = gen.throw(type(send_value), send_value.args)
                else:
                    yield_value = gen.send(send_value)
            except StopIteration as excp:
                ret_value = excp.args[0] if excp.args else None
                try:
                    ret_value = cls.trace_return_value(info, trace_opts, True, ret_value)
                except Exception:
                    pass

                raise StopIteration(ret_value)
            except Exception as excp:
                try:
                    raise
                finally:
                    id_label = getattr(excp, '__name__', None)
                    if not id_label and hasattr(excp, '__class__'):
                        id_label = excp.__class__.__name__
                    exc_info = sys.exc_info()
                    frame_records = inspect.trace()
                    try:
                        try:
                            locals_dict = cls.traverse_framestack(frame_records, exc_info, copy_locals=True)
                            dummy_context, trace_id = cls.create_context(info.fullname, info.self_arg, locals_dict, id_label=id_label, context_type='exceptions', excp=excp, exc_info=exc_info)
                            cls.callback_handler.callback(trace_id, info.methodtype, info.modulename, info.classname, info.fn.__name__)
                        except Exception as excp:
                            pass

                    finally:
                        del frame_records

                    try:
                        del locals_dict
                        del dummy_context
                    except Exception:
                        pass

            try:
                send_value = yield yield_value
                exception_flag = False
            except GeneratorExit as excp:
                try:
                    gen.close()
                except Exception:
                    pass

                raise StopIteration()
            except Exception as excp:
                send_value = excp
                exception_flag = True

        return

    @classmethod
    def trace_function(cls, function, classname='', modulename='', methodtype='', unwrap=False):
        """Wrap function for tracing. (If unwrap, unwrap function.)
        classname is the name of the class for instance/class/static methods.
        methodtype = "" (function) or "instancemethod" or "classmethod" or "staticmethod"
        """
        if hasattr(function, cls.orig_function_attr):
            if unwrap:
                orig_function = getattr(function, cls.orig_function_attr)
                delattr(function, cls.orig_function_attr)
                return orig_function
            else:
                return function

        elif unwrap:
            return function
        func_info = FunctionInfo(function, classname=classname, modulename=modulename, methodtype=methodtype)

        @functools.wraps(function)
        def otrace_wrapped(*args, **kwargs):
            if not cls.trace_active:
                return function(*args, **kwargs)
            return cls.otrace_function_call(func_info, *args, **kwargs)

        setattr(otrace_wrapped, cls.orig_function_attr, function)
        return otrace_wrapped

    @classmethod
    def trace_method(cls, parent_cls, method, modulename='', unwrap=False):
        """Trace a method in a class"""
        methodtype = get_method_type(parent_cls, method)
        methodname = method.__name__
        if methodname.startswith('__') and not methodname.endswith('__'):
            methodname = '_' + parent_cls.__name__ + methodname
        if methodname not in ('__str__', '__repr__'):
            new_function = cls.trace_function(get_naked_function(method), classname=parent_cls.__name__, modulename=modulename, methodtype=methodtype, unwrap=unwrap)
            if methodtype == 'classmethod':
                new_function = classmethod(new_function)
            elif methodtype == 'staticmethod':
                new_function = staticmethod(new_function)
            setattr(parent_cls, methodname, new_function)
        return getattr(parent_cls, methodname)

    @classmethod
    def trace_modulefunction(cls, mod, function, unwrap=False):
        """Trace function in module"""
        setattr(mod, function.__name__, cls.trace_function(function, modulename=mod.__name__, unwrap=unwrap))

    @classmethod
    def trace_entity(cls, entity, exclude=[], include=[], modulename='', unwrap=False):
        """ Trace an entity (which may be a module or a class)
        All members are traced recursively, except for members in the the exclude list,
        unless include list is specified, in which case only included members are traced.
        """
        if inspect.isclass(entity):
            if unwrap:
                if hasattr(entity, cls.class_trace_attr):
                    delattr(entity, cls.class_trace_attr)
            else:
                setattr(entity, cls.class_trace_attr, True)
            members = inspect.getmembers(entity, ismethod_or_function)
            members = [ (name, member) for name, member in members if name in entity.__dict__ ]
        else:
            if inspect.ismodule(entity):
                modulename = entity.__name__
                members = inspect.getmembers(entity, inspect.isfunction)
                members += inspect.getmembers(entity, inspect.isclass)
            if include:
                trace_set = set(include)
            else:
                trace_set = set(x[0] for x in members)
                for name in exclude:
                    trace_set.discard(name)

            trace_list = []
            for name, member in members:
                if name not in trace_set:
                    continue
                trace_list.append(name)
                if inspect.isclass(entity):
                    cls.trace_method(entity, member, modulename=modulename, unwrap=unwrap)
                elif inspect.isfunction(member):
                    cls.trace_modulefunction(entity, member, unwrap=unwrap)
                else:
                    cls.trace_entity(member, modulename=modulename, unwrap=unwrap)

        return trace_list

    @classmethod
    def web_hook(cls, op_type, path, data):
        if not OShell.instance:
            return
        else:
            oshell = OShell.instance
            try:
                if op_type == 'stderr':
                    if oshell.repeat_interval:
                        oshell.set_repeat(None)
                    oshell.std_output(data + '\n')
                if op_type == 'stdout':
                    if oshell.repeat_interval:
                        data = CLEAR_SCREEN_SEQUENCE + data
                        if oshell.repeat_alt_screen == 1:
                            oshell.repeat_alt_screen = 2
                            data = ALT_SCREEN_ONSEQ + data
                    else:
                        if oshell.repeat_alt_screen == 2:
                            oshell.repeat_alt_screen = 0
                            data = ALT_SCREEN_OFFSEQ + data
                        data = data + '\n' + oshell.prompt1
                    oshell.std_output(data, flush=True)
            except Exception:
                pass

            return

    @classmethod
    def access_hook(cls, op_type, entity_key, entity_cache):
        if not cls.trace_keys:
            return
        else:
            key_str = str(entity_key)
            trace_opts = cls.trace_keys.get(key_str)
            if not trace_opts:
                return
            name_str = urllib.unquote(key_str).replace(PATH_SEP, '_')
            trace_matched = False
            entity = None
            if trace_opts.access_type:
                if op_type == 'get':
                    if trace_opts.access_type not in ('get', 'all'):
                        return
                elif op_type == 'put':
                    if trace_opts.access_type not in ('put', 'modify', 'all'):
                        return
                elif op_type == 'delete':
                    if trace_opts.access_type not in ('delete', 'modify', 'all'):
                        return
                trace_matched = True
            else:
                if trace_opts.argmatch:
                    if not entity_cache:
                        return
                    entity = entity_cache.unpack()
                    for attr, value in trace_opts.argmatch.iteritems():
                        attr, cmp_op = strip_compare_op(attr)
                        if not compare(getattr(entity, attr, None), cmp_op, value):
                            return

                    trace_matched = True
                if not trace_matched:
                    return
                if trace_opts.break_count < 0:
                    trace_opts.break_count += 1
                    return
            if trace_opts.break_count > 0:
                trace_opts.break_count -= 1
                if trace_opts.break_count == 0:
                    cls.remove_trace(trace_opts.trace_name)
                    return
            if not entity and entity_cache:
                entity = entity_cache.unpack()
            locals_dict = TraceDict({ENTITY_CHAR: entity})
            locals_dict.set_trc('stack', ('').join(traceback.format_stack()[:-3]))
            trace_context, trace_id = cls.create_context(name_str, None, locals_dict, context_type='dbaccess', id_label=op_type)
            cls.callback_handler.accessback(trace_id, op_type, key_str, entity)
            if trace_opts.break_action in BREAK_ACTIONS:
                cls.break_flow(trace_id, action=trace_opts.break_action)
            return

    @classmethod
    def getsourcelines(cls, method):
        """ Returns (list_of_source_lines, start_line)
        start_line is 0 if source is obtained from patch attribute, rather than the source file.
        If no source is found, IOError is raised.
        """
        orig_fn = getattr(method, cls.orig_function_attr, None) or method
        patch_source_list = getattr(orig_fn, cls.patch_source_attr, None)
        if patch_source_list:
            return (patch_source_list, 0)
        else:
            return inspect.getsourcelines(orig_fn)
            return

    @classmethod
    def monkey_patch(cls, new_func, method, parent, methodtype='', repatch=False, source=None):
        """ Override a function or a class/instance method with a new function,
        returning new_func on success and None on failure.
        parent must be a class or a module that contains the method/function.
        The original unpatched method is saved as an attribute of the patched method,
        and can be used by the patched method to invoke the unpatched method, e.g.
            def method(self, *args, **kwargs):
                unpatched = getattr(self.method, "_otrace_unpatched_function")
                # Modify args/kwargs
                ret_value = unpatched(self, *args, **kwargs)
                # Modify ret_value
                return ret_value
        For new methods, specify
            methodtype = "" (function) or "instancemethod" or "classmethod" or "staticmethod"
        If repatch, force overwriting of previous patch, if present.
        If source (list of strings) is specified, it is also saved as an attribute.
        """
        assert not parent or inspect.isclass(parent) or inspect.ismodule(parent)
        with Trace_rlock:
            if not parent:
                parent = getattr(method, cls.patch_parent_attr, None)
            if not method:
                wrapped = False
                mname = new_func.__name__
                orig_method = None
            else:
                methodtype = ''
                mname = method.__name__
                if inspect.isclass(parent):
                    methodtype = get_method_type(parent, method)
                    if mname.startswith('__') and not mname.endswith('__'):
                        mname = '_%s%s' % (parent.__name__, mname)
                wrapped = hasattr(method, cls.orig_function_attr)
                if wrapped:
                    if inspect.isclass(parent):
                        method = cls.trace_method(parent, method, unwrap=True)
                    else:
                        setattr(parent, mname, cls.trace_function(method, methodtype=methodtype, unwrap=True))
                orig_method = getattr(method, OTrace.unpatched_function_attr, None)
            if not orig_method or repatch:
                setattr(new_func, cls.unpatched_function_attr, orig_method or method)
                setattr(new_func, cls.patch_source_attr, source)
                setattr(new_func, cls.patch_parent_attr, parent)
                if methodtype == 'classmethod':
                    new_func = classmethod(new_func)
                elif methodtype == 'staticmethod':
                    new_func = staticmethod(new_func)
                setattr(parent, mname, new_func)
            if wrapped:
                if inspect.isclass(parent):
                    cls.trace_method(parent, getattr(parent, mname), unwrap=False)
                else:
                    setattr(parent, mname, cls.trace_function(getattr(parent, mname), methodtype=methodtype, unwrap=False))
            if not orig_method or repatch:
                return new_func
            return
        return

    @classmethod
    def monkey_unpatch(cls, method):
        """ Revert to original value for overridden function or method, returning True on success
        """
        with Trace_rlock:
            parent = getattr(method, cls.patch_parent_attr, None)
            if not parent:
                return
            methodtype = ''
            mname = method.__name__
            if inspect.isclass(parent):
                methodtype = get_method_type(parent, method)
                if mname.startswith('__') and not mname.endswith('__'):
                    mname = '_%s%s' % (parent.__name__, mname)
            wrapped = hasattr(method, cls.orig_function_attr)
            if wrapped:
                if inspect.isclass(parent):
                    method = cls.trace_method(parent, method, unwrap=True)
                else:
                    setattr(parent, mname, cls.trace_function(method, methodtype=methodtype, unwrap=True))
            unpatch = hasattr(method, cls.unpatched_function_attr)
            if unpatch:
                orig_method = getattr(method, cls.unpatched_function_attr)
                if orig_method:
                    setattr(parent, mname, orig_method)
                else:
                    delattr(parent, mname)
                func = get_naked_function(method)
                delattr(func, cls.unpatched_function_attr)
                delattr(func, cls.patch_source_attr)
                delattr(func, cls.patch_parent_attr)
            if wrapped:
                if inspect.isclass(parent):
                    cls.trace_method(parent, getattr(parent, mname), unwrap=False)
                else:
                    setattr(parent, mname, cls.trace_function(getattr(parent, mname), methodtype=methodtype, unwrap=False))
            return unpatch
        return


def schedule_callback(callback=None):
    if not callback:
        return
    if OTrace.eventloop_callback:
        OTrace.eventloop_callback(callback)
    else:
        callback()


class HoldHandler(object):
    """ Hold handler for use with otrace (callable instance)
    """

    def __init__(self, self_arg, path, resume_value=None):
        self.self_arg = self_arg
        self.path = path
        self.resume_value = resume_value
        self.callback = None
        return

    def __call__(self, callback=None):
        self.callback = callback
        if hasattr(self.self_arg, OTrace.hold_attr):
            delattr(self.self_arg, OTrace.hold_attr)
        setattr(self.self_arg, OTrace.resume_attr, self.resume)

    def resume(self):
        if hasattr(self.self_arg, OTrace.resume_attr):
            delattr(self.self_arg, OTrace.resume_attr)
        callback = self.callback
        self.callback = None
        if not callback:
            return
        else:
            schedule_callback(functools.partial(callback, self.resume_value))
            return


class PickleInterface(object):
    root_depth = 4
    write_connection = None
    read_connection = None
    write_file = ''
    read_file = ''

    @classmethod
    def set_monitor(cls, monitor):
        pass

    @classmethod
    def set_access_hook(cls, hook):
        pass

    @classmethod
    def key_from_path(cls, path_list):
        """ Construct key from list of path components
        """
        if not path_list:
            return None
        else:
            if len(path_list) < 2:
                path_list = path_list + ['*']
            if len(path_list) < 3:
                for ctype, context_type in ContextDict.context_types.items():
                    if path_list[0] == context_type:
                        return TRACE_ID_SEP.join([path_list[1], ctype + '-*', '*'])

                return None
            if len(path_list) < 4:
                path_list = path_list + ['*']
            return TRACE_ID_SEP.join(path_list[1:4])

    @classmethod
    def path_from_key(cls, key):
        """ Convert key to path component list
        """
        return ContextDict.split_trace_id(key)

    @classmethod
    def get_entity(cls, entity_key):
        """Read and return trace context from db"""
        key = cls.key_from_path([''] + entity_key.replace(PATH_SEP, TRACE_ID_SEP).split(TRACE_ID_SEP))
        contexts = cls.read_records_pickle_db(key=key)
        if contexts:
            return contexts[0]
        else:
            return

    @classmethod
    def delete_entities(cls, key_list, recursive=False):
        """ Delete directory tree entries for key_list (not the actual pickled entities)"""
        deleted = []
        for key in key_list:
            path = cls.path_from_key(key)
            context = OTrace.base_context[PICKLED_DIR]
            parents = []
            while path:
                cdir = path.pop(0)
                if cdir == '*':
                    break
                elif cdir in context:
                    parents.append([context, cdir])
                    context = context[cdir]
                else:
                    context = None
                    break

            if not context:
                continue
            context.clear()
            deleted.append(key)
            while parents:
                context, cdir = parents.pop()
                if not context.get(cdir):
                    context.pop(cdir, None)

        return deleted

    @classmethod
    def get_root_tree(cls):
        """ Returns dict tree (with root_depth) that is updated automatically
        """
        return OTrace.base_context[PICKLED_DIR]

    @classmethod
    def get_child_tree(cls, ancestor_key, entity_char=':'):
        """ Returns dict tree branch below the root tree
        """
        path = cls.path_from_key(ancestor_key)
        context = {entity_char: cls.get_entity(ancestor_key)}
        while path:
            key = path.pop()
            context = {key: context}

        return context

    @classmethod
    def create_pickle_db(cls, filename):
        """Create pickle database file for writing
        (accessed only from application, not otrace)
        """
        try:
            cls.write_connection = sqlite3.connect(filename, check_same_thread=False)
            cls.write_file = filename
            cls.pickle_names = ['otrace_context', 'recnum', 'key', 'methodname', 'context_id', 'timestamp', 'pickled_object']
            cls.pickle_create_sql = 'CREATE TABLE IF NOT EXISTS %s (%s INTEGER PRIMARY KEY AUTOINCREMENT, %s TEXT UNIQUE, %s TEXT, %s TEXT, %s TEXT, %s TEXT)' % tuple(cls.pickle_names[:])
            cls.pickle_insert_sql = 'INSERT INTO %s VALUES (null, :%s, :%s, :%s, :%s, :%s)' % tuple(cls.pickle_names[:1] + cls.pickle_names[2:])
            cls.pickle_select_key_sql = 'SELECT %s FROM %s' % (cls.pickle_names[2], cls.pickle_names[0])
            cls.pickle_select_record_sql = 'SELECT * FROM %s' % (cls.pickle_names[0],)
            cls.write_connection.execute(cls.pickle_create_sql)
            cls.write_connection.commit()
        except sqlite3.OperationalError as msg:
            logging.error('Error in creating pickle database %s: %s' % (cls.write_file, msg))
            raise

    @classmethod
    def pickle_check(cls, obj, depth=0):
        """Return copy of object to be pickled, replacing non-pickleable components with string
        representations
        """
        if depth < MAX_PICKLE_CHECK_DEPTH:
            if isinstance(obj, (list, tuple)):
                new_obj = [ cls.pickle_check(x, depth=depth + 1) for x in obj ]
                if isinstance(obj, list):
                    return new_obj
                return tuple(new_obj)
            if isinstance(obj, dict):
                return dict((key, cls.pickle_check(value, depth=depth + 1)) for key, value in obj.iteritems())
        try:
            pickled = cPickle.dumps(obj)
            if len(pickled) <= MAX_PICKLE_DATA_LENGTH:
                return obj
        except Exception:
            pass

        s = str(obj)
        if len(s) <= MAX_PICKLE_DATA_LENGTH:
            return s
        return s[:MAX_PICKLE_DATA_LENGTH] + '...'

    @classmethod
    def write_pickle_db(cls, trace_id, obj):
        """Write pickled context object corresponding to trace_id
        """
        context_type, methodname, context_id, timestamp = ContextDict.split_trace_id(trace_id)
        try:
            pickled = cPickle.dumps(cls.pickle_check(obj), cPickle.HIGHEST_PROTOCOL)
            with Pickle_rlock:
                cursor = cls.write_connection.execute(cls.pickle_insert_sql, {'key': trace_id, 'timestamp': timestamp, 'methodname': methodname, 'context_id': context_id, 
                   'pickled_object': sqlite3.Binary(pickled)})
                cls.write_connection.commit()
        except Exception as excp:
            logging.error('Error in adding entry to pickle_db %s: %s', cls.write_file, excp)

    @classmethod
    def open_pickle_db(cls, filename):
        """Open pickle database file for reading
        (accessed only from otrace thread)
        """
        try:
            cls.read_file = filename
            if filename == cls.write_file:
                cls.read_connection = cls.write_connection
            else:
                if cls.read_connection and cls.read_connection is not cls.write_connection:
                    cls.read_connection.close()
                    cls.read_connection = None
                cls.read_connection = sqlite3.connect(filename)
        except sqlite3.OperationalError as msg:
            logging.error('Error in reading pickle database %s: %s' % (cls.read_file, msg))
            raise

        return

    @classmethod
    def read_keys_pickle_db(cls, **kwargs):
        """Read keys as filtered by kwargs
        (key=..., methodname=..., context_id=...)
        and return list of matching keys
        (If no filters, all keys are returned)
        """
        try:
            with Pickle_rlock:
                select_sql = cls.pickle_select_key_sql
                select_vals = []
                for arg_name, arg_value in kwargs.items():
                    select_sql += ' WHERE %s=?' % arg_name
                    select_vals.append(arg_value)

                cursor = cls.read_connection.execute(select_sql, select_vals)
                return [ str(x[0]) for x in cursor.fetchall() ]
        except Exception as excp:
            logging.error('Error in retrieving key(s) from pickle_db: %s', kwargs, excp)

    @classmethod
    def read_records_pickle_db(cls, **kwargs):
        """Read contexts as filtered by kwargs
        (key=..., methodname=..., context_id=...)
        and return list of unpickled context objects
        (If no filters, all records are returned)
        """
        try:
            with Pickle_rlock:
                select_sql = cls.pickle_select_record_sql
                select_vals = []
                for arg_name, arg_value in kwargs.items():
                    select_sql += ' WHERE %s=?' % arg_name
                    select_vals.append(arg_value)

                cursor = cls.read_connection.execute(select_sql, select_vals)
                rows = cursor.fetchall()
                return [ cPickle.loads(str(row[(-1)])) for row in rows ]
        except Exception as excp:
            logging.error('Error in retrieving record(s) from pickle_db: %s', kwargs, excp)


traceassert = OTrace.traceassert
tag = OTrace.tag
untag = OTrace.untag
get_tag = OTrace.get_tag
set_tag = OTrace.set_tag

def set_trace(globals_dict, locals_dict=None, new_thread=False, wait_to_run=False, init_file=''):
    """Invoke otrace and return OShell instance.
    pdb-like usage:
       import otrace
       otrace.set_trace(globals())

    The above call will block and otrace will read commands from stdin
    until the 'quit' command is issued.

    If new_thread=True, the call will return immediately, and otrace will wait for
    commands from stdin in a new thread, while the main thread executes the program.
    (For clean termination, the main thread should invoke the 'shutdown' method on
    the returned OShell instance.)

    If wait_to_run=True, the call will block, and the 'run' command in otrace
    can be used to run functions. (new_thread is implied)

    Optional init_file contains commands to initialize otrace.
    """
    trace_shell = OShell(globals_dict=globals_dict, locals_dict=locals_dict or globals_dict, new_thread=new_thread or wait_to_run, init_file=init_file, allow_unsafe=True)
    trace_shell.loop(wait_to_run=wait_to_run)
    return trace_shell


def test():

    class TestClass(object):

        def method(self, arg1, kwarg1=None):
            print 'Invoked method with arg1=' + str(arg1) + ', kwarg1=' + str(kwarg1)

        def method2(self, arg1, kwarg1=None):
            print 'Invoked method2 with arg1=' + str(arg1) + ', kwarg1=' + str(kwarg1)
            return arg1

        @classmethod
        def cmethod(cls, arg1):
            print 'Invoked cmethod with arg1=' + str(arg1)
            return (1, 2)

        @staticmethod
        def smethod(self, arg1):
            print 'Invoked smethod with arg1=' + str(arg1)
            return False

    def method2(self, *args, **kwargs):
        unpatched = getattr(self.method2, '_otrace_unpatched_function')
        args = tuple([args[0] + '-MODIFIED'] + list(args[1:]))
        ret_value = unpatched(self, *args, **kwargs)
        return ret_value + '-RETMODIFIED'

    glob_dict = {'gvar': 'gvalue'}
    loc_dict = {'arg1': 'value1'}
    trace_int = TraceInterpreter()
    print trace_int.evaluate('arg1', print_out=True, locals_dict=loc_dict)
    print trace_int.evaluate("arg1 = 'new_value'", locals_dict=loc_dict, globals_dict=glob_dict)
    print trace_int.evaluate('arg1', print_out=True, locals_dict=loc_dict)
    print trace_int.evaluate('arg1.', print_out=True, locals_dict=loc_dict)
    print trace_int.evaluate('arg1 = undefined_value', locals_dict=loc_dict)
    print trace_int.evaluate('gvar', print_out=True, globals_dict=glob_dict)
    print trace_int.evaluate("global gvar; gvar = 'new_glob_value ' + arg1", locals_dict=loc_dict, globals_dict=glob_dict)
    print trace_int.evaluate('gvar', print_out=True, locals_dict=loc_dict, globals_dict=glob_dict)
    print glob_dict['gvar']
    print trace_int.evaluate("gvar = 'new_local_value2'", locals_dict=loc_dict, globals_dict=glob_dict)
    print trace_int.evaluate('gvar', print_out=True, locals_dict=loc_dict, globals_dict=glob_dict)
    print glob_dict['gvar']
    print loc_dict['gvar']
    OTrace.trace_entity(TestClass)
    OTrace.add_trace()
    testobj = TestClass()
    testobj.method(11, kwarg1='KWRD')
    testobj.cmethod(True)
    testobj.smethod('ss', 33)
    OTrace.add_trace('.method', argmatch={'arg1': 33})
    OTrace.add_trace('.method2', argmatch={'return': 44})
    testobj.method(11, kwarg1='KWRD')
    testobj.method(33, kwarg1='KWRD')
    testobj.method2(22, kwarg1='KWRD')
    testobj.method2(44, kwarg1='KWRD')
    testobj.cmethod(True)
    testobj.smethod('ss', 33)
    print testobj.method2('55orig', kwarg1='KWRD')
    OTrace.monkey_patch(method2, TestClass.method2, TestClass)
    print testobj.method2('55patch', kwarg1='KWRD')
    OTrace.monkey_unpatch(TestClass.method2)
    print testobj.method2('55unpatch', kwarg1='KWRD')


def main(args=None):
    import imp, signal
    if args is None:
        args = sys.argv[1:]
    if len(args) < 1 or args[0] == '-f' and len(args) < 3:
        print >> sys.stderr, 'Usage: otrace [-f function_name] program_file [arg1 arg2 ...]'
        sys.exit(1)
    if args[0] == '-f':
        funcname, filepath = args[1], args[2]
        args = args[3:]
    else:
        funcname, filepath = '', args[0]
        args = args[1:]
    if not os.path.isfile(filepath) or not os.access(filepath, os.R_OK):
        print >> sys.stderr, 'otrace: Unable to read file %s' % filepath
        sys.exit(1)
    abspath = os.path.abspath(filepath)
    filedir, basename = os.path.split(abspath)
    modname, extension = os.path.splitext(basename)
    modfile, modpath, moddesc = imp.find_module(modname, [filedir])
    modobj = imp.load_module(modname, modfile, modpath, moddesc)
    orig_funcobj = getattr(modobj, funcname, None) if funcname else None
    if funcname and not callable(orig_funcobj):
        print >> sys.stderr, "otrace: Program %s does not have function named '%s'" % (filepath, funcname)
        sys.exit(1)
    oshell_globals = modobj.__dict__
    Trace_shell = OShell(locals_dict=oshell_globals, globals_dict=oshell_globals, allow_unsafe=True, init_file=modname + '.trc', new_thread=True)

    def sigterm(signal, frame):
        logging.warning('SIGTERM signal received')
        Trace_shell.shutdown()

    signal.signal(signal.SIGTERM, sigterm)
    try:
        try:
            Trace_shell.loop(wait_to_run=not funcname)
            if funcname:
                time.sleep(1)
                funcobj = getattr(modobj, funcname)
                if args:
                    funcobj(args)
                else:
                    funcobj()
        except Exception as excp:
            traceback.print_exc()
            print >> sys.stderr, '\nPress Enter to trace; ^C to abort: ',
            Trace_shell.execute('cd ~~')
            while True:
                time.sleep(1)

    finally:
        Trace_shell.shutdown()

    return


if __name__ == '__main__':
    main(args=sys.argv[1:])