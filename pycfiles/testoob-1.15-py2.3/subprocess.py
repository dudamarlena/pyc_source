# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/compatibility/subprocess.py
# Compiled at: 2009-10-07 18:08:46
"""subprocess - Subprocesses with accessible I/O streams

This module allows you to spawn processes and connect to their
input/output/error pipes and obtain their return codes under Unix.
This module intends to replace several other, older modules and
functions, like:

os.system
os.spawn*
os.popen*
popen2.*
commands.*

Information about how the subprocess module can be used to replace these
modules and functions can be found below.

Using the subprocess module
===========================
This module defines one class called Popen:

class Popen(args, bufsize=0, executable=None,
            stdin=None, stdout=None, stderr=None,
            preexec_fn=None, close_fds=False, shell=False,
            cwd=None, env=None, universal_newlines=False,
            startupinfo=None, creationflags=0):

Arguments are:

args should be a string, or a sequence of program arguments.  The
program to execute is normally the first item in the args sequence or
string, but can be explicitly set by using the executable argument.

On UNIX, with shell=False (default): In this case, the Popen class
uses os.execvp() to execute the child program.  args should normally
be a sequence.  A string will be treated as a sequence with the string
as the only item (the program to execute).

On UNIX, with shell=True: If args is a string, it specifies the
command string to execute through the shell.  If args is a sequence,
the first item specifies the command string, and any additional items
will be treated as additional shell arguments.

On Windows: the Popen class uses CreateProcess() to execute the child
program, which operates on strings.  If args is a sequence, it will be
converted to a string using the list2cmdline method.  Please note that
not all MS Windows applications interpret the command line the same
way: The list2cmdline is designed for applications using the same
rules as the MS C runtime.

bufsize, if given, has the same meaning as the corresponding argument
to the built-in open() function: 0 means unbuffered, 1 means line
buffered, any other positive value means use a buffer of
(approximately) that size.  A negative bufsize means to use the system
default, which usually means fully buffered.  The default value for
bufsize is 0 (unbuffered).

stdin, stdout and stderr specify the executed programs' standard
input, standard output and standard error file handles, respectively.
Valid values are PIPE, an existing file descriptor (a positive
integer), an existing file object, and None.  PIPE indicates that a
new pipe to the child should be created.  With None, no redirection
will occur; the child's file handles will be inherited from the
parent.  Additionally, stderr can be STDOUT, which indicates that the
stderr data from the applications should be captured into the same
file handle as for stdout.

If preexec_fn is set to a callable object, this object will be called
in the child process just before the child is executed.

If close_fds is true, all file descriptors except 0, 1 and 2 will be
closed before the child process is executed.

if shell is true, the specified command will be executed through the
shell.

If cwd is not None, the current directory will be changed to cwd
before the child is executed.

If env is not None, it defines the environment variables for the new
process.

If universal_newlines is true, the file objects stdout and stderr are
opened as a text files, but lines may be terminated by any of '
',
the Unix end-of-line convention, '
', the Macintosh convention or
'
', the Windows convention.  All of these external representations
are seen as '
' by the Python program.  Note: This feature is only
available if Python is built with universal newline support (the
default).  Also, the newlines attribute of the file objects stdout,
stdin and stderr are not updated by the communicate() method.

The startupinfo and creationflags, if given, will be passed to the
underlying CreateProcess() function.  They can specify things such as
appearance of the main window and priority for the new process.
(Windows only)

This module also defines two shortcut functions:

call(*args, **kwargs):
    Run command with arguments.  Wait for command to complete, then
    return the returncode attribute.

    The arguments are the same as for the Popen constructor.  Example:

    retcode = call(["ls", "-l"])

Exceptions
----------
Exceptions raised in the child process, before the new program has
started to execute, will be re-raised in the parent.  Additionally,
the exception object will have one extra attribute called
'child_traceback', which is a string containing traceback information
from the childs point of view.

The most common exception raised is OSError.  This occurs, for
example, when trying to execute a non-existent file.  Applications
should prepare for OSErrors.

A ValueError will be raised if Popen is called with invalid arguments.

Security
--------
Unlike some other popen functions, this implementation will never call
/bin/sh implicitly.  This means that all characters, including shell
metacharacters, can safely be passed to child processes.

Popen objects
=============
Instances of the Popen class have the following methods:

poll()
    Check if child process has terminated.  Returns returncode
    attribute.

wait()
    Wait for child process to terminate.  Returns returncode attribute.

communicate(input=None)
    Interact with process: Send data to stdin.  Read data from stdout
    and stderr, until end-of-file is reached.  Wait for process to
    terminate.  The optional stdin argument should be a string to be
    sent to the child process, or None, if no data should be sent to
    the child.

    communicate() returns a tuple (stdout, stderr).

    Note: The data read is buffered in memory, so do not use this
    method if the data size is large or unlimited.

The following attributes are also available:

stdin
    If the stdin argument is PIPE, this attribute is a file object
    that provides input to the child process.  Otherwise, it is None.

stdout
    If the stdout argument is PIPE, this attribute is a file object
    that provides output from the child process.  Otherwise, it is
    None.

stderr
    If the stderr argument is PIPE, this attribute is file object that
    provides error output from the child process.  Otherwise, it is
    None.

pid
    The process ID of the child process.

returncode
    The child return code.  A None value indicates that the process
    hasn't terminated yet.  A negative value -N indicates that the
    child was terminated by signal N (UNIX only).

Replacing older functions with the subprocess module
====================================================
In this section, "a ==> b" means that b can be used as a replacement
for a.

Note: All functions in this section fail (more or less) silently if
the executed program cannot be found; this module raises an OSError
exception.

In the following examples, we assume that the subprocess module is
imported with "from subprocess import *".

Replacing /bin/sh shell backquote
---------------------------------
output=`mycmd myarg`
==>
output = Popen(["mycmd", "myarg"], stdout=PIPE).communicate()[0]

Replacing shell pipe line
-------------------------
output=`dmesg | grep hda`
==>
p1 = Popen(["dmesg"], stdout=PIPE)
p2 = Popen(["grep", "hda"], stdin=p1.stdout)
output = p2.communicate()[0]

Replacing os.system()
---------------------
sts = os.system("mycmd" + " myarg")
==>
p = Popen("mycmd" + " myarg", shell=True)
sts = os.waitpid(p.pid, 0)

Note:

* Calling the program through the shell is usually not required.

* It's easier to look at the returncode attribute than the
  exitstatus.

A more real-world example would look like this:

try:
    retcode = call("mycmd" + " myarg", shell=True)
    if retcode < 0:
        print >>sys.stderr, "Child was terminated by signal", -retcode
    else:
        print >>sys.stderr, "Child returned", retcode
except OSError, e:
    print >>sys.stderr, "Execution failed:", e

Replacing os.spawn*
-------------------
P_NOWAIT example:

pid = os.spawnlp(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg")
==>
pid = Popen(["/bin/mycmd", "myarg"]).pid

P_WAIT example:

retcode = os.spawnlp(os.P_WAIT, "/bin/mycmd", "mycmd", "myarg")
==>
retcode = call(["/bin/mycmd", "myarg"])

Vector example:

os.spawnvp(os.P_NOWAIT, path, args)
==>
Popen([path] + args[1:])

Environment example:

os.spawnlpe(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg", env)
==>
Popen(["/bin/mycmd", "myarg"], env={"PATH": "/usr/bin"})

Replacing os.popen*
-------------------
pipe = os.popen(cmd, mode='r', bufsize)
==>
pipe = Popen(cmd, shell=True, bufsize=bufsize, stdout=PIPE).stdout

pipe = os.popen(cmd, mode='w', bufsize)
==>
pipe = Popen(cmd, shell=True, bufsize=bufsize, stdin=PIPE).stdin

(child_stdin, child_stdout) = os.popen2(cmd, mode, bufsize)
==>
p = Popen(cmd, shell=True, bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, close_fds=True)
(child_stdin, child_stdout) = (p.stdin, p.stdout)

(child_stdin,
 child_stdout,
 child_stderr) = os.popen3(cmd, mode, bufsize)
==>
p = Popen(cmd, shell=True, bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
(child_stdin,
 child_stdout,
 child_stderr) = (p.stdin, p.stdout, p.stderr)

(child_stdin, child_stdout_and_stderr) = os.popen4(cmd, mode, bufsize)
==>
p = Popen(cmd, shell=True, bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
(child_stdin, child_stdout_and_stderr) = (p.stdin, p.stdout)

Replacing popen2.*
------------------
Note: If the cmd argument to popen2 functions is a string, the command
is executed through /bin/sh.  If it is a list, the command is directly
executed.

(child_stdout, child_stdin) = popen2.popen2("somestring", bufsize, mode)
==>
p = Popen(["somestring"], shell=True, bufsize=bufsize
          stdin=PIPE, stdout=PIPE, close_fds=True)
(child_stdout, child_stdin) = (p.stdout, p.stdin)

(child_stdout, child_stdin) = popen2.popen2(["mycmd", "myarg"], bufsize, mode)
==>
p = Popen(["mycmd", "myarg"], bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, close_fds=True)
(child_stdout, child_stdin) = (p.stdout, p.stdin)

The popen2.Popen3 and popen3.Popen4 basically works as subprocess.Popen,
except that:

* subprocess.Popen raises an exception if the execution fails
* the capturestderr argument is replaced with the stderr argument.
* stdin=PIPE and stdout=PIPE must be specified.
* popen2 closes all filedescriptors by default, but you have to specify
  close_fds=True with subprocess.Popen.

"""
import sys
mswindows = sys.platform == 'win32'
import os, types, traceback
if mswindows:
    import threading, msvcrt
    try:
        from _subprocess import *

        class STARTUPINFO:
            __module__ = __name__
            dwFlags = 0
            hStdInput = None
            hStdOutput = None
            hStdError = None


        class pywintypes:
            __module__ = __name__
            error = IOError


    except ImportError:
        import pywintypes
        from win32api import GetStdHandle, STD_INPUT_HANDLE, STD_OUTPUT_HANDLE, STD_ERROR_HANDLE
        from win32api import GetCurrentProcess, DuplicateHandle, GetModuleFileName, GetVersion
        from win32con import DUPLICATE_SAME_ACCESS
        from win32pipe import CreatePipe
        from win32process import CreateProcess, STARTUPINFO, GetExitCodeProcess, STARTF_USESTDHANDLES, CREATE_NEW_CONSOLE
        from win32event import WaitForSingleObject, INFINITE, WAIT_OBJECT_0

else:
    import select, errno, fcntl, pickle
__all__ = [
 'Popen', 'PIPE', 'STDOUT', 'call']
try:
    MAXFD = os.sysconf('SC_OPEN_MAX')
except:
    MAXFD = 256

try:
    False
except NameError:
    False = 0
    True = 1

_active = []

def _cleanup():
    for inst in _active[:]:
        inst.poll()


PIPE = -1
STDOUT = -2

def call(*args, **kwargs):
    """Run command with arguments.  Wait for command to complete, then
    return the returncode attribute.

    The arguments are the same as for the Popen constructor.  Example:

    retcode = call(["ls", "-l"])
    """
    return Popen(*args, **kwargs).wait()


def list2cmdline(seq):
    """
    Translate a sequence of arguments into a command line
    string, using the same rules as the MS C runtime:

    1) Arguments are delimited by white space, which is either a
       space or a tab.

    2) A string surrounded by double quotation marks is
       interpreted as a single argument, regardless of white space
       contained within.  A quoted string can be embedded in an
       argument.

    3) A double quotation mark preceded by a backslash is
       interpreted as a literal double quotation mark.

    4) Backslashes are interpreted literally, unless they
       immediately precede a double quotation mark.

    5) If backslashes immediately precede a double quotation mark,
       every pair of backslashes is interpreted as a literal
       backslash.  If the number of backslashes is odd, the last
       backslash escapes the next double quotation mark as
       described in rule 3.
    """
    result = []
    needquote = False
    for arg in seq:
        bs_buf = []
        if result:
            result.append(' ')
        needquote = ' ' in arg or '\t' in arg
        if needquote:
            result.append('"')
        for c in arg:
            if c == '\\':
                bs_buf.append(c)
            elif c == '"':
                result.append('\\' * len(bs_buf) * 2)
                bs_buf = []
                result.append('\\"')
            else:
                if bs_buf:
                    result.extend(bs_buf)
                    bs_buf = []
                result.append(c)

        if bs_buf:
            result.extend(bs_buf)
        if needquote:
            result.append('"')

    return ('').join(result)


class Popen(object):
    __module__ = __name__

    def __init__(self, args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0):
        """Create new Popen instance."""
        _cleanup()
        if mswindows:
            if preexec_fn is not None:
                raise ValueError('preexec_fn is not supported on Windows platforms')
            if close_fds:
                raise ValueError('close_fds is not supported on Windows platforms')
        else:
            if startupinfo is not None:
                raise ValueError('startupinfo is only supported on Windows platforms')
            if creationflags != 0:
                raise ValueError('creationflags is only supported on Windows platforms')
        self.stdin = None
        self.stdout = None
        self.stderr = None
        self.pid = None
        self.returncode = None
        self.universal_newlines = universal_newlines
        (p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite) = self._get_handles(stdin, stdout, stderr)
        self._execute_child(args, executable, preexec_fn, close_fds, cwd, env, universal_newlines, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)
        if p2cwrite:
            self.stdin = os.fdopen(p2cwrite, 'wb', bufsize)
        if c2pread:
            if universal_newlines:
                self.stdout = os.fdopen(c2pread, 'rU', bufsize)
            else:
                self.stdout = os.fdopen(c2pread, 'rb', bufsize)
        if errread:
            if universal_newlines:
                self.stderr = os.fdopen(errread, 'rU', bufsize)
            else:
                self.stderr = os.fdopen(errread, 'rb', bufsize)
        _active.append(self)
        return

    def _translate_newlines(self, data):
        data = data.replace('\r\n', '\n')
        data = data.replace('\r', '\n')
        return data

    if mswindows:

        def _get_handles(self, stdin, stdout, stderr):
            """Construct and return tupel with IO objects:
            p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite
            """
            if stdin == None and stdout == None and stderr == None:
                return (
                 None, None, None, None, None, None)
            (p2cread, p2cwrite) = (None, None)
            (c2pread, c2pwrite) = (None, None)
            (errread, errwrite) = (None, None)
            if stdin == None:
                p2cread = GetStdHandle(STD_INPUT_HANDLE)
            elif stdin == PIPE:
                (p2cread, p2cwrite) = CreatePipe(None, 0)
                p2cwrite = p2cwrite.Detach()
                p2cwrite = msvcrt.open_osfhandle(p2cwrite, 0)
            elif type(stdin) == types.IntType:
                p2cread = msvcrt.get_osfhandle(stdin)
            else:
                p2cread = msvcrt.get_osfhandle(stdin.fileno())
            p2cread = self._make_inheritable(p2cread)
            if stdout == None:
                c2pwrite = GetStdHandle(STD_OUTPUT_HANDLE)
            elif stdout == PIPE:
                (c2pread, c2pwrite) = CreatePipe(None, 0)
                c2pread = c2pread.Detach()
                c2pread = msvcrt.open_osfhandle(c2pread, 0)
            elif type(stdout) == types.IntType:
                c2pwrite = msvcrt.get_osfhandle(stdout)
            else:
                c2pwrite = msvcrt.get_osfhandle(stdout.fileno())
            c2pwrite = self._make_inheritable(c2pwrite)
            if stderr == None:
                errwrite = GetStdHandle(STD_ERROR_HANDLE)
            elif stderr == PIPE:
                (errread, errwrite) = CreatePipe(None, 0)
                errread = errread.Detach()
                errread = msvcrt.open_osfhandle(errread, 0)
            elif stderr == STDOUT:
                errwrite = c2pwrite
            elif type(stderr) == types.IntType:
                errwrite = msvcrt.get_osfhandle(stderr)
            else:
                errwrite = msvcrt.get_osfhandle(stderr.fileno())
            errwrite = self._make_inheritable(errwrite)
            return (
             p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)
            return

        def _make_inheritable(self, handle):
            """Return a duplicate of handle, which is inheritable"""
            return DuplicateHandle(GetCurrentProcess(), handle, GetCurrentProcess(), 0, 1, DUPLICATE_SAME_ACCESS)

        def _find_w9xpopen(self):
            """Find and return absolut path to w9xpopen.exe"""
            w9xpopen = os.path.join(os.path.dirname(GetModuleFileName(0)), 'w9xpopen.exe')
            if not os.path.exists(w9xpopen):
                w9xpopen = os.path.join(os.path.dirname(sys.exec_prefix), 'w9xpopen.exe')
                if not os.path.exists(w9xpopen):
                    raise RuntimeError('Cannot locate w9xpopen.exe, which is needed for Popen to work with your shell or platform.')
            return w9xpopen

        def _execute_child(self, args, executable, preexec_fn, close_fds, cwd, env, universal_newlines, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite):
            """Execute program (MS Windows version)"""
            if not isinstance(args, types.StringTypes):
                args = list2cmdline(args)
            if shell:
                comspec = os.environ.get('COMSPEC', 'cmd.exe')
                args = comspec + ' /c ' + args
                if GetVersion() >= 2147483648 or os.path.basename(comspec).lower() == 'command.com':
                    w9xpopen = self._find_w9xpopen()
                    args = '"%s" %s' % (w9xpopen, args)
                    creationflags |= CREATE_NEW_CONSOLE
            if startupinfo == None:
                startupinfo = STARTUPINFO()
            if not None in (p2cread, c2pwrite, errwrite):
                startupinfo.dwFlags |= STARTF_USESTDHANDLES
                startupinfo.hStdInput = p2cread
                startupinfo.hStdOutput = c2pwrite
                startupinfo.hStdError = errwrite
            try:
                (hp, ht, pid, tid) = CreateProcess(executable, args, None, None, 1, creationflags, env, cwd, startupinfo)
            except pywintypes.error, e:
                raise WindowsError(*e.args)

            self._handle = hp
            self.pid = pid
            ht.Close()
            if p2cread != None:
                p2cread.Close()
            if c2pwrite != None:
                c2pwrite.Close()
            if errwrite != None:
                errwrite.Close()
            return

        def poll(self):
            """Check if child process has terminated.  Returns returncode
            attribute."""
            if self.returncode == None:
                if WaitForSingleObject(self._handle, 0) == WAIT_OBJECT_0:
                    self.returncode = GetExitCodeProcess(self._handle)
                    _active.remove(self)
            return self.returncode
            return

        def wait(self):
            """Wait for child process to terminate.  Returns returncode
            attribute."""
            if self.returncode == None:
                obj = WaitForSingleObject(self._handle, INFINITE)
                self.returncode = GetExitCodeProcess(self._handle)
                _active.remove(self)
            return self.returncode
            return

        def _readerthread(self, fh, buffer):
            buffer.append(fh.read())

        def communicate(self, input=None):
            """Interact with process: Send data to stdin.  Read data from
            stdout and stderr, until end-of-file is reached.  Wait for
            process to terminate.  The optional input argument should be a
            string to be sent to the child process, or None, if no data
            should be sent to the child.

            communicate() returns a tuple (stdout, stderr)."""
            stdout = None
            stderr = None
            if self.stdout:
                stdout = []
                stdout_thread = threading.Thread(target=self._readerthread, args=(self.stdout, stdout))
                stdout_thread.setDaemon(True)
                stdout_thread.start()
            if self.stderr:
                stderr = []
                stderr_thread = threading.Thread(target=self._readerthread, args=(self.stderr, stderr))
                stderr_thread.setDaemon(True)
                stderr_thread.start()
            if self.stdin:
                if input != None:
                    self.stdin.write(input)
                self.stdin.close()
            if self.stdout:
                stdout_thread.join()
            if self.stderr:
                stderr_thread.join()
            if stdout != None:
                stdout = stdout[0]
            if stderr != None:
                stderr = stderr[0]
            if self.universal_newlines and hasattr(open, 'newlines'):
                if stdout:
                    stdout = self._translate_newlines(stdout)
                if stderr:
                    stderr = self._translate_newlines(stderr)
            self.wait()
            return (stdout, stderr)
            return

    else:

        def _get_handles(self, stdin, stdout, stderr):
            """Construct and return tupel with IO objects:
            p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite
            """
            (p2cread, p2cwrite) = (
             None, None)
            (c2pread, c2pwrite) = (None, None)
            (errread, errwrite) = (None, None)
            if stdin == None:
                pass
            elif stdin == PIPE:
                (p2cread, p2cwrite) = os.pipe()
            elif type(stdin) == types.IntType:
                p2cread = stdin
            else:
                p2cread = stdin.fileno()
            if stdout == None:
                pass
            elif stdout == PIPE:
                (c2pread, c2pwrite) = os.pipe()
            elif type(stdout) == types.IntType:
                c2pwrite = stdout
            else:
                c2pwrite = stdout.fileno()
            if stderr == None:
                pass
            elif stderr == PIPE:
                (errread, errwrite) = os.pipe()
            elif stderr == STDOUT:
                errwrite = c2pwrite
            elif type(stderr) == types.IntType:
                errwrite = stderr
            else:
                errwrite = stderr.fileno()
            return (p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)
            return

        def _set_cloexec_flag(self, fd):
            try:
                cloexec_flag = fcntl.FD_CLOEXEC
            except AttributeError:
                cloexec_flag = 1

            old = fcntl.fcntl(fd, fcntl.F_GETFD)
            fcntl.fcntl(fd, fcntl.F_SETFD, old | cloexec_flag)

        def _close_fds(self, but):
            for i in range(3, MAXFD):
                if i == but:
                    continue
                try:
                    os.close(i)
                except:
                    pass

        def _execute_child(self, args, executable, preexec_fn, close_fds, cwd, env, universal_newlines, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite):
            """Execute program (POSIX version)"""
            if isinstance(args, types.StringTypes):
                args = [
                 args]
            if shell:
                args = [
                 '/bin/sh', '-c'] + args
            if executable == None:
                executable = args[0]
            (errpipe_read, errpipe_write) = os.pipe()
            self._set_cloexec_flag(errpipe_write)
            self.pid = os.fork()
            if self.pid == 0:
                try:
                    if p2cwrite:
                        os.close(p2cwrite)
                    if c2pread:
                        os.close(c2pread)
                    if errread:
                        os.close(errread)
                    os.close(errpipe_read)
                    if p2cread:
                        os.dup2(p2cread, 0)
                    if c2pwrite:
                        os.dup2(c2pwrite, 1)
                    if errwrite:
                        os.dup2(errwrite, 2)
                    if p2cread:
                        os.close(p2cread)
                    if c2pwrite and c2pwrite not in (p2cread,):
                        os.close(c2pwrite)
                    if errwrite and errwrite not in (p2cread, c2pwrite):
                        os.close(errwrite)
                    if close_fds:
                        self._close_fds(but=errpipe_write)
                    if cwd != None:
                        os.chdir(cwd)
                    if preexec_fn:
                        apply(preexec_fn)
                    if env == None:
                        os.execvp(executable, args)
                    else:
                        os.execvpe(executable, args, env)
                except:
                    (exc_type, exc_value, tb) = sys.exc_info()
                    exc_lines = traceback.format_exception(exc_type, exc_value, tb)
                    exc_value.child_traceback = ('').join(exc_lines)
                    os.write(errpipe_write, pickle.dumps(exc_value))
                else:
                    os._exit(255)
            os.close(errpipe_write)
            if p2cread and p2cwrite:
                os.close(p2cread)
            if c2pwrite and c2pread:
                os.close(c2pwrite)
            if errwrite and errread:
                os.close(errwrite)
            data = os.read(errpipe_read, 1048576)
            os.close(errpipe_read)
            if data != '':
                child_exception = pickle.loads(data)
                raise child_exception
            return

        def _handle_exitstatus(self, sts):
            if os.WIFSIGNALED(sts):
                self.returncode = -os.WTERMSIG(sts)
            elif os.WIFEXITED(sts):
                self.returncode = os.WEXITSTATUS(sts)
            else:
                raise RuntimeError('Unknown child exit status!')
            _active.remove(self)

        def poll(self):
            """Check if child process has terminated.  Returns returncode
            attribute."""
            if self.returncode == None:
                try:
                    (pid, sts) = os.waitpid(self.pid, os.WNOHANG)
                    if pid == self.pid:
                        self._handle_exitstatus(sts)
                except os.error:
                    pass

            return self.returncode
            return

        def wait(self):
            """Wait for child process to terminate.  Returns returncode
            attribute."""
            if self.returncode == None:
                (pid, sts) = os.waitpid(self.pid, 0)
                self._handle_exitstatus(sts)
            return self.returncode
            return

        def communicate(self, input=None):
            """Interact with process: Send data to stdin.  Read data from
            stdout and stderr, until end-of-file is reached.  Wait for
            process to terminate.  The optional input argument should be a
            string to be sent to the child process, or None, if no data
            should be sent to the child.

            communicate() returns a tuple (stdout, stderr)."""
            read_set = []
            write_set = []
            stdout = None
            stderr = None
            if self.stdin:
                self.stdin.flush()
                if input:
                    write_set.append(self.stdin)
                else:
                    self.stdin.close()
            if self.stdout:
                read_set.append(self.stdout)
                stdout = []
            if self.stderr:
                read_set.append(self.stderr)
                stderr = []
            while read_set or write_set:
                (rlist, wlist, xlist) = select.select(read_set, write_set, [])
                if self.stdin in wlist:
                    bytes_written = os.write(self.stdin.fileno(), input[:512])
                    input = input[bytes_written:]
                    if not input:
                        self.stdin.close()
                        write_set.remove(self.stdin)
                if self.stdout in rlist:
                    data = os.read(self.stdout.fileno(), 1024)
                    if data == '':
                        self.stdout.close()
                        read_set.remove(self.stdout)
                    stdout.append(data)
                if self.stderr in rlist:
                    data = os.read(self.stderr.fileno(), 1024)
                    if data == '':
                        self.stderr.close()
                        read_set.remove(self.stderr)
                    stderr.append(data)

            if stdout != None:
                stdout = ('').join(stdout)
            if stderr != None:
                stderr = ('').join(stderr)
            if self.universal_newlines and hasattr(open, 'newlines'):
                if stdout:
                    stdout = self._translate_newlines(stdout)
                if stderr:
                    stderr = self._translate_newlines(stderr)
            self.wait()
            return (stdout, stderr)
            return


def _demo_posix():
    plist = Popen(['ps'], stdout=PIPE).communicate()[0]
    print 'Process list:'
    print plist
    if os.getuid() == 0:
        p = Popen(['id'], preexec_fn=lambda : os.setuid(100))
        p.wait()
    print "Looking for 'hda'..."
    p1 = Popen(['dmesg'], stdout=PIPE)
    p2 = Popen(['grep', 'hda'], stdin=p1.stdout, stdout=PIPE)
    print repr(p2.communicate()[0])
    print
    print 'Trying a weird file...'
    try:
        print Popen(['/this/path/does/not/exist']).communicate()
    except OSError, e:
        if e.errno == errno.ENOENT:
            print "The file didn't exist.  I thought so..."
            print 'Child traceback:'
            print e.child_traceback
        else:
            print 'Error', e.errno
    else:
        print >> sys.stderr, 'Gosh.  No error.'


def _demo_windows():
    print "Looking for 'PROMPT' in set output..."
    p1 = Popen('set', stdout=PIPE, shell=True)
    p2 = Popen('find "PROMPT"', stdin=p1.stdout, stdout=PIPE)
    print repr(p2.communicate()[0])
    print 'Executing calc...'
    p = Popen('calc')
    p.wait()


if __name__ == '__main__':
    if mswindows:
        _demo_windows()
    else:
        _demo_posix()