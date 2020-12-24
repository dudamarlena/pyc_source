# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/Worker/fastsubprocess.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 15810 bytes
__doc__ = '_subprocess - Subprocesses with accessible I/O non-blocking file\ndescriptors\n\nFaster revision of subprocess-like module.\n'
import gc, os, signal, sys, types
try:
    basestring
except NameError:
    basestring = str

class CalledProcessError(Exception):
    """CalledProcessError"""

    def __init__(self, returncode, cmd):
        self.returncode = returncode
        self.cmd = cmd

    def __str__(self):
        return "Command '%s' returned non-zero exit status %d" % (self.cmd,
         self.returncode)


import select, errno, fcntl
__all__ = [
 'Popen', 'PIPE', 'STDOUT', 'call', 'check_call',
 'CalledProcessError']
try:
    MAXFD = os.sysconf('SC_OPEN_MAX')
except:
    MAXFD = 256

_active = []

def _cleanup():
    for inst in _active[:]:
        if inst._internal_poll(_deadstate=(sys.maxsize)) >= 0:
            try:
                _active.remove(inst)
            except ValueError:
                pass


PIPE = -1
STDOUT = -2

def call(*popenargs, **kwargs):
    """Run command with arguments.  Wait for command to complete, then
    return the returncode attribute.

    The arguments are the same as for the Popen constructor.  Example:

    retcode = call(["ls", "-l"])
    """
    return Popen(*popenargs, **kwargs).wait()


def check_call(*popenargs, **kwargs):
    """Run command with arguments.  Wait for command to complete.  If
    the exit code was zero then return, otherwise raise
    CalledProcessError.  The CalledProcessError object will have the
    return code in the returncode attribute.

    The arguments are the same as for the Popen constructor.  Example:

    check_call(["ls", "-l"])
    """
    retcode = call(*popenargs, **kwargs)
    cmd = kwargs.get('args')
    if cmd is None:
        cmd = popenargs[0]
    if retcode:
        raise CalledProcessError(retcode, cmd)
    return retcode


def set_nonblock_flag(fd):
    """Set non blocking flag to file descriptor fd"""
    old = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, old | os.O_NDELAY)


class Popen(object):
    """Popen"""

    def __init__(self, args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, shell=False, cwd=None, env=None, universal_newlines=False):
        """Create new Popen instance."""
        _cleanup()
        self._child_created = False
        if not isinstance(bufsize, int):
            raise TypeError('bufsize must be an integer')
        self.pid = None
        self.returncode = None
        self.universal_newlines = universal_newlines
        p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite = self._get_handles(stdin, stdout, stderr)
        self._execute_child(args, executable, preexec_fn, cwd, env, universal_newlines, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)
        if p2cwrite is not None:
            set_nonblock_flag(p2cwrite)
        self.stdin = p2cwrite
        if c2pread is not None:
            set_nonblock_flag(c2pread)
        self.stdout = c2pread
        if errread is not None:
            set_nonblock_flag(errread)
        self.stderr = errread

    def _translate_newlines(self, data):
        data = data.replace('\r\n', '\n')
        data = data.replace('\r', '\n')
        return data

    def __del__(self, sys=sys):
        if not self._child_created:
            return
        self._internal_poll(_deadstate=(sys.maxsize))
        if self.returncode is None:
            if _active is not None:
                _active.append(self)

    def communicate(self, input=None):
        """Interact with process: Send data to stdin.  Read data from
        stdout and stderr, until end-of-file is reached.  Wait for
        process to terminate.  The optional input argument should be a
        string to be sent to the child process, or None, if no data
        should be sent to the child.

        communicate() returns a tuple (stdout, stderr)."""
        if [
         self.stdin, self.stdout, self.stderr].count(None) >= 2:
            stdout = None
            stderr = None
            if self.stdin:
                if input:
                    self.stdin.write(input)
                self.stdin.close()
            else:
                if self.stdout:
                    stdout = self.stdout.read()
                    self.stdout.close()
                else:
                    if self.stderr:
                        stderr = self.stderr.read()
                        self.stderr.close()
            self.wait()
            return (
             stdout, stderr)
        else:
            return self._communicate(input)

    def poll(self):
        return self._internal_poll()

    def _get_handles(self, stdin, stdout, stderr):
        """Construct and return tuple with IO objects:
        p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite
        """
        p2cread, p2cwrite = (None, None)
        c2pread, c2pwrite = (None, None)
        errread, errwrite = (None, None)
        if stdin is None:
            pass
        else:
            if stdin == PIPE:
                p2cread, p2cwrite = os.pipe()
            else:
                if isinstance(stdin, int):
                    p2cread = stdin
                else:
                    p2cread = stdin.fileno()
            if stdout is None:
                pass
            else:
                if stdout == PIPE:
                    try:
                        c2pread, c2pwrite = os.pipe()
                    except:
                        if stdin == PIPE:
                            os.close(p2cread)
                            os.close(p2cwrite)
                        raise

                else:
                    if isinstance(stdout, int):
                        c2pwrite = stdout
                    else:
                        c2pwrite = stdout.fileno()
                    if stderr is None:
                        pass
                    elif stderr == PIPE:
                        try:
                            errread, errwrite = os.pipe()
                        except:
                            if stdin == PIPE:
                                os.close(p2cread)
                                os.close(p2cwrite)
                            if stdout == PIPE:
                                os.close(c2pread)
                                os.close(c2pwrite)
                            raise

                    else:
                        if stderr == STDOUT:
                            errwrite = c2pwrite
                        else:
                            if isinstance(stderr, int):
                                errwrite = stderr
                            else:
                                errwrite = stderr.fileno()
                        return (p2cread, p2cwrite,
                         c2pread, c2pwrite,
                         errread, errwrite)

    def _execute_child(self, args, executable, preexec_fn, cwd, env, universal_newlines, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite):
        """Execute program (POSIX version)"""
        if isinstance(args, basestring):
            args = [
             args]
        else:
            args = list(args)
        if shell:
            args = [
             '/bin/sh', '-c'] + args
        if executable is None:
            executable = args[0]
        gc_was_enabled = gc.isenabled()
        gc.disable()
        try:
            self.pid = os.fork()
        except:
            if gc_was_enabled:
                gc.enable()
            raise

        self._child_created = True
        if self.pid == 0:
            try:
                if p2cwrite is not None:
                    os.close(p2cwrite)
                else:
                    if c2pread is not None:
                        os.close(c2pread)
                    else:
                        if errread is not None:
                            os.close(errread)
                        else:
                            if p2cread is not None:
                                os.dup2(p2cread, 0)
                            elif c2pwrite is not None:
                                os.dup2(c2pwrite, 1)
                            else:
                                if errwrite is not None:
                                    os.dup2(errwrite, 2)
                                else:
                                    if p2cread is not None:
                                        if p2cread not in (0, ):
                                            os.close(p2cread)
                                    if c2pwrite is not None:
                                        if c2pwrite not in (p2cread, 1):
                                            os.close(c2pwrite)
                                if errwrite is not None:
                                    if errwrite not in (
                                     p2cread, c2pwrite, 2):
                                        os.close(errwrite)
                            if cwd is not None:
                                os.chdir(cwd)
                        if preexec_fn:
                            preexec_fn()
                    if env is None:
                        os.execvp(executable, args)
                    else:
                        os.execvpe(executable, args, env)
            except:
                os._exit(255)

        if gc_was_enabled:
            gc.enable()
        if p2cread is not None:
            if p2cwrite is not None:
                os.close(p2cread)
        if c2pwrite is not None:
            if c2pread is not None:
                os.close(c2pwrite)
        if errwrite is not None:
            if errread is not None:
                os.close(errwrite)

    def _handle_exitstatus(self, sts):
        if os.WIFSIGNALED(sts):
            self.returncode = -os.WTERMSIG(sts)
        else:
            if os.WIFEXITED(sts):
                self.returncode = os.WEXITSTATUS(sts)
            else:
                raise RuntimeError('Unknown child exit status!')

    def _internal_poll(self, _deadstate=None):
        """Check if child process has terminated.  Returns returncode
        attribute."""
        if self.returncode is None:
            try:
                pid, sts = os.waitpid(self.pid, os.WNOHANG)
                if pid == self.pid:
                    self._handle_exitstatus(sts)
            except os.error:
                if _deadstate is not None:
                    self.returncode = _deadstate

        return self.returncode

    def wait(self):
        """Wait for child process to terminate.  Returns returncode
        attribute."""
        if self.returncode is None:
            pid, sts = os.waitpid(self.pid, 0)
            self._handle_exitstatus(sts)
        return self.returncode

    def _communicate(self, input):
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
        input_offset = 0
        while read_set or write_set:
            try:
                rlist, wlist, xlist = select.select(read_set, write_set, [])
            except select.error as ex:
                if ex.args[0] == errno.EINTR:
                    continue
                raise

            if self.stdin in wlist:
                chunk = input[input_offset:input_offset + 512]
                bytes_written = os.write(self.stdin.fileno(), chunk)
                input_offset += bytes_written
                if input_offset >= len(input):
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
            stdout = ''.join(stdout)
        if stderr is not None:
            stderr = ''.join(stderr)
        if self.universal_newlines:
            if hasattr(file, 'newlines'):
                if stdout:
                    stdout = self._translate_newlines(stdout)
                if stderr:
                    stderr = self._translate_newlines(stderr)
        self.wait()
        return (
         stdout, stderr)

    def send_signal(self, sig):
        """Send a signal to the process
        """
        os.kill(self.pid, sig)

    def terminate(self):
        """Terminate the process with SIGTERM
        """
        self.send_signal(signal.SIGTERM)

    def kill(self):
        """Kill the process with SIGKILL
        """
        self.send_signal(signal.SIGKILL)