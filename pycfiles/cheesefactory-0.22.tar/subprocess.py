# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cheesecake/subprocess.py
# Compiled at: 2016-04-28 07:08:56
__doc__ = 'subprocess - Subprocesses with accessible I/O streams\n\nThis module allows you to spawn processes, connect to their\ninput/output/error pipes, and obtain their return codes.  This module\nintends to replace several other, older modules and functions, like:\n\nos.system\nos.spawn*\nos.popen*\npopen2.*\ncommands.*\n\nInformation about how the subprocess module can be used to replace these\nmodules and functions can be found below.\n\n\n\nUsing the subprocess module\n===========================\nThis module defines one class called Popen:\n\nclass Popen(args, bufsize=0, executable=None,\n            stdin=None, stdout=None, stderr=None,\n            preexec_fn=None, close_fds=False, shell=False,\n            cwd=None, env=None, universal_newlines=False,\n            startupinfo=None, creationflags=0):\n\n\nArguments are:\n\nargs should be a string, or a sequence of program arguments.  The\nprogram to execute is normally the first item in the args sequence or\nstring, but can be explicitly set by using the executable argument.\n\nOn UNIX, with shell=False (default): In this case, the Popen class\nuses os.execvp() to execute the child program.  args should normally\nbe a sequence.  A string will be treated as a sequence with the string\nas the only item (the program to execute).\n\nOn UNIX, with shell=True: If args is a string, it specifies the\ncommand string to execute through the shell.  If args is a sequence,\nthe first item specifies the command string, and any additional items\nwill be treated as additional shell arguments.\n\nOn Windows: the Popen class uses CreateProcess() to execute the child\nprogram, which operates on strings.  If args is a sequence, it will be\nconverted to a string using the list2cmdline method.  Please note that\nnot all MS Windows applications interpret the command line the same\nway: The list2cmdline is designed for applications using the same\nrules as the MS C runtime.\n\nbufsize, if given, has the same meaning as the corresponding argument\nto the built-in open() function: 0 means unbuffered, 1 means line\nbuffered, any other positive value means use a buffer of\n(approximately) that size.  A negative bufsize means to use the system\ndefault, which usually means fully buffered.  The default value for\nbufsize is 0 (unbuffered).\n\nstdin, stdout and stderr specify the executed programs\' standard\ninput, standard output and standard error file handles, respectively.\nValid values are PIPE, an existing file descriptor (a positive\ninteger), an existing file object, and None.  PIPE indicates that a\nnew pipe to the child should be created.  With None, no redirection\nwill occur; the child\'s file handles will be inherited from the\nparent.  Additionally, stderr can be STDOUT, which indicates that the\nstderr data from the applications should be captured into the same\nfile handle as for stdout.\n\nIf preexec_fn is set to a callable object, this object will be called\nin the child process just before the child is executed.\n\nIf close_fds is true, all file descriptors except 0, 1 and 2 will be\nclosed before the child process is executed.\n\nif shell is true, the specified command will be executed through the\nshell.\n\nIf cwd is not None, the current directory will be changed to cwd\nbefore the child is executed.\n\nIf env is not None, it defines the environment variables for the new\nprocess.\n\nIf universal_newlines is true, the file objects stdout and stderr are\nopened as a text files, but lines may be terminated by any of \'\\n\',\nthe Unix end-of-line convention, \'\\r\', the Macintosh convention or\n\'\\r\\n\', the Windows convention.  All of these external representations\nare seen as \'\\n\' by the Python program.  Note: This feature is only\navailable if Python is built with universal newline support (the\ndefault).  Also, the newlines attribute of the file objects stdout,\nstdin and stderr are not updated by the communicate() method.\n\nThe startupinfo and creationflags, if given, will be passed to the\nunderlying CreateProcess() function.  They can specify things such as\nappearance of the main window and priority for the new process.\n(Windows only)\n\n\nThis module also defines two shortcut functions:\n\ncall(*args, **kwargs):\n    Run command with arguments.  Wait for command to complete, then\n    return the returncode attribute.\n\n    The arguments are the same as for the Popen constructor.  Example:\n\n    retcode = call(["ls", "-l"])\n\n\nExceptions\n----------\nExceptions raised in the child process, before the new program has\nstarted to execute, will be re-raised in the parent.  Additionally,\nthe exception object will have one extra attribute called\n\'child_traceback\', which is a string containing traceback information\nfrom the childs point of view.\n\nThe most common exception raised is OSError.  This occurs, for\nexample, when trying to execute a non-existent file.  Applications\nshould prepare for OSErrors.\n\nA ValueError will be raised if Popen is called with invalid arguments.\n\n\nSecurity\n--------\nUnlike some other popen functions, this implementation will never call\n/bin/sh implicitly.  This means that all characters, including shell\nmetacharacters, can safely be passed to child processes.\n\n\nPopen objects\n=============\nInstances of the Popen class have the following methods:\n\npoll()\n    Check if child process has terminated.  Returns returncode\n    attribute.\n\nwait()\n    Wait for child process to terminate.  Returns returncode attribute.\n\ncommunicate(input=None)\n    Interact with process: Send data to stdin.  Read data from stdout\n    and stderr, until end-of-file is reached.  Wait for process to\n    terminate.  The optional stdin argument should be a string to be\n    sent to the child process, or None, if no data should be sent to\n    the child.\n\n    communicate() returns a tuple (stdout, stderr).\n\n    Note: The data read is buffered in memory, so do not use this\n    method if the data size is large or unlimited.\n\nThe following attributes are also available:\n\nstdin\n    If the stdin argument is PIPE, this attribute is a file object\n    that provides input to the child process.  Otherwise, it is None.\n\nstdout\n    If the stdout argument is PIPE, this attribute is a file object\n    that provides output from the child process.  Otherwise, it is\n    None.\n\nstderr\n    If the stderr argument is PIPE, this attribute is file object that\n    provides error output from the child process.  Otherwise, it is\n    None.\n\npid\n    The process ID of the child process.\n\nreturncode\n    The child return code.  A None value indicates that the process\n    hasn\'t terminated yet.  A negative value -N indicates that the\n    child was terminated by signal N (UNIX only).\n\n\nReplacing older functions with the subprocess module\n====================================================\nIn this section, "a ==> b" means that b can be used as a replacement\nfor a.\n\nNote: All functions in this section fail (more or less) silently if\nthe executed program cannot be found; this module raises an OSError\nexception.\n\nIn the following examples, we assume that the subprocess module is\nimported with "from subprocess import *".\n\n\nReplacing /bin/sh shell backquote\n---------------------------------\noutput=`mycmd myarg`\n==>\noutput = Popen(["mycmd", "myarg"], stdout=PIPE).communicate()[0]\n\n\nReplacing shell pipe line\n-------------------------\noutput=`dmesg | grep hda`\n==>\np1 = Popen(["dmesg"], stdout=PIPE)\np2 = Popen(["grep", "hda"], stdin=p1.stdout)\noutput = p2.communicate()[0]\n\n\nReplacing os.system()\n---------------------\nsts = os.system("mycmd" + " myarg")\n==>\np = Popen("mycmd" + " myarg", shell=True)\nsts = os.waitpid(p.pid, 0)\n\nNote:\n\n* Calling the program through the shell is usually not required.\n\n* It\'s easier to look at the returncode attribute than the\n  exitstatus.\n\nA more real-world example would look like this:\n\ntry:\n    retcode = call("mycmd" + " myarg", shell=True)\n    if retcode < 0:\n        print("Child was terminated by signal %i" % retcode, file=sys.stderr)\n    else:\n        print("Child returned %i" % retcode, file=sys.stderr)\nexcept OSError, e:\n    print("Execution failed: %s" % str(e), file=sys.stderr)\n\n\nReplacing os.spawn*\n-------------------\nP_NOWAIT example:\n\npid = os.spawnlp(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg")\n==>\npid = Popen(["/bin/mycmd", "myarg"]).pid\n\n\nP_WAIT example:\n\nretcode = os.spawnlp(os.P_WAIT, "/bin/mycmd", "mycmd", "myarg")\n==>\nretcode = call(["/bin/mycmd", "myarg"])\n\n\nVector example:\n\nos.spawnvp(os.P_NOWAIT, path, args)\n==>\nPopen([path] + args[1:])\n\n\nEnvironment example:\n\nos.spawnlpe(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg", env)\n==>\nPopen(["/bin/mycmd", "myarg"], env={"PATH": "/usr/bin"})\n\n\nReplacing os.popen*\n-------------------\npipe = os.popen(cmd, mode=\'r\', bufsize)\n==>\npipe = Popen(cmd, shell=True, bufsize=bufsize, stdout=PIPE).stdout\n\npipe = os.popen(cmd, mode=\'w\', bufsize)\n==>\npipe = Popen(cmd, shell=True, bufsize=bufsize, stdin=PIPE).stdin\n\n\n(child_stdin, child_stdout) = os.popen2(cmd, mode, bufsize)\n==>\np = Popen(cmd, shell=True, bufsize=bufsize,\n          stdin=PIPE, stdout=PIPE, close_fds=True)\n(child_stdin, child_stdout) = (p.stdin, p.stdout)\n\n\n(child_stdin,\n child_stdout,\n child_stderr) = os.popen3(cmd, mode, bufsize)\n==>\np = Popen(cmd, shell=True, bufsize=bufsize,\n          stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)\n(child_stdin,\n child_stdout,\n child_stderr) = (p.stdin, p.stdout, p.stderr)\n\n\n(child_stdin, child_stdout_and_stderr) = os.popen4(cmd, mode, bufsize)\n==>\np = Popen(cmd, shell=True, bufsize=bufsize,\n          stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)\n(child_stdin, child_stdout_and_stderr) = (p.stdin, p.stdout)\n\n\nReplacing popen2.*\n------------------\nNote: If the cmd argument to popen2 functions is a string, the command\nis executed through /bin/sh.  If it is a list, the command is directly\nexecuted.\n\n(child_stdout, child_stdin) = popen2.popen2("somestring", bufsize, mode)\n==>\np = Popen(["somestring"], shell=True, bufsize=bufsize\n          stdin=PIPE, stdout=PIPE, close_fds=True)\n(child_stdout, child_stdin) = (p.stdout, p.stdin)\n\n\n(child_stdout, child_stdin) = popen2.popen2(["mycmd", "myarg"], bufsize, mode)\n==>\np = Popen(["mycmd", "myarg"], bufsize=bufsize,\n          stdin=PIPE, stdout=PIPE, close_fds=True)\n(child_stdout, child_stdin) = (p.stdout, p.stdin)\n\nThe popen2.Popen3 and popen3.Popen4 basically works as subprocess.Popen,\nexcept that:\n\n* subprocess.Popen raises an exception if the execution fails\n* the capturestderr argument is replaced with the stderr argument.\n* stdin=PIPE and stdout=PIPE must be specified.\n* popen2 closes all filedescriptors by default, but you have to specify\n  close_fds=True with subprocess.Popen.\n\n\n'
from __future__ import print_function
import sys
mswindows = sys.platform == 'win32'
import os, types, traceback
if mswindows:
    import threading, msvcrt
    from _subprocess import *

    class STARTUPINFO():
        dwFlags = 0
        hStdInput = None
        hStdOutput = None
        hStdError = None


    class pywintypes():
        error = IOError


else:
    import select, errno, fcntl, pickle
__all__ = [
 'Popen', 'PIPE', 'STDOUT', 'call', 'ProcessError']
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


class ProcessError(Exception):
    """This exception is raised when there is an error calling
    a subprocess."""


class Popen(object):

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
        p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite = self._get_handles(stdin, stdout, stderr)
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
            if stdin is None and stdout is None and stderr is None:
                return (None, None, None, None, None, None)
            else:
                p2cread, p2cwrite = (None, None)
                c2pread, c2pwrite = (None, None)
                errread, errwrite = (None, None)
                if stdin is None:
                    p2cread = GetStdHandle(STD_INPUT_HANDLE)
                elif stdin == PIPE:
                    p2cread, p2cwrite = CreatePipe(None, 0)
                    p2cwrite = p2cwrite.Detach()
                    p2cwrite = msvcrt.open_osfhandle(p2cwrite, 0)
                elif type(stdin) == types.IntType:
                    p2cread = msvcrt.get_osfhandle(stdin)
                else:
                    p2cread = msvcrt.get_osfhandle(stdin.fileno())
                p2cread = self._make_inheritable(p2cread)
                if stdout is None:
                    c2pwrite = GetStdHandle(STD_OUTPUT_HANDLE)
                elif stdout == PIPE:
                    c2pread, c2pwrite = CreatePipe(None, 0)
                    c2pread = c2pread.Detach()
                    c2pread = msvcrt.open_osfhandle(c2pread, 0)
                elif type(stdout) == types.IntType:
                    c2pwrite = msvcrt.get_osfhandle(stdout)
                else:
                    c2pwrite = msvcrt.get_osfhandle(stdout.fileno())
                c2pwrite = self._make_inheritable(c2pwrite)
                if stderr is None:
                    errwrite = GetStdHandle(STD_ERROR_HANDLE)
                elif stderr == PIPE:
                    errread, errwrite = CreatePipe(None, 0)
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
                 p2cread, p2cwrite,
                 c2pread, c2pwrite,
                 errread, errwrite)

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
            default_startupinfo = STARTUPINFO()
            if startupinfo is None:
                startupinfo = default_startupinfo
            if None not in (p2cread, c2pwrite, errwrite):
                startupinfo.dwFlags |= STARTF_USESTDHANDLES
                startupinfo.hStdInput = p2cread
                startupinfo.hStdOutput = c2pwrite
                startupinfo.hStdError = errwrite
            if shell:
                default_startupinfo.dwFlags |= STARTF_USESHOWWINDOW
                default_startupinfo.wShowWindow = SW_HIDE
                comspec = os.environ.get('COMSPEC', 'cmd.exe')
                args = comspec + ' /c ' + args
                if GetVersion() >= 2147483648 or os.path.basename(comspec).lower() == 'command.com':
                    w9xpopen = self._find_w9xpopen()
                    args = '"%s" %s' % (w9xpopen, args)
                    creationflags |= CREATE_NEW_CONSOLE
            try:
                hp, ht, pid, tid = CreateProcess(executable, args, None, None, 1, creationflags, env, cwd, startupinfo)
            except pywintypes.error as e:
                raise WindowsError(*e.args)

            self._handle = hp
            self.pid = pid
            ht.Close()
            if p2cread is not None:
                p2cread.Close()
            if c2pwrite is not None:
                c2pwrite.Close()
            if errwrite is not None:
                errwrite.Close()
            return

        def poll(self):
            """Check if child process has terminated.  Returns returncode
            attribute."""
            if self.returncode is None:
                if WaitForSingleObject(self._handle, 0) == WAIT_OBJECT_0:
                    self.returncode = GetExitCodeProcess(self._handle)
                    _active.remove(self)
            return self.returncode

        def wait(self):
            """Wait for child process to terminate.  Returns returncode
            attribute."""
            if self.returncode is None:
                obj = WaitForSingleObject(self._handle, INFINITE)
                self.returncode = GetExitCodeProcess(self._handle)
                _active.remove(self)
            return self.returncode

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
                stdout_thread = threading.Thread(target=self._readerthread, args=(
                 self.stdout, stdout))
                stdout_thread.setDaemon(True)
                stdout_thread.start()
            if self.stderr:
                stderr = []
                stderr_thread = threading.Thread(target=self._readerthread, args=(
                 self.stderr, stderr))
                stderr_thread.setDaemon(True)
                stderr_thread.start()
            if self.stdin:
                if input is not None:
                    self.stdin.write(input)
                self.stdin.close()
            if self.stdout:
                stdout_thread.join()
            if self.stderr:
                stderr_thread.join()
            if stdout is not None:
                stdout = stdout[0]
            if stderr is not None:
                stderr = stderr[0]
            if self.universal_newlines and hasattr(open, 'newlines'):
                if stdout:
                    stdout = self._translate_newlines(stdout)
                if stderr:
                    stderr = self._translate_newlines(stderr)
            self.wait()
            return (
             stdout, stderr)

    else:

        def _get_handles(self, stdin, stdout, stderr):
            """Construct and return tupel with IO objects:
            p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite
            """
            p2cread, p2cwrite = (None, None)
            c2pread, c2pwrite = (None, None)
            errread, errwrite = (None, None)
            if stdin is None:
                pass
            elif stdin == PIPE:
                p2cread, p2cwrite = os.pipe()
            elif type(stdin) == types.IntType:
                p2cread = stdin
            else:
                p2cread = stdin.fileno()
            if stdout is None:
                pass
            elif stdout == PIPE:
                c2pread, c2pwrite = os.pipe()
            elif type(stdout) == types.IntType:
                c2pwrite = stdout
            else:
                c2pwrite = stdout.fileno()
            if stderr is None:
                pass
            elif stderr == PIPE:
                errread, errwrite = os.pipe()
            elif stderr == STDOUT:
                errwrite = c2pwrite
            elif type(stderr) == types.IntType:
                errwrite = stderr
            else:
                errwrite = stderr.fileno()
            return (
             p2cread, p2cwrite,
             c2pread, c2pwrite,
             errread, errwrite)

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
            if executable is None:
                executable = args[0]
            errpipe_read, errpipe_write = os.pipe()
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
                    if cwd is not None:
                        os.chdir(cwd)
                    if preexec_fn:
                        apply(preexec_fn)
                    if env is None:
                        os.execvp(executable, args)
                    else:
                        os.execvpe(executable, args, env)
                except:
                    exc_type, exc_value, tb = sys.exc_info()
                    exc_lines = traceback.format_exception(exc_type, exc_value, tb)
                    exc_value.child_traceback = ('').join(exc_lines)
                    os.write(errpipe_write, pickle.dumps(exc_value))

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
                raise ProcessError, child_exception
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
            if self.returncode is None:
                try:
                    pid, sts = os.waitpid(self.pid, os.WNOHANG)
                    if pid == self.pid:
                        self._handle_exitstatus(sts)
                except os.error:
                    pass

            return self.returncode

        def wait(self):
            """Wait for child process to terminate.  Returns returncode
            attribute."""
            if self.returncode is None:
                pid, sts = os.waitpid(self.pid, 0)
                self._handle_exitstatus(sts)
            return self.returncode

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
                rlist, wlist, xlist = select.select(read_set, write_set, [])
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

            if stdout is not None:
                stdout = ('').join(stdout)
            if stderr is not None:
                stderr = ('').join(stderr)
            if self.universal_newlines and hasattr(open, 'newlines'):
                if stdout:
                    stdout = self._translate_newlines(stdout)
                if stderr:
                    stderr = self._translate_newlines(stderr)
            self.wait()
            return (
             stdout, stderr)


def _demo_posix():
    plist = Popen(['ps'], stdout=PIPE).communicate()[0]
    print('Process list:')
    print(plist)
    if os.getuid() == 0:
        p = Popen(['id'], preexec_fn=lambda : os.setuid(100))
        p.wait()
    print("Looking for 'hda'...")
    p1 = Popen(['dmesg'], stdout=PIPE)
    p2 = Popen(['grep', 'hda'], stdin=p1.stdout, stdout=PIPE)
    print(repr(p2.communicate()[0]))
    print('')
    print('Trying a weird file...')
    try:
        print(Popen(['/this/path/does/not/exist']).communicate())
    except OSError as e:
        if e.errno == errno.ENOENT:
            print("The file didn't exist.  I thought so...")
            print('Child traceback:')
            print(e.child_traceback)
        else:
            print('Error', e.errno)
    else:
        print('Gosh.  No error.', file=sys.stderr)


def _demo_windows():
    print("Looking for 'PROMPT' in set output...")
    p1 = Popen('set', stdout=PIPE, shell=True)
    p2 = Popen('find "PROMPT"', stdin=p1.stdout, stdout=PIPE)
    print(repr(p2.communicate()[0]))
    print('Executing calc...')
    p = Popen('calc')
    p.wait()


if __name__ == '__main__':
    if mswindows:
        _demo_windows()
    else:
        _demo_posix()