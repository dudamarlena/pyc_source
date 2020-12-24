# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zTrix/prj/zio/test/zio.py
# Compiled at: 2014-12-01 22:05:31
__version__ = '1.0.3'
__project__ = 'https://github.com/zTrix/zio'
import struct, socket, os, sys, subprocess, threading, pty, time, re, select, termios, resource, tty, errno, signal, fcntl, gc, platform, datetime, inspect, atexit
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from termcolor import colored
except:
    ATTRIBUTES = dict(list(zip(['bold', 'dark', '', 'underline', 'blink', '', 'reverse', 'concealed'], list(range(1, 9)))))
    del ATTRIBUTES['']
    HIGHLIGHTS = dict(list(zip(['on_grey', 'on_red', 'on_green', 'on_yellow', 'on_blue', 'on_magenta', 'on_cyan', 'on_white'], list(range(40, 48)))))
    COLORS = dict(list(zip(['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'], list(range(30, 38)))))
    RESET = '\x1b[0m'

    def colored(text, color=None, on_color=None, attrs=None):
        fmt_str = '\x1b[%dm%s'
        if color is not None:
            text = fmt_str % (COLORS[color], text)
        if on_color is not None:
            text = fmt_str % (HIGHLIGHTS[on_color], text)
        if attrs is not None:
            for attr in attrs:
                text = fmt_str % (ATTRIBUTES[attr], text)

        text += RESET
        return text


__all__ = ['stdout', 'log', 'l8', 'b8', 'l16', 'b16', 'l32', 'b32', 'l64', 'b64', 'zio', 'EOF', 'TIMEOUT', 'SOCKET', 'PROCESS', 'REPR', 'EVAL', 'HEX', 'UNHEX', 'BIN', 'UNBIN', 'RAW', 'NONE', 'COLORED', 'PIPE', 'TTY', 'TTY_RAW', 'cmdline']

def stdout(s, color=None, on_color=None, attrs=None):
    if not color:
        sys.stdout.write(s)
    else:
        sys.stdout.write(colored(s, color, on_color, attrs))
    sys.stdout.flush()


def log(s, color=None, on_color=None, attrs=None, new_line=True, timestamp=False, f=sys.stderr):
    if timestamp is True:
        now = datetime.datetime.now().strftime('[%Y-%m-%d_%H:%M:%S]')
    elif timestamp is False:
        now = None
    elif timestamp:
        now = timestamp
    if not color:
        s = str(s)
    else:
        s = colored(str(s), color, on_color, attrs)
    if now:
        f.write(now)
        f.write(' ')
    f.write(s)
    if new_line:
        f.write('\n')
    f.flush()
    return


def _lb_wrapper(func):
    endian = func.func_name[0] == 'l' and '<' or '>'
    bits = int(func.func_name[1:])
    pfs = {8: 'B', 16: 'H', 32: 'I', 64: 'Q'}

    def wrapper(*args):
        ret = []
        join = False
        for i in args:
            if isinstance(i, (int, long)):
                join = True
                v = struct.pack(endian + pfs[bits], i % (1 << bits))
                ret.append(v)
            elif not i:
                ret.append(None)
            else:
                v = struct.unpack(endian + pfs[bits] * (len(i) * 8 / bits), i)
                ret += v

        if join:
            return ('').join(ret)
        else:
            if len(ret) == 1:
                return ret[0]
            else:
                if len(ret) == 0:
                    return
                return ret

            return

    wrapper.func_name = func.func_name
    return wrapper


@_lb_wrapper
def l8(*args):
    pass


@_lb_wrapper
def b8(*args):
    pass


@_lb_wrapper
def l16(*args):
    pass


@_lb_wrapper
def b16(*args):
    pass


@_lb_wrapper
def l32(*args):
    pass


@_lb_wrapper
def b32(*args):
    pass


@_lb_wrapper
def l64(*args):
    pass


@_lb_wrapper
def b64(*args):
    pass


class EOF(Exception):
    """Raised when EOF is read from child or socket.
    This usually means the child has exited or socket shutdown at remote end"""
    pass


class TIMEOUT(Exception):
    """Raised when a read timeout exceeds the timeout. """
    pass


SOCKET = 'socket'
PROCESS = 'process'
PIPE = 'pipe'
TTY = 'tty'
TTY_RAW = 'ttyraw'

def COLORED(f, color='cyan', on_color=None, attrs=None):
    return lambda s: colored(f(s), color, on_color, attrs)


def REPR(s):
    return repr(str(s)) + '\r\n'


def EVAL(s):
    st = 0
    ret = []
    i = 0
    while i < len(s):
        if st == 0:
            if s[i] == '\\':
                st = 1
            else:
                ret.append(s[i])
        elif st == 1:
            if s[i] in ('"', "'", '\\', 't', 'n', 'r'):
                if s[i] == 't':
                    ret.append('\t')
                elif s[i] == 'n':
                    ret.append('\n')
                elif s[i] == 'r':
                    ret.append('\r')
                else:
                    ret.append(s[i])
                st = 0
            elif s[i] == 'x':
                st = 2
            else:
                raise Exception('invalid repr of str %s' % s)
        else:
            num = int(s[i:i + 2], 16)
            assert 0 <= num < 256
            ret.append(chr(num))
            st = 0
            i += 1
        i += 1

    return ('').join(ret)


def HEX(s):
    return str(s).encode('hex') + '\r\n'


def UNHEX(s):
    s = str(s).strip()
    return (len(s) % 2 and '0' + s or s).decode('hex')


def BIN(s):
    return ('').join([ format(ord(x), '08b') for x in str(s) ]) + '\r\n'


def UNBIN(s):
    s = str(s).strip()
    return ('').join([ chr(int(s[x:x + 8], 2)) for x in xrange(0, len(s), 8) ])


def RAW(s):
    return str(s)


def NONE(s):
    return ''


class zio(object):

    def __init__(self, target, stdin=PIPE, stdout=TTY_RAW, print_read=RAW, print_write=RAW, timeout=8, cwd=None, env=None, sighup=signal.SIG_DFL, write_delay=0.05, ignorecase=False, debug=None):
        """
        zio is an easy-to-use io library for pwning development, supporting an unified interface for local process pwning and remote tcp socket io

        example:

        io = zio(('localhost', 80))
        io = zio(socket.create_connection(('127.0.0.1', 80)))
        io = zio('ls -l')
        io = zio(['ls', '-l'])

        params:
            print_read = bool, if true, print all the data read from target
            print_write = bool, if true, print all the data sent out
        """
        if not target:
            raise Exception('cmdline or socket not provided for zio, try zio("ls -l")')
        self.debug = debug
        self.target = target
        self.print_read = print_read
        self.print_write = print_write
        if isinstance(timeout, (int, long)) and timeout > 0:
            self.timeout = timeout
        else:
            self.timeout = 8
        self.wfd = -1
        self.rfd = -1
        self.write_delay = write_delay
        self.close_delay = 0.1
        self.terminate_delay = 0.1
        self.cwd = cwd
        self.env = env
        self.sighup = sighup
        self.flag_eof = False
        self.closed = True
        self.exit_code = None
        self.ignorecase = ignorecase
        self.buffer = str()
        if self.mode() == SOCKET:
            if isinstance(self.target, socket.socket):
                self.sock = self.target
                self.name = repr(self.target)
            else:
                self.sock = socket.create_connection(self.target, self.timeout)
                self.name = '<socket ' + self.target[0] + ':' + str(self.target[1]) + '>'
            self.rfd = self.wfd = self.sock.fileno()
            self.closed = False
            return
        else:
            if 'windows' in platform.system().lower():
                raise Exception('zio (version %s) process mode is currently only supported on linux and osx.' % __version__)
            self.pid = None
            self.closed = False
            if isinstance(target, type('')):
                self.args = split_command_line(target)
                self.command = self.args[0]
            else:
                self.args = target
                self.command = self.args[0]
            command_with_path = which(self.command)
            if command_with_path is None:
                raise Exception('zio (process mode) Command not found in path: %s' % self.command)
            self.command = command_with_path
            self.args[0] = self.command
            self.name = '<' + (' ').join(self.args) + '>'
            assert self.pid is None, 'pid must be None, to prevent double spawn'
            assert self.command is not None, 'The command to be spawn must not be None'
            if stdout == PIPE:
                stdout_slave_fd, stdout_master_fd = self.pipe_cloexec()
            else:
                stdout_master_fd, stdout_slave_fd = pty.openpty()
            if stdout_master_fd < 0 or stdout_slave_fd < 0:
                raise Exception('Could not create pipe or openpty for stdout/stderr')
            stdin_master_fd, stdin_slave_fd = stdin == PIPE and self.pipe_cloexec() or pty.openpty()
            if stdin_master_fd < 0 or stdin_slave_fd < 0:
                raise Exception('Could not openpty for stdin')
            gc_enabled = gc.isenabled()
            gc.disable()
            try:
                self.pid = os.fork()
            except:
                if gc_enabled:
                    gc.enable()
                raise

            if self.pid < 0:
                raise Exception('failed to fork')
            elif self.pid == 0:
                os.close(stdout_master_fd)
                if os.isatty(stdin_slave_fd):
                    self.__pty_make_controlling_tty(stdin_slave_fd)
                try:
                    if os.isatty(stdout_slave_fd) and os.isatty(pty.STDIN_FILENO):
                        h, w = self.getwinsize(0)
                        self.setwinsize(stdout_slave_fd, h, w)
                except BaseException as ex:
                    if self.debug:
                        log('[ WARN ] setwinsize exception: %s' % str(ex), f=self.debug)

                def _dup2(a, b):
                    if a == b:
                        self._set_cloexec_flag(a, False)
                    elif a is not None:
                        os.dup2(a, b)
                    return

                os.dup2(stdout_slave_fd, pty.STDOUT_FILENO)
                os.dup2(stdout_slave_fd, pty.STDERR_FILENO)
                _dup2(stdin_slave_fd, pty.STDIN_FILENO)
                if stdout_slave_fd > 2:
                    os.close(stdout_slave_fd)
                if stdin_master_fd is not None:
                    os.close(stdin_master_fd)
                max_fd = resource.getrlimit(resource.RLIMIT_NOFILE)[0]
                os.closerange(3, max_fd)
                if self.sighup is not None:
                    signal.signal(signal.SIGHUP, self.sighup)
                if self.cwd is not None:
                    os.chdir(self.cwd)
                if self.env is None:
                    os.execv(self.command, self.args)
                else:
                    os.execvpe(self.command, self.args, self.env)
                os._exit(255)
            else:
                self.wfd = stdin_master_fd
                self.rfd = stdout_master_fd
                if os.isatty(self.wfd):
                    self._wfd_init_mode = tty.tcgetattr(self.wfd)[:]
                    if stdin == TTY_RAW:
                        self.ttyraw(self.wfd)
                        self._wfd_raw_mode = tty.tcgetattr(self.wfd)[:]
                    else:
                        self._wfd_raw_mode = self._wfd_init_mode[:]
                if os.isatty(self.rfd):
                    self._rfd_init_mode = tty.tcgetattr(self.rfd)[:]
                    if stdout == TTY_RAW:
                        self.ttyraw(self.rfd, raw_in=False, raw_out=True)
                        self._rfd_raw_mode = tty.tcgetattr(self.rfd)[:]
                        if self.debug:
                            log('stdout tty raw mode: %r' % self._rfd_raw_mode, f=self.debug)
                    else:
                        self._rfd_raw_mode = self._rfd_init_mode[:]
                os.close(stdin_slave_fd)
                os.close(stdout_slave_fd)
                if gc_enabled:
                    gc.enable()
                time.sleep(self.close_delay)
                atexit.register(self.kill, signal.SIGHUP)
            return

    @property
    def print_read(self):
        return self._print_read and self._print_read is not NONE

    @print_read.setter
    def print_read(self, value):
        if value is True:
            self._print_read = RAW
        elif value is False:
            self._print_read = NONE
        elif callable(value):
            self._print_read = value
        else:
            raise Exception('bad print_read value')
        assert callable(self._print_read) and len(inspect.getargspec(self._print_read).args) == 1

    @property
    def print_write(self):
        return self._print_write and self._print_write is not NONE

    @print_write.setter
    def print_write(self, value):
        if value is True:
            self._print_write = RAW
        elif value is False:
            self._print_write = NONE
        elif callable(value):
            self._print_write = value
        else:
            raise Exception('bad print_write value')
        assert callable(self._print_write) and len(inspect.getargspec(self._print_write).args) == 1

    def __pty_make_controlling_tty(self, tty_fd):
        """This makes the pseudo-terminal the controlling tty. This should be
        more portable than the pty.fork() function. Specifically, this should
        work on Solaris. """
        child_name = os.ttyname(tty_fd)
        try:
            fd = os.open('/dev/tty', os.O_RDWR | os.O_NOCTTY)
            if fd >= 0:
                os.close(fd)
        except:
            pass

        os.setsid()
        try:
            fd = os.open('/dev/tty', os.O_RDWR | os.O_NOCTTY)
            if fd >= 0:
                os.close(fd)
                raise Exception('Failed to disconnect from ' + 'controlling tty. It is still possible to open /dev/tty.')
        except:
            pass

        fd = os.open(child_name, os.O_RDWR)
        if fd < 0:
            raise Exception('Could not open child pty, ' + child_name)
        else:
            os.close(fd)
        fd = os.open('/dev/tty', os.O_WRONLY)
        if fd < 0:
            raise Exception('Could not open controlling tty, /dev/tty')
        else:
            os.close(fd)

    def _set_cloexec_flag(self, fd, cloexec=True):
        try:
            cloexec_flag = fcntl.FD_CLOEXEC
        except AttributeError:
            cloexec_flag = 1

        old = fcntl.fcntl(fd, fcntl.F_GETFD)
        if cloexec:
            fcntl.fcntl(fd, fcntl.F_SETFD, old | cloexec_flag)
        else:
            fcntl.fcntl(fd, fcntl.F_SETFD, old & ~cloexec_flag)

    def pipe_cloexec(self):
        """Create a pipe with FDs set CLOEXEC."""
        r, w = os.pipe()
        self._set_cloexec_flag(r)
        self._set_cloexec_flag(w)
        return (w, r)

    def fileno(self):
        """This returns the file descriptor of the pty for the child.
        """
        if self.mode() == SOCKET:
            return self.sock.fileno()
        else:
            return self.rfd

    def setwinsize(self, fd, rows, cols):
        """This sets the terminal window size of the child tty. This will cause
        a SIGWINCH signal to be sent to the child. This does not change the
        physical window size. It changes the size reported to TTY-aware
        applications like vi or curses -- applications that respond to the
        SIGWINCH signal. """
        TIOCSWINSZ = getattr(termios, 'TIOCSWINSZ', -2146929561)
        if TIOCSWINSZ == 2148037735:
            TIOCSWINSZ = -2146929561
        s = struct.pack('HHHH', rows, cols, 0, 0)
        fcntl.ioctl(fd, TIOCSWINSZ, s)

    def getwinsize(self, fd):
        """This returns the terminal window size of the child tty. The return
        value is a tuple of (rows, cols). """
        TIOCGWINSZ = getattr(termios, 'TIOCGWINSZ', 1074295912)
        s = struct.pack('HHHH', 0, 0, 0, 0)
        x = fcntl.ioctl(fd, TIOCGWINSZ, s)
        return struct.unpack('HHHH', x)[0:2]

    def __str__(self):
        ret = [
         'io-mode: %s' % self.mode(),
         'name: %s' % self.name,
         'timeout: %f' % self.timeout,
         'write-fd: %d' % (isinstance(self.wfd, (int, long)) and self.wfd or self.fileno()),
         'read-fd: %d' % (isinstance(self.rfd, (int, long)) and self.rfd or self.fileno()),
         'buffer(last 100 chars): %r' % self.buffer[-100:],
         'eof: %s' % self.flag_eof]
        if self.mode() == SOCKET:
            pass
        elif self.mode() == PROCESS:
            ret.append('command: %s' % str(self.command))
            ret.append('args: %r' % (self.args,))
            ret.append('write-delay: %f' % self.write_delay)
            ret.append('close-delay: %f' % self.close_delay)
        return ('\n').join(ret)

    def eof(self):
        """This returns True if the EOF exception was ever raised.
        """
        return self.flag_eof

    def terminate(self, force=False):
        """This forces a child process to terminate. It starts nicely with
        SIGHUP and SIGINT. If "force" is True then moves onto SIGKILL. This
        returns True if the child was terminated. This returns False if the
        child could not be terminated. """
        if self.mode() != PROCESS:
            return
        if not self.isalive():
            return True
        try:
            self.kill(signal.SIGHUP)
            time.sleep(self.terminate_delay)
            if not self.isalive():
                return True
            self.kill(signal.SIGCONT)
            time.sleep(self.terminate_delay)
            if not self.isalive():
                return True
            self.kill(signal.SIGINT)
            time.sleep(self.terminate_delay)
            if not self.isalive():
                return True
            if force:
                self.kill(signal.SIGKILL)
                time.sleep(self.terminate_delay)
                if not self.isalive():
                    return True
                return False
            return False
        except OSError:
            time.sleep(self.terminate_delay)
            if not self.isalive():
                return True
            return False

    def kill(self, sig):
        raw_input()
        print 'killing ', self.pid, 'with', sig
        if self.isalive():
            os.kill(self.pid, sig)

    def wait(self):
        """This waits until the child exits. This is a blocking call. This will
        not read any data from the child, so this will block forever if the
        child has unread output and has terminated. In other words, the child
        may have printed output then called exit(), but, the child is
        technically still alive until its output is read by the parent. """
        if self.isalive():
            pid, status = os.waitpid(self.pid, 0)
        else:
            raise Exception('Cannot wait for dead child process.')
        self.exit_code = os.WEXITSTATUS(status)
        if os.WIFEXITED(status):
            self.exit_code = os.WEXITSTATUS(status)
        elif os.WIFSIGNALED(status):
            self.exit_code = os.WTERMSIG(status)
        elif os.WIFSTOPPED(status):
            raise Exception('Called wait() on a stopped child ' + 'process. This is not supported. Is some other ' + 'process attempting job control with our child pid?')
        return self.exit_code

    def isalive(self):
        """This tests if the child process is running or not. This is
        non-blocking. If the child was terminated then this will read the
        exit code or signalstatus of the child. This returns True if the child
        process appears to be running or False if not. It can take literally
        SECONDS for Solaris to return the right status. """
        if self.mode() == SOCKET:
            return not self.flag_eof
        else:
            if self.exit_code is not None:
                return False
            if self.flag_eof:
                waitpid_options = 0
            else:
                waitpid_options = os.WNOHANG
            try:
                pid, status = os.waitpid(self.pid, waitpid_options)
            except OSError:
                err = sys.exc_info()[1]
                if err.errno == errno.ECHILD:
                    raise Exception('isalive() encountered condition ' + 'where "terminated" is 0, but there was no child ' + 'process. Did someone else call waitpid() ' + 'on our process?')
                else:
                    raise err

            if pid == 0:
                try:
                    pid, status = os.waitpid(self.pid, waitpid_options)
                except OSError as e:
                    if e.errno == errno.ECHILD:
                        raise Exception('isalive() encountered condition ' + 'that should never happen. There was no child ' + 'process. Did someone else call waitpid() ' + 'on our process?')
                    else:
                        raise

                if pid == 0:
                    return True
            if pid == 0:
                return True
            if os.WIFEXITED(status):
                self.exit_code = os.WEXITSTATUS(status)
            elif os.WIFSIGNALED(status):
                self.exit_code = os.WTERMSIG(status)
            elif os.WIFSTOPPED(status):
                raise Exception('isalive() encountered condition ' + 'where child process is stopped. This is not ' + 'supported. Is some other process attempting ' + 'job control with our child pid?')
            return False

    def interact(self, escape_character=chr(29), input_filter=None, output_filter=None, raw_rw=True):
        """
        when stdin is passed using os.pipe, backspace key will not work as expected,
        if wfd is not a tty, then when backspace pressed, I can see that 0x7f is passed, but vim does not delete backwards, so you should choose the right input when using zio
        """
        if self.mode() == SOCKET:
            while self.isalive():
                try:
                    r, w, e = self.__select([self.rfd, pty.STDIN_FILENO], [], [])
                except KeyboardInterrupt:
                    break

                if self.rfd in r:
                    try:
                        data = None
                        data = self._read(1024)
                        if data:
                            if output_filter:
                                data = output_filter(data)
                            stdout(raw_rw and data or self._print_read(data))
                        else:
                            self.flag_eof = True
                            break
                    except EOF:
                        self.flag_eof = True
                        break

                if pty.STDIN_FILENO in r:
                    try:
                        data = None
                        data = os.read(pty.STDIN_FILENO, 1024)
                    except OSError as e:
                        if e.errno != errno.EIO:
                            raise

                    if data is not None:
                        if input_filter:
                            data = input_filter(data)
                        i = input_filter and -1 or data.rfind(escape_character)
                        if i != -1:
                            data = data[:i]
                        try:
                            while data != '' and self.isalive():
                                n = self._write(data)
                                data = data[n:]

                            if i != -1:
                                break
                        except:
                            break

            return
        else:
            self.buffer = str()
            if not input_filter and os.isatty(pty.STDIN_FILENO):
                mode = tty.tcgetattr(pty.STDIN_FILENO)
                self.ttyraw(pty.STDIN_FILENO)
            if os.isatty(self.wfd):
                wfd_mode = tty.tcgetattr(self.wfd)
                if self.debug:
                    log('wfd now mode = ' + repr(wfd_mode), f=self.debug)
                    log('wfd raw mode = ' + repr(self._wfd_raw_mode), f=self.debug)
                    log('wfd ini mode = ' + repr(self._wfd_init_mode), f=self.debug)
                if wfd_mode == self._wfd_raw_mode:
                    tty.tcsetattr(self.wfd, tty.TCSAFLUSH, self._wfd_init_mode)
                    if self.debug:
                        log('change wfd back to init mode', f=self.debug)
            try:
                rfdlist = [
                 self.rfd, pty.STDIN_FILENO]
                if os.isatty(self.wfd):
                    rfdlist.append(self.wfd)
                while self.isalive():
                    if len(rfdlist) == 0:
                        break
                    if self.rfd not in rfdlist:
                        break
                    try:
                        r, w, e = self.__select(rfdlist, [], [])
                    except KeyboardInterrupt:
                        break

                    if self.debug:
                        log('r  = ' + repr(r), f=self.debug)
                    if self.wfd in r:
                        try:
                            data = None
                            data = os.read(self.wfd, 1024)
                        except OSError as e:
                            if e.errno != errno.EIO:
                                raise

                        if data:
                            if output_filter:
                                data = output_filter(data)
                            stdout(raw_rw and data or self._print_write(data))
                        else:
                            rfdlist.remove(self.wfd)
                    if self.rfd in r:
                        try:
                            data = None
                            data = os.read(self.rfd, 1024)
                        except OSError as e:
                            if e.errno != errno.EIO:
                                raise

                        if data:
                            if output_filter:
                                data = output_filter(data)
                            stdout(raw_rw and data or self._print_read(data))
                        else:
                            rfdlist.remove(self.rfd)
                            self.flag_eof = True
                    if pty.STDIN_FILENO in r:
                        try:
                            data = None
                            data = os.read(pty.STDIN_FILENO, 1024)
                        except OSError as e:
                            if e.errno != errno.EIO:
                                raise

                        if self.debug and os.isatty(self.wfd):
                            wfd_mode = tty.tcgetattr(self.wfd)
                            log('stdin wfd mode = ' + repr(wfd_mode), f=self.debug)
                        if data:
                            if input_filter:
                                data = input_filter(data)
                            i = input_filter and -1 or data.rfind(escape_character)
                            if i != -1:
                                data = data[:i]
                            if not os.isatty(self.wfd):
                                data = data.replace('\r', '\n')
                                stdout(raw_rw and data or self._print_write(data))
                            while data != '' and self.isalive():
                                n = self._write(data)
                                data = data[n:]

                            if i != -1:
                                self.end(force_close=True)
                                break
                        else:
                            self.end(force_close=True)
                            rfdlist.remove(pty.STDIN_FILENO)

                while True:
                    r, w, e = self.__select([self.rfd], [], [], timeout=self.close_delay)
                    if self.rfd in r:
                        try:
                            data = None
                            data = os.read(self.rfd, 1024)
                        except OSError as e:
                            if e.errno != errno.EIO:
                                raise

                        if data:
                            if output_filter:
                                data = output_filter(data)
                            stdout(raw_rw and data or self._print_read(data))
                        else:
                            self.flag_eof = True
                            break
                    else:
                        break

            finally:
                if not input_filter and os.isatty(pty.STDIN_FILENO):
                    tty.tcsetattr(pty.STDIN_FILENO, tty.TCSAFLUSH, mode)
                if os.isatty(self.wfd):
                    self.ttyraw(self.wfd)

            return

    def flush(self):
        """
        just keep to be a file-like object
        """
        pass

    def isatty(self):
        """This returns True if the file descriptor is open and connected to a
        tty(-like) device, else False. """
        return os.isatty(self.rfd)

    def ttyraw(self, fd, when=tty.TCSAFLUSH, echo=False, raw_in=True, raw_out=False):
        mode = tty.tcgetattr(fd)[:]
        if raw_in:
            mode[tty.IFLAG] = mode[tty.IFLAG] & ~(tty.BRKINT | tty.ICRNL | tty.INPCK | tty.ISTRIP | tty.IXON)
            mode[tty.CFLAG] = mode[tty.CFLAG] & ~(tty.CSIZE | tty.PARENB)
            mode[tty.CFLAG] = mode[tty.CFLAG] | tty.CS8
            if echo:
                mode[tty.LFLAG] = mode[tty.LFLAG] & ~(tty.ICANON | tty.IEXTEN | tty.ISIG)
            else:
                mode[tty.LFLAG] = mode[tty.LFLAG] & ~(tty.ECHO | tty.ICANON | tty.IEXTEN | tty.ISIG)
        if raw_out:
            mode[tty.OFLAG] = mode[tty.OFLAG] & ~tty.OPOST
        mode[tty.CC][tty.VMIN] = 1
        mode[tty.CC][tty.VTIME] = 0
        tty.tcsetattr(fd, when, mode)

    def mode(self):
        if not hasattr(self, '_io_mode'):
            if hostport_tuple(self.target) or isinstance(self.target, socket.socket):
                self._io_mode = SOCKET
            else:
                self._io_mode = PROCESS
        return self._io_mode

    def __select(self, iwtd, owtd, ewtd, timeout=None):
        """This is a wrapper around select.select() that ignores signals. If
        select.select raises a select.error exception and errno is an EINTR
        error then it is ignored. Mainly this is used to ignore sigwinch
        (terminal resize). """
        if timeout is not None:
            end_time = time.time() + timeout
        while True:
            try:
                return select.select(iwtd, owtd, ewtd, timeout)
            except select.error:
                err = sys.exc_info()[1]
                if err[0] == errno.EINTR:
                    if timeout is not None:
                        timeout = end_time - time.time()
                        if timeout < 0:
                            return ([], [], [])
                else:
                    raise

        return

    def writelines(self, sequence):
        n = 0
        for s in sequence:
            n += self.writeline(s)

        return n

    def writeline(self, s=''):
        return self.write(s + os.linesep)

    def write(self, s):
        if not s:
            return 0
        if self.mode() == SOCKET:
            if self.print_write:
                stdout(self._print_write(s))
            self.sock.sendall(s)
            return len(s)
        if self.mode() == PROCESS:
            time.sleep(self.write_delay)
            if not isinstance(s, bytes):
                s = s.encode('utf-8')
            ret = os.write(self.wfd, s)
            if self.print_write:
                stdout(self._print_write(s))
            return ret

    def end(self, force_close=False):
        """
        end of writing stream, but we can still read
        """
        if self.mode() == SOCKET:
            self.sock.shutdown(socket.SHUT_WR)
        elif not os.isatty(self.wfd):
            os.close(self.wfd)
        elif platform.system() == 'Darwin':
            os.close(self.wfd)
        else:
            mode = tty.tcgetattr(self.wfd)[:]
            mode[tty.CC][tty.VMIN] = 0
            mode[tty.CC][tty.VTIME] = 1
            tty.tcsetattr(self.wfd, tty.TCSAFLUSH, mode)
            if force_close:
                time.sleep(self.close_delay)
                os.close(self.wfd)

    def close(self, force=True):
        """
        close and clean up, nothing can and should be done after closing
        """
        if self.closed:
            return
        else:
            if self.mode() == 'socket':
                if self.sock:
                    self.sock.close()
                self.sock = None
            else:
                try:
                    os.close(self.wfd)
                except:
                    pass

            os.close(self.rfd)
            time.sleep(self.close_delay)
            if self.isalive():
                if not self.terminate(force):
                    raise Exception('Could not terminate child process')
            self.flag_eof = True
            self.rfd = -1
            self.wfd = -1
            self.closed = True
            return

    def read(self, size=None, timeout=-1):
        if size == 0:
            return str()
        else:
            if size < 0 or size is None:
                self.read_loop(searcher_re(self.compile_pattern_list(EOF)), timeout=timeout)
                return self.before
            cre = re.compile('.{%d}' % size, re.DOTALL)
            index = self.read_loop(searcher_re(self.compile_pattern_list([cre, EOF])), timeout=timeout)
            if index == 0:
                assert self.before == ''
                return self.after
            return self.before

    def read_until_timeout(self, timeout=0.05):
        try:
            incoming = self.buffer
            while True:
                c = self.read_nonblocking(2048, timeout)
                incoming = incoming + c
                if self.mode() == PROCESS:
                    time.sleep(0.0001)

        except EOF:
            err = sys.exc_info()[1]
            self.buffer = str()
            self.before = str()
            self.after = EOF
            self.match = incoming
            self.match_index = None
            raise EOF(str(err) + '\n' + str(self))
        except TIMEOUT:
            self.buffer = str()
            self.before = str()
            self.after = TIMEOUT
            self.match = incoming
            self.match_index = None
            return incoming
        except:
            self.before = str()
            self.after = None
            self.match = incoming
            self.match_index = None
            raise

        return

    read_eager = read_until_timeout

    def readable(self):
        return self.__select([self.rfd], [], [], 0) == ([self.rfd], [], [])

    def readline(self, size=-1):
        if size == 0:
            return str()
        else:
            lineseps = [
             '\r\n', '\n', EOF]
            index = self.read_loop(searcher_re(self.compile_pattern_list(lineseps)))
            if index < 2:
                return self.before + lineseps[index]
            return self.before

    read_line = readline

    def readlines(self, sizehint=-1):
        lines = []
        while True:
            line = self.readline()
            if not line:
                break
            lines.append(line)

        return lines

    def read_until(self, pattern_list, timeout=-1, searchwindowsize=None):
        if isinstance(pattern_list, basestring) or pattern_list in (TIMEOUT, EOF):
            pattern_list = [
             pattern_list]

        def prepare_pattern(pattern):
            if pattern in (TIMEOUT, EOF):
                return pattern
            if isinstance(pattern, basestring):
                return pattern
            self._pattern_type_err(pattern)

        try:
            pattern_list = iter(pattern_list)
        except TypeError:
            self._pattern_type_err(pattern_list)

        pattern_list = [ prepare_pattern(p) for p in pattern_list ]
        matched = self.read_loop(searcher_string(pattern_list), timeout, searchwindowsize)
        ret = self.before
        if isinstance(self.after, basestring):
            ret += self.after
        return ret

    def read_until_re(self, pattern, timeout=-1, searchwindowsize=None):
        compiled_pattern_list = self.compile_pattern_list(pattern)
        matched = self.read_loop(searcher_re(compiled_pattern_list), timeout, searchwindowsize)
        ret = self.before
        if isinstance(self.after, basestring):
            ret += self.after
        return ret

    def read_loop(self, searcher, timeout=-1, searchwindowsize=None):
        """This is the common loop used inside expect. The 'searcher' should be
        an instance of searcher_re or searcher_string, which describes how and
        what to search for in the input.

        See expect() for other arguments, return value and exceptions. """
        self.searcher = searcher
        if timeout == -1:
            timeout = self.timeout
        if timeout is not None:
            end_time = time.time() + timeout
        try:
            incoming = self.buffer
            freshlen = len(incoming)
            while True:
                index = searcher.search(incoming, freshlen, searchwindowsize)
                if index >= 0:
                    self.buffer = incoming[searcher.end:]
                    self.before = incoming[:searcher.start]
                    self.after = incoming[searcher.start:searcher.end]
                    self.match = searcher.match
                    self.match_index = index
                    return self.match_index
                if timeout is not None and timeout < 0:
                    raise TIMEOUT('Timeout exceeded in expect_any().')
                c = self.read_nonblocking(2048, timeout)
                freshlen = len(c)
                time.sleep(0.0001)
                incoming = incoming + c
                if timeout is not None:
                    timeout = end_time - time.time()

        except EOF:
            err = sys.exc_info()[1]
            self.buffer = str()
            self.before = incoming
            self.after = EOF
            index = searcher.eof_index
            if index >= 0:
                self.match = EOF
                self.match_index = index
                return self.match_index
            self.match = None
            self.match_index = None
            raise EOF(str(err) + '\n' + str(self))
        except TIMEOUT:
            err = sys.exc_info()[1]
            self.buffer = incoming
            self.before = incoming
            self.after = TIMEOUT
            index = searcher.timeout_index
            if index >= 0:
                self.match = TIMEOUT
                self.match_index = index
                return self.match_index
            self.match = None
            self.match_index = None
            raise TIMEOUT(str(err) + '\n' + str(self))
        except:
            self.before = incoming
            self.after = None
            self.match = None
            self.match_index = None
            raise

        return

    def _pattern_type_err(self, pattern):
        raise TypeError(('got {badtype} ({badobj!r}) as pattern, must be one of: {goodtypes}, pexpect.EOF, pexpect.TIMEOUT').format(badtype=type(pattern), badobj=pattern, goodtypes=(', ').join([ str(ast) for ast in basestring
                                                                                                                                                                                                 ])))

    def compile_pattern_list(self, patterns):
        """This compiles a pattern-string or a list of pattern-strings.
        Patterns must be a StringType, EOF, TIMEOUT, SRE_Pattern, or a list of
        those. Patterns may also be None which results in an empty list (you
        might do this if waiting for an EOF or TIMEOUT condition without
        expecting any pattern).

        This is used by expect() when calling expect_list(). Thus expect() is
        nothing more than::

             cpl = self.compile_pattern_list(pl)
             return self.expect_list(cpl, timeout)

        If you are using expect() within a loop it may be more
        efficient to compile the patterns first and then call expect_list().
        This avoid calls in a loop to compile_pattern_list()::

             cpl = self.compile_pattern_list(my_pattern)
             while some_condition:
                ...
                i = self.expect_list(clp, timeout)
                ...
        """
        if patterns is None:
            return []
        else:
            if not isinstance(patterns, list):
                patterns = [
                 patterns]
            compile_flags = re.DOTALL
            if self.ignorecase:
                compile_flags = compile_flags | re.IGNORECASE
            compiled_pattern_list = []
            for idx, p in enumerate(patterns):
                if isinstance(p, basestring):
                    compiled_pattern_list.append(re.compile(p, compile_flags))
                elif p is EOF:
                    compiled_pattern_list.append(EOF)
                elif p is TIMEOUT:
                    compiled_pattern_list.append(TIMEOUT)
                elif isinstance(p, type(re.compile(''))):
                    compiled_pattern_list.append(p)
                else:
                    self._pattern_type_err(p)

            return compiled_pattern_list

    def _read(self, size):
        if self.mode() == PROCESS:
            return os.read(self.rfd, size)
        try:
            return self.sock.recv(size)
        except socket.error as err:
            if err.args[0] == errno.ECONNRESET:
                raise EOF('Connection reset by peer')
            raise err

    def _write(self, s):
        if self.mode() == PROCESS:
            return os.write(self.wfd, s)
        else:
            self.sock.sendall(s)
            return len(s)

    def read_nonblocking(self, size=1, timeout=-1):
        """This reads at most size characters from the child application. It
        includes a timeout. If the read does not complete within the timeout
        period then a TIMEOUT exception is raised. If the end of file is read
        then an EOF exception will be raised.

        If timeout is None then the read may block indefinitely.
        If timeout is -1 then the self.timeout value is used. If timeout is 0
        then the child is polled and if there is no data immediately ready
        then this will raise a TIMEOUT exception.

        The timeout refers only to the amount of time to read at least one
        character. This is not effected by the 'size' parameter, so if you call
        read_nonblocking(size=100, timeout=30) and only one character is
        available right away then one character will be returned immediately.
        It will not wait for 30 seconds for another 99 characters to come in.

        This is a wrapper around os.read(). It uses select.select() to
        implement the timeout. """
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        if timeout == -1:
            timeout = self.timeout
        if not self.isalive():
            r, w, e = self.__select([self.rfd], [], [], 0)
            if not r:
                self.flag_eof = True
                raise EOF('End Of File (EOF). Braindead platform.')
        if timeout is not None and timeout > 0:
            end_time = time.time() + timeout
        else:
            end_time = float('inf')
        readfds = [self.rfd]
        if self.mode() == PROCESS:
            try:
                os.fstat(self.wfd)
                readfds.append(self.wfd)
            except:
                pass

        while True:
            now = time.time()
            if now > end_time:
                break
            if timeout is not None and timeout > 0:
                timeout = end_time - now
            r, w, e = self.__select(readfds, [], [], timeout)
            if not r:
                if not self.isalive():
                    self.flag_eof = True
                    raise EOF('End of File (EOF). Very slow platform.')
                else:
                    continue
            if self.mode() == PROCESS:
                try:
                    if self.wfd in r:
                        data = os.read(self.wfd, 1024)
                        if data and self.print_read:
                            stdout(self._print_read(data))
                except OSError as err:
                    pass

            if self.rfd in r:
                try:
                    s = self._read(size)
                    if s and self.print_read:
                        stdout(self._print_read(s))
                except OSError:
                    self.flag_eof = True
                    raise EOF('End Of File (EOF). Exception style platform.')
                else:
                    if s == '':
                        self.flag_eof = True
                        raise EOF('End Of File (EOF). Empty string style platform.')
                    return s

        raise TIMEOUT('Timeout exceeded. size to read: %d' % size)
        return

    def gdb_hint(self, breakpoints=None, relative=None, extras=None):
        if self.mode() == SOCKET:
            pid = pidof_socket(self.sock)
        else:
            pid = self.pid
        if not pid:
            raw_input(colored('[ WARN ] pid unavailable to attach gdb, please find out the pid by your own', 'yellow'))
            return
        hints = ['attach %d' % pid]
        base = 0
        if relative:
            vmmap = open('/proc/%d/maps' % pid).read()
            for line in vmmap.splitlines():
                if line.lower().find(relative.lower()) > -1:
                    base = int(line.split('-')[0], 16)
                    break

        if breakpoints:
            for b in breakpoints:
                hints.append('b *' + hex(base + b))

        if extras:
            for e in extras:
                hints.append(str(e))

        gdb = colored('zio -l 0.5 -b "For help" -a "`printf \'' + ('\\r\\n').join(hints) + '\\r\\n\'`" gdb', 'magenta') + '\nuse cmdline above to attach gdb then press enter to continue ... '
        raw_input(gdb)

    def _not_impl(self):
        raise NotImplementedError('Not Implemented')

    read_after = read_before = read_between = read_range = _not_impl


class searcher_string(object):
    """This is a plain string search helper for the spawn.expect_any() method.
    This helper class is for speed. For more powerful regex patterns
    see the helper class, searcher_re.

    Attributes:

        eof_index     - index of EOF, or -1
        timeout_index - index of TIMEOUT, or -1

    After a successful match by the search() method the following attributes
    are available:

        start - index into the buffer, first byte of match
        end   - index into the buffer, first byte after match
        match - the matching string itself

    """

    def __init__(self, strings):
        """This creates an instance of searcher_string. This argument 'strings'
        may be a list; a sequence of strings; or the EOF or TIMEOUT types. """
        self.eof_index = -1
        self.timeout_index = -1
        self._strings = []
        for n, s in enumerate(strings):
            if s is EOF:
                self.eof_index = n
                continue
            if s is TIMEOUT:
                self.timeout_index = n
                continue
            self._strings.append((n, s))

    def __str__(self):
        """This returns a human-readable string that represents the state of
        the object."""
        ss = [ (ns[0], '    %d: "%s"' % ns) for ns in self._strings ]
        ss.append((-1, 'searcher_string:'))
        if self.eof_index >= 0:
            ss.append((self.eof_index, '    %d: EOF' % self.eof_index))
        if self.timeout_index >= 0:
            ss.append((self.timeout_index,
             '    %d: TIMEOUT' % self.timeout_index))
        ss.sort()
        ss = list(zip(*ss))[1]
        return ('\n').join(ss)

    def search(self, buffer, freshlen, searchwindowsize=None):
        """This searches 'buffer' for the first occurence of one of the search
        strings.  'freshlen' must indicate the number of bytes at the end of
        'buffer' which have not been searched before. It helps to avoid
        searching the same, possibly big, buffer over and over again.

        See class spawn for the 'searchwindowsize' argument.

        If there is a match this returns the index of that string, and sets
        'start', 'end' and 'match'. Otherwise, this returns -1. """
        first_match = None
        for index, s in self._strings:
            if searchwindowsize is None:
                offset = -(freshlen + len(s))
            else:
                offset = -searchwindowsize
            n = buffer.find(s, offset)
            if n >= 0 and (first_match is None or n < first_match):
                first_match = n
                best_index, best_match = index, s

        if first_match is None:
            return -1
        else:
            self.match = best_match
            self.start = first_match
            self.end = self.start + len(self.match)
            return best_index


class searcher_re(object):
    """This is regular expression string search helper for the
    spawn.expect_any() method. This helper class is for powerful
    pattern matching. For speed, see the helper class, searcher_string.

    Attributes:

        eof_index     - index of EOF, or -1
        timeout_index - index of TIMEOUT, or -1

    After a successful match by the search() method the following attributes
    are available:

        start - index into the buffer, first byte of match
        end   - index into the buffer, first byte after match
        match - the re.match object returned by a succesful re.search

    """

    def __init__(self, patterns):
        """This creates an instance that searches for 'patterns' Where
        'patterns' may be a list or other sequence of compiled regular
        expressions, or the EOF or TIMEOUT types."""
        self.eof_index = -1
        self.timeout_index = -1
        self._searches = []
        for n, s in zip(list(range(len(patterns))), patterns):
            if s is EOF:
                self.eof_index = n
                continue
            if s is TIMEOUT:
                self.timeout_index = n
                continue
            self._searches.append((n, s))

    def __str__(self):
        """This returns a human-readable string that represents the state of
        the object."""
        ss = list()
        for n, s in self._searches:
            try:
                ss.append((n, '    %d: re.compile("%s")' % (n, s.pattern)))
            except UnicodeEncodeError:
                ss.append((n, '    %d: re.compile(%r)' % (n, s.pattern)))

        ss.append((-1, 'searcher_re:'))
        if self.eof_index >= 0:
            ss.append((self.eof_index, '    %d: EOF' % self.eof_index))
        if self.timeout_index >= 0:
            ss.append((self.timeout_index,
             '    %d: TIMEOUT' % self.timeout_index))
        ss.sort()
        ss = list(zip(*ss))[1]
        return ('\n').join(ss)

    def search(self, buffer, freshlen, searchwindowsize=None):
        """This searches 'buffer' for the first occurence of one of the regular
        expressions. 'freshlen' must indicate the number of bytes at the end of
        'buffer' which have not been searched before.

        See class spawn for the 'searchwindowsize' argument.

        If there is a match this returns the index of that string, and sets
        'start', 'end' and 'match'. Otherwise, returns -1."""
        first_match = None
        if searchwindowsize is None:
            searchstart = 0
        else:
            searchstart = max(0, len(buffer) - searchwindowsize)
        for index, s in self._searches:
            match = s.search(buffer, searchstart)
            if match is None:
                continue
            n = match.start()
            if first_match is None or n < first_match:
                first_match = n
                the_match = match
                best_index = index

        if first_match is None:
            return -1
        else:
            self.start = first_match
            self.match = the_match
            self.end = self.match.end()
            return best_index


def which(filename):
    """This takes a given filename; tries to find it in the environment path;
    then checks if it is executable. This returns the full path to the filename
    if found and executable. Otherwise this returns None."""
    if os.path.dirname(filename) != '':
        if os.access(filename, os.X_OK):
            return filename
    if 'PATH' not in os.environ or os.environ['PATH'] == '':
        p = os.defpath
    else:
        p = os.environ['PATH']
    pathlist = p.split(os.pathsep)
    for path in pathlist:
        ff = os.path.join(path, filename)
        if os.access(ff, os.X_OK):
            return ff

    return


def split_command_line(command_line):
    """This splits a command line into a list of arguments. It splits arguments
    on spaces, but handles embedded quotes, doublequotes, and escaped
    characters. It's impossible to do this with a regular expression, so I
    wrote a little state machine to parse the command line. """
    arg_list = []
    arg = ''
    state_basic = 0
    state_esc = 1
    state_singlequote = 2
    state_doublequote = 3
    state_whitespace = 4
    state = state_basic
    for c in command_line:
        if state == state_basic or state == state_whitespace:
            if c == '\\':
                state = state_esc
            elif c == "'":
                state = state_singlequote
            elif c == '"':
                state = state_doublequote
            elif c.isspace():
                if state == state_whitespace:
                    None
                else:
                    arg_list.append(arg)
                    arg = ''
                    state = state_whitespace
            else:
                arg = arg + c
                state = state_basic
        elif state == state_esc:
            arg = arg + c
            state = state_basic
        elif state == state_singlequote:
            if c == "'":
                state = state_basic
            else:
                arg = arg + c
        elif state == state_doublequote:
            if c == '"':
                state = state_basic
            else:
                arg = arg + c

    if arg != '':
        arg_list.append(arg)
    return arg_list


def all_pids():
    return [ int(pid) for pid in os.listdir('/proc') if pid.isdigit() ]


def pidof_socket(prog):

    def toaddr((host, port)):
        return '%08X:%04X' % (l32(socket.inet_aton(host)), port)

    def getpid(loc, rem):
        loc = toaddr(loc)
        rem = toaddr(rem)
        inode = 0
        with open('/proc/net/tcp') as (fd):
            for line in fd:
                line = line.split()
                if line[1] == loc and line[2] == rem:
                    inode = line[9]

        if inode == 0:
            return []
        for pid in all_pids():
            try:
                for fd in os.listdir('/proc/%d/fd' % pid):
                    fd = os.readlink('/proc/%d/fd/%s' % (pid, fd))
                    m = re.match('socket:\\[(\\d+)\\]', fd)
                    if m:
                        this_inode = m.group(1)
                        if this_inode == inode:
                            return pid

            except:
                pass

    sock = prog.getsockname()
    peer = prog.getpeername()
    pids = [getpid(peer, sock), getpid(sock, peer)]
    if pids[0]:
        return pids[0]
    else:
        if pids[1]:
            return pids[1]
        return


def hostport_tuple(target):

    def _check_host(host):
        try:
            socket.gethostbyname(host)
            return True
        except:
            return False

    return type(target) == tuple and len(target) == 2 and isinstance(target[1], (int, long)) and target[1] >= 0 and target[1] < 65536 and _check_host(target[0])


def usage():
    print '\nusage:\n\n    $ zio [options] cmdline | host port\n\noptions:\n\n    -h, --help              help page, you are reading this now!\n    -i, --stdin             tty|pipe, specify tty or pipe stdin, default to tty\n    -o, --stdout            tty|pipe, specify tty or pipe stdout, default to tty\n    -t, --timeout           integer seconds, specify timeout\n    -r, --read              how to print out content read from child process, may be RAW(True), NONE(False), REPR, HEX\n    -w, --write             how to print out content written to child process, may be RAW(True), NONE(False), REPR, HEX\n    -a, --ahead             message to feed into stdin before interact\n    -b, --before            don\'t do anything before reading those input\n    -d, --decode            when in interact mode, this option can be used to specify decode function REPR/HEX to input raw hex bytes\n    -l, --delay             write delay, time to wait before write\n\nexamples:\n\n    $ zio -h\n        you are reading this help message\n\n    $ zio [-t seconds] [-i [tty|pipe]] [-o [tty|pipe]] "cmdline -x opts and args"\n        spawning process and interact with it\n\n    $ zio [-t seconds] host port\n        zio becomes a netcat\n\n    $ zio tty\n    $ zio cat\n    $ zio vim\n    $ zio ssh -p 22 root@127.0.0.1\n    $ zio xxd\n    $ zio 127.1 22                 # WOW! you can talk with sshd by hand!\n    $ zio -i pipe ssh root@127.1   # you must be crazy to do this!\n'


def cmdline(argv):
    import getopt
    try:
        opts, args = getopt.getopt(argv, 'hi:o:t:r:w:d:a:b:l:', ['help', 'stdin=', 'stdout=', 'timeout=', 'read=', 'write=', 'decode=', 'ahead=', 'before=', 'debug=', 'delay='])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(10)

    kwargs = {'stdin': TTY, 
       'stdout': TTY}
    decode = None
    ahead = None
    before = None
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif o in ('-i', '--stdin'):
            if a.lower() == TTY.lower():
                kwargs['stdin'] = TTY
            elif a.lower() == TTY_RAW.lower():
                kwargs['stdin'] = TTY_RAW
            else:
                kwargs['stdin'] = PIPE
        elif o in ('-o', '--stdout'):
            if a.lower() == PIPE.lower():
                kwargs['stdout'] = PIPE
            elif a.lower() == TTY_RAW.lower():
                kwargs['stdout'] = TTY_RAW
            else:
                kwargs['stdout'] = TTY
        elif o in ('-t', '--timeout'):
            try:
                kwargs['timeout'] = int(a)
            except:
                usage()
                sys.exit(11)

        elif o in ('-r', '--read'):
            if a.lower() == 'hex':
                kwargs['print_read'] = COLORED(HEX, 'yellow')
            elif a.lower() == 'repr':
                kwargs['print_read'] = COLORED(REPR, 'yellow')
            elif a.lower() == 'none':
                kwargs['print_read'] = NONE
            else:
                kwargs['print_read'] = RAW
        elif o in ('-w', '--write'):
            if a.lower() == 'hex':
                kwargs['print_write'] = COLORED(HEX, 'cyan')
            elif a.lower() == 'repr':
                kwargs['print_write'] = COLORED(REPR, 'cyan')
            elif a.lower() == 'none':
                kwargs['print_write'] = NONE
            else:
                kwargs['print_write'] = RAW
        elif o in ('-d', '--decode'):
            if a.lower() == 'eval':
                decode = EVAL
            elif a.lower() == 'unhex':
                decode = UNHEX
        elif o in ('-a', '--ahead'):
            ahead = a
        elif o in ('-b', '--before'):
            before = a
        elif o in ('--debug', ):
            kwargs['debug'] = open(a, 'w')
        elif o in ('-l', '--delay'):
            kwargs['write_delay'] = float(a)

    target = None
    if len(args) == 2:
        try:
            port = int(args[1])
            if hostport_tuple((args[0], port)):
                target = (
                 args[0], port)
        except:
            pass

    if not target:
        if len(args) == 1:
            target = args[0]
        else:
            target = args
    io = zio(target, **kwargs)
    if before:
        io.read_until(before)
    if ahead:
        io.write(ahead)
    io.interact(input_filter=decode, raw_rw=False)
    return


def main():
    if len(sys.argv) >= 2:
        test = sys.argv[1]
    else:
        usage()
        sys.exit(0)
    cmdline(sys.argv[1:])


if __name__ == '__main__':
    main()