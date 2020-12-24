# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/financespy/sh.py
# Compiled at: 2019-06-26 14:52:36
# Size of source mod 2**32: 120879 bytes
"""
http://amoffat.github.io/sh/
"""
__version__ = '1.12.14'
__project_url__ = 'https://github.com/amoffat/sh'
import platform
if 'windows' in platform.system().lower():
    raise ImportError('sh %s is currently only supported on linux and osx. please install pbs 0.110 (http://pypi.python.org/pypi/pbs) for windows support.' % __version__)
else:
    import sys
    IS_PY3 = sys.version_info[0] == 3
    MINOR_VER = sys.version_info[1]
    IS_PY26 = sys.version_info[0] == 2 and MINOR_VER == 6
    import traceback, os, re, time, getpass
    from types import ModuleType, GeneratorType
    from functools import partial
    import inspect, tempfile, stat, glob as glob_module, ast
    from contextlib import contextmanager
    import pwd, errno
    from io import UnsupportedOperation, open as fdopen
    from locale import getpreferredencoding
    DEFAULT_ENCODING = getpreferredencoding() or 'UTF-8'
    RUNNING_TESTS = bool(int(os.environ.get('SH_TESTS_RUNNING', '0')))
    FORCE_USE_SELECT = bool(int(os.environ.get('SH_TESTS_USE_SELECT', '0')))
    if IS_PY3:
        from io import StringIO
        ioStringIO = StringIO
        from io import BytesIO as cStringIO
        iocStringIO = cStringIO
        from queue import Queue, Empty
        if not hasattr(__builtins__, 'callable'):

            def callable(ob):
                return hasattr(ob, '__call__')


    else:
        from StringIO import StringIO
        from cStringIO import OutputType as cStringIO
        from io import StringIO as ioStringIO
        from io import BytesIO as iocStringIO
        from Queue import Queue, Empty
    IS_OSX = platform.system() == 'Darwin'
    THIS_DIR = os.path.dirname(os.path.realpath(__file__))
    SH_LOGGER_NAME = __name__
    import errno, pty, termios, signal, gc, select, threading, tty, fcntl, struct, resource
    from collections import deque
    import logging, weakref
    PUSHD_LOCK = threading.RLock()
    if hasattr(inspect, 'getfullargspec'):

        def get_num_args(fn):
            return len(inspect.getfullargspec(fn).args)


    else:

        def get_num_args(fn):
            return len(inspect.getargspec(fn).args)


if IS_PY3:
    raw_input = input
    unicode = str
    basestring = str
    long = int
else:
    _unicode_methods = set(dir(unicode()))
    HAS_POLL = hasattr(select, 'poll')
    POLLER_EVENT_READ = 1
    POLLER_EVENT_WRITE = 2
    POLLER_EVENT_HUP = 4
    POLLER_EVENT_ERROR = 8
    if HAS_POLL and not FORCE_USE_SELECT:

        class Poller(object):

            def __init__(self):
                self._poll = select.poll()
                self.fd_lookup = {}
                self.fo_lookup = {}

            def __nonzero__(self):
                return len(self.fd_lookup) != 0

            def __len__(self):
                return len(self.fd_lookup)

            def _set_fileobject(self, f):
                if hasattr(f, 'fileno'):
                    fd = f.fileno()
                    self.fd_lookup[fd] = f
                    self.fo_lookup[f] = fd
                else:
                    self.fd_lookup[f] = f
                    self.fo_lookup[f] = f

            def _remove_fileobject(self, f):
                if hasattr(f, 'fileno'):
                    fd = f.fileno()
                    del self.fd_lookup[fd]
                    del self.fo_lookup[f]
                else:
                    del self.fd_lookup[f]
                    del self.fo_lookup[f]

            def _get_file_descriptor(self, f):
                return self.fo_lookup.get(f)

            def _get_file_object(self, fd):
                return self.fd_lookup.get(fd)

            def _register(self, f, events):
                self._set_fileobject(f)
                fd = self._get_file_descriptor(f)
                self._poll.register(fd, events)

            def register_read(self, f):
                self._register(f, select.POLLIN | select.POLLPRI)

            def register_write(self, f):
                self._register(f, select.POLLOUT)

            def register_error(self, f):
                self._register(f, select.POLLERR | select.POLLHUP | select.POLLNVAL)

            def unregister(self, f):
                fd = self._get_file_descriptor(f)
                self._poll.unregister(fd)
                self._remove_fileobject(f)

            def poll(self, timeout):
                if timeout is not None:
                    timeout *= 1000
                changes = self._poll.poll(timeout)
                results = []
                for fd, events in changes:
                    f = self._get_file_object(fd)
                    if events & (select.POLLIN | select.POLLPRI):
                        results.append((f, POLLER_EVENT_READ))
                    else:
                        if events & select.POLLOUT:
                            results.append((f, POLLER_EVENT_WRITE))
                        else:
                            if events & select.POLLHUP:
                                results.append((f, POLLER_EVENT_HUP))
                            else:
                                if events & (select.POLLERR | select.POLLNVAL):
                                    results.append((f, POLLER_EVENT_ERROR))

                return results


    else:

        class Poller(object):

            def __init__(self):
                self.rlist = []
                self.wlist = []
                self.xlist = []

            def __nonzero__(self):
                return len(self.rlist) + len(self.wlist) + len(self.xlist) != 0

            def __len__(self):
                return len(self.rlist) + len(self.wlist) + len(self.xlist)

            def _register(self, f, l):
                if f not in l:
                    l.append(f)

            def _unregister(self, f, l):
                if f in l:
                    l.remove(f)

            def register_read(self, f):
                self._register(f, self.rlist)

            def register_write(self, f):
                self._register(f, self.wlist)

            def register_error(self, f):
                self._register(f, self.xlist)

            def unregister(self, f):
                self._unregister(f, self.rlist)
                self._unregister(f, self.wlist)
                self._unregister(f, self.xlist)

            def poll(self, timeout):
                _in, _out, _err = select.select(self.rlist, self.wlist, self.xlist, timeout)
                results = []
                for f in _in:
                    results.append((f, POLLER_EVENT_READ))

                for f in _out:
                    results.append((f, POLLER_EVENT_WRITE))

                for f in _err:
                    results.append((f, POLLER_EVENT_ERROR))

                return results


def encode_to_py3bytes_or_py2str(s):
    """ takes anything and attempts to return a py2 string or py3 bytes.  this
    is typically used when creating command + arguments to be executed via
    os.exec* """
    fallback_encoding = 'utf8'
    if IS_PY3:
        if isinstance(s, bytes):
            pass
        else:
            s = str(s)
            try:
                s = bytes(s, DEFAULT_ENCODING)
            except UnicodeEncodeError:
                s = bytes(s, fallback_encoding)

    else:
        try:
            s = unicode(s, DEFAULT_ENCODING)
        except TypeError:
            s = unicode(s)

        try:
            s = s.encode(DEFAULT_ENCODING)
        except:
            s = s.encode(fallback_encoding, 'replace')

        return s


def _indent_text(text, num=4):
    lines = []
    for line in text.split('\n'):
        line = ' ' * num + line
        lines.append(line)

    return '\n'.join(lines)


class ForkException(Exception):

    def __init__(self, orig_exc):
        tmpl = '\n\nOriginal exception:\n===================\n\n%s\n'
        msg = tmpl % _indent_text(orig_exc)
        Exception.__init__(self, msg)


class ErrorReturnCodeMeta(type):
    __doc__ = " a metaclass which provides the ability for an ErrorReturnCode (or\n    derived) instance, imported from one sh module, to be considered the\n    subclass of ErrorReturnCode from another module.  this is mostly necessary\n    in the tests, where we do assertRaises, but the ErrorReturnCode that the\n    program we're testing throws may not be the same class that we pass to\n    assertRaises\n    "

    def __subclasscheck__(self, o):
        other_bases = set([b.__name__ for b in o.__bases__])
        return self.__name__ in other_bases or o.__name__ == self.__name__


class ErrorReturnCode(Exception):
    __metaclass__ = ErrorReturnCodeMeta
    truncate_cap = 750

    def __init__(self, full_cmd, stdout, stderr, truncate=True):
        self.full_cmd = full_cmd
        self.stdout = stdout
        self.stderr = stderr
        exc_stdout = self.stdout
        if truncate:
            exc_stdout = exc_stdout[:self.truncate_cap]
            out_delta = len(self.stdout) - len(exc_stdout)
            if out_delta:
                exc_stdout += ('... (%d more, please see e.stdout)' % out_delta).encode()
        exc_stderr = self.stderr
        if truncate:
            exc_stderr = exc_stderr[:self.truncate_cap]
            err_delta = len(self.stderr) - len(exc_stderr)
            if err_delta:
                exc_stderr += ('... (%d more, please see e.stderr)' % err_delta).encode()
        msg_tmpl = unicode('\n\n  RAN: {cmd}\n\n  STDOUT:\n{stdout}\n\n  STDERR:\n{stderr}')
        msg = msg_tmpl.format(cmd=(self.full_cmd),
          stdout=(exc_stdout.decode(DEFAULT_ENCODING, 'replace')),
          stderr=(exc_stderr.decode(DEFAULT_ENCODING, 'replace')))
        super(ErrorReturnCode, self).__init__(msg)


class SignalException(ErrorReturnCode):
    pass


class TimeoutException(Exception):
    __doc__ = ' the exception thrown when a command is killed because a specified\n    timeout (via _timeout) was hit '

    def __init__(self, exit_code):
        self.exit_code = exit_code
        super(Exception, self).__init__()


SIGNALS_THAT_SHOULD_THROW_EXCEPTION = set((
 signal.SIGABRT,
 signal.SIGBUS,
 signal.SIGFPE,
 signal.SIGILL,
 signal.SIGINT,
 signal.SIGKILL,
 signal.SIGPIPE,
 signal.SIGQUIT,
 signal.SIGSEGV,
 signal.SIGTERM,
 signal.SIGSYS))

class CommandNotFound(AttributeError):
    pass


rc_exc_regex = re.compile('(ErrorReturnCode|SignalException)_((\\d+)|SIG[a-zA-Z]+)')
rc_exc_cache = {}
SIGNAL_MAPPING = {}
for k, v in signal.__dict__.items():
    if re.match('SIG[a-zA-Z]+', k):
        SIGNAL_MAPPING[v] = k

def get_exc_from_name(name):
    """ takes an exception name, like:

        ErrorReturnCode_1
        SignalException_9
        SignalException_SIGHUP

    and returns the corresponding exception.  this is primarily used for
    importing exceptions from sh into user code, for instance, to capture those
    exceptions """
    exc = None
    try:
        return rc_exc_cache[name]
    except KeyError:
        m = rc_exc_regex.match(name)
        if m:
            base = m.group(1)
            rc_or_sig_name = m.group(2)
            if base == 'SignalException':
                try:
                    rc = -int(rc_or_sig_name)
                except ValueError:
                    rc = -getattr(signal, rc_or_sig_name)

            else:
                rc = int(rc_or_sig_name)
            exc = get_rc_exc(rc)

    return exc


def get_rc_exc(rc):
    """ takes a exit code or negative signal number and produces an exception
    that corresponds to that return code.  positive return codes yield
    ErrorReturnCode exception, negative return codes yield SignalException

    we also cache the generated exception so that only one signal of that type
    exists, preserving identity """
    try:
        return rc_exc_cache[rc]
    except KeyError:
        pass

    if rc > 0:
        name = 'ErrorReturnCode_%d' % rc
        base = ErrorReturnCode
    else:
        signame = SIGNAL_MAPPING[abs(rc)]
        name = 'SignalException_' + signame
        base = SignalException
    exc = ErrorReturnCodeMeta(name, (base,), {'exit_code': rc})
    rc_exc_cache[rc] = exc
    return exc


_old_glob = glob_module.glob

class GlobResults(list):

    def __init__(self, path, results):
        self.path = path
        list.__init__(self, results)


def glob(path, *args, **kwargs):
    expanded = GlobResults(path, _old_glob(path, *args, **kwargs))
    return expanded


glob_module.glob = glob

def which(program, paths=None):
    """ takes a program name or full path, plus an optional collection of search
    paths, and returns the full path of the requested executable.  if paths is
    specified, it is the entire list of search paths, and the PATH env is not
    used at all.  otherwise, PATH env is used to look for the program """

    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK) and os.path.isfile(os.path.realpath(fpath))

    found_path = None
    fpath, fname = os.path.split(program)
    if fpath:
        program = os.path.abspath(os.path.expanduser(program))
        if is_exe(program):
            found_path = program
    else:
        paths_to_search = []
        if isinstance(paths, (tuple, list)):
            paths_to_search.extend(paths)
        else:
            env_paths = os.environ.get('PATH', '').split(os.pathsep)
            paths_to_search.extend(env_paths)
        for path in paths_to_search:
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                found_path = exe_file
                break

    return found_path


def resolve_command_path(program):
    path = which(program)
    if not path:
        if '_' in program:
            path = which(program.replace('_', '-'))
        return path or None
    else:
        return path


def resolve_command(name, baked_args=None):
    path = resolve_command_path(name)
    cmd = None
    if path:
        cmd = Command(path)
        if baked_args:
            cmd = (cmd.bake)(**baked_args)
    return cmd


class Logger(object):
    __doc__ = ' provides a memory-inexpensive logger.  a gotcha about python\'s builtin\n    logger is that logger objects are never garbage collected.  if you create a\n    thousand loggers with unique names, they\'ll sit there in memory until your\n    script is done.  with sh, it\'s easy to create loggers with unique names if\n    we want our loggers to include our command arguments.  for example, these\n    are all unique loggers:\n        \n            ls -l\n            ls -l /tmp\n            ls /tmp\n\n    so instead of creating unique loggers, and without sacrificing logging\n    output, we use this class, which maintains as part of its state, the logging\n    "context", which will be the very unique name.  this allows us to get a\n    logger with a very general name, eg: "command", and have a unique name\n    appended to it via the context, eg: "ls -l /tmp" '

    def __init__(self, name, context=None):
        self.name = name
        self.log = logging.getLogger('%s.%s' % (SH_LOGGER_NAME, name))
        self.set_context(context)

    def _format_msg(self, msg, *args):
        if self.context:
            msg = '%s: %s' % (self.context, msg)
        return msg % args

    def set_context(self, context):
        if context:
            context = context.replace('%', '%%')
        self.context = context or ''

    def get_child(self, name, context):
        new_name = self.name + '.' + name
        new_context = self.context + '.' + context
        l = Logger(new_name, new_context)
        return l

    def info(self, msg, *args):
        self.log.info((self._format_msg)(msg, *args))

    def debug(self, msg, *args):
        self.log.debug((self._format_msg)(msg, *args))

    def error(self, msg, *args):
        self.log.error((self._format_msg)(msg, *args))

    def exception(self, msg, *args):
        self.log.exception((self._format_msg)(msg, *args))


def default_logger_str(cmd, call_args, pid=None):
    if pid:
        s = '<Command %r, pid %d>' % (cmd, pid)
    else:
        s = '<Command %r>' % cmd
    return s


class RunningCommand(object):
    __doc__ = " this represents an executing Command object.  it is returned as the\n    result of __call__() being executed on a Command instance.  this creates a\n    reference to a OProc instance, which is a low-level wrapper around the\n    process that was exec'd\n\n    this is the class that gets manipulated the most by user code, and so it\n    implements various convenience methods and logical mechanisms for the\n    underlying process.  for example, if a user tries to access a\n    backgrounded-process's stdout/err, the RunningCommand object is smart enough\n    to know to wait() on the process to finish first.  and when the process\n    finishes, RunningCommand is smart enough to translate exit codes to\n    exceptions. "
    _OProc_attr_whitelist = set(('signal', 'terminate', 'kill', 'kill_group', 'signal_group',
                                 'pid', 'sid', 'pgid', 'ctty', 'input_thread_exc',
                                 'output_thread_exc', 'bg_thread_exc'))

    def __init__(self, cmd, call_args, stdin, stdout, stderr):
        """
            cmd is an array, where each element is encoded as bytes (PY3) or str
            (PY2)
        """
        enc = call_args['encoding']
        self.ran = ' '.join([arg.decode(enc, 'ignore') for arg in cmd])
        self.call_args = call_args
        self.cmd = cmd
        self.process = None
        self._process_completed = False
        should_wait = True
        spawn_process = True
        self._stopped_iteration = False
        if call_args['with']:
            spawn_process = False
            get_prepend_stack().append(self)
        if call_args['piped'] or call_args['iter'] or call_args['iter_noblock']:
            should_wait = False
        if call_args['bg']:
            should_wait = False
        if call_args['err_to_out']:
            stderr = OProc.STDOUT
        done_callback = call_args['done']
        if done_callback:
            call_args['done'] = partial(done_callback, self)
        pipe = OProc.STDOUT
        if call_args['iter'] == 'out' or call_args['iter'] is True:
            pipe = OProc.STDOUT
        else:
            if call_args['iter'] == 'err':
                pipe = OProc.STDERR
            if call_args['iter_noblock'] == 'out' or call_args['iter_noblock'] is True:
                pipe = OProc.STDOUT
            elif call_args['iter_noblock'] == 'err':
                pipe = OProc.STDERR
        self._spawned_and_waited = False
        if spawn_process:
            log_str_factory = call_args['log_msg'] or default_logger_str
            logger_str = log_str_factory(self.ran, call_args)
            self.log = Logger('command', logger_str)
            self.log.info('starting process')
            if should_wait:
                self._spawned_and_waited = True
            process_assign_lock = threading.Lock()
            with process_assign_lock:
                self.process = OProc(self, self.log, cmd, stdin, stdout, stderr, self.call_args, pipe, process_assign_lock)
            logger_str = log_str_factory(self.ran, call_args, self.process.pid)
            self.log.set_context(logger_str)
            self.log.info('process started')
            if should_wait:
                self.wait()

    def wait(self):
        """ waits for the running command to finish.  this is called on all
        running commands, eventually, except for ones that run in the background
        """
        if not self._process_completed:
            self._process_completed = True
            exit_code = self.process.wait()
            if self.process.timed_out:
                raise TimeoutException(-exit_code)
            else:
                self.handle_command_exit_code(exit_code)
                if self.process._stdin_process:
                    self.process._stdin_process.command.wait()
        self.log.info('process completed')
        return self

    def handle_command_exit_code(self, code):
        """ here we determine if we had an exception, or an error code that we
        weren't expecting to see.  if we did, we create and raise an exception
        """
        ca = self.call_args
        exc_class = get_exc_exit_code_would_raise(code, ca['ok_code'], ca['piped'])
        if exc_class:
            exc = exc_class(self.ran, self.process.stdout, self.process.stderr, ca['truncate_exc'])
            raise exc

    @property
    def stdout(self):
        self.wait()
        return self.process.stdout

    @property
    def stderr(self):
        self.wait()
        return self.process.stderr

    @property
    def exit_code(self):
        self.wait()
        return self.process.exit_code

    def __len__(self):
        return len(str(self))

    def __enter__(self):
        """ we don't actually do anything here because anything that should have
        been done would have been done in the Command.__call__ call.
        essentially all that has to happen is the comand be pushed on the
        prepend stack. """
        pass

    def __iter__(self):
        return self

    def next(self):
        """ allow us to iterate over the output of our command """
        if self._stopped_iteration:
            raise StopIteration()
        while True:
            try:
                chunk = self.process._pipe_queue.get(True, 0.001)
            except Empty:
                if self.call_args['iter_noblock']:
                    return errno.EWOULDBLOCK
            else:
                if chunk is None:
                    self.wait()
                    self._stopped_iteration = True
                    raise StopIteration()
                try:
                    return chunk.decode(self.call_args['encoding'], self.call_args['decode_errors'])
                except UnicodeDecodeError:
                    return chunk

    __next__ = next

    def __exit__(self, typ, value, traceback):
        if self.call_args['with']:
            if get_prepend_stack():
                get_prepend_stack().pop()

    def __str__(self):
        """ in python3, should return unicode.  in python2, should return a
        string of bytes """
        if IS_PY3:
            return self.__unicode__()
        else:
            return unicode(self).encode(self.call_args['encoding'])

    def __unicode__(self):
        """ a magic method defined for python2.  calling unicode() on a
        RunningCommand object will call this """
        if self.process:
            if self.stdout:
                return self.stdout.decode(self.call_args['encoding'], self.call_args['decode_errors'])
        if IS_PY3:
            return ''
        else:
            return unicode('')

    def __eq__(self, other):
        return unicode(self) == unicode(other)

    __hash__ = None

    def __contains__(self, item):
        return item in str(self)

    def __getattr__(self, p):
        if p in self._OProc_attr_whitelist:
            if self.process:
                return getattr(self.process, p)
            raise AttributeError
        if p in _unicode_methods:
            return getattr(unicode(self), p)
        raise AttributeError

    def __repr__(self):
        """ in python3, should return unicode.  in python2, should return a
        string of bytes """
        try:
            return str(self)
        except UnicodeDecodeError:
            if self.process:
                if self.stdout:
                    return repr(self.stdout)
            return repr('')

    def __long__(self):
        return long(str(self).strip())

    def __float__(self):
        return float(str(self).strip())

    def __int__(self):
        return int(str(self).strip())


def output_redirect_is_filename(out):
    return isinstance(out, basestring)


def get_prepend_stack():
    tl = Command.thread_local
    if not hasattr(tl, '_prepend_stack'):
        tl._prepend_stack = []
    return tl._prepend_stack


def special_kwarg_validator(kwargs, invalid_list):
    s1 = set(kwargs.keys())
    invalid_args = []
    for args in invalid_list:
        if callable(args):
            fn = args
            ret = fn(kwargs)
            invalid_args.extend(ret)
        else:
            args, error_msg = args
            if s1.issuperset(args):
                invalid_args.append((args, error_msg))

    return invalid_args


def get_fileno(ob):
    fileno_meth = getattr(ob, 'fileno', None)
    fileno = None
    if fileno_meth:
        try:
            fileno = fileno_meth()
        except UnsupportedOperation:
            pass

    else:
        if isinstance(ob, (int, long)):
            if ob >= 0:
                fileno = ob
        return fileno


def ob_is_tty(ob):
    """ checks if an object (like a file-like object) is a tty.  """
    fileno = get_fileno(ob)
    is_tty = False
    if fileno:
        is_tty = os.isatty(fileno)
    return is_tty


def ob_is_pipe(ob):
    fileno = get_fileno(ob)
    is_pipe = False
    if fileno:
        fd_stat = os.fstat(fileno)
        is_pipe = stat.S_ISFIFO(fd_stat.st_mode)
    return is_pipe


def tty_in_validator(kwargs):
    pairs = (('tty_in', 'in'), ('tty_out', 'out'))
    invalid = []
    for tty, std in pairs:
        if tty in kwargs and ob_is_tty(kwargs.get(std, None)):
            args = (
             tty, std)
            error = "`_%s` is a TTY already, so so it doesn't make sense to set up a TTY with `_%s`" % (std, tty)
            invalid.append((args, error))

    return invalid


def bufsize_validator(kwargs):
    """ a validator to prevent a user from saying that they want custom
    buffering when they're using an in/out object that will be os.dup'd to the
    process, and has its own buffering.  an example is a pipe or a tty.  it
    doesn't make sense to tell them to have a custom buffering, since the os
    controls this. """
    invalid = []
    in_ob = kwargs.get('in', None)
    out_ob = kwargs.get('out', None)
    in_buf = kwargs.get('in_bufsize', None)
    out_buf = kwargs.get('out_bufsize', None)
    in_no_buf = ob_is_tty(in_ob) or ob_is_pipe(in_ob)
    out_no_buf = ob_is_tty(out_ob) or ob_is_pipe(out_ob)
    err = "Can't specify an {target} bufsize if the {target} target is a pipe or TTY"
    if in_no_buf:
        if in_buf is not None:
            invalid.append((('in', 'in_bufsize'), err.format(target='in')))
    if out_no_buf:
        if out_buf is not None:
            invalid.append((('out', 'out_bufsize'), err.format(target='out')))
    return invalid


class Command(object):
    __doc__ = ' represents an un-run system program, like "ls" or "cd".  because it\n    represents the program itself (and not a running instance of it), it should\n    hold very little state.  in fact, the only state it does hold is baked\n    arguments.\n    \n    when a Command object is called, the result that is returned is a\n    RunningCommand object, which represents the Command put into an execution\n    state. '
    thread_local = threading.local()
    _call_args = {'fg':False, 
     'bg':False, 
     'bg_exc':True, 
     'with':False, 
     'in':None, 
     'out':None, 
     'err':None, 
     'err_to_out':None, 
     'in_bufsize':0, 
     'out_bufsize':1, 
     'err_bufsize':1, 
     'internal_bufsize':3145728, 
     'env':None, 
     'piped':None, 
     'iter':None, 
     'iter_noblock':None, 
     'ok_code':0, 
     'cwd':None, 
     'long_sep':'=', 
     'long_prefix':'--', 
     'tty_in':False, 
     'tty_out':True, 
     'encoding':DEFAULT_ENCODING, 
     'decode_errors':'strict', 
     'timeout':None, 
     'timeout_signal':signal.SIGKILL, 
     'no_out':False, 
     'no_err':False, 
     'no_pipe':False, 
     'tee':None, 
     'done':None, 
     'tty_size':(20, 80), 
     'truncate_exc':True, 
     'preexec_fn':None, 
     'uid':None, 
     'new_session':True, 
     'arg_preprocess':None, 
     'log_msg':None}
    _kwarg_validators = (
     (('fg', 'bg'), "Command can't be run in the foreground and background"),
     (('fg', 'err_to_out'), "Can't redirect STDERR in foreground mode"),
     (('err', 'err_to_out'), 'Stderr is already being redirected'),
     (('piped', 'iter'), 'You cannot iterate when this command is being piped'),
     (('piped', 'no_pipe'), "Using a pipe doesn't make sense if you've disabled the pipe"),
     (('no_out', 'iter'), 'You cannot iterate over output if there is no output'),
     tty_in_validator,
     bufsize_validator)

    def __init__(self, path, search_paths=None):
        found = which(path, search_paths)
        self._path = encode_to_py3bytes_or_py2str('')
        self._partial = False
        self._partial_baked_args = []
        self._partial_call_args = {}
        self.__name__ = str(self)
        if not found:
            raise CommandNotFound(path)
        self._path = encode_to_py3bytes_or_py2str(found)
        self.__name__ = str(self)

    def __getattribute__(self, name):
        getattr = partial(object.__getattribute__, self)
        val = None
        if name.startswith('_'):
            val = getattr(name)
        else:
            if name == 'bake':
                val = getattr('bake')
            else:
                if name.endswith('_'):
                    name = name[:-1]
        if val is None:
            val = getattr('bake')(name)
        return val

    @staticmethod
    def _extract_call_args(kwargs):
        """ takes kwargs that were passed to a command's __call__ and extracts
        out the special keyword arguments, we return a tuple of special keyword
        args, and kwargs that will go to the execd command """
        kwargs = kwargs.copy()
        call_args = {}
        for parg, default in Command._call_args.items():
            key = '_' + parg
            if key in kwargs:
                call_args[parg] = kwargs[key]
                del kwargs[key]

        invalid_kwargs = special_kwarg_validator(call_args, Command._kwarg_validators)
        if invalid_kwargs:
            exc_msg = []
            for args, error_msg in invalid_kwargs:
                exc_msg.append('  %r: %s' % (args, error_msg))

            exc_msg = '\n'.join(exc_msg)
            raise TypeError('Invalid special arguments:\n\n%s\n' % exc_msg)
        return (call_args, kwargs)

    def bake(self, *args, **kwargs):
        fn = type(self)(self._path)
        fn._partial = True
        call_args, kwargs = self._extract_call_args(kwargs)
        pruned_call_args = call_args
        for k, v in Command._call_args.items():
            try:
                if pruned_call_args[k] == v:
                    del pruned_call_args[k]
            except KeyError:
                continue

        fn._partial_call_args.update(self._partial_call_args)
        fn._partial_call_args.update(pruned_call_args)
        fn._partial_baked_args.extend(self._partial_baked_args)
        sep = pruned_call_args.get('long_sep', self._call_args['long_sep'])
        prefix = pruned_call_args.get('long_prefix', self._call_args['long_prefix'])
        fn._partial_baked_args.extend(compile_args(args, kwargs, sep, prefix))
        return fn

    def __str__(self):
        """ in python3, should return unicode.  in python2, should return a
        string of bytes """
        if IS_PY3:
            return self.__unicode__()
        else:
            return self.__unicode__().encode(DEFAULT_ENCODING)

    def __eq__(self, other):
        return str(self) == str(other)

    __hash__ = None

    def __repr__(self):
        """ in python3, should return unicode.  in python2, should return a
        string of bytes """
        return '<Command %r>' % str(self)

    def __unicode__(self):
        """ a magic method defined for python2.  calling unicode() on a
        self will call this """
        baked_args = ' '.join(item.decode(DEFAULT_ENCODING) for item in self._partial_baked_args)
        if baked_args:
            baked_args = ' ' + baked_args
        return self._path.decode(DEFAULT_ENCODING) + baked_args

    def __enter__(self):
        self(_with=True)

    def __exit__(self, typ, value, traceback):
        get_prepend_stack().pop()

    def __call__(self, *args, **kwargs):
        kwargs = kwargs.copy()
        args = list(args)
        cmd = []
        call_args = Command._call_args.copy()
        for prepend in get_prepend_stack():
            pcall_args = prepend.call_args.copy()
            pcall_args.pop('with', None)
            call_args.update(pcall_args)
            cmd.extend(prepend.cmd)

        cmd.append(self._path)
        preprocessor = self._partial_call_args.get('arg_preprocess', None)
        if preprocessor:
            args, kwargs = preprocessor(args, kwargs)
        extracted_call_args, kwargs = self._extract_call_args(kwargs)
        call_args.update(self._partial_call_args)
        call_args.update(extracted_call_args)
        if call_args['ok_code'] is None:
            call_args['ok_code'] = 0
        if not getattr(call_args['ok_code'], '__iter__', None):
            call_args['ok_code'] = [
             call_args['ok_code']]
        stdin = call_args['in']
        if args:
            first_arg = args.pop(0)
            if isinstance(first_arg, RunningCommand):
                if first_arg.call_args['piped']:
                    stdin = first_arg.process
                else:
                    stdin = first_arg.process._pipe_queue
            else:
                args.insert(0, first_arg)
        processed_args = compile_args(args, kwargs, call_args['long_sep'], call_args['long_prefix'])
        split_args = self._partial_baked_args + processed_args
        final_args = split_args
        cmd.extend(final_args)
        if call_args['fg']:
            if call_args['env'] is None:
                launch = lambda : os.spawnv(os.P_WAIT, cmd[0], cmd)
            else:
                launch = lambda : os.spawnve(os.P_WAIT, cmd[0], cmd, call_args['env'])
            exit_code = launch()
            exc_class = get_exc_exit_code_would_raise(exit_code, call_args['ok_code'], call_args['piped'])
            if exc_class:
                if IS_PY3:
                    ran = ' '.join([arg.decode(DEFAULT_ENCODING, 'ignore') for arg in cmd])
                else:
                    ran = ' '.join(cmd)
                exc = exc_class(ran, b'', b'', call_args['truncate_exc'])
                raise exc
            return
        else:
            stdout = call_args['out']
            if output_redirect_is_filename(stdout):
                stdout = open(str(stdout), 'wb')
            stderr = call_args['err']
            if output_redirect_is_filename(stderr):
                stderr = open(str(stderr), 'wb')
            return RunningCommand(cmd, call_args, stdin, stdout, stderr)


def compile_args(args, kwargs, sep, prefix):
    """ takes args and kwargs, as they were passed into the command instance
    being executed with __call__, and compose them into a flat list that
    will eventually be fed into exec.  example:

    with this call:

        sh.ls("-l", "/tmp", color="never")

    this function receives

        args = ['-l', '/tmp']
        kwargs = {'color': 'never'}

    and produces

        ['-l', '/tmp', '--color=never']
        
    """
    processed_args = []
    encode = encode_to_py3bytes_or_py2str
    for arg in args:
        if isinstance(arg, (list, tuple)):
            if isinstance(arg, GlobResults):
                if not arg:
                    arg = [
                     arg.path]
            for sub_arg in arg:
                processed_args.append(encode(sub_arg))

        else:
            if isinstance(arg, dict):
                processed_args += aggregate_keywords(arg, sep, prefix, raw=True)
            else:
                processed_args.append(encode(arg))

    processed_args += aggregate_keywords(kwargs, sep, prefix)
    return processed_args


def aggregate_keywords(keywords, sep, prefix, raw=False):
    """ take our keyword arguments, and a separator, and compose the list of
    flat long (and short) arguments.  example

        {'color': 'never', 't': True, 'something': True} with sep '='

    becomes

        ['--color=never', '-t', '--something']

    the `raw` argument indicates whether or not we should leave the argument
    name alone, or whether we should replace "_" with "-".  if we pass in a
    dictionary, like this:

        sh.command({"some_option": 12})

    then `raw` gets set to True, because we want to leave the key as-is, to
    produce:

        ['--some_option=12']

    but if we just use a command's kwargs, `raw` is False, which means this:

        sh.command(some_option=12)

    becomes:

        ['--some-option=12']

    eessentially, using kwargs is a convenience, but it lacks the ability to
    put a '-' in the name, so we do the replacement of '_' to '-' for you.
    but when you really don't want that to happen, you should use a
    dictionary instead with the exact names you want
    """
    processed = []
    encode = encode_to_py3bytes_or_py2str
    for k, v in keywords.items():
        if len(k) == 1:
            if v is not False:
                processed.append(encode('-' + k))
                if v is not True:
                    processed.append(encode(v))
        else:
            if not raw:
                k = k.replace('_', '-')
            if v is True:
                processed.append(encode('--' + k))
            else:
                if v is False:
                    continue
                if sep is None or sep == ' ':
                    processed.append(encode(prefix + k))
                    processed.append(encode(v))
                else:
                    arg = encode('%s%s%s%s' % (prefix, k, sep, v))
                    processed.append(arg)

    return processed


def _start_daemon_thread(fn, name, exc_queue, *args):

    def wrap(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except Exception as e:
            exc_queue.put(e)
            raise

    thrd = threading.Thread(target=wrap, name=name, args=args)
    thrd.daemon = True
    thrd.start()
    return thrd


def setwinsize(fd, rows_cols):
    """ set the terminal size of a tty file descriptor.  borrowed logic
    from pexpect.py """
    rows, cols = rows_cols
    TIOCSWINSZ = getattr(termios, 'TIOCSWINSZ', -2146929561)
    s = struct.pack('HHHH', rows, cols, 0, 0)
    fcntl.ioctl(fd, TIOCSWINSZ, s)


def construct_streamreader_callback(process, handler):
    """ here we're constructing a closure for our streamreader callback.  this
    is used in the case that we pass a callback into _out or _err, meaning we
    want to our callback to handle each bit of output

    we construct the closure based on how many arguments it takes.  the reason
    for this is to make it as easy as possible for people to use, without
    limiting them.  a new user will assume the callback takes 1 argument (the
    data).  as they get more advanced, they may want to terminate the process,
    or pass some stdin back, and will realize that they can pass a callback of
    more args """
    implied_arg = 0
    partial_args = 0
    handler_to_inspect = handler
    if isinstance(handler, partial):
        partial_args = len(handler.args)
        handler_to_inspect = handler.func
    if inspect.ismethod(handler_to_inspect):
        implied_arg = 1
        num_args = get_num_args(handler_to_inspect)
    else:
        if inspect.isfunction(handler_to_inspect):
            num_args = get_num_args(handler_to_inspect)
        else:
            implied_arg = 1
            num_args = get_num_args(handler_to_inspect.__call__)
        net_args = num_args - implied_arg - partial_args
        handler_args = ()
        if net_args == 1:
            handler_args = ()
        if net_args == 2:
            handler_args = (
             process.stdin,)
        elif net_args == 3:
            handler_args = (
             process.stdin, weakref.ref(process))

    def fn(chunk):
        args = handler_args
        if len(args) == 2:
            args = (
             handler_args[0], handler_args[1]())
        return handler(chunk, *args)

    return fn


def get_exc_exit_code_would_raise(exit_code, ok_codes, sigpipe_ok):
    exc = None
    success = exit_code in ok_codes
    bad_sig = -exit_code in SIGNALS_THAT_SHOULD_THROW_EXCEPTION
    if sigpipe_ok:
        if -exit_code == signal.SIGPIPE:
            bad_sig = False
            success = True
    if not success or bad_sig:
        exc = get_rc_exc(exit_code)
    return exc


def handle_process_exit_code(exit_code):
    """ this should only ever be called once for each child process """
    if os.WIFSIGNALED(exit_code):
        exit_code = -os.WTERMSIG(exit_code)
    else:
        if os.WIFEXITED(exit_code):
            exit_code = os.WEXITSTATUS(exit_code)
        else:
            raise RuntimeError('Unknown child exit status!')
    return exit_code


def no_interrupt(syscall, *args, **kwargs):
    """ a helper for making system calls immune to EINTR """
    ret = None
    while True:
        try:
            ret = syscall(*args, **kwargs)
        except OSError as e:
            if e.errno == errno.EINTR:
                continue
            else:
                raise
        else:
            break

    return ret


class OProc(object):
    __doc__ = " this class is instantiated by RunningCommand for a command to be exec'd.\n    it handles all the nasty business involved with correctly setting up the\n    input/output to the child process.  it gets its name for subprocess.Popen\n    (process open) but we're calling ours OProc (open process) "
    _default_window_size = (24, 80)
    STDOUT = -1
    STDERR = -2

    def __init__(self, command, parent_log, cmd, stdin, stdout, stderr, call_args, pipe, process_assign_lock):
        """
            cmd is the full string that will be exec'd.  it includes the program
            name and all its arguments

            stdin, stdout, stderr are what the child will use for standard
            input/output/err

            call_args is a mapping of all the special keyword arguments to apply
            to the child process
        """
        self.command = command
        self.call_args = call_args
        ca = self.call_args
        if ca['uid'] is not None:
            if os.getuid() != 0:
                raise RuntimeError('UID setting requires root privileges')
            target_uid = ca['uid']
            pwrec = pwd.getpwuid(ca['uid'])
            target_gid = pwrec.pw_gid
        elif ca['piped']:
            ca['tty_out'] = False
        else:
            self._stdin_process = None
            stdin_is_tty_or_pipe = ob_is_tty(stdin) or ob_is_pipe(stdin)
            stdout_is_tty_or_pipe = ob_is_tty(stdout) or ob_is_pipe(stdout)
            stderr_is_tty_or_pipe = ob_is_tty(stderr) or ob_is_pipe(stderr)
            tee_out = ca['tee'] in (True, 'out')
            tee_err = ca['tee'] == 'err'
            custom_in_out_err = stdin or stdout or stderr
            single_tty = ca['tty_in'] and ca['tty_out'] and not custom_in_out_err
            if single_tty:
                self._stdin_read_fd, self._stdin_write_fd = pty.openpty()
                self._stdout_read_fd = os.dup(self._stdin_read_fd)
                self._stdout_write_fd = os.dup(self._stdin_write_fd)
                self._stderr_read_fd = os.dup(self._stdin_read_fd)
                self._stderr_write_fd = os.dup(self._stdin_write_fd)
            else:
                if isinstance(stdin, OProc):
                    if stdin.call_args['piped']:
                        self._stdin_write_fd = stdin._pipe_fd
                        self._stdin_read_fd = None
                        self._stdin_process = stdin
            if stdin_is_tty_or_pipe:
                self._stdin_write_fd = os.dup(get_fileno(stdin))
                self._stdin_read_fd = None
            else:
                if ca['tty_in']:
                    self._stdin_read_fd, self._stdin_write_fd = pty.openpty()
                else:
                    self._stdin_write_fd, self._stdin_read_fd = os.pipe()
                if stdout_is_tty_or_pipe:
                    if not tee_out:
                        self._stdout_write_fd = os.dup(get_fileno(stdout))
                        self._stdout_read_fd = None
                if ca['tty_out']:
                    self._stdout_read_fd, self._stdout_write_fd = pty.openpty()
                else:
                    self._stdout_read_fd, self._stdout_write_fd = os.pipe()
            if stderr is OProc.STDOUT:
                if stdout_is_tty_or_pipe:
                    if not tee_out:
                        self._stderr_read_fd = None
                else:
                    self._stderr_read_fd = os.dup(self._stdout_read_fd)
                self._stderr_write_fd = os.dup(self._stdout_write_fd)
            elif stderr_is_tty_or_pipe:
                if not tee_err:
                    self._stderr_write_fd = os.dup(get_fileno(stderr))
                    self._stderr_read_fd = None
            else:
                self._stderr_read_fd, self._stderr_write_fd = os.pipe()
        piped = ca['piped']
        self._pipe_fd = None
        if piped:
            fd_to_use = self._stdout_read_fd
            if piped == 'err':
                fd_to_use = self._stderr_read_fd
            self._pipe_fd = os.dup(fd_to_use)
        new_session = ca['new_session']
        needs_ctty = ca['tty_in'] and new_session
        self.ctty = None
        if needs_ctty:
            self.ctty = os.ttyname(self._stdin_write_fd)
        cwd = ca['cwd']
        if cwd is not None:
            if not os.path.exists(cwd):
                os.chdir(cwd)
        gc_enabled = gc.isenabled()
        if gc_enabled:
            gc.disable()
        session_pipe_read, session_pipe_write = os.pipe()
        exc_pipe_read, exc_pipe_write = os.pipe()
        if IS_OSX:
            close_pipe_read, close_pipe_write = os.pipe()
        self.sid = None
        self.pgid = None
        self.pid = os.fork()
        if self.pid == 0:
            if IS_OSX:
                os.read(close_pipe_read, 1)
                os.close(close_pipe_read)
                os.close(close_pipe_write)
            try:
                if ca['bg'] is True:
                    signal.signal(signal.SIGHUP, signal.SIG_IGN)
                else:
                    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
                    if new_session:
                        os.setsid()
                    else:
                        os.setpgrp()
                    sid = os.getsid(0)
                    pgid = os.getpgid(0)
                    payload = ('%d,%d' % (sid, pgid)).encode(DEFAULT_ENCODING)
                    os.write(session_pipe_write, payload)
                    if ca['tty_out']:
                        if not stdout_is_tty_or_pipe:
                            if not single_tty:
                                tty.setraw(self._stdout_write_fd)
                    if self._stdin_read_fd:
                        os.close(self._stdin_read_fd)
                    if self._stdout_read_fd:
                        os.close(self._stdout_read_fd)
                    if self._stderr_read_fd:
                        os.close(self._stderr_read_fd)
                    os.close(session_pipe_read)
                    os.close(exc_pipe_read)
                    if cwd:
                        os.chdir(cwd)
                    os.dup2(self._stdin_write_fd, 0)
                    os.dup2(self._stdout_write_fd, 1)
                    os.dup2(self._stderr_write_fd, 2)
                    if needs_ctty:
                        tmp_fd = os.open(os.ttyname(0), os.O_RDWR)
                        os.close(tmp_fd)
                    if ca['tty_out']:
                        if not stdout_is_tty_or_pipe:
                            setwinsize(1, ca['tty_size'])
                    if ca['uid'] is not None:
                        os.setgid(target_gid)
                        os.setuid(target_uid)
                    preexec_fn = ca['preexec_fn']
                    if callable(preexec_fn):
                        preexec_fn()
                    max_fd = resource.getrlimit(resource.RLIMIT_NOFILE)[0]
                    os.closerange(3, max_fd)
                    if ca['env'] is None:
                        os.execv(cmd[0], cmd)
                    else:
                        os.execve(cmd[0], cmd, ca['env'])
            except:
                try:
                    tb = traceback.format_exc().encode('utf8', 'ignore')
                    os.write(exc_pipe_write, tb)
                finally:
                    os._exit(255)

        else:
            if gc_enabled:
                gc.enable()
            else:
                os.close(self._stdin_write_fd)
                os.close(self._stdout_write_fd)
                os.close(self._stderr_write_fd)
                if IS_OSX:
                    os.close(close_pipe_read)
                    os.write(close_pipe_write, str(1).encode(DEFAULT_ENCODING))
                    os.close(close_pipe_write)
                os.close(exc_pipe_write)
                fork_exc = os.read(exc_pipe_read, 1048576)
                os.close(exc_pipe_read)
                if fork_exc:
                    fork_exc = fork_exc.decode(DEFAULT_ENCODING)
                    raise ForkException(fork_exc)
                os.close(session_pipe_write)
                sid, pgid = os.read(session_pipe_read, 1024).decode(DEFAULT_ENCODING).split(',')
                os.close(session_pipe_read)
                self.sid = int(sid)
                self.pgid = int(pgid)
                self.timed_out = False
                self.started = time.time()
                self.cmd = cmd
                self.exit_code = None
                self.stdin = stdin or Queue()
                self._pipe_queue = Queue()
                self._wait_lock = threading.Lock()
                self._stdout = deque(maxlen=(ca['internal_bufsize']))
                self._stderr = deque(maxlen=(ca['internal_bufsize']))
                if ca['tty_in']:
                    if not stdin_is_tty_or_pipe:
                        setwinsize(self._stdin_read_fd, ca['tty_size'])
                self.log = parent_log.get_child('process', repr(self))
                self.log.debug('started process')
                if ca['tty_in']:
                    if not stdin_is_tty_or_pipe:
                        attr = termios.tcgetattr(self._stdin_read_fd)
                        attr[3] &= ~termios.ECHO
                        termios.tcsetattr(self._stdin_read_fd, termios.TCSANOW, attr)
                potentially_has_input = callable(stdout) or stdin
                self._stdin_stream = None
                if self._stdin_read_fd:
                    if potentially_has_input:
                        log = self.log.get_child('streamwriter', 'stdin')
                        self._stdin_stream = StreamWriter(log, self._stdin_read_fd, self.stdin, ca['in_bufsize'], ca['encoding'], ca['tty_in'])
                stdout_pipe = None
                if pipe is OProc.STDOUT:
                    if not ca['no_pipe']:
                        stdout_pipe = self._pipe_queue
                save_stdout = not ca['no_out'] and (tee_out or stdout is None)
                pipe_out = ca['piped'] in ('out', True)
                pipe_err = ca['piped'] in ('err', )
                self._stdout_stream = None
                if not pipe_out:
                    if self._stdout_read_fd:
                        if callable(stdout):
                            stdout = construct_streamreader_callback(self, stdout)
                        self._stdout_stream = StreamReader((self.log.get_child('streamreader', 'stdout')),
                          (self._stdout_read_fd),
                          stdout, (self._stdout), (ca['out_bufsize']),
                          (ca['encoding']), (ca['decode_errors']),
                          stdout_pipe, save_data=save_stdout)
                if self._stdout_read_fd:
                    os.close(self._stdout_read_fd)
                self._stderr_stream = None
                if stderr is not OProc.STDOUT:
                    if not single_tty:
                        if not pipe_err:
                            if self._stderr_read_fd:
                                stderr_pipe = None
                                if pipe is OProc.STDERR:
                                    if not ca['no_pipe']:
                                        stderr_pipe = self._pipe_queue
                                save_stderr = not ca['no_err'] and (ca['tee'] in ('err', ) or stderr is None)
                                if callable(stderr):
                                    stderr = construct_streamreader_callback(self, stderr)
                                self._stderr_stream = StreamReader((Logger('streamreader')), (self._stderr_read_fd),
                                  stderr, (self._stderr), (ca['err_bufsize']),
                                  (ca['encoding']), (ca['decode_errors']), stderr_pipe,
                                  save_data=save_stderr)
                if self._stderr_read_fd:
                    os.close(self._stderr_read_fd)

                def timeout_fn():
                    self.timed_out = True
                    self.signal(ca['timeout_signal'])

                self._timeout_event = None
                self._timeout_timer = None
                if ca['timeout']:
                    self._timeout_event = threading.Event()
                    self._timeout_timer = threading.Timer(ca['timeout'], self._timeout_event.set)
                    self._timeout_timer.start()
                handle_exit_code = None
                if not self.command._spawned_and_waited:
                    if ca['bg_exc']:

                        def fn(exit_code):
                            with process_assign_lock:
                                return self.command.handle_command_exit_code(exit_code)

                        handle_exit_code = fn
                self._quit_threads = threading.Event()
                thread_name = 'background thread for pid %d' % self.pid
                self._bg_thread_exc_queue = Queue(1)
                self._background_thread = _start_daemon_thread(background_thread, thread_name, self._bg_thread_exc_queue, timeout_fn, self._timeout_event, handle_exit_code, self.is_alive, self._quit_threads)
                self._input_thread = None
                self._input_thread_exc_queue = Queue(1)
                if self._stdin_stream:
                    close_before_term = not needs_ctty
                    thread_name = 'STDIN thread for pid %d' % self.pid
                    self._input_thread = _start_daemon_thread(input_thread, thread_name, self._input_thread_exc_queue, self.log, self._stdin_stream, self.is_alive, self._quit_threads, close_before_term)
            self._stop_output_event = threading.Event()
            self._output_thread_exc_queue = Queue(1)
            thread_name = 'STDOUT/ERR thread for pid %d' % self.pid
            self._output_thread = _start_daemon_thread(output_thread, thread_name, self._output_thread_exc_queue, self.log, self._stdout_stream, self._stderr_stream, self._timeout_event, self.is_alive, self._quit_threads, self._stop_output_event)

    def __repr__(self):
        return '<Process %d %r>' % (self.pid, self.cmd[:500])

    @property
    def output_thread_exc(self):
        exc = None
        try:
            exc = self._output_thread_exc_queue.get(False)
        except Empty:
            pass

        return exc

    @property
    def input_thread_exc(self):
        exc = None
        try:
            exc = self._input_thread_exc_queue.get(False)
        except Empty:
            pass

        return exc

    @property
    def bg_thread_exc(self):
        exc = None
        try:
            exc = self._bg_thread_exc_queue.get(False)
        except Empty:
            pass

        return exc

    def change_in_bufsize(self, buf):
        self._stdin_stream.stream_bufferer.change_buffering(buf)

    def change_out_bufsize(self, buf):
        self._stdout_stream.stream_bufferer.change_buffering(buf)

    def change_err_bufsize(self, buf):
        self._stderr_stream.stream_bufferer.change_buffering(buf)

    @property
    def stdout(self):
        return ''.encode(self.call_args['encoding']).join(self._stdout)

    @property
    def stderr(self):
        return ''.encode(self.call_args['encoding']).join(self._stderr)

    def get_pgid(self):
        """ return the CURRENT group id of the process. this differs from
        self.pgid in that this refects the current state of the process, where
        self.pgid is the group id at launch """
        return os.getpgid(self.pid)

    def get_sid(self):
        """ return the CURRENT session id of the process. this differs from
        self.sid in that this refects the current state of the process, where
        self.sid is the session id at launch """
        return os.getsid(self.pid)

    def signal_group(self, sig):
        self.log.debug('sending signal %d to group', sig)
        os.killpg(self.get_pgid(), sig)

    def signal(self, sig):
        self.log.debug('sending signal %d', sig)
        os.kill(self.pid, sig)

    def kill_group(self):
        self.log.debug('killing group')
        self.signal_group(signal.SIGKILL)

    def kill(self):
        self.log.debug('killing')
        self.signal(signal.SIGKILL)

    def terminate(self):
        self.log.debug('terminating')
        self.signal(signal.SIGTERM)

    def is_alive(self):
        """ polls if our child process has completed, without blocking.  this
        method has side-effects, such as setting our exit_code, if we happen to
        see our child exit while this is running """
        if self.exit_code is not None:
            return (
             False, self.exit_code)
        acquired = self._wait_lock.acquire(False)
        if not acquired:
            if self.exit_code is not None:
                return (False, self.exit_code)
            else:
                return (
                 True, self.exit_code)
        try:
            try:
                pid, exit_code = no_interrupt(os.waitpid, self.pid, os.WNOHANG)
                if pid == self.pid:
                    self.exit_code = handle_process_exit_code(exit_code)
                    self._process_just_ended()
                    return (
                     False, self.exit_code)
            except OSError:
                return (
                 False, self.exit_code)
            else:
                return (
                 True, self.exit_code)
        finally:
            self._wait_lock.release()

    def _process_just_ended(self):
        if self._timeout_timer:
            self._timeout_timer.cancel()
        else:
            done_callback = self.call_args['done']
            if done_callback:
                success = self.exit_code in self.call_args['ok_code']
                done_callback(success, self.exit_code)
            if self._stdin_read_fd:
                if not self._stdin_stream:
                    os.close(self._stdin_read_fd)

    def wait(self):
        """ waits for the process to complete, handles the exit code """
        self.log.debug('acquiring wait lock to wait for completion')
        with self._wait_lock:
            self.log.debug('got wait lock')
            witnessed_end = False
            if self.exit_code is None:
                self.log.debug('exit code not set, waiting on pid')
                pid, exit_code = no_interrupt(os.waitpid, self.pid, 0)
                self.exit_code = handle_process_exit_code(exit_code)
                witnessed_end = True
            else:
                self.log.debug('exit code already set (%d), no need to wait', self.exit_code)
            self._quit_threads.set()
            if self._input_thread:
                self._input_thread.join()
            timer = threading.Timer(2.0, self._stop_output_event.set)
            timer.start()
            self._output_thread.join()
            timer.cancel()
            self._background_thread.join()
            if witnessed_end:
                self._process_just_ended()
            return self.exit_code


def input_thread(log, stdin, is_alive, quit, close_before_term):
    """ this is run in a separate thread.  it writes into our process's
    stdin (a streamwriter) and waits the process to end AND everything that
    can be written to be written """
    done = False
    closed = False
    alive = True
    poller = Poller()
    poller.register_write(stdin)
    while poller and alive:
        changed = poller.poll(1)
        for fd, events in changed:
            if events & (POLLER_EVENT_WRITE | POLLER_EVENT_HUP):
                log.debug('%r ready for more input', stdin)
                done = stdin.write()
                if done:
                    poller.unregister(stdin)
                    if close_before_term:
                        stdin.close()
                        closed = True

        alive, _ = is_alive()

    while alive:
        quit.wait(1)
        alive, _ = is_alive()

    if not closed:
        stdin.close()


def event_wait(ev, timeout=None):
    triggered = ev.wait(timeout)
    if IS_PY26:
        triggered = ev.is_set()
    return triggered


def background_thread(timeout_fn, timeout_event, handle_exit_code, is_alive, quit):
    """ handles the timeout logic """
    if timeout_event:
        while not quit.is_set():
            timed_out = event_wait(timeout_event, 0.1)
            if timed_out:
                timeout_fn()
                break

    if handle_exit_code:
        if not RUNNING_TESTS:
            alive = True
            while alive:
                quit.wait(1)
                alive, exit_code = is_alive()

            handle_exit_code(exit_code)


def output_thread--- This code section failed: ---

 L.2468         0  LOAD_GLOBAL              Poller
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  STORE_FAST               'poller'

 L.2469         6  LOAD_FAST                'stdout'
                8  LOAD_CONST               None
               10  COMPARE_OP               is-not
               12  POP_JUMP_IF_FALSE    24  'to 24'

 L.2470        14  LOAD_FAST                'poller'
               16  LOAD_ATTR                register_read
               18  LOAD_FAST                'stdout'
               20  CALL_FUNCTION_1       1  '1 positional argument'
               22  POP_TOP          
             24_0  COME_FROM            12  '12'

 L.2471        24  LOAD_FAST                'stderr'
               26  LOAD_CONST               None
               28  COMPARE_OP               is-not
               30  POP_JUMP_IF_FALSE    42  'to 42'

 L.2472        32  LOAD_FAST                'poller'
               34  LOAD_ATTR                register_read
               36  LOAD_FAST                'stderr'
               38  CALL_FUNCTION_1       1  '1 positional argument'
               40  POP_TOP          
             42_0  COME_FROM            30  '30'

 L.2479        42  SETUP_LOOP          162  'to 162'
               44  LOAD_FAST                'poller'
               46  POP_JUMP_IF_FALSE   160  'to 160'

 L.2480        48  LOAD_GLOBAL              no_interrupt
               50  LOAD_FAST                'poller'
               52  LOAD_ATTR                poll
               54  LOAD_CONST               0.1
               56  CALL_FUNCTION_2       2  '2 positional arguments'
               58  STORE_FAST               'changed'

 L.2481        60  SETUP_LOOP          134  'to 134'
               62  LOAD_FAST                'changed'
               64  GET_ITER         
               66  FOR_ITER            132  'to 132'
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'f'
               72  STORE_FAST               'events'

 L.2482        74  LOAD_FAST                'events'
               76  LOAD_GLOBAL              POLLER_EVENT_READ
               78  LOAD_GLOBAL              POLLER_EVENT_HUP
               80  BINARY_OR        
               82  BINARY_AND       
               84  POP_JUMP_IF_FALSE   122  'to 122'

 L.2483        86  LOAD_FAST                'log'
               88  LOAD_ATTR                debug
               90  LOAD_STR                 '%r ready to be read from'
               92  LOAD_FAST                'f'
               94  CALL_FUNCTION_2       2  '2 positional arguments'
               96  POP_TOP          

 L.2484        98  LOAD_FAST                'f'
              100  LOAD_ATTR                read
              102  CALL_FUNCTION_0       0  '0 positional arguments'
              104  STORE_FAST               'done'

 L.2485       106  LOAD_FAST                'done'
              108  POP_JUMP_IF_FALSE   130  'to 130'

 L.2486       110  LOAD_FAST                'poller'
              112  LOAD_ATTR                unregister
              114  LOAD_FAST                'f'
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  POP_TOP          
              120  JUMP_BACK            66  'to 66'
              122  ELSE                     '130'

 L.2487       122  LOAD_FAST                'events'
              124  LOAD_GLOBAL              POLLER_EVENT_ERROR
              126  BINARY_AND       
            128_0  COME_FROM           108  '108'
              128  POP_JUMP_IF_FALSE    66  'to 66'

 L.2491       130  JUMP_BACK            66  'to 66'
              132  POP_BLOCK        
            134_0  COME_FROM_LOOP       60  '60'

 L.2493       134  LOAD_FAST                'timeout_event'
              136  POP_JUMP_IF_FALSE   148  'to 148'
              138  LOAD_FAST                'timeout_event'
              140  LOAD_ATTR                is_set
              142  CALL_FUNCTION_0       0  '0 positional arguments'
              144  POP_JUMP_IF_FALSE   148  'to 148'

 L.2494       146  BREAK_LOOP       
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM           136  '136'

 L.2496       148  LOAD_FAST                'stop_output_event'
              150  LOAD_ATTR                is_set
              152  CALL_FUNCTION_0       0  '0 positional arguments'
              154  POP_JUMP_IF_FALSE    44  'to 44'

 L.2497       156  BREAK_LOOP       
            158_0  COME_FROM           154  '154'
              158  JUMP_BACK            44  'to 44'
              160  POP_BLOCK        
            162_0  COME_FROM_LOOP       42  '42'

 L.2501       162  LOAD_FAST                'is_alive'
              164  CALL_FUNCTION_0       0  '0 positional arguments'
              166  UNPACK_SEQUENCE_2     2 
              168  STORE_FAST               'alive'
              170  STORE_FAST               '_'

 L.2502       172  SETUP_LOOP          202  'to 202'
              174  LOAD_FAST                'alive'
              176  POP_JUMP_IF_FALSE   200  'to 200'

 L.2503       178  LOAD_FAST                'quit'
              180  LOAD_ATTR                wait
              182  LOAD_CONST               1
              184  CALL_FUNCTION_1       1  '1 positional argument'
              186  POP_TOP          

 L.2504       188  LOAD_FAST                'is_alive'
              190  CALL_FUNCTION_0       0  '0 positional arguments'
              192  UNPACK_SEQUENCE_2     2 
              194  STORE_FAST               'alive'
              196  STORE_FAST               '_'
              198  JUMP_BACK           174  'to 174'
              200  POP_BLOCK        
            202_0  COME_FROM_LOOP      172  '172'

 L.2506       202  LOAD_FAST                'stdout'
              204  POP_JUMP_IF_FALSE   214  'to 214'

 L.2507       206  LOAD_FAST                'stdout'
              208  LOAD_ATTR                close
              210  CALL_FUNCTION_0       0  '0 positional arguments'
              212  POP_TOP          
            214_0  COME_FROM           204  '204'

 L.2509       214  LOAD_FAST                'stderr'
              216  POP_JUMP_IF_FALSE   226  'to 226'

 L.2510       218  LOAD_FAST                'stderr'
              220  LOAD_ATTR                close
              222  CALL_FUNCTION_0       0  '0 positional arguments'
              224  POP_TOP          
            226_0  COME_FROM           216  '216'

Parse error at or near `COME_FROM' instruction at offset 128_0


class DoneReadingForever(Exception):
    pass


class NotYetReadyToRead(Exception):
    pass


def determine_how_to_read_input(input_obj):
    """ given some kind of input object, return a function that knows how to
    read chunks of that input object.
    
    each reader function should return a chunk and raise a DoneReadingForever
    exception, or return None, when there's no more data to read

    NOTE: the function returned does not need to care much about the requested
    buffering type (eg, unbuffered vs newline-buffered).  the StreamBufferer
    will take care of that.  these functions just need to return a
    reasonably-sized chunk of data. """
    get_chunk = None
    if isinstance(input_obj, Queue):
        log_msg = 'queue'
        get_chunk = get_queue_chunk_reader(input_obj)
    else:
        if callable(input_obj):
            log_msg = 'callable'
            get_chunk = get_callable_chunk_reader(input_obj)
        else:
            if hasattr(input_obj, 'read'):
                log_msg = 'file descriptor'
                get_chunk = get_file_chunk_reader(input_obj)
            else:
                if isinstance(input_obj, basestring):
                    log_msg = 'string'
                    get_chunk = get_iter_string_reader(input_obj)
                else:
                    if isinstance(input_obj, bytes):
                        log_msg = 'bytes'
                        get_chunk = get_iter_string_reader(input_obj)
                    else:
                        if isinstance(input_obj, GeneratorType):
                            log_msg = 'generator'
                            get_chunk = get_iter_chunk_reader(iter(input_obj))
                        else:
                            try:
                                it = iter(input_obj)
                            except TypeError:
                                raise Exception('unknown input object')
                            else:
                                log_msg = 'general iterable'
                                get_chunk = get_iter_chunk_reader(it)
    return (
     get_chunk, log_msg)


def get_queue_chunk_reader(stdin):

    def fn():
        try:
            chunk = stdin.get(True, 0.1)
        except Empty:
            raise NotYetReadyToRead

        if chunk is None:
            raise DoneReadingForever
        return chunk

    return fn


def get_callable_chunk_reader(stdin):

    def fn():
        try:
            data = stdin()
        except DoneReadingForever:
            raise

        if not data:
            raise DoneReadingForever
        return data

    return fn


def get_iter_string_reader(stdin):
    """ return an iterator that returns a chunk of a string every time it is
    called.  notice that even though bufsize_type might be line buffered, we're
    not doing any line buffering here.  that's because our StreamBufferer
    handles all buffering.  we just need to return a reasonable-sized chunk. """
    bufsize = 1024
    iter_str = (stdin[i:i + bufsize] for i in range(0, len(stdin), bufsize))
    return get_iter_chunk_reader(iter_str)


def get_iter_chunk_reader(stdin):

    def fn():
        try:
            if IS_PY3:
                chunk = stdin.__next__()
            else:
                chunk = stdin.next()
            return chunk
        except StopIteration:
            raise DoneReadingForever

    return fn


def get_file_chunk_reader(stdin):
    bufsize = 1024

    def fn():
        is_real_file = True
        if IS_PY3:
            try:
                stdin.fileno()
            except UnsupportedOperation:
                is_real_file = False

        else:
            if is_real_file:
                if hasattr(stdin, 'fileno'):
                    poller = Poller()
                    poller.register_read(stdin)
                    changed = poller.poll(0.1)
                    ready = False
                    for fd, events in changed:
                        if events & (POLLER_EVENT_READ | POLLER_EVENT_HUP):
                            ready = True

                    if not ready:
                        raise NotYetReadyToRead
            chunk = stdin.read(bufsize)
            if not chunk:
                raise DoneReadingForever
            else:
                return chunk

    return fn


def bufsize_type_to_bufsize(bf_type):
    """ for a given bufsize type, return the actual bufsize we will read.
    notice that although 1 means "newline-buffered", we're reading a chunk size
    of 1024.  this is because we have to read something.  we let a
    StreamBufferer instance handle splitting our chunk on newlines """
    if bf_type == 1:
        bufsize = 1024
    else:
        if bf_type == 0:
            bufsize = 1
        else:
            bufsize = bf_type
    return bufsize


class StreamWriter(object):
    __doc__ = ' StreamWriter reads from some input (the stdin param) and writes to a fd\n    (the stream param).  the stdin may be a Queue, a callable, something with\n    the "read" method, a string, or an iterable '

    def __init__(self, log, stream, stdin, bufsize_type, encoding, tty_in):
        self.stream = stream
        self.stdin = stdin
        self.log = log
        self.encoding = encoding
        self.tty_in = tty_in
        self.stream_bufferer = StreamBufferer(bufsize_type, self.encoding)
        self.get_chunk, log_msg = determine_how_to_read_input(stdin)
        self.log.debug('parsed stdin as a %s', log_msg)

    def fileno(self):
        """ defining this allows us to do poll on an instance of this
        class """
        return self.stream

    def write(self):
        """ attempt to get a chunk of data to write to our child process's
        stdin, then write it.  the return value answers the questions "are we
        done writing forever?" """
        try:
            chunk = self.get_chunk()
            if chunk is None:
                raise DoneReadingForever
        except DoneReadingForever:
            self.log.debug('done reading')
            if self.tty_in:
                try:
                    char = termios.tcgetattr(self.stream)[6][termios.VEOF]
                except:
                    char = chr(4).encode()

                os.write(self.stream, char)
                os.write(self.stream, char)
            return True
        except NotYetReadyToRead:
            self.log.debug('received no data')
            return False
        else:
            if IS_PY3:
                if hasattr(chunk, 'encode'):
                    chunk = chunk.encode(self.encoding)
            for proc_chunk in self.stream_bufferer.process(chunk):
                self.log.debug('got chunk size %d: %r', len(proc_chunk), proc_chunk[:30])
                self.log.debug('writing chunk to process')
                try:
                    os.write(self.stream, proc_chunk)
                except OSError:
                    self.log.debug('OSError writing stdin chunk')
                    return True

    def close(self):
        self.log.debug('closing, but flushing first')
        chunk = self.stream_bufferer.flush()
        self.log.debug('got chunk size %d to flush: %r', len(chunk), chunk[:30])
        try:
            if chunk:
                os.write(self.stream, chunk)
        except OSError:
            pass

        os.close(self.stream)


def determine_how_to_feed_output(handler, encoding, decode_errors):
    if callable(handler):
        process, finish = get_callback_chunk_consumer(handler, encoding, decode_errors)
    else:
        if isinstance(handler, (cStringIO, iocStringIO)):
            process, finish = get_cstringio_chunk_consumer(handler)
        else:
            if isinstance(handler, (StringIO, ioStringIO)):
                process, finish = get_stringio_chunk_consumer(handler, encoding, decode_errors)
            else:
                if hasattr(handler, 'write'):
                    process, finish = get_file_chunk_consumer(handler)
                else:
                    try:
                        handler = int(handler)
                    except (ValueError, TypeError):
                        process = lambda chunk: False
                        finish = lambda : None
                    else:
                        process, finish = get_fd_chunk_consumer(handler)
    return (
     process, finish)


def get_fd_chunk_consumer(handler):
    handler = fdopen(handler, 'w', closefd=False)
    return get_file_chunk_consumer(handler)


def get_file_chunk_consumer(handler):
    encode = lambda chunk: chunk
    if getattr(handler, 'encoding', None):
        encode = lambda chunk: chunk.decode(handler.encoding)
    flush = lambda : None
    if hasattr(handler, 'flush'):
        flush = handler.flush

    def process(chunk):
        handler.write(encode(chunk))
        flush()
        return False

    def finish():
        flush()

    return (
     process, finish)


def get_callback_chunk_consumer(handler, encoding, decode_errors):

    def process(chunk):
        try:
            chunk = chunk.decode(encoding, decode_errors)
        except UnicodeDecodeError:
            pass

        return handler(chunk)

    def finish():
        pass

    return (
     process, finish)


def get_cstringio_chunk_consumer(handler):

    def process(chunk):
        handler.write(chunk)
        return False

    def finish():
        pass

    return (
     process, finish)


def get_stringio_chunk_consumer(handler, encoding, decode_errors):

    def process(chunk):
        handler.write(chunk.decode(encoding, decode_errors))
        return False

    def finish():
        pass

    return (
     process, finish)


class StreamReader(object):
    __doc__ = ' reads from some output (the stream) and sends what it just read to the\n    handler.  '

    def __init__(self, log, stream, handler, buffer, bufsize_type, encoding, decode_errors, pipe_queue=None, save_data=True):
        self.stream = stream
        self.buffer = buffer
        self.save_data = save_data
        self.encoding = encoding
        self.decode_errors = decode_errors
        self.pipe_queue = None
        if pipe_queue:
            self.pipe_queue = weakref.ref(pipe_queue)
        self.log = log
        self.stream_bufferer = StreamBufferer(bufsize_type, self.encoding, self.decode_errors)
        self.bufsize = bufsize_type_to_bufsize(bufsize_type)
        self.process_chunk, self.finish_chunk_processor = determine_how_to_feed_output(handler, encoding, decode_errors)
        self.should_quit = False

    def fileno(self):
        """ defining this allows us to do poll on an instance of this
        class """
        return self.stream

    def close(self):
        chunk = self.stream_bufferer.flush()
        self.log.debug('got chunk size %d to flush: %r', len(chunk), chunk[:30])
        if chunk:
            self.write_chunk(chunk)
        self.finish_chunk_processor()
        if self.pipe_queue:
            if self.save_data:
                self.pipe_queue().put(None)
        os.close(self.stream)

    def write_chunk(self, chunk):
        if not self.should_quit:
            self.should_quit = self.process_chunk(chunk)
        if self.save_data:
            self.buffer.append(chunk)
            if self.pipe_queue:
                self.log.debug('putting chunk onto pipe: %r', chunk[:30])
                self.pipe_queue().put(chunk)

    def read(self):
        try:
            chunk = no_interrupt(os.read, self.stream, self.bufsize)
        except OSError as e:
            self.log.debug('got errno %d, done reading', e.errno)
            return True

        if not chunk:
            self.log.debug('got no chunk, done reading')
            return True
        self.log.debug('got chunk size %d: %r', len(chunk), chunk[:30])
        for chunk in self.stream_bufferer.process(chunk):
            self.write_chunk(chunk)


class StreamBufferer(object):
    __doc__ = ' this is used for feeding in chunks of stdout/stderr, and breaking it up\n    into chunks that will actually be put into the internal buffers.  for\n    example, if you have two processes, one being piped to the other, and you\n    want that, first process to feed lines of data (instead of the chunks\n    however they come in), OProc will use an instance of this class to chop up\n    the data and feed it as lines to be sent down the pipe '

    def __init__(self, buffer_type, encoding=DEFAULT_ENCODING, decode_errors='strict'):
        self.type = buffer_type
        self.buffer = []
        self.n_buffer_count = 0
        self.encoding = encoding
        self.decode_errors = decode_errors
        self._use_up_buffer_first = False
        self._buffering_lock = threading.RLock()
        self.log = Logger('stream_bufferer')

    def change_buffering(self, new_type):
        self.log.debug('acquiring buffering lock for changing buffering')
        self._buffering_lock.acquire()
        self.log.debug('got buffering lock for changing buffering')
        try:
            if new_type == 0:
                self._use_up_buffer_first = True
            self.type = new_type
        finally:
            self._buffering_lock.release()
            self.log.debug('released buffering lock for changing buffering')

    def process(self, chunk):
        self.log.debug('acquiring buffering lock to process chunk (buffering: %d)', self.type)
        self._buffering_lock.acquire()
        self.log.debug('got buffering lock to process chunk (buffering: %d)', self.type)
        try:
            if self.type == 0:
                if self._use_up_buffer_first:
                    self._use_up_buffer_first = False
                    to_write = self.buffer
                    self.buffer = []
                    to_write.append(chunk)
                    return to_write
                return [
                 chunk]
            else:
                if self.type == 1:
                    total_to_write = []
                    nl = '\n'.encode(self.encoding)
                    while True:
                        newline = chunk.find(nl)
                        if newline == -1:
                            break
                        chunk_to_write = chunk[:newline + 1]
                        if self.buffer:
                            chunk_to_write = (b'').join(self.buffer) + chunk_to_write
                            self.buffer = []
                            self.n_buffer_count = 0
                        chunk = chunk[newline + 1:]
                        total_to_write.append(chunk_to_write)

                    if chunk:
                        self.buffer.append(chunk)
                        self.n_buffer_count += len(chunk)
                    return total_to_write
                total_to_write = []
                while 1:
                    overage = self.n_buffer_count + len(chunk) - self.type
                    if overage >= 0:
                        ret = ''.encode(self.encoding).join(self.buffer) + chunk
                        chunk_to_write = ret[:self.type]
                        chunk = ret[self.type:]
                        total_to_write.append(chunk_to_write)
                        self.buffer = []
                        self.n_buffer_count = 0
                    else:
                        self.buffer.append(chunk)
                        self.n_buffer_count += len(chunk)
                        break

                return total_to_write
        finally:
            self._buffering_lock.release()
            self.log.debug('released buffering lock for processing chunk (buffering: %d)', self.type)

    def flush(self):
        self.log.debug('acquiring buffering lock for flushing buffer')
        self._buffering_lock.acquire()
        self.log.debug('got buffering lock for flushing buffer')
        try:
            ret = ''.encode(self.encoding).join(self.buffer)
            self.buffer = []
            return ret
        finally:
            self._buffering_lock.release()
            self.log.debug('released buffering lock for flushing buffer')


def with_lock(lock):

    def wrapped(fn):
        fn = contextmanager(fn)

        @contextmanager
        def wrapped2(*args, **kwargs):
            with lock:
                with fn(*args, **kwargs):
                    yield

        return wrapped2

    return wrapped


@with_lock(PUSHD_LOCK)
def pushd(path):
    """ pushd changes the actual working directory for the duration of the
    context, unlike the _cwd arg this will work with other built-ins such as
    sh.glob correctly """
    orig_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(orig_path)


@contextmanager
def args(**kwargs):
    """ allows us to temporarily override all the special keyword parameters in
    a with context """
    kwargs_str = ','.join(['%s=%r' % (k, v) for k, v in kwargs.items()])
    raise DeprecationWarning('\n\nsh.args() has been deprecated because it was never thread safe.  use the\nfollowing instead:\n\n    sh2 = sh({kwargs})\n    sh2.your_command()\n\nor\n\n    sh2 = sh({kwargs})\n    from sh2 import your_command\n    your_command()\n\n'.format(kwargs=kwargs_str))


class Environment(dict):
    __doc__ = ' this allows lookups to names that aren\'t found in the global scope to be\n    searched for as a program name.  for example, if "ls" isn\'t found in this\n    module\'s scope, we consider it a system program and try to find it.\n\n    we use a dict instead of just a regular object as the base class because the\n    exec() statement used in the run_repl requires the "globals" argument to be a\n    dictionary '
    whitelist = set([
     'Command',
     'RunningCommand',
     'CommandNotFound',
     'DEFAULT_ENCODING',
     'DoneReadingForever',
     'ErrorReturnCode',
     'NotYetReadyToRead',
     'SignalException',
     'ForkException',
     'TimeoutException',
     '__project_url__',
     '__version__',
     '__file__',
     'args',
     'pushd',
     'glob',
     'contrib'])

    def __init__(self, globs, baked_args={}):
        """ baked_args are defaults for the 'sh' execution context.  for
        example:
            
            tmp = sh(_out=StringIO())

        'out' would end up in here as an entry in the baked_args dict """
        self.globs = globs
        self.baked_args = baked_args
        self.disable_whitelist = False

    def __getitem__(self, k):
        if k == '_disable_whitelist':
            self.disable_whitelist = True
            return
        else:
            if k in self.whitelist or self.disable_whitelist:
                return self.globs[k]
            else:
                if k == '__all__':
                    raise RuntimeError('Cannot import * from sh. Please import sh or import programs individually.')
                else:
                    exc = get_exc_from_name(k)
                    if exc:
                        return exc
                    if k.startswith('__'):
                        if k.endswith('__'):
                            raise AttributeError
                    builtin = getattr(self, 'b_' + k, None)
                    if builtin:
                        return builtin
                cmd = resolve_command(k, self.baked_args)
                if cmd:
                    return cmd
            try:
                return os.environ[k]
            except KeyError:
                pass

        raise CommandNotFound(k)

    def b_cd(self, path=None):
        if path:
            os.chdir(path)
        else:
            os.chdir(os.path.expanduser('~'))

    def b_which(self, program, paths=None):
        return which(program, paths)


class Contrib(ModuleType):

    @classmethod
    def __call__(cls, name):

        def wrapper1(fn):

            @property
            def cmd_getter(self):
                cmd = resolve_command(name)
                if not cmd:
                    raise CommandNotFound(name)
                new_cmd = fn(cmd)
                return new_cmd

            setattr(cls, name, cmd_getter)
            return fn

        return wrapper1


mod_name = __name__ + '.contrib'
contrib = Contrib(mod_name)
sys.modules[mod_name] = contrib

@contrib('git')
def git(orig):
    """ most git commands play nicer without a TTY """
    cmd = orig.bake(_tty_out=False)
    return cmd


@contrib('sudo')
def sudo(orig):
    """ a nicer version of sudo that uses getpass to ask for a password, or
    allows the first argument to be a string password """
    prompt = '[sudo] password for %s: ' % getpass.getuser()

    def stdin():
        pw = getpass.getpass(prompt=prompt) + '\n'
        yield pw

    def process(args, kwargs):
        password = kwargs.pop('password', None)
        if password is None:
            pass_getter = stdin()
        else:
            pass_getter = password.rstrip('\n') + '\n'
        kwargs['_in'] = pass_getter
        return (args, kwargs)

    cmd = orig.bake('-S', _arg_preprocess=process)
    return cmd


def run_repl(env):
    banner = '\n>> sh v{version}\n>> https://github.com/amoffat/sh\n'
    print(banner.format(version=__version__))
    while True:
        try:
            line = raw_input('sh> ')
        except (ValueError, EOFError):
            break

        try:
            exec(compile(line, '<dummy>', 'single'), env, env)
        except SystemExit:
            break
        except:
            print(traceback.format_exc())

    print('')


class SelfWrapper(ModuleType):

    def __init__(self, self_module, baked_args={}):
        for attr in ('__builtins__', '__doc__', '__file__', '__name__', '__package__'):
            setattr(self, attr, getattr(self_module, attr, None))

        self.__path__ = []
        self._SelfWrapper__self_module = self_module
        self._SelfWrapper__env = Environment((globals()), baked_args=baked_args)

    def __getattr__(self, name):
        return self._SelfWrapper__env[name]

    def __call__(self, **kwargs):
        """ returns a new SelfWrapper object, where all commands spawned from it
        have the baked_args kwargs set on them by default """
        baked_args = self._SelfWrapper__env.baked_args.copy()
        baked_args.update(kwargs)
        new_mod = self.__class__(self._SelfWrapper__self_module, baked_args)
        parent = inspect.stack()[1]
        code = parent[4][0].strip()
        parsed = ast.parse(code)
        module_name = parsed.body[0].targets[0].id
        if module_name == __name__:
            raise RuntimeError("Cannot use the name 'sh' as an execution context")
        sys.modules.pop(module_name, None)
        return new_mod


def in_importlib(frame):
    """ helper for checking if a filename is in importlib guts """
    return frame.f_code.co_filename == '<frozen importlib._bootstrap>'


def register_importer():
    """ registers our fancy importer that can let us import from a module name,
    like:

        import sh
        tmp = sh()
        from tmp import ls
    """

    def test(importer):
        return importer.__class__.__name__ == ModuleImporterFromVariables.__name__

    already_registered = any([True for i in sys.meta_path if test(i)])
    if not already_registered:
        importer = ModuleImporterFromVariables(restrict_to=[
         'SelfWrapper'])
        sys.meta_path.insert(0, importer)
    return not already_registered


def fetch_module_from_frame(name, frame):
    mod = frame.f_locals.get(name, frame.f_globals.get(name, None))
    return mod


class ModuleImporterFromVariables(object):
    __doc__ = ' a fancy importer that allows us to import from a variable that was\n    recently set in either the local or global scope, like this:\n\n        sh2 = sh(_timeout=3)\n        from sh2 import ls\n    \n    '

    def __init__(self, restrict_to=None):
        self.restrict_to = set(restrict_to or set())

    def find_module(self, mod_fullname, path=None):
        """ mod_fullname doubles as the name of the VARIABLE holding our new sh
        context.  for example:

            derp = sh()
            from derp import ls

        here, mod_fullname will be "derp".  keep that in mind as we go throug
        the rest of this function """
        parent_frame = inspect.currentframe().f_back
        while in_importlib(parent_frame):
            parent_frame = parent_frame.f_back

        module = fetch_module_from_frame(mod_fullname, parent_frame)
        if not module:
            return
        else:
            if module.__class__.__name__ not in self.restrict_to:
                return
            return self

    def load_module(self, mod_fullname):
        parent_frame = inspect.currentframe().f_back
        while in_importlib(parent_frame):
            parent_frame = parent_frame.f_back

        module = fetch_module_from_frame(mod_fullname, parent_frame)
        sys.modules[mod_fullname] = module
        module.__loader__ = self
        return module


def run_tests(env, locale, args, version, force_select, **extra_env):
    py_version = 'python'
    py_version += str(version)
    py_bin = which(py_version)
    return_code = None
    poller = 'poll'
    if force_select:
        poller = 'select'
    if py_bin:
        print('Testing %s, locale %r, poller: %s' % (py_version.capitalize(),
         locale, poller))
        env['SH_TESTS_USE_SELECT'] = str(int(force_select))
        env['LANG'] = locale
        for k, v in extra_env.items():
            env[k] = str(v)

        cmd = [py_bin, '-W', 'ignore', os.path.join(THIS_DIR, 'test.py')] + args[1:]
        launch = lambda : os.spawnve(os.P_WAIT, cmd[0], cmd, env)
        return_code = launch()
    return return_code


if __name__ == '__main__':

    def parse_args():
        from optparse import OptionParser
        parser = OptionParser()
        parser.add_option('-e', '--envs', dest='envs', action='append')
        parser.add_option('-l', '--locales', dest='constrain_locales', action='append')
        options, args = parser.parse_args()
        envs = options.envs or []
        constrain_locales = options.constrain_locales or []
        return (
         args, envs, constrain_locales)


    args, constrain_versions, constrain_locales = parse_args()
    action = None
    if args:
        action = args[0]
    if action in ('test', 'travis'):
        import test
        coverage = None
        if test.HAS_UNICODE_LITERAL:
            import coverage
        env = os.environ.copy()
        env['SH_TESTS_RUNNING'] = '1'
        if coverage:
            test.append_module_path(env, coverage)
        if action == 'test':
            all_versions = ('2.6', '2.7', '3.1', '3.2', '3.3', '3.4', '3.5', '3.6')
        elif action == 'travis':
            v = sys.version_info
            sys_ver = '%d.%d' % (v[0], v[1])
            all_versions = (sys_ver,)
        all_force_select = [True]
        if HAS_POLL:
            all_force_select.append(False)
        all_locales = ('en_US.UTF-8', 'C')
        i = 0
        for locale in all_locales:
            if constrain_locales:
                if locale not in constrain_locales:
                    continue
            for version in all_versions:
                if constrain_versions:
                    if version not in constrain_versions:
                        continue
                for force_select in all_force_select:
                    env_copy = env.copy()
                    exit_code = run_tests(env_copy, locale, args, version, force_select,
                      SH_TEST_RUN_IDX=i)
                    if exit_code is None:
                        print("Couldn't find %s, skipping" % version)
                    else:
                        if exit_code != 0:
                            print('Failed for %s, %s' % (version, locale))
                            exit(1)
                    i += 1

        ran_versions = ','.join(all_versions)
        print('Tested Python versions: %s' % ran_versions)
    else:
        env = Environment(globals())
        run_repl(env)
else:
    self = sys.modules[__name__]
    sys.modules[__name__] = SelfWrapper(self)
    register_importer()