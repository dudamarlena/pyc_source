# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/process.py
# Compiled at: 2019-10-17 02:30:59
# Size of source mod 2**32: 101266 bytes
""" Contents of LICENSE.txt:
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import os, sys, threading, types, pprint, noval.util.utils as utils, noval.util.compat as compat, six
if sys.platform.startswith('win'):
    import msvcrt, win32api, win32file, win32pipe, pywintypes, win32process, win32event
    VER_PLATFORM_WIN32_WINDOWS = 1
    CTRL_BREAK_EVENT = 1
    SW_SHOWDEFAULT = 10
    WM_CLOSE = 16
    DUPLICATE_SAME_ACCESS = 2
else:
    import signal

class ProcessError(Exception):

    def __init__(self, msg, errno=-1):
        Exception.__init__(self, msg)
        self.errno = errno


class Logger:
    DEBUG, INFO, WARN, ERROR, FATAL = range(5)

    def __init__(self, name, level=None, streamOrFileName=sys.stderr):
        self.name = name
        if level is None:
            self.level = self.WARN
        else:
            self.level = level
        if type(streamOrFileName) == str:
            self.stream = open(streamOrFileName, 'w')
            self._opennedStream = 1
        else:
            self.stream = streamOrFileName
            self._opennedStream = 0

    def __del__(self):
        if self._opennedStream:
            self.stream.close()

    def _getLevelName(self, level):
        levelNameMap = {self.DEBUG: 'DEBUG', 
         self.INFO: 'INFO', 
         self.WARN: 'WARN', 
         self.ERROR: 'ERROR', 
         self.FATAL: 'FATAL'}
        return levelNameMap[level]

    def log(self, level, msg, *args):
        if level < self.level:
            return
        message = '%s: %s:' % (self.name, self._getLevelName(level).lower())
        message = message + msg % args + '\n'
        self.stream.write(message)
        self.stream.flush()

    def debug(self, msg, *args):
        self.log(self.DEBUG, msg, *args)

    def info(self, msg, *args):
        self.log(self.INFO, msg, *args)

    def warn(self, msg, *args):
        self.log(self.WARN, msg, *args)

    def error(self, msg, *args):
        self.log(self.ERROR, msg, *args)

    def fatal(self, msg, *args):
        self.log(self.FATAL, msg, *args)


log = Logger('process', Logger.WARN)
logres = Logger('process.res', Logger.WARN)
logfix = Logger('process.waitfix', Logger.WARN)
_version_ = (
 0, 5, 0)
_processes = []

def _escapeArg(arg):
    """Escape the given command line argument for the shell."""
    return arg.replace('"', '\\"')


def _joinArgv(argv):
    r"""Join an arglist to a string appropriate for running.

        >>> import os
        >>> _joinArgv(['foo', 'bar "baz'])
        'foo "bar \\"baz"'
    """
    cmdstr = ''
    for arg in argv:
        if ' ' in arg or ';' in arg:
            cmdstr += '"%s"' % _escapeArg(arg)
        else:
            cmdstr += _escapeArg(arg)
        cmdstr += ' '

    if cmdstr.endswith(' '):
        cmdstr = cmdstr[:-1]
    return cmdstr


def _getPathFromEnv(env):
    """Return the PATH environment variable or None.

    Do the right thing for case sensitivity per platform.
    XXX Icky. This guarantee of proper case sensitivity of environment
        variables should be done more fundamentally in this module.
    """
    if sys.platform.startswith('win'):
        for key in env.keys():
            if key.upper() == 'PATH':
                return env[key]
        else:
            return

    else:
        if env.has_key('PATH'):
            return env['PATH']
        else:
            return


def _whichFirstArg(cmd, env=None):
    """Return the given command ensuring that the first arg (the command to
    launch) is a full path to an existing file.

    Raise a ProcessError if no such executable could be found.
    """
    if cmd.startswith('"'):
        idx = cmd.replace('\\"', 'XX').find('"', 1)
        if idx == -1:
            raise ProcessError('Malformed command: %r' % cmd)
        first, rest = cmd[1:idx], cmd[idx + 1:]
        rest = rest.lstrip()
    else:
        if ' ' in cmd:
            first, rest = cmd.split(' ', 1)
        else:
            first, rest = cmd, ''
        import noval.util.which as which
        if os.sep in first:
            altpath = [
             os.path.dirname(first)]
            firstbase = os.path.basename(first)
            candidates = [which.which(firstbase, path=altpath)]
        else:
            if env:
                altpath = _getPathFromEnv(env)
                if altpath:
                    candidates = [
                     which.which(first, altpath.split(os.pathsep))]
                else:
                    candidates = [
                     which.which(first)]
            else:
                candidates = [
                 which.which(first)]
        if candidates:
            return _joinArgv([candidates[0]]) + ' ' + rest
    raise ProcessError('Could not find an appropriate leading command for: %r' % cmd)


if sys.platform.startswith('win'):

    def _SaferCreateProcess(appName, cmd, processSA, threadSA, inheritHandles, creationFlags, env, cwd, si):
        """If CreateProcess fails from environment type inconsistency then
        fix that and try again.
        
        win32process.CreateProcess requires that all environment keys and
        values either be all ASCII or all unicode. Try to remove this burden
        from the user of process.py.
        """
        isWin9x = win32api.GetVersionEx()[3] == VER_PLATFORM_WIN32_WINDOWS
        if isWin9x and env:
            aenv = {}
            for key, value in env.items():
                aenv[str(key)] = str(value)

            env = aenv
        log.debug('_SaferCreateProcess(appName=%r,\n                    cmd=%r,\n                    env=%r,\n                    cwd=%r)\n    os.getcwd(): %r\n', appName, cmd, env, cwd, os.getcwd())
        try:
            hProcess, hThread, processId, threadId = win32process.CreateProcess(appName, cmd, processSA, threadSA, inheritHandles, creationFlags, env, cwd, si)
        except TypeError as ex:
            if ex.args == ('All dictionary items must be strings, or all must be unicode', ):
                if isWin9x and env:
                    aenv = {}
                    try:
                        for key, value in env.items():
                            aenv[str(key)] = str(value)

                    except UnicodeError as ex:
                        raise ProcessError(str(ex))

                    env = aenv
                elif env:
                    uenv = {}
                    for key, val in env.items():
                        try:
                            uenv[str(key)] = str(val)
                        except UnicodeError:
                            try:
                                uenv[unicode(key, 'iso-8859-1')] = unicode(val, 'iso-8859-1')
                            except UnicodeError:
                                log.warn('Skipping environment variable "%s" in execution process: unable to convert to unicode using either the default encoding or ISO-8859-1' % key)

                    env = uenv
                hProcess, hThread, processId, threadId = win32process.CreateProcess(appName, cmd, processSA, threadSA, inheritHandles, creationFlags, env, cwd, si)
            else:
                raise

        return (
         hProcess, hThread, processId, threadId)


def _registerProcess(process):
    global _processes
    log.info('_registerprocess(process=%r)', process)
    for p in _processes[:]:
        try:
            if sys.platform.startswith('win'):
                timeout = 0
            else:
                timeout = os.WNOHANG
            p.wait(timeout)
            _unregisterProcess(p)
        except ProcessError as ex:
            if ex.errno == ProcessProxy.WAIT_TIMEOUT:
                pass
            else:
                raise

    _processes.append(process)


def _unregisterProcess(process):
    log.info('_unregisterProcess(process=%r)', process)
    try:
        _processes.remove(process)
        del process
    except ValueError:
        pass


def _fixupCommand(cmd, env=None):
    r"""Fixup the command string so it is launchable via CreateProcess.

    One cannot just launch, say "python", via CreateProcess. A full path
    to an executable is required. In general there are two choices:
        1. Launch the command string via the shell. The shell will find
           the fullpath to the appropriate executable. This shell will
           also be able to execute special shell commands, like "dir",
           which don't map to an actual executable.
        2. Find the fullpath to the appropriate executable manually and
           launch that exe.

    Option (1) is preferred because you don't have to worry about not
    exactly duplicating shell behaviour and you get the added bonus of
    being able to launch "dir" and friends.

    However, (1) is not always an option. Doing so when the shell is
    command.com (as on all Win9x boxes) or when using WinNT's cmd.exe,
    problems are created with .kill() because these shells seem to eat
    up Ctrl-C's and Ctrl-Break's sent via
    win32api.GenerateConsoleCtrlEvent().  Strangely this only happens
    when spawn via this Python interface. For example, Ctrl-C get
    through to hang.exe here:
      C:\> ...\w9xpopen.exe "C:\WINDOWS\COMMAND.COM /c hang.exe"
      ^C
    but not here:
      >>> p = ProcessOpen('hang.exe')
      # This results in the same command to CreateProcess as
      # above.
      >>> p.kill()

    Hence, for these platforms we fallback to option (2).  Cons:
      - cannot spawn shell commands like 'dir' directly
      - cannot spawn batch files
    """
    if sys.platform.startswith('win'):
        comspec = os.environ.get('COMSPEC', None)
        win32Version = win32api.GetVersion()
        if comspec is None:
            raise ProcessError('Cannot locate a COMSPEC environment variable to use as the shell')
        if utils.is_py2():
            win32_8_ver = long(2147483648)
        else:
            if utils.is_py3_plus():
                win32_8_ver = 2147483648
            else:
                if win32Version & win32_8_ver == 0 and win32Version & 5 >= 5 and os.path.basename(comspec).lower() != 'command.com':
                    if '"' in cmd or "'" in cmd:
                        cmd = comspec + ' /c "%s"' % cmd
                    else:
                        cmd = comspec + ' /c ' + cmd
                else:
                    if win32Version & win32_8_ver == 0 and win32Version & 5 < 5 and os.path.basename(comspec).lower() != 'command.com':
                        try:
                            cmd = _whichFirstArg(cmd, env)
                        except ProcessError:
                            raise ProcessError("Could not find a suitable executable to launch for '%s'. On WinNT you must manually prefix shell commands and batch files with 'cmd.exe /c' to have the shell run them." % cmd)

                    else:
                        w9xpopen = os.path.join(os.path.dirname(win32api.GetModuleFileName(0)), 'w9xpopen.exe')
                        if not os.path.exists(w9xpopen):
                            w9xpopen = os.path.join(os.path.dirname(sys.exec_prefix), 'w9xpopen.exe')
                            if not os.path.exists(w9xpopen):
                                raise ProcessError("Can not locate 'w9xpopen.exe' which is needed for ProcessOpen to work with your shell or platform.")
                            try:
                                cmd = _whichFirstArg(cmd, env)
                            except ProcessError:
                                raise ProcessError("Could not find a suitable executable to launch for '%s'. On Win9x you must manually prefix shell commands and batch files with 'command.com /c' to have the shell run them." % cmd)

                            cmd = '%s "%s"' % (w9xpopen, cmd.replace('"', '\\"'))
        return cmd


class _FileWrapper:
    __doc__ = 'Wrap a system file object, hiding some nitpicky details.\n    \n    This class provides a Python file-like interface to either a Python\n    file object (pretty easy job), a file descriptor, or an OS-specific\n    file handle (e.g.  Win32 handles to file objects on Windows). Any or\n    all of these object types may be passed to this wrapper. If more\n    than one is specified this wrapper prefers to work with certain one\n    in this order:\n        - file descriptor (because usually this allows for\n          return-immediately-on-read-if-anything-available semantics and\n          also provides text mode translation on Windows)\n        - OS-specific handle (allows for the above read semantics)\n        - file object (buffering can cause difficulty for interacting\n          with spawned programs)\n\n    It also provides a place where related such objects can be kept\n    alive together to prevent premature ref-counted collection. (E.g. on\n    Windows a Python file object may be associated with a Win32 file\n    handle. If the file handle is not kept alive the Python file object\n    will cease to function.)\n    '

    def __init__(self, file=None, descriptor=None, handle=None):
        self._file = file
        self._descriptor = descriptor
        self._handle = handle
        self._closed = 0
        if self._descriptor is not None or self._handle is not None:
            self._lineBuf = ''

    def __del__(self):
        self.close()

    def __getattr__(self, name):
        """Forward to the underlying file object."""
        if self._file is not None:
            return getattr(self._file, name)
        raise ProcessError("no file object to pass '%s' attribute to" % name)

    def _win32Read(self, nBytes):
        try:
            log.info('[%s] _FileWrapper.read: waiting for read on pipe', id(self))
            errCode, text = win32file.ReadFile(self._handle, nBytes)
        except pywintypes.error as ex:
            log.info('[%s] _FileWrapper.read: error reading from pipe: %s', id(self), ex)
            return ''

        assert errCode == 0, "Why is 'errCode' from ReadFile non-zero? %r" % errCode
        if not text:
            log.info('[%s] _FileWrapper.read: observed close of parent', id(self))
            self.close()
            return ''
        log.info('[%s] _FileWrapper.read: read %d bytes from pipe: %r', id(self), len(text), text)
        return text

    def read(self, nBytes=-1):
        if self._descriptor is not None:
            if nBytes <= 0:
                text, self._lineBuf = self._lineBuf, ''
                while True:
                    t = os.read(self._descriptor, 4092)
                    if not t:
                        break
                    else:
                        text += t

            else:
                if len(self._lineBuf) >= nBytes:
                    text, self._lineBuf = self._lineBuf[:nBytes], self._lineBuf[nBytes:]
                else:
                    self._lineBuf = os.read(self._descriptor, nBytes)
                if utils.is_py3_plus():
                    try:
                        self._lineBuf = compat.ensure_string(self._lineBuf)
                    except:
                        self._lineBuf = compat.ensure_string(self._lineBuf, encoding=utils.get_default_encoding())

                    return self._lineBuf
            if self._handle is not None:
                if nBytes <= 0:
                    text, self._lineBuf = self._lineBuf, ''
                    while True:
                        t = self._win32Read(4092)
                        if not t:
                            break
                        else:
                            text += t

                else:
                    if len(self._lineBuf) >= nBytes:
                        text, self._lineBuf = self._lineBuf[:nBytes], self._lineBuf[nBytes:]
                    else:
                        nBytesToGo = nBytes - len(self._lineBuf)
                        text, self._lineBuf = self._lineBuf + self._win32Read(nBytesToGo), ''
                    return text
                if self._file is not None:
                    return self._file.read(nBytes)
                raise RuntimeError('FileHandle.read: no handle to read with')

    def readline(self):
        if self._descriptor is not None or self._handle is not None:
            while 1:
                idx = self._lineBuf.find('\n')
                if idx != -1:
                    line, self._lineBuf = self._lineBuf[:idx + 1], self._lineBuf[idx + 1:]
                    break
                else:
                    lengthBefore = len(self._lineBuf)
                    if lengthBefore > 0:
                        line, self._lineBuf = self._lineBuf, ''
                        break
                    t = self.read(4092)
                    if 0 == len(t):
                        line = t
                        assert 0 == len(self._lineBuf)
                        break

            return line
        if self._file is not None:
            return self._file.readline()
        raise RuntimeError('FileHandle.readline: no handle to read with')

    def readline2(self):
        if self._descriptor is not None or self._handle is not None:
            while True:
                idx = self._lineBuf.find('\n')
                if idx != -1:
                    line, self._lineBuf = self._lineBuf[:idx + 1], self._lineBuf[idx + 1:]
                    break
                else:
                    lengthBefore = len(self._lineBuf)
                    t = self.read(4092)
                    if len(t) <= lengthBefore:
                        line, self._lineBuf = t, ''
                        break
                    else:
                        self._lineBuf += t

            return line
        if self._file is not None:
            return self._file.readline()
        raise RuntimeError('FileHandle.readline: no handle to read with')

    def readlines(self):
        if self._descriptor is not None or self._handle is not None:
            lines = []
            while True:
                line = self.readline()
                if line:
                    lines.append(line)
                else:
                    break

            return lines
        if self._file is not None:
            return self._file.readlines()
        raise RuntimeError('FileHandle.readline: no handle to read with')

    def write(self, text):
        if self._descriptor is not None:
            if utils.is_py3_plus():
                text = compat.ensure_bytes(text)
            os.write(self._descriptor, text)
        else:
            if self._handle is not None:
                try:
                    errCode, nBytesWritten = win32file.WriteFile(self._handle, text)
                except pywintypes.error as ex:
                    log.info('[%s] _FileWrapper.write: error writing to pipe, ignored', id(self))
                    return

                assert errCode == 0, "Why is 'errCode' from WriteFile non-zero? %r" % errCode
                if not nBytesWritten:
                    log.info('[%s] _FileWrapper.write: observed close of pipe', id(self))
                    return
                log.info('[%s] _FileWrapper.write: wrote %d bytes to pipe: %r', id(self), len(text), text)
            else:
                if self._file is not None:
                    self._file.write(text)
                else:
                    raise RuntimeError('FileHandle.write: nothing to write with')

    def close(self):
        """Close all associated file objects and handles."""
        log.debug('[%s] _FileWrapper.close()', id(self))
        if not self._closed:
            self._closed = 1
            if self._file is not None:
                log.debug('[%s] _FileWrapper.close: close file', id(self))
                self._file.close()
                log.debug('[%s] _FileWrapper.close: done file close', id(self))
            if self._descriptor is not None:
                try:
                    os.close(self._descriptor)
                except OSError as ex:
                    if ex.errno == 9:
                        log.debug('[%s] _FileWrapper.close: closing descriptor raised OSError', id(self))
                    else:
                        raise

            if self._handle is not None:
                log.debug('[%s] _FileWrapper.close: close handle', id(self))
                try:
                    win32api.CloseHandle(self._handle)
                except win32api.error:
                    log.debug('[%s] _FileWrapper.close: closing handle raised', id(self))

                log.debug('[%s] _FileWrapper.close: done closing handle', id(self))

    def __repr__(self):
        return '<_FileWrapper: file:%r fd:%r os_handle:%r>' % (
         self._file, self._descriptor, self._handle)


class _CountingCloser:
    __doc__ = 'Call .close() on the given object after own .close() is called\n    the precribed number of times.\n    '

    def __init__(self, objectsToClose, count):
        """
        "objectsToClose" is a list of object on which to call .close().
        "count" is the number of times this object's .close() method
            must be called before .close() is called on the given objects.
        """
        self.objectsToClose = objectsToClose
        self.count = count
        if self.count <= 0:
            raise ProcessError("illegal 'count' value: %s" % self.count)

    def close(self):
        self.count -= 1
        log.debug('[%d] _CountingCloser.close(): count=%d', id(self), self.count)
        if self.count == 0:
            for objectToClose in self.objectsToClose:
                objectToClose.close()


class Process:
    __doc__ = "Create a process.\n\n    One can optionally specify the starting working directory, the\n    process environment, and std handles to have the child process\n    inherit (all defaults are the parent's current settings). 'wait' and\n    'kill' method allow for control of the child's termination.\n    "
    if sys.platform.startswith('win'):
        INFINITE = win32event.INFINITE
        WAIT_FAILED = win32event.WAIT_FAILED
        WAIT_TIMEOUT = win32event.WAIT_TIMEOUT
        CREATE_NEW_CONSOLE = win32process.CREATE_NEW_CONSOLE
    else:
        INFINITE = 0
        WAIT_TIMEOUT = 258
        WAIT_FAILED = -1
        CREATE_NEW_CONSOLE = 16

    def __init__(self, cmd, cwd=None, env=None, flags=0):
        """Create a child process.

        "cmd" is a command string or argument vector to spawn.
        "cwd" is a working directory in which to start the child process.
        "env" is an environment dictionary for the child.
        "flags" are system-specific process creation flags. On Windows
            this can be a bitwise-OR of any of the win32process.CREATE_*
            constants (Note: win32process.CREATE_NEW_PROCESS_GROUP is always
            OR'd in). On Unix, this is currently ignored.
        """
        log.info('Process.__init__(cmd=%r, cwd=%r, env=%r, flags=%r)', cmd, cwd, env, flags)
        self._cmd = cmd
        if not self._cmd:
            raise ProcessError('You must specify a command.')
        self._cwd = cwd
        self._env = env
        self._flags = flags
        if sys.platform.startswith('win'):
            self._flags |= win32process.CREATE_NEW_PROCESS_GROUP
        if sys.platform.startswith('win'):
            self._startOnWindows()
        else:
            self._Process__retvalCache = None
            self._startOnUnix()

    def _runChildOnUnix(self):
        if isinstance(self._cmd, six.string_types[0]):
            cmd = [
             '/bin/sh', '-c', self._cmd]
        else:
            cmd = self._cmd
        MAXFD = 256
        for i in range(3, MAXFD):
            try:
                os.close(i)
            except OSError:
                pass

        try:
            if self._env:
                os.execvpe(cmd[0], cmd, self._env)
            else:
                os.execvp(cmd[0], cmd)
        finally:
            os._exit(1)

    def _forkAndExecChildOnUnix(self):
        """Fork and start the child process.

        Sets self._pid as a side effect.
        """
        pid = os.fork()
        if pid == 0:
            self._runChildOnUnix()
        self._pid = pid

    def _startOnUnix(self):
        if self._cwd:
            oldDir = os.getcwd()
            try:
                os.chdir(self._cwd)
            except OSError as ex:
                raise ProcessError(msg=str(ex), errno=ex.errno)

            self._forkAndExecChildOnUnix()
            if self._cwd:
                os.chdir(oldDir)

    def _startOnWindows(self):
        if type(self._cmd) in (types.ListType, types.TupleType):
            cmd = _joinArgv(self._cmd)
        else:
            cmd = self._cmd
        si = win32process.STARTUPINFO()
        si.dwFlags = win32process.STARTF_USESHOWWINDOW
        si.wShowWindow = SW_SHOWDEFAULT
        if not self._flags & self.CREATE_NEW_CONSOLE:
            try:
                cmd = _whichFirstArg(cmd, self._env)
            except ProcessError:
                cmd = _fixupCommand(cmd, self._env)

        else:
            cmd = _fixupCommand(cmd, self._env)
        log.debug('cmd = %r', cmd)
        try:
            self._hProcess, self._hThread, self._processId, self._threadId = _SaferCreateProcess(None, cmd, None, None, 0, self._flags, self._env, self._cwd, si)
            win32api.CloseHandle(self._hThread)
        except win32api.error as ex:
            raise ProcessError(msg="Error creating process for '%s': %s" % (
             cmd, ex.args[2]), errno=ex.args[0])

    def wait(self, timeout=None):
        """Wait for the started process to complete.
        
        "timeout" (on Windows) is a floating point number of seconds after
            which to timeout.  Default is win32event.INFINITE.
        "timeout" (on Unix) is akin to the os.waitpid() "options" argument
            (os.WNOHANG may be used to return immediately if the process has
            not exited). Default is 0, i.e. wait forever.

        If the wait time's out it will raise a ProcessError. Otherwise it
        will return the child's exit value (on Windows) or the child's exit
        status excoded as per os.waitpid() (on Linux):
            "a 16-bit number, whose low byte is the signal number that killed
            the process, and whose high byte is the exit status (if the
            signal number is zero); the high bit of the low byte is set if a
            core file was produced."
        In the latter case, use the os.W*() methods to interpret the return
        value.
        """
        if sys.platform.startswith('win'):
            if timeout is None:
                timeout = win32event.INFINITE
            else:
                timeout = timeout * 1000.0
            rc = win32event.WaitForSingleObject(self._hProcess, timeout)
            if rc == win32event.WAIT_FAILED:
                raise ProcessError("'WAIT_FAILED' when waiting for process to terminate: %r" % self._cmd, rc)
            elif rc == win32event.WAIT_TIMEOUT:
                raise ProcessError("'WAIT_TIMEOUT' when waiting for process to terminate: %r" % self._cmd, rc)
            retval = win32process.GetExitCodeProcess(self._hProcess)
        else:
            if self._Process__retvalCache is not None:
                retval = self._Process__retvalCache
            else:
                if timeout is None:
                    timeout = 0
                pid, sts = os.waitpid(self._pid, timeout)
                if pid == self._pid:
                    self._Process__retvalCache = retval = sts
                else:
                    raise ProcessError('Wait for process timed out.', self.WAIT_TIMEOUT)
        return retval

    def kill(self, exitCode=0, gracePeriod=1.0, sig=None):
        """Kill process.
        
        "exitCode" [deprecated, not supported] (Windows only) is the
            code the terminated process should exit with.
        "gracePeriod" (Windows only) is a number of seconds the process is
            allowed to shutdown with a WM_CLOSE signal before a hard
            terminate is called.
        "sig" (Unix only) is the signal to use to kill the process. Defaults
            to signal.SIGKILL. See os.kill() for more information.

        Windows:
            Try for an orderly shutdown via WM_CLOSE.  If still running
            after gracePeriod (1 sec. default), terminate.
        """
        if sys.platform.startswith('win'):
            import win32gui
            win32gui.EnumWindows(self._close_, 0)
            try:
                win32api.GenerateConsoleCtrlEvent(CTRL_BREAK_EVENT, self._processId)
            except AttributeError:
                log.warn('The win32api module does not have GenerateConsoleCtrlEvent(). This may mean that parts of this process group have NOT been killed.')
            except win32api.error as ex:
                if ex.args[0] not in (6, 87):
                    raise

            retval = 0
            try:
                self.wait(gracePeriod)
            except ProcessError as ex:
                log.info('[%s] Process.kill: calling TerminateProcess', id(self))
                win32process.TerminateProcess(self._hProcess, -1)
                win32api.Sleep(100)

        if sig is None:
            sig = signal.SIGKILL
        try:
            os.kill(self._pid, sig)
        except OSError as ex:
            if ex.errno != 3:
                raise

    def _close_(self, hwnd, dummy):
        """Callback used by .kill() on Windows.

        EnumWindows callback - sends WM_CLOSE to any window owned by this
        process.
        """
        threadId, processId = win32process.GetWindowThreadProcessId(hwnd)
        if processId == self._processId:
            import win32gui
            win32gui.PostMessage(hwnd, WM_CLOSE, 0, 0)


class ProcessOpen(Process):
    __doc__ = 'Create a process and setup pipes to it standard handles.\n\n    This is a super popen3.\n    '

    def __init__(self, cmd, mode='t', cwd=None, env=None):
        """Create a Process with proxy threads for each std handle.

        "cmd" is the command string or argument vector to run.
        "mode" (Windows only) specifies whether the pipes used to communicate
            with the child are openned in text, 't', or binary, 'b', mode.
            This is ignored on platforms other than Windows. Default is 't'.
        "cwd" optionally specifies the directory in which the child process
            should be started. Default is None, a.k.a. inherits the cwd from
            the parent.
        "env" is optionally a mapping specifying the environment in which to
            start the child. Default is None, a.k.a. inherits the environment
            of the parent.
        """
        self._ProcessOpen__log = log
        log.info('ProcessOpen.__init__(cmd=%r, mode=%r, cwd=%r, env=%r)', cmd, mode, cwd, env)
        self._cmd = cmd
        if not self._cmd:
            raise ProcessError('You must specify a command.')
        self._cwd = cwd
        self._env = env
        self._mode = mode
        if self._mode not in ('t', 'b'):
            raise ProcessError("'mode' must be 't' or 'b'.")
        self._closed = 0
        if sys.platform.startswith('win'):
            self._startOnWindows()
        else:
            self._ProcessOpen__retvalCache = None
            self._startOnUnix()
        _registerProcess(self)

    def __del__(self):
        logres.info('[%s] ProcessOpen.__del__()', id(self))
        self.close()
        del self._ProcessOpen__log

    def close(self):
        if not self._closed:
            self._ProcessOpen__log.info('[%s] ProcessOpen.close()' % id(self))
            try:
                self._ProcessOpen__log.info('[%s] ProcessOpen: closing stdin (%r).' % (
                 id(self), self.stdin))
                self.stdin.close()
            except AttributeError:
                pass

            try:
                self._ProcessOpen__log.info('[%s] ProcessOpen: closing stdout (%r).' % (
                 id(self), self.stdout))
                self.stdout.close()
            except AttributeError:
                pass

            try:
                self._ProcessOpen__log.info('[%s] ProcessOpen: closing stderr (%r).' % (
                 id(self), self.stderr))
                self.stderr.close()
            except AttributeError:
                pass

            self._closed = 1

    def _forkAndExecChildOnUnix(self, fdChildStdinRd, fdChildStdoutWr, fdChildStderrWr):
        """Fork and start the child process.

        Sets self._pid as a side effect.
        """
        pid = os.fork()
        if pid == 0:
            os.dup2(fdChildStdinRd, 0)
            os.dup2(fdChildStdoutWr, 1)
            os.dup2(fdChildStderrWr, 2)
            self._runChildOnUnix()
        self._pid = pid

    def _startOnUnix(self):
        fdChildStdinRd, fdChildStdinWr = os.pipe()
        fdChildStdoutRd, fdChildStdoutWr = os.pipe()
        fdChildStderrRd, fdChildStderrWr = os.pipe()
        if self._cwd:
            oldDir = None
            try:
                oldDir = os.getcwd()
                os.chdir(self._cwd)
            except OSError as ex:
                print('getcwd or chdir error,warning....', ex)

        self._forkAndExecChildOnUnix(fdChildStdinRd, fdChildStdoutWr, fdChildStderrWr)
        if self._cwd and oldDir:
            os.chdir(oldDir)
        os.close(fdChildStdinRd)
        os.close(fdChildStdoutWr)
        os.close(fdChildStderrWr)
        self.stdin = _FileWrapper(descriptor=fdChildStdinWr)
        logres.info('[%s] ProcessOpen._start(): create child stdin: %r', id(self), self.stdin)
        self.stdout = _FileWrapper(descriptor=fdChildStdoutRd)
        logres.info('[%s] ProcessOpen._start(): create child stdout: %r', id(self), self.stdout)
        self.stderr = _FileWrapper(descriptor=fdChildStderrRd)
        logres.info('[%s] ProcessOpen._start(): create child stderr: %r', id(self), self.stderr)

    def _startOnWindows(self):
        if type(self._cmd) in (list, tuple):
            cmd = _joinArgv(self._cmd)
        else:
            cmd = self._cmd
        saAttr = pywintypes.SECURITY_ATTRIBUTES()
        saAttr.bInheritHandle = 1
        hChildStdinRd, hChildStdinWr = win32pipe.CreatePipe(saAttr, 0)
        hChildStdoutRd, hChildStdoutWr = win32pipe.CreatePipe(saAttr, 0)
        hChildStderrRd, hChildStderrWr = win32pipe.CreatePipe(saAttr, 0)
        try:
            hChildStdinWrDup = win32api.DuplicateHandle(win32api.GetCurrentProcess(), hChildStdinWr, win32api.GetCurrentProcess(), 0, 0, DUPLICATE_SAME_ACCESS)
            win32api.CloseHandle(hChildStdinWr)
            self._hChildStdinWr = hChildStdinWrDup
            hChildStdoutRdDup = win32api.DuplicateHandle(win32api.GetCurrentProcess(), hChildStdoutRd, win32api.GetCurrentProcess(), 0, 0, DUPLICATE_SAME_ACCESS)
            win32api.CloseHandle(hChildStdoutRd)
            self._hChildStdoutRd = hChildStdoutRdDup
            hChildStderrRdDup = win32api.DuplicateHandle(win32api.GetCurrentProcess(), hChildStderrRd, win32api.GetCurrentProcess(), 0, 0, DUPLICATE_SAME_ACCESS)
            win32api.CloseHandle(hChildStderrRd)
            self._hChildStderrRd = hChildStderrRdDup
            if self._mode == 't':
                flags = os.O_TEXT
            else:
                flags = 0
            fdChildStdinWr = msvcrt.open_osfhandle(self._hChildStdinWr, flags)
            fdChildStdoutRd = msvcrt.open_osfhandle(self._hChildStdoutRd, flags)
            fdChildStderrRd = msvcrt.open_osfhandle(self._hChildStderrRd, flags)
            self.stdin = _FileWrapper(descriptor=fdChildStdinWr, handle=self._hChildStdinWr)
            logres.info('[%s] ProcessOpen._start(): create child stdin: %r', id(self), self.stdin)
            self.stdout = _FileWrapper(descriptor=fdChildStdoutRd, handle=self._hChildStdoutRd)
            logres.info('[%s] ProcessOpen._start(): create child stdout: %r', id(self), self.stdout)
            self.stderr = _FileWrapper(descriptor=fdChildStderrRd, handle=self._hChildStderrRd)
            logres.info('[%s] ProcessOpen._start(): create child stderr: %r', id(self), self.stderr)
            si = win32process.STARTUPINFO()
            si.dwFlags = win32process.STARTF_USESHOWWINDOW
            si.wShowWindow = True
            si.hStdInput = hChildStdinRd
            si.hStdOutput = hChildStdoutWr
            si.hStdError = hChildStderrWr
            si.dwFlags |= win32process.STARTF_USESTDHANDLES
            cmd = _fixupCommand(cmd, self._env)
            creationFlags = win32process.CREATE_NEW_PROCESS_GROUP | win32process.CREATE_NO_WINDOW
            try:
                self._hProcess, hThread, self._processId, threadId = _SaferCreateProcess(None, cmd, None, None, 1, creationFlags, self._env, self._cwd, si)
            except win32api.error as ex:
                raise ProcessError(msg=ex.args[2], errno=ex.args[0])

            win32api.CloseHandle(hThread)
        finally:
            win32file.CloseHandle(hChildStdinRd)
            win32file.CloseHandle(hChildStdoutWr)
            win32file.CloseHandle(hChildStderrWr)

    def wait(self, timeout=None):
        """Wait for the started process to complete.
        
        "timeout" (on Windows) is a floating point number of seconds after
            which to timeout.  Default is win32event.INFINITE.
        "timeout" (on Unix) is akin to the os.waitpid() "options" argument
            (os.WNOHANG may be used to return immediately if the process has
            not exited). Default is 0, i.e. wait forever.

        If the wait time's out it will raise a ProcessError. Otherwise it
        will return the child's exit value (on Windows) or the child's exit
        status excoded as per os.waitpid() (on Linux):
            "a 16-bit number, whose low byte is the signal number that killed
            the process, and whose high byte is the exit status (if the
            signal number is zero); the high bit of the low byte is set if a
            core file was produced."
        In the latter case, use the os.W*() methods to interpret the return
        value.
        """
        if sys.platform.startswith('win'):
            if timeout is None:
                timeout = win32event.INFINITE
            else:
                timeout = timeout * 1000.0
            rc = win32event.WaitForSingleObject(self._hProcess, int(timeout))
            if rc == win32event.WAIT_FAILED:
                raise ProcessError("'WAIT_FAILED' when waiting for process to terminate: %r" % self._cmd, rc)
            elif rc == win32event.WAIT_TIMEOUT:
                raise ProcessError("'WAIT_TIMEOUT' when waiting for process to terminate: %r" % self._cmd, rc)
            retval = win32process.GetExitCodeProcess(self._hProcess)
        else:
            if self._ProcessOpen__retvalCache is not None:
                retval = self._ProcessOpen__retvalCache
            else:
                if timeout is None:
                    timeout = 0
                pid, sts = os.waitpid(self._pid, timeout)
                if pid == self._pid:
                    self._ProcessOpen__retvalCache = retval = sts
                else:
                    raise ProcessError('Wait for process timed out.', self.WAIT_TIMEOUT)
        _unregisterProcess(self)
        return retval

    def kill(self, exitCode=0, gracePeriod=1.0, sig=None):
        """Kill process.
        
        "exitCode" [deprecated, not supported] (Windows only) is the
            code the terminated process should exit with.
        "gracePeriod" (Windows only) is a number of seconds the process is
            allowed to shutdown with a WM_CLOSE signal before a hard
            terminate is called.
        "sig" (Unix only) is the signal to use to kill the process. Defaults
            to signal.SIGKILL. See os.kill() for more information.

        Windows:
            Try for an orderly shutdown via WM_CLOSE.  If still running
            after gracePeriod (1 sec. default), terminate.
        """
        if sys.platform.startswith('win'):
            import win32gui
            win32gui.EnumWindows(self._close_, 0)
            try:
                win32api.GenerateConsoleCtrlEvent(CTRL_BREAK_EVENT, self._processId)
            except AttributeError:
                log.warn('The win32api module does not have GenerateConsoleCtrlEvent(). This may mean that parts of this process group have NOT been killed.')
            except win32api.error as ex:
                if ex.args[0] not in (6, 87):
                    raise

            retval = 0
            try:
                self.wait(gracePeriod)
            except ProcessError as ex:
                log.info('[%s] Process.kill: calling TerminateProcess', id(self))
                win32process.TerminateProcess(self._hProcess, -1)
                win32api.Sleep(100)

        else:
            if sig is None:
                sig = signal.SIGKILL
            try:
                for pid in utils.get_child_pids(self._pid):
                    os.kill(pid, sig)

                os.kill(self._pid, sig)
            except OSError as ex:
                if ex.errno != 3:
                    raise

            _unregisterProcess(self)

    def _close_(self, hwnd, dummy):
        """Callback used by .kill() on Windows.

        EnumWindows callback - sends WM_CLOSE to any window owned by this
        process.
        """
        threadId, processId = win32process.GetWindowThreadProcessId(hwnd)
        if processId == self._processId:
            import win32gui
            win32gui.PostMessage(hwnd, WM_CLOSE, 0, 0)


class ProcessProxy(Process):
    __doc__ = 'Create a process and proxy communication via the standard handles.\n    '

    def __init__(self, cmd, mode='t', cwd=None, env=None, stdin=None, stdout=None, stderr=None):
        """Create a Process with proxy threads for each std handle.

        "cmd" is the command string or argument vector to run.
        "mode" (Windows only) specifies whether the pipes used to communicate
            with the child are openned in text, 't', or binary, 'b', mode.
            This is ignored on platforms other than Windows. Default is 't'.
        "cwd" optionally specifies the directory in which the child process
            should be started. Default is None, a.k.a. inherits the cwd from
            the parent.
        "env" is optionally a mapping specifying the environment in which to
            start the child. Default is None, a.k.a. inherits the environment
            of the parent.
        "stdin", "stdout", "stderr" can be used to specify objects with
            file-like interfaces to handle read (stdout/stderr) and write
            (stdin) events from the child. By default a process.IOBuffer
            instance is assigned to each handler. IOBuffer may be
            sub-classed. See the IOBuffer doc string for more information.
        """
        self._ProcessProxy__log = log
        log.info('ProcessProxy.__init__(cmd=%r, mode=%r, cwd=%r, env=%r, stdin=%r, stdout=%r, stderr=%r)', cmd, mode, cwd, env, stdin, stdout, stderr)
        self._cmd = cmd
        if not self._cmd:
            raise ProcessError('You must specify a command.')
        self._mode = mode
        if self._mode not in ('t', 'b'):
            raise ProcessError("'mode' must be 't' or 'b'.")
        self._cwd = cwd
        self._env = env
        if stdin is None:
            self.stdin = IOBuffer(name='<stdin>')
        else:
            self.stdin = stdin
        if stdout is None:
            self.stdout = IOBuffer(name='<stdout>')
        else:
            self.stdout = stdout
        if stderr is None:
            self.stderr = IOBuffer(name='<stderr>')
        else:
            self.stderr = stderr
        self._closed = 0
        if sys.platform.startswith('win'):
            self._startOnWindows()
        else:
            self._ProcessProxy__retvalCache = None
            self._startOnUnix()
        _registerProcess(self)

    def __del__(self):
        logres.info('[%s] ProcessProxy.__del__()', id(self))
        self.close()
        del self._ProcessProxy__log

    def close(self):
        if not self._closed:
            self._ProcessProxy__log.info('[%s] ProcessProxy.close()' % id(self))
            self._ProcessProxy__log.info('[%s] ProcessProxy: closing stdin (%r).' % (
             id(self), self.stdin))
            try:
                self.stdin.close()
                self._stdinProxy.join()
            except AttributeError:
                pass

            self._ProcessProxy__log.info('[%s] ProcessProxy: closing stdout (%r).' % (
             id(self), self.stdout))
            try:
                self.stdout.close()
                if self._stdoutProxy is not threading.currentThread():
                    self._stdoutProxy.join()
            except AttributeError:
                pass

            self._ProcessProxy__log.info('[%s] ProcessProxy: closing stderr (%r).' % (
             id(self), self.stderr))
            try:
                self.stderr.close()
                if self._stderrProxy is not threading.currentThread():
                    self._stderrProxy.join()
            except AttributeError:
                pass

            self._closed = 1

    def _forkAndExecChildOnUnix(self, fdChildStdinRd, fdChildStdoutWr, fdChildStderrWr):
        """Fork and start the child process.

        Sets self._pid as a side effect.
        """
        pid = os.fork()
        if pid == 0:
            os.dup2(fdChildStdinRd, 0)
            os.dup2(fdChildStdoutWr, 1)
            os.dup2(fdChildStderrWr, 2)
            self._runChildOnUnix()
        self._pid = pid

    def _startOnUnix(self):
        fdChildStdinRd, fdChildStdinWr = os.pipe()
        fdChildStdoutRd, fdChildStdoutWr = os.pipe()
        fdChildStderrRd, fdChildStderrWr = os.pipe()
        if self._cwd:
            oldDir = os.getcwd()
            try:
                os.chdir(self._cwd)
            except OSError as ex:
                raise ProcessError(msg=str(ex), errno=ex.errno)

        self._forkAndExecChildOnUnix(fdChildStdinRd, fdChildStdoutWr, fdChildStderrWr)
        if self._cwd:
            os.chdir(oldDir)
        os.close(fdChildStdinRd)
        os.close(fdChildStdoutWr)
        os.close(fdChildStderrWr)
        childStdin = _FileWrapper(descriptor=fdChildStdinWr)
        logres.info('[%s] ProcessProxy._start(): create child stdin: %r', id(self), childStdin)
        childStdout = _FileWrapper(descriptor=fdChildStdoutRd)
        logres.info('[%s] ProcessProxy._start(): create child stdout: %r', id(self), childStdout)
        childStderr = _FileWrapper(descriptor=fdChildStderrRd)
        logres.info('[%s] ProcessProxy._start(): create child stderr: %r', id(self), childStderr)
        self._stdinProxy = _InFileProxy(self.stdin, childStdin, name='<stdin>')
        self._stdinProxy.start()
        closer = _CountingCloser([self.stdin, childStdin, self], 2)
        self._stdoutProxy = _OutFileProxy(childStdout, self.stdout, [
         closer], name='<stdout>')
        self._stdoutProxy.start()
        self._stderrProxy = _OutFileProxy(childStderr, self.stderr, [
         closer], name='<stderr>')
        self._stderrProxy.start()

    def _startOnWindows(self):
        if type(self._cmd) in (types.ListType, types.TupleType):
            cmd = _joinArgv(self._cmd)
        else:
            cmd = self._cmd
        saAttr = pywintypes.SECURITY_ATTRIBUTES()
        saAttr.bInheritHandle = 1
        hChildStdinRd, hChildStdinWr = win32pipe.CreatePipe(saAttr, 0)
        hChildStdoutRd, hChildStdoutWr = win32pipe.CreatePipe(saAttr, 0)
        hChildStderrRd, hChildStderrWr = win32pipe.CreatePipe(saAttr, 0)
        try:
            hChildStdinWrDup = win32api.DuplicateHandle(win32api.GetCurrentProcess(), hChildStdinWr, win32api.GetCurrentProcess(), 0, 0, DUPLICATE_SAME_ACCESS)
            win32api.CloseHandle(hChildStdinWr)
            self._hChildStdinWr = hChildStdinWrDup
            hChildStdoutRdDup = win32api.DuplicateHandle(win32api.GetCurrentProcess(), hChildStdoutRd, win32api.GetCurrentProcess(), 0, 0, DUPLICATE_SAME_ACCESS)
            win32api.CloseHandle(hChildStdoutRd)
            self._hChildStdoutRd = hChildStdoutRdDup
            hChildStderrRdDup = win32api.DuplicateHandle(win32api.GetCurrentProcess(), hChildStderrRd, win32api.GetCurrentProcess(), 0, 0, DUPLICATE_SAME_ACCESS)
            win32api.CloseHandle(hChildStderrRd)
            self._hChildStderrRd = hChildStderrRdDup
            if self._mode == 't':
                flags = os.O_TEXT
                mode = ''
            else:
                flags = 0
                mode = 'b'
            fdChildStdinWr = msvcrt.open_osfhandle(self._hChildStdinWr, flags)
            fdChildStdoutRd = msvcrt.open_osfhandle(self._hChildStdoutRd, flags)
            fdChildStderrRd = msvcrt.open_osfhandle(self._hChildStderrRd, flags)
            childStdin = _FileWrapper(descriptor=fdChildStdinWr, handle=self._hChildStdinWr)
            logres.info('[%s] ProcessProxy._start(): create child stdin: %r', id(self), childStdin)
            childStdout = _FileWrapper(descriptor=fdChildStdoutRd, handle=self._hChildStdoutRd)
            logres.info('[%s] ProcessProxy._start(): create child stdout: %r', id(self), childStdout)
            childStderr = _FileWrapper(descriptor=fdChildStderrRd, handle=self._hChildStderrRd)
            logres.info('[%s] ProcessProxy._start(): create child stderr: %r', id(self), childStderr)
            si = win32process.STARTUPINFO()
            si.dwFlags = win32process.STARTF_USESHOWWINDOW
            si.wShowWindow = 0
            si.hStdInput = hChildStdinRd
            si.hStdOutput = hChildStdoutWr
            si.hStdError = hChildStderrWr
            si.dwFlags |= win32process.STARTF_USESTDHANDLES
            cmd = _fixupCommand(cmd, self._env)
            log.debug('cmd = %r', cmd)
            creationFlags = win32process.CREATE_NEW_PROCESS_GROUP
            try:
                self._hProcess, hThread, self._processId, threadId = _SaferCreateProcess(None, cmd, None, None, 1, creationFlags, self._env, self._cwd, si)
            except win32api.error as ex:
                raise ProcessError(msg=ex.args[2], errno=ex.args[0])

            win32api.CloseHandle(hThread)
        finally:
            win32file.CloseHandle(hChildStdinRd)
            win32file.CloseHandle(hChildStdoutWr)
            win32file.CloseHandle(hChildStderrWr)

        self._stdinProxy = _InFileProxy(self.stdin, childStdin, name='<stdin>')
        self._stdinProxy.start()
        self._stdoutProxy = _OutFileProxy(childStdout, self.stdout, [
         self.stdin, childStdin, self], name='<stdout>')
        self._stdoutProxy.start()
        self._stderrProxy = _OutFileProxy(childStderr, self.stderr, name='<stderr>')
        self._stderrProxy.start()

    def wait(self, timeout=None):
        """Wait for the started process to complete.
        
        "timeout" (on Windows) is a floating point number of seconds after
            which to timeout.  Default is win32event.INFINITE.
        "timeout" (on Unix) is akin to the os.waitpid() "options" argument
            (os.WNOHANG may be used to return immediately if the process has
            not exited). Default is 0, i.e. wait forever.

        If the wait time's out it will raise a ProcessError. Otherwise it
        will return the child's exit value (on Windows) or the child's exit
        status excoded as per os.waitpid() (on Linux):
            "a 16-bit number, whose low byte is the signal number that killed
            the process, and whose high byte is the exit status (if the
            signal number is zero); the high bit of the low byte is set if a
            core file was produced."
        In the latter case, use the os.W*() methods to interpret the return
        value.
        """
        if sys.platform.startswith('win'):
            if timeout is None:
                timeout = win32event.INFINITE
            else:
                timeout = timeout * 1000.0
            rc = win32event.WaitForSingleObject(self._hProcess, timeout)
            if rc == win32event.WAIT_FAILED:
                raise ProcessError("'WAIT_FAILED' when waiting for process to terminate: %r" % self._cmd, rc)
            elif rc == win32event.WAIT_TIMEOUT:
                raise ProcessError("'WAIT_TIMEOUT' when waiting for process to terminate: %r" % self._cmd, rc)
            retval = win32process.GetExitCodeProcess(self._hProcess)
        else:
            if self._ProcessProxy__retvalCache is not None:
                retval = self._ProcessProxy__retvalCache
            else:
                if timeout is None:
                    timeout = 0
                pid, sts = os.waitpid(self._pid, timeout)
                if pid == self._pid:
                    self._ProcessProxy__retvalCache = retval = sts
                else:
                    raise ProcessError('Wait for process timed out.', self.WAIT_TIMEOUT)
        _unregisterProcess(self)
        return retval

    def kill(self, exitCode=0, gracePeriod=1.0, sig=None):
        """Kill process.
        
        "exitCode" [deprecated, not supported] (Windows only) is the
            code the terminated process should exit with.
        "gracePeriod" (Windows only) is a number of seconds the process is
            allowed to shutdown with a WM_CLOSE signal before a hard
            terminate is called.
        "sig" (Unix only) is the signal to use to kill the process. Defaults
            to signal.SIGKILL. See os.kill() for more information.

        Windows:
            Try for an orderly shutdown via WM_CLOSE.  If still running
            after gracePeriod (1 sec. default), terminate.
        """
        if sys.platform.startswith('win'):
            import win32gui
            win32gui.EnumWindows(self._close_, 0)
            try:
                win32api.GenerateConsoleCtrlEvent(CTRL_BREAK_EVENT, self._processId)
            except AttributeError:
                log.warn('The win32api module does not have GenerateConsoleCtrlEvent(). This may mean that parts of this process group have NOT been killed.')
            except win32api.error as ex:
                if ex.args[0] not in (6, 87):
                    raise

            retval = 0
            try:
                self.wait(gracePeriod)
            except ProcessError as ex:
                log.info('[%s] Process.kill: calling TerminateProcess', id(self))
                win32process.TerminateProcess(self._hProcess, -1)
                win32api.Sleep(100)

        else:
            if sig is None:
                sig = signal.SIGKILL
            try:
                os.kill(self._pid, sig)
            except OSError as ex:
                if ex.errno != 3:
                    raise

            _unregisterProcess(self)

    def _close_(self, hwnd, dummy):
        """Callback used by .kill() on Windows.

        EnumWindows callback - sends WM_CLOSE to any window owned by this
        process.
        """
        threadId, processId = win32process.GetWindowThreadProcessId(hwnd)
        if processId == self._processId:
            import win32gui
            win32gui.PostMessage(hwnd, WM_CLOSE, 0, 0)


class IOBuffer:
    __doc__ = 'Want to be able to both read and write to this buffer from\n    difference threads and have the same read/write semantics as for a\n    std handler.\n\n    This class is subclass-able. _doRead(), _doWrite(), _doReadline(),\n    _doClose(), _haveLine(), and _haveNumBytes() can be overridden for\n    specific functionality. The synchronization issues (block on read\n    until write provides the needed data, termination) are handled for\n    free.\n\n    Cannot support:\n        .seek()     # Because we are managing *two* positions (one each\n        .tell()     #   for reading and writing), these do not make\n                    #   sense.\n    '

    def __init__(self, mutex=None, stateChange=None, name=None):
        """'name' can be set for debugging, it will be used in log messages."""
        if name is not None:
            self._name = name
        else:
            self._name = id(self)
        log.info('[%s] IOBuffer.__init__()' % self._name)
        self._IOBuffer__buf = ''
        if mutex is not None:
            self._mutex = mutex
        else:
            self._mutex = threading.Lock()
        if stateChange is not None:
            self._stateChange = stateChange
        else:
            self._stateChange = threading.Condition()
        self._closed = 0

    def _doWrite(self, s):
        self._IOBuffer__buf += s

    def write(self, s):
        log.info('[%s] IOBuffer.write(s=%r)', self._name, s)
        if self._closed:
            return
        if not s:
            self.close()
            return
        self._mutex.acquire()
        self._doWrite(s)
        self._stateChange.acquire()
        self._stateChange.notifyAll()
        self._stateChange.release()
        self._mutex.release()

    def writelines(self, list):
        self.write(''.join(list))

    def _doRead(self, n):
        """Pop 'n' bytes from the internal buffer and return them."""
        if n < 0:
            idx = len(self._IOBuffer__buf)
        else:
            idx = min(n, len(self._IOBuffer__buf))
        retval, self._IOBuffer__buf = self._IOBuffer__buf[:idx], self._IOBuffer__buf[idx:]
        return retval

    def read(self, n=-1):
        log.info('[%s] IOBuffer.read(n=%r)' % (self._name, n))
        log.info('[%s] IOBuffer.read(): wait for data' % self._name)
        if n < 0:
            while True:
                if self._closed:
                    break
                self._stateChange.acquire()
                self._stateChange.wait()
                self._stateChange.release()

        else:
            while True:
                if self._closed:
                    break
                if self._haveNumBytes(n):
                    break
                self._stateChange.acquire()
                self._stateChange.wait()
                self._stateChange.release()

        log.info('[%s] IOBuffer.read(): done waiting for data' % self._name)
        self._mutex.acquire()
        retval = self._doRead(n)
        self._mutex.release()
        return retval

    def _doReadline(self, n):
        """Pop the front line (or n bytes of it, whichever is less) from
        the internal buffer and return it.
        """
        idx = self._IOBuffer__buf.find('\n')
        if idx == -1:
            idx = len(self._IOBuffer__buf)
        else:
            idx += 1
        if n is not None:
            idx = min(idx, n)
        retval, self._IOBuffer__buf = self._IOBuffer__buf[:idx], self._IOBuffer__buf[idx:]
        return retval

    def _haveLine(self):
        return self._IOBuffer__buf.find('\n') != -1

    def _haveNumBytes(self, n=None):
        return len(self._IOBuffer__buf) >= n

    def readline(self, n=None):
        log.info('[%s] IOBuffer.readline(n=%r)' % (self._name, n))
        log.info('[%s] IOBuffer.readline(): wait for data' % self._name)
        while True:
            if self._closed:
                break
            if self._haveLine():
                break
            if n is not None and self._haveNumBytes(n):
                break
            self._stateChange.acquire()
            self._stateChange.wait()
            self._stateChange.release()

        log.info('[%s] IOBuffer.readline(): done waiting for data' % self._name)
        self._mutex.acquire()
        retval = self._doReadline(n)
        self._mutex.release()
        return retval

    def readlines(self):
        lines = []
        while True:
            line = self.readline()
            if line:
                lines.append(line)
            else:
                break

        return lines

    def _doClose(self):
        pass

    def close(self):
        if not self._closed:
            log.info('[%s] IOBuffer.close()' % self._name)
            self._doClose()
            self._closed = 1
            self._stateChange.acquire()
            self._stateChange.notifyAll()
            self._stateChange.release()

    def flush(self):
        log.info('[%s] IOBuffer.flush()' % self._name)


class _InFileProxy(threading.Thread):
    __doc__ = "A thread to proxy stdin.write()'s from the parent to the child."

    def __init__(self, fParent, fChild, name=None):
        """
        "fParent" is a Python file-like object setup for writing.
        "fChild" is a Win32 handle to the a child process' output pipe.
        "name" can be set for debugging, it will be used in log messages.
        """
        log.info('[%s, %s] _InFileProxy.__init__(fChild=%r, fParent=%r)', name, id(self), fChild, fParent)
        threading.Thread.__init__(self, name=name)
        self.fChild = fChild
        self.fParent = fParent

    def run(self):
        log.info('[%s] _InFileProxy: start' % self.getName())
        try:
            self._proxyFromParentToChild()
        finally:
            log.info('[%s] _InFileProxy: closing parent (%r)' % (
             self.getName(), self.fParent))
            try:
                self.fParent.close()
            except IOError:
                pass

        log.info('[%s] _InFileProxy: done' % self.getName())

    def _proxyFromParentToChild(self):
        CHUNKSIZE = 4096
        while True:
            log.info('[%s] _InFileProxy: waiting for read on parent (%r)' % (
             self.getName(), self.fParent))
            try:
                text = self.fParent.read(CHUNKSIZE)
            except ValueError as ex:
                text = None

            if not text:
                log.info('[%s] _InFileProxy: observed close of parent (%r)' % (
                 self.getName(), self.fParent))
                try:
                    logres.info("[%s] _InFileProxy: closing child after observing parent's close: %r", self.getName(), self.fChild)
                    try:
                        self.fChild.close()
                    except IOError:
                        pass

                except IOError as ex:
                    pass

                break
            else:
                log.info('[%s] _InFileProxy: read %d bytes from parent: %r' % (
                 self.getName(), len(text), text))
            log.info('[%s, %s] _InFileProxy: writing %r to child (%r)', self.getName(), id(self), text, self.fChild)
            try:
                self.fChild.write(text)
            except (OSError, IOError) as ex:
                log.info('[%s] _InFileProxy: error writing to child (%r), closing: %s' % (
                 self.getName(), self.fParent, ex))
                break

            log.info('[%s] _InFileProxy: wrote %d bytes to child: %r' % (
             self.getName(), len(text), text))


class _OutFileProxy(threading.Thread):
    __doc__ = 'A thread to watch an "out" file from the spawned child process\n    and pass on write\'s to the parent.\n    '

    def __init__(self, fChild, fParent, toClose=[], name=None):
        """
        "fChild" is a Win32 handle to the a child process' output pipe.
        "fParent" is a Python file-like object setup for writing.
        "toClose" is a list of objects on which to call .close when this
            proxy is terminating.
        "name" can be set for debugging, it will be used in log messages.
        """
        log.info('[%s] _OutFileProxy.__init__(fChild=%r, fParent=%r, toClose=%r)', name, fChild, fParent, toClose)
        threading.Thread.__init__(self, name=name)
        self.fChild = fChild
        self.fParent = fParent
        self.toClose = toClose

    def run(self):
        log.info('[%s] _OutFileProxy: start' % self.getName())
        try:
            self._proxyFromChildToParent()
        finally:
            logres.info('[%s] _OutFileProxy: terminating, close child (%r)', self.getName(), self.fChild)
            try:
                self.fChild.close()
            except IOError:
                pass

            log.info('[%s] _OutFileProxy: closing parent (%r)', self.getName(), self.fParent)
            try:
                self.fParent.close()
            except IOError:
                pass

            while self.toClose:
                logres.info('[%s] _OutFileProxy: closing %r after closing parent', self.getName(), self.toClose[0])
                try:
                    self.toClose[0].close()
                except IOError:
                    pass

                del self.toClose[0]

        log.info('[%s] _OutFileProxy: done' % self.getName())

    def _proxyFromChildToParent(self):
        CHUNKSIZE = 4096
        while True:
            text = None
            try:
                log.info('[%s] _OutFileProxy: waiting for read on child (%r)' % (
                 self.getName(), self.fChild))
                text = self.fChild.read(CHUNKSIZE)
            except IOError as ex:
                log.info('[%s] _OutFileProxy: error reading from child (%r), shutting down: %s', self.getName(), self.fChild, ex)
                break

            if not text:
                log.info('[%s] _OutFileProxy: observed close of child (%r)' % (
                 self.getName(), self.fChild))
                break
            log.info('[%s] _OutFileProxy: text(len=%d): %r', self.getName(), len(text), text)
            self.fParent.write(text)


if sys.platform.startswith('linux'):

    class _ThreadFixer:
        __doc__ = "Mixin class for various classes in the Process hierarchy to\n        work around the known LinuxThreads bug where one cannot .wait()\n        on a created process from a subthread of the thread that created\n        the process.\n\n        Usage:\n            class ProcessXXX(_ThreadFixer, BrokenProcessXXX):\n                _pclass = BrokenProcessXXX\n\n        Details:\n            Because we must do all real os.wait() calls on the child\n            process from the thread that spawned it, we use a proxy\n            thread whose only responsibility is just that. The proxy\n            thread just starts the child and then immediately wait's for\n            the child to terminate. On termination is stores the exit\n            status (for use by the main thread) and notifies any thread\n            waiting for this termination (possibly the main thread). The\n            overriden .wait() uses this stored exit status and the\n            termination notification to simulate the .wait().\n        "

        def __init__(self, *args, **kwargs):
            self._ThreadFixer__log = log
            self._ThreadFixer__waiter = None
            self._ThreadFixer__hasTerminated = threading.Condition()
            self._ThreadFixer__terminationResult = None
            self._ThreadFixer__childStarted = threading.Condition()
            self._pclass.__init__(self, *args, **kwargs)

        def _forkAndExecChildOnUnix(self, *args, **kwargs):
            """Fork and start the child process do it in a special subthread
            that will negotiate subsequent .wait()'s.

            Sets self._pid as a side effect.
            """
            self._ThreadFixer__waiter = threading.Thread(target=self._ThreadFixer__launchAndWait, args=args, kwargs=kwargs)
            self._ThreadFixer__childStarted.acquire()
            self._ThreadFixer__waiter.start()
            self._ThreadFixer__childStarted.wait()
            self._ThreadFixer__childStarted.release()

        def __launchAndWait(self, *args, **kwargs):
            """Launch the given command and wait for it to terminate.

            When the process has terminated then store its exit value
            and finish.
            """
            logfix.info('start child in thread %s', threading.currentThread().getName())
            self._ThreadFixer__childStarted.acquire()
            self._pclass._forkAndExecChildOnUnix(self, *args, **kwargs)
            self._ThreadFixer__childStarted.notifyAll()
            self._ThreadFixer__childStarted.release()
            try:
                waitResult = self._pclass.wait(self)
            except ProcessError as ex:
                waitResult = ex

            self._ThreadFixer__hasTerminated.acquire()
            self._ThreadFixer__terminationResult = waitResult
            self._ThreadFixer__hasTerminated.notifyAll()
            self._ThreadFixer__hasTerminated.release()
            self._ThreadFixer__waiter = None

        def wait(self, timeout=None):
            self._ThreadFixer__hasTerminated.acquire()
            if self._ThreadFixer__terminationResult is None:
                if timeout == os.WNOHANG:
                    self._ThreadFixer__hasTerminated.wait(0)
            else:
                self._ThreadFixer__hasTerminated.wait()
            terminationResult = self._ThreadFixer__terminationResult
            self._ThreadFixer__hasTerminated.release()
            if terminationResult is None:
                raise ProcessError('Wait for process timed out.', self.WAIT_TIMEOUT)
            else:
                if isinstance(terminationResult, Exception):
                    raise terminationResult
                else:
                    return terminationResult


    _ThreadBrokenProcess = Process

    class Process(_ThreadFixer, _ThreadBrokenProcess):
        _pclass = _ThreadBrokenProcess


    _ThreadBrokenProcessOpen = ProcessOpen

    class ProcessOpen(_ThreadFixer, _ThreadBrokenProcessOpen):
        _pclass = _ThreadBrokenProcessOpen


    _ThreadBrokenProcessProxy = ProcessProxy

    class ProcessProxy(_ThreadFixer, _ThreadBrokenProcessProxy):
        _pclass = _ThreadBrokenProcessProxy