# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahal/.pyenv/versions/3.7.4/lib/python3.7/site-packages/mozprocess/processhandler.py
# Compiled at: 2019-12-02 09:22:55
# Size of source mod 2**32: 51675 bytes
from __future__ import absolute_import, print_function
import errno, os, signal, subprocess, sys, threading, traceback
from datetime import datetime
import six, time
if six.PY2:
    from Queue import Queue, Empty
else:
    from queue import Queue, Empty
__all__ = [
 'ProcessHandlerMixin', 'ProcessHandler', 'LogOutput',
 'StoreOutput', 'StreamOutput']
MOZPROCESS_DEBUG = os.getenv('MOZPROCESS_DEBUG')
INTERVAL_PROCESS_ALIVE_CHECK = 0.02
isWin = os.name == 'nt'
isPosix = os.name == 'posix'
if isWin:
    from ctypes import sizeof, addressof, c_ulong, byref, WinError, c_longlong
    from . import winprocess
    from .qijo import JobObjectAssociateCompletionPortInformation, JOBOBJECT_ASSOCIATE_COMPLETION_PORT, JobObjectExtendedLimitInformation, JOBOBJECT_BASIC_LIMIT_INFORMATION, JOBOBJECT_EXTENDED_LIMIT_INFORMATION, IO_COUNTERS

class ProcessHandlerMixin(object):
    __doc__ = '\n    A class for launching and manipulating local processes.\n\n    :param cmd: command to run. May be a string or a list. If specified as a list, the first\n      element will be interpreted as the command, and all additional elements will be interpreted\n      as arguments to that command.\n    :param args: list of arguments to pass to the command (defaults to None). Must not be set when\n      `cmd` is specified as a list.\n    :param cwd: working directory for command (defaults to None).\n    :param env: is the environment to use for the process (defaults to os.environ).\n    :param ignore_children: causes system to ignore child processes when True,\n      defaults to False (which tracks child processes).\n    :param kill_on_timeout: when True, the process will be killed when a timeout is reached.\n      When False, the caller is responsible for killing the process.\n      Failure to do so could cause a call to wait() to hang indefinitely. (Defaults to True.)\n    :param processOutputLine: function or list of functions to be called for\n        each line of output produced by the process (defaults to an empty\n        list).\n    :param processStderrLine: function or list of functions to be called\n        for each line of error output - stderr - produced by the process\n        (defaults to an empty list). If this is not specified, stderr lines\n        will be sent to the *processOutputLine* callbacks.\n    :param onTimeout: function or list of functions to be called when the process times out.\n    :param onFinish: function or list of functions to be called when the process terminates\n      normally without timing out.\n    :param kwargs: additional keyword args to pass directly into Popen.\n\n    NOTE: Child processes will be tracked by default.  If for any reason\n    we are unable to track child processes and ignore_children is set to False,\n    then we will fall back to only tracking the root process.  The fallback\n    will be logged.\n    '

    class Process(subprocess.Popen):
        __doc__ = '\n        Represents our view of a subprocess.\n        It adds a kill() method which allows it to be stopped explicitly.\n        '
        MAX_IOCOMPLETION_PORT_NOTIFICATION_DELAY = 180
        MAX_PROCESS_KILL_DELAY = 30
        TIMEOUT_BEFORE_SIGKILL = 1.0

        def __init__(self, args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0, ignore_children=False):
            self._ignore_children = ignore_children
            if not self._ignore_children:
                if not isWin:

                    def setpgidfn():
                        os.setpgid(0, 0)

                    preexec_fn = setpgidfn
            try:
                subprocess.Popen.__init__(self, args, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell, cwd, env, universal_newlines, startupinfo, creationflags)
            except OSError:
                print(args, file=(sys.stderr))
                raise

        def debug(self, msg):
            if not MOZPROCESS_DEBUG:
                return
            thread = threading.current_thread().name
            print('DBG::MOZPROC PID:{} ({}) | {}'.format(self.pid, thread, msg))

        def __del__--- This code section failed: ---

 L. 135         0  LOAD_GLOBAL              isWin
                2  POP_JUMP_IF_FALSE    78  'to 78'

 L. 136         4  LOAD_GLOBAL              six
                6  LOAD_ATTR                PY2
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 137        10  LOAD_GLOBAL              sys
               12  LOAD_ATTR                maxint
               14  STORE_FAST               '_maxint'
               16  JUMP_FORWARD         24  'to 24'
             18_0  COME_FROM             8  '8'

 L. 139        18  LOAD_GLOBAL              sys
               20  LOAD_ATTR                maxsize
               22  STORE_FAST               '_maxint'
             24_0  COME_FROM            16  '16'

 L. 140        24  LOAD_GLOBAL              getattr
               26  LOAD_FAST                'self'
               28  LOAD_STR                 '_handle'
               30  LOAD_CONST               None
               32  CALL_FUNCTION_3       3  '3 positional arguments'
               34  STORE_FAST               'handle'

 L. 141        36  LOAD_FAST                'handle'
               38  POP_JUMP_IF_FALSE    52  'to 52'

 L. 142        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _internal_poll
               44  LOAD_FAST                '_maxint'
               46  LOAD_CONST               ('_deadstate',)
               48  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               50  POP_TOP          
             52_0  COME_FROM            38  '38'

 L. 143        52  LOAD_FAST                'handle'
               54  POP_JUMP_IF_TRUE     68  'to 68'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                _job
               60  POP_JUMP_IF_TRUE     68  'to 68'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _io_port
               66  POP_JUMP_IF_FALSE    90  'to 90'
             68_0  COME_FROM            60  '60'
             68_1  COME_FROM            54  '54'

 L. 144        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _cleanup
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  POP_TOP          
               76  JUMP_FORWARD         90  'to 90'
             78_0  COME_FROM             2  '2'

 L. 146        78  LOAD_GLOBAL              subprocess
               80  LOAD_ATTR                Popen
               82  LOAD_METHOD              __del__
               84  LOAD_FAST                'self'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  POP_TOP          
             90_0  COME_FROM            76  '76'
             90_1  COME_FROM            66  '66'

Parse error at or near `COME_FROM' instruction at offset 78_0

        def kill(self, sig=None):
            if isWin:
                try:
                    if (self._ignore_children or self)._handle and self._job:
                        self.debug('calling TerminateJobObject')
                        winprocess.TerminateJobObject(self._job, winprocess.ERROR_CONTROL_C_EXIT)
                    else:
                        if self._handle:
                            self.debug('calling TerminateProcess')
                            winprocess.TerminateProcess(self._handle, winprocess.ERROR_CONTROL_C_EXIT)
                except WindowsError:
                    self._cleanup()
                    traceback.print_exc()
                    raise OSError('Could not terminate process')

            else:

                def send_sig(sig, retries=0):
                    pid = self.detached_pid or self.pid
                    if not self._ignore_children:
                        try:
                            os.killpg(pid, sig)
                        except BaseException as e:
                            try:
                                if retries < 1:
                                    if getattr(e, 'errno', None) == errno.EPERM:
                                        try:
                                            os.waitpid(-pid, 0)
                                        finally:
                                            return

                                        return send_sig(sig, retries + 1)
                                if getattr(e, 'errno', None) != errno.ESRCH:
                                    print(('Could not terminate process: %s' % self.pid),
                                      file=(sys.stderr))
                                    raise
                            finally:
                                e = None
                                del e

                    else:
                        os.kill(pid, sig)

                if sig is None and isPosix:
                    send_sig(signal.SIGTERM)
                    limit = time.time() + self.TIMEOUT_BEFORE_SIGKILL
                    while time.time() <= limit:
                        if self.poll() is not None:
                            break
                        time.sleep(INTERVAL_PROCESS_ALIVE_CHECK)

                    send_sig(signal.SIGKILL)
                else:
                    send_sig(sig or signal.SIGKILL)
            self.returncode = self.wait()
            self._cleanup()
            return self.returncode

        def poll(self):
            """ Popen.poll
                Check if child process has terminated. Set and return returncode attribute.
            """
            if isWin:
                if getattr(self, '_handle', None):
                    return
            return subprocess.Popen.poll(self)

        def wait(self, timeout=None):
            """ Popen.wait
                Called to wait for a running process to shut down and return
                its exit code
                Returns the main process's exit code
            """
            self.returncode = self._custom_wait(timeout=timeout)
            self._cleanup()
            return self.returncode

        if isWin:

            def _execute_child(self, *args_tuple):
                if six.PY3:
                    args, executable, preexec_fn, close_fds, pass_fds, cwd, env, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite, restore_signals, start_new_session = args_tuple
                else:
                    if sys.hexversion < 34014720:
                        args, executable, preexec_fn, close_fds, cwd, env, universal_newlines, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite = args_tuple
                        to_close = set()
                    else:
                        args, executable, preexec_fn, close_fds, cwd, env, universal_newlines, startupinfo, creationflags, shell, to_close, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite = args_tuple
                if not isinstance(args, six.string_types):
                    args = subprocess.list2cmdline(args)
                creationflags |= winprocess.CREATE_NEW_PROCESS_GROUP
                if startupinfo is None:
                    startupinfo = winprocess.STARTUPINFO()
                if None not in (p2cread, c2pwrite, errwrite):
                    startupinfo.dwFlags |= winprocess.STARTF_USESTDHANDLES
                    startupinfo.hStdInput = int(p2cread)
                    startupinfo.hStdOutput = int(c2pwrite)
                    startupinfo.hStdError = int(errwrite)
                if shell:
                    startupinfo.dwFlags |= winprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = winprocess.SW_HIDE
                    comspec = os.environ.get('COMSPEC', 'cmd.exe')
                    args = comspec + ' /c ' + args
                else:
                    can_create_job = winprocess.CanCreateJobObject()
                    can_nest_jobs = self._can_nest_jobs()
                    if not can_create_job:
                        if not can_nest_jobs:
                            if not self._ignore_children:
                                print('ProcessManager UNABLE to use job objects to manage child processes', file=(sys.stderr))
                    creationflags |= winprocess.CREATE_SUSPENDED
                    creationflags |= winprocess.CREATE_UNICODE_ENVIRONMENT
                    if can_create_job:
                        creationflags |= winprocess.CREATE_BREAKAWAY_FROM_JOB
                    elif not can_create_job:
                        if not can_nest_jobs:
                            print('ProcessManager NOT managing child processes')
                    else:
                        hp, ht, pid, tid = winprocess.CreateProcess(executable, args, None, None, 1, creationflags, winprocess.EnvironmentBlock(env), cwd, startupinfo)
                        self._child_created = True
                        self._handle = hp
                        self._thread = ht
                        self.pid = pid
                        self.tid = tid
                        if self._ignore_children or can_create_job or can_nest_jobs:
                            try:
                                self._io_port = winprocess.CreateIoCompletionPort()
                                self._job = winprocess.CreateJobObject()
                                joacp = JOBOBJECT_ASSOCIATE_COMPLETION_PORT(winprocess.COMPKEY_JOBOBJECT, self._io_port)
                                winprocess.SetInformationJobObject(self._job, JobObjectAssociateCompletionPortInformation, addressof(joacp), sizeof(joacp))
                                limit_flags = winprocess.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
                                if not can_nest_jobs:
                                    limit_flags |= winprocess.JOB_OBJECT_LIMIT_BREAKAWAY_OK
                                jbli = JOBOBJECT_BASIC_LIMIT_INFORMATION(c_longlong(0), c_longlong(0), limit_flags, 0, 0, 0, None, 0, 0)
                                iocntr = IO_COUNTERS()
                                jeli = JOBOBJECT_EXTENDED_LIMIT_INFORMATION(jbli, iocntr, 0, 0, 0, 0)
                                winprocess.SetInformationJobObject(self._job, JobObjectExtendedLimitInformation, addressof(jeli), sizeof(jeli))
                                winprocess.AssignProcessToJobObject(self._job, int(hp))
                                self._process_events = Queue()
                                self._procmgrthread = threading.Thread(target=(self._procmgr))
                            except Exception:
                                print('Exception trying to use job objects;\nfalling back to not using job objects for managing child processes',
                                  file=(sys.stderr))
                                tb = traceback.format_exc()
                                print(tb, file=(sys.stderr))
                                self._cleanup_job_io_port()

                    self._job = None
                winprocess.ResumeThread(int(ht))
                if getattr(self, '_procmgrthread', None):
                    self._procmgrthread.start()
                ht.Close()
                for i in (p2cread, c2pwrite, errwrite):
                    if i is not None:
                        i.Close()

            def _can_nest_jobs(self):
                winver = sys.getwindowsversion()
                return winver.major > 6 or winver.major == 6 and winver.minor >= 2

            def _procmgr(self):
                return self._io_port and self._job or None
                try:
                    self._poll_iocompletion_port()
                except KeyboardInterrupt:
                    raise KeyboardInterrupt

            def _poll_iocompletion_port--- This code section failed: ---

 L. 422         0  BUILD_MAP_0           0 
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _spawned_procs

 L. 423         6  LOAD_CONST               0
                8  STORE_FAST               'countdowntokill'

 L. 425        10  LOAD_FAST                'self'
               12  LOAD_METHOD              debug
               14  LOAD_STR                 'start polling IO completion port'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  POP_TOP          

 L. 427     20_22  SETUP_LOOP          688  'to 688'
             24_0  COME_FROM           370  '370'

 L. 428        24  LOAD_GLOBAL              c_ulong
               26  LOAD_CONST               0
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  STORE_FAST               'msgid'

 L. 429        32  LOAD_GLOBAL              c_ulong
               34  LOAD_CONST               0
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  STORE_FAST               'compkey'

 L. 430        40  LOAD_GLOBAL              c_ulong
               42  LOAD_CONST               0
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  STORE_FAST               'pid'

 L. 431        48  LOAD_GLOBAL              winprocess
               50  LOAD_METHOD              GetQueuedCompletionStatus
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _io_port

 L. 432        56  LOAD_GLOBAL              byref
               58  LOAD_FAST                'msgid'
               60  CALL_FUNCTION_1       1  '1 positional argument'

 L. 433        62  LOAD_GLOBAL              byref
               64  LOAD_FAST                'compkey'
               66  CALL_FUNCTION_1       1  '1 positional argument'

 L. 434        68  LOAD_GLOBAL              byref
               70  LOAD_FAST                'pid'
               72  CALL_FUNCTION_1       1  '1 positional argument'

 L. 435        74  LOAD_CONST               5000
               76  CALL_METHOD_5         5  '5 positional arguments'
               78  STORE_FAST               'portstatus'

 L. 439        80  LOAD_FAST                'countdowntokill'
               82  LOAD_CONST               0
               84  COMPARE_OP               !=
               86  POP_JUMP_IF_FALSE   224  'to 224'

 L. 440        88  LOAD_GLOBAL              datetime
               90  LOAD_METHOD              now
               92  CALL_METHOD_0         0  '0 positional arguments'
               94  LOAD_FAST                'countdowntokill'
               96  BINARY_SUBTRACT  
               98  STORE_FAST               'diff'

 L. 446       100  LOAD_FAST                'diff'
              102  LOAD_ATTR                seconds
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                MAX_IOCOMPLETION_PORT_NOTIFICATION_DELAY
              108  COMPARE_OP               >
              110  POP_JUMP_IF_FALSE   224  'to 224'

 L. 447       112  LOAD_GLOBAL              print
              114  LOAD_STR                 'WARNING | IO Completion Port failed to signal process shutdown'

 L. 448       116  LOAD_GLOBAL              sys
              118  LOAD_ATTR                stderr
              120  LOAD_CONST               ('file',)
              122  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              124  POP_TOP          

 L. 449       126  LOAD_GLOBAL              print
              128  LOAD_STR                 'Parent process %s exited with children alive:'

 L. 450       130  LOAD_FAST                'self'
              132  LOAD_ATTR                pid
              134  BINARY_MODULO    
              136  LOAD_GLOBAL              sys
              138  LOAD_ATTR                stderr
              140  LOAD_CONST               ('file',)
              142  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              144  POP_TOP          

 L. 451       146  LOAD_GLOBAL              print
              148  LOAD_STR                 'PIDS: %s'
              150  LOAD_STR                 ', '
              152  LOAD_METHOD              join
              154  LOAD_LISTCOMP            '<code_object <listcomp>>'
              156  LOAD_STR                 'ProcessHandlerMixin.Process._poll_iocompletion_port.<locals>.<listcomp>'
              158  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                _spawned_procs
              164  GET_ITER         
              166  CALL_FUNCTION_1       1  '1 positional argument'
              168  CALL_METHOD_1         1  '1 positional argument'
              170  BINARY_MODULO    

 L. 452       172  LOAD_GLOBAL              sys
              174  LOAD_ATTR                stderr
              176  LOAD_CONST               ('file',)
              178  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              180  POP_TOP          

 L. 453       182  LOAD_GLOBAL              print
              184  LOAD_STR                 'Attempting to kill them, but no guarantee of success'

 L. 454       186  LOAD_GLOBAL              sys
              188  LOAD_ATTR                stderr
              190  LOAD_CONST               ('file',)
              192  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              194  POP_TOP          

 L. 456       196  LOAD_FAST                'self'
              198  LOAD_METHOD              kill
              200  CALL_METHOD_0         0  '0 positional arguments'
              202  POP_TOP          

 L. 457       204  LOAD_FAST                'self'
              206  LOAD_ATTR                _process_events
              208  LOAD_METHOD              put
              210  LOAD_FAST                'self'
              212  LOAD_ATTR                pid
              214  LOAD_STR                 'FINISHED'
              216  BUILD_MAP_1           1 
              218  CALL_METHOD_1         1  '1 positional argument'
              220  POP_TOP          

 L. 458       222  BREAK_LOOP       
            224_0  COME_FROM           110  '110'
            224_1  COME_FROM            86  '86'

 L. 460       224  LOAD_FAST                'portstatus'
          226_228  POP_JUMP_IF_TRUE    330  'to 330'

 L. 462       230  LOAD_GLOBAL              winprocess
              232  LOAD_METHOD              GetLastError
              234  CALL_METHOD_0         0  '0 positional arguments'
              236  STORE_FAST               'errcode'

 L. 463       238  LOAD_FAST                'errcode'
              240  LOAD_GLOBAL              winprocess
              242  LOAD_ATTR                ERROR_ABANDONED_WAIT_0
              244  COMPARE_OP               ==
          246_248  POP_JUMP_IF_FALSE   286  'to 286'

 L. 465       250  LOAD_GLOBAL              print
              252  LOAD_STR                 'IO Completion Port unexpectedly closed'
              254  LOAD_GLOBAL              sys
              256  LOAD_ATTR                stderr
              258  LOAD_CONST               ('file',)
              260  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              262  POP_TOP          

 L. 466       264  LOAD_FAST                'self'
              266  LOAD_ATTR                _process_events
              268  LOAD_METHOD              put
              270  LOAD_FAST                'self'
              272  LOAD_ATTR                pid
              274  LOAD_STR                 'FINISHED'
              276  BUILD_MAP_1           1 
              278  CALL_METHOD_1         1  '1 positional argument'
              280  POP_TOP          

 L. 467       282  BREAK_LOOP       
              284  JUMP_FORWARD        330  'to 330'
            286_0  COME_FROM           246  '246'

 L. 468       286  LOAD_FAST                'errcode'
              288  LOAD_GLOBAL              winprocess
              290  LOAD_ATTR                WAIT_TIMEOUT
              292  COMPARE_OP               ==
          294_296  POP_JUMP_IF_FALSE   302  'to 302'

 L. 470       298  CONTINUE             24  'to 24'
              300  JUMP_FORWARD        330  'to 330'
            302_0  COME_FROM           294  '294'

 L. 472       302  LOAD_GLOBAL              print
              304  LOAD_STR                 'Error Code %s trying to query IO Completion Port, exiting'

 L. 473       306  LOAD_FAST                'errcode'
              308  BINARY_MODULO    
              310  LOAD_GLOBAL              sys
              312  LOAD_ATTR                stderr
              314  LOAD_CONST               ('file',)
              316  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              318  POP_TOP          

 L. 474       320  LOAD_GLOBAL              WinError
              322  LOAD_FAST                'errcode'
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  RAISE_VARARGS_1       1  'exception instance'

 L. 475       328  BREAK_LOOP       
            330_0  COME_FROM           300  '300'
            330_1  COME_FROM           284  '284'
            330_2  COME_FROM           226  '226'

 L. 477       330  LOAD_FAST                'compkey'
              332  LOAD_ATTR                value
              334  LOAD_GLOBAL              winprocess
              336  LOAD_ATTR                COMPKEY_TERMINATE
              338  LOAD_ATTR                value
              340  COMPARE_OP               ==
          342_344  POP_JUMP_IF_FALSE   358  'to 358'

 L. 478       346  LOAD_FAST                'self'
              348  LOAD_METHOD              debug
              350  LOAD_STR                 'compkeyterminate detected'
              352  CALL_METHOD_1         1  '1 positional argument'
              354  POP_TOP          

 L. 480       356  BREAK_LOOP       
            358_0  COME_FROM           342  '342'

 L. 483       358  LOAD_FAST                'compkey'
              360  LOAD_ATTR                value
              362  LOAD_GLOBAL              winprocess
              364  LOAD_ATTR                COMPKEY_JOBOBJECT
              366  LOAD_ATTR                value
              368  COMPARE_OP               ==
              370  POP_JUMP_IF_FALSE    24  'to 24'

 L. 484       372  LOAD_FAST                'msgid'
              374  LOAD_ATTR                value
              376  LOAD_GLOBAL              winprocess
              378  LOAD_ATTR                JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO
              380  COMPARE_OP               ==
          382_384  POP_JUMP_IF_FALSE   418  'to 418'

 L. 487       386  LOAD_FAST                'self'
              388  LOAD_METHOD              debug
              390  LOAD_STR                 'job object msg active processes zero'
              392  CALL_METHOD_1         1  '1 positional argument'
              394  POP_TOP          

 L. 488       396  LOAD_FAST                'self'
              398  LOAD_ATTR                _process_events
              400  LOAD_METHOD              put
              402  LOAD_FAST                'self'
              404  LOAD_ATTR                pid
              406  LOAD_STR                 'FINISHED'
              408  BUILD_MAP_1           1 
              410  CALL_METHOD_1         1  '1 positional argument'
              412  POP_TOP          

 L. 489       414  BREAK_LOOP       
              416  JUMP_BACK            24  'to 24'
            418_0  COME_FROM           382  '382'

 L. 490       418  LOAD_FAST                'msgid'
              420  LOAD_ATTR                value
              422  LOAD_GLOBAL              winprocess
              424  LOAD_ATTR                JOB_OBJECT_MSG_NEW_PROCESS
              426  COMPARE_OP               ==
          428_430  POP_JUMP_IF_FALSE   476  'to 476'

 L. 494       432  LOAD_FAST                'pid'
              434  LOAD_ATTR                value
              436  LOAD_FAST                'self'
              438  LOAD_ATTR                pid
              440  COMPARE_OP               !=
          442_444  POP_JUMP_IF_FALSE   684  'to 684'

 L. 495       446  LOAD_CONST               1
              448  LOAD_FAST                'self'
              450  LOAD_ATTR                _spawned_procs
              452  LOAD_FAST                'pid'
              454  LOAD_ATTR                value
              456  STORE_SUBSCR     

 L. 496       458  LOAD_FAST                'self'
              460  LOAD_METHOD              debug
              462  LOAD_STR                 'new process detected with pid value: %s'
              464  LOAD_FAST                'pid'
              466  LOAD_ATTR                value
              468  BINARY_MODULO    
              470  CALL_METHOD_1         1  '1 positional argument'
              472  POP_TOP          
              474  JUMP_BACK            24  'to 24'
            476_0  COME_FROM           428  '428'

 L. 497       476  LOAD_FAST                'msgid'
              478  LOAD_ATTR                value
              480  LOAD_GLOBAL              winprocess
              482  LOAD_ATTR                JOB_OBJECT_MSG_EXIT_PROCESS
              484  COMPARE_OP               ==
          486_488  POP_JUMP_IF_FALSE   572  'to 572'

 L. 498       490  LOAD_FAST                'self'
              492  LOAD_METHOD              debug
              494  LOAD_STR                 'process id %s exited normally'
              496  LOAD_FAST                'pid'
              498  LOAD_ATTR                value
              500  BINARY_MODULO    
              502  CALL_METHOD_1         1  '1 positional argument'
              504  POP_TOP          

 L. 500       506  LOAD_FAST                'pid'
              508  LOAD_ATTR                value
              510  LOAD_FAST                'self'
              512  LOAD_ATTR                pid
              514  COMPARE_OP               ==
          516_518  POP_JUMP_IF_FALSE   546  'to 546'
              520  LOAD_GLOBAL              len
              522  LOAD_FAST                'self'
              524  LOAD_ATTR                _spawned_procs
              526  CALL_FUNCTION_1       1  '1 positional argument'
              528  LOAD_CONST               0
              530  COMPARE_OP               >
          532_534  POP_JUMP_IF_FALSE   546  'to 546'

 L. 502       536  LOAD_GLOBAL              datetime
              538  LOAD_METHOD              now
              540  CALL_METHOD_0         0  '0 positional arguments'
              542  STORE_FAST               'countdowntokill'
              544  JUMP_FORWARD        570  'to 570'
            546_0  COME_FROM           532  '532'
            546_1  COME_FROM           516  '516'

 L. 503       546  LOAD_FAST                'pid'
              548  LOAD_ATTR                value
              550  LOAD_FAST                'self'
              552  LOAD_ATTR                _spawned_procs
              554  COMPARE_OP               in
          556_558  POP_JUMP_IF_FALSE   684  'to 684'

 L. 505       560  LOAD_FAST                'self'
              562  LOAD_ATTR                _spawned_procs
              564  LOAD_FAST                'pid'
              566  LOAD_ATTR                value
              568  DELETE_SUBSCR    
            570_0  COME_FROM           544  '544'
              570  JUMP_BACK            24  'to 24'
            572_0  COME_FROM           486  '486'

 L. 506       572  LOAD_FAST                'msgid'
              574  LOAD_ATTR                value
              576  LOAD_GLOBAL              winprocess
              578  LOAD_ATTR                JOB_OBJECT_MSG_ABNORMAL_EXIT_PROCESS
              580  COMPARE_OP               ==
          582_584  POP_JUMP_IF_FALSE   668  'to 668'

 L. 508       586  LOAD_FAST                'self'
              588  LOAD_METHOD              debug
              590  LOAD_STR                 'process id %s exited abnormally'
              592  LOAD_FAST                'pid'
              594  LOAD_ATTR                value
              596  BINARY_MODULO    
              598  CALL_METHOD_1         1  '1 positional argument'
              600  POP_TOP          

 L. 509       602  LOAD_FAST                'pid'
              604  LOAD_ATTR                value
              606  LOAD_FAST                'self'
              608  LOAD_ATTR                pid
              610  COMPARE_OP               ==
          612_614  POP_JUMP_IF_FALSE   642  'to 642'
              616  LOAD_GLOBAL              len
              618  LOAD_FAST                'self'
              620  LOAD_ATTR                _spawned_procs
              622  CALL_FUNCTION_1       1  '1 positional argument'
              624  LOAD_CONST               0
              626  COMPARE_OP               >
          628_630  POP_JUMP_IF_FALSE   642  'to 642'

 L. 511       632  LOAD_GLOBAL              datetime
              634  LOAD_METHOD              now
              636  CALL_METHOD_0         0  '0 positional arguments'
              638  STORE_FAST               'countdowntokill'
              640  JUMP_FORWARD        666  'to 666'
            642_0  COME_FROM           628  '628'
            642_1  COME_FROM           612  '612'

 L. 512       642  LOAD_FAST                'pid'
              644  LOAD_ATTR                value
              646  LOAD_FAST                'self'
              648  LOAD_ATTR                _spawned_procs
              650  COMPARE_OP               in
          652_654  POP_JUMP_IF_FALSE   684  'to 684'

 L. 514       656  LOAD_FAST                'self'
              658  LOAD_ATTR                _spawned_procs
              660  LOAD_FAST                'pid'
              662  LOAD_ATTR                value
              664  DELETE_SUBSCR    
            666_0  COME_FROM           640  '640'
              666  JUMP_BACK            24  'to 24'
            668_0  COME_FROM           582  '582'

 L. 517       668  LOAD_FAST                'self'
              670  LOAD_METHOD              debug
              672  LOAD_STR                 'We got a message %s'
              674  LOAD_FAST                'msgid'
              676  LOAD_ATTR                value
              678  BINARY_MODULO    
              680  CALL_METHOD_1         1  '1 positional argument'
              682  POP_TOP          
            684_0  COME_FROM           652  '652'
            684_1  COME_FROM           556  '556'
            684_2  COME_FROM           442  '442'

 L. 518       684  JUMP_BACK            24  'to 24'
              686  POP_BLOCK        
            688_0  COME_FROM_LOOP       20  '20'

Parse error at or near `COME_FROM' instruction at offset 684_0

            def _custom_wait(self, timeout=None):
                """ Custom implementation of wait.

                - timeout: number of seconds before timing out. If None,
                  will wait indefinitely.
                """
                if self._handle:
                    self.returncode = winprocess.GetExitCodeProcess(self._handle)
                else:
                    return self.returncode
                    threadalive = False
                    if hasattr(self, '_procmgrthread'):
                        threadalive = self._procmgrthread.is_alive()
                    elif self._job and threadalive and threading.current_thread() != self._procmgrthread:
                        self.debug('waiting with IO completion port')
                        if timeout is None:
                            timeout = self.MAX_IOCOMPLETION_PORT_NOTIFICATION_DELAY + self.MAX_PROCESS_KILL_DELAY
                        try:
                            try:
                                item = self._process_events.get(timeout=timeout)
                                if item[self.pid] == 'FINISHED':
                                    self.debug("received 'FINISHED' from _procmgrthread")
                                    self._process_events.task_done()
                            except Exception:
                                traceback.print_exc()
                                raise OSError('IO Completion Port failed to signal process shutdown')

                        finally:
                            if self._handle:
                                self.returncode = winprocess.GetExitCodeProcess(self._handle)
                            self._cleanup()

                    else:
                        self.debug('waiting without IO completion port')
                        if not self._ignore_children:
                            self.debug('NOT USING JOB OBJECTS!!!')
                        if self.returncode != winprocess.STILL_ACTIVE:
                            self._cleanup()
                            return self.returncode
                        rc = None
                        if self._handle:
                            if timeout is None:
                                timeout = -1
                            else:
                                timeout = timeout * 1000
                            rc = winprocess.WaitForSingleObject(self._handle, timeout)
                        if rc == winprocess.WAIT_TIMEOUT:
                            print('Timed out waiting for process to close, attempting TerminateProcess')
                            self.kill()
                        else:
                            if rc == winprocess.WAIT_OBJECT_0:
                                print('Single process terminated successfully')
                                self.returncode = winprocess.GetExitCodeProcess(self._handle)
                            else:
                                rc = winprocess.GetLastError()
                                if rc:
                                    raise WinError(rc)
                                self._cleanup()
                    return self.returncode

            def _cleanup_job_io_port(self):
                """ Do the job and IO port cleanup separately because there are
                    cases where we want to clean these without killing _handle
                    (i.e. if we fail to create the job object in the first place)
                """
                if getattr(self, '_job') and self._job != winprocess.INVALID_HANDLE_VALUE:
                    self._job.Close()
                    self._job = None
                else:
                    self._job = None
                if getattr(self, '_io_port', None) and self._io_port != winprocess.INVALID_HANDLE_VALUE:
                    self._io_port.Close()
                    self._io_port = None
                else:
                    self._io_port = None
                if getattr(self, '_procmgrthread', None):
                    self._procmgrthread = None

            def _cleanup(self):
                self._cleanup_job_io_port()
                if self._thread and self._thread != winprocess.INVALID_HANDLE_VALUE:
                    self._thread.Close()
                    self._thread = None
                else:
                    self._thread = None
                if self._handle and self._handle != winprocess.INVALID_HANDLE_VALUE:
                    self._handle.Close()
                    self._handle = None
                else:
                    self._handle = None

        else:
            if isPosix:

                def _custom_wait(self, timeout=None):
                    """ Haven't found any reason to differentiate between these platforms
                    so they all use the same wait callback.  If it is necessary to
                    craft different styles of wait, then a new _custom_wait method
                    could be easily implemented.
                """
                    if not self._ignore_children:
                        try:
                            status = os.waitpid(self.pid, 0)[1]
                            if status > 255:
                                return status >> 8
                            return -status
                        except OSError as e:
                            try:
                                if getattr(e, 'errno', None) != 10:
                                    print(('Encountered error waiting for pid to close: %s' % e), file=(sys.stderr))
                                    raise
                                return self.returncode
                            finally:
                                e = None
                                del e

                    else:
                        if six.PY2:
                            subprocess.Popen.wait(self)
                        else:
                            subprocess.Popen.wait(self, timeout=timeout)
                        return self.returncode

                def _cleanup(self):
                    pass

            else:
                print('Unrecognized platform, process groups may not be managed properly', file=(sys.stderr))

                def _custom_wait(self, timeout=None):
                    if six.PY2:
                        self.returncode = subprocess.Popen.wait(self)
                    else:
                        self.returncode = subprocess.Popen.wait(self, timeout=timeout)
                    return self.returncode

                def _cleanup(self):
                    pass

    def __init__(self, cmd, args=None, cwd=None, env=None, ignore_children=False, kill_on_timeout=True, processOutputLine=(), processStderrLine=(), onTimeout=(), onFinish=(), **kwargs):
        self.cmd = cmd
        self.args = args
        self.cwd = cwd
        self.didTimeout = False
        self.didOutputTimeout = False
        self._ignore_children = ignore_children
        self.keywordargs = kwargs
        self.read_buffer = ''
        if env is None:
            env = os.environ.copy()
        else:
            self.env = env

            def to_callable_list(arg):
                if callable(arg):
                    arg = [
                     arg]
                return CallableList(arg)

            processOutputLine = to_callable_list(processOutputLine)
            processStderrLine = to_callable_list(processStderrLine)
            onTimeout = to_callable_list(onTimeout)
            onFinish = to_callable_list(onFinish)

            def on_timeout():
                self.didTimeout = True
                self.didOutputTimeout = self.reader.didOutputTimeout
                if kill_on_timeout:
                    self.kill()

            onTimeout.insert(0, on_timeout)
            self._stderr = subprocess.STDOUT
            if processStderrLine:
                self._stderr = subprocess.PIPE
            self.reader = ProcessReader(stdout_callback=processOutputLine, stderr_callback=processStderrLine,
              finished_callback=onFinish,
              timeout_callback=onTimeout)
            if isinstance(self.cmd, list):
                if self.args is not None:
                    raise TypeError('cmd and args must not both be lists')
                self.cmd, self.args = self.cmd[0], self.cmd[1:]
            else:
                if self.args is None:
                    self.args = []

    def debug(self, msg):
        if not MOZPROCESS_DEBUG:
            return
        cmd = self.cmd.split(os.sep)[-1:]
        print('DBG::MOZPROC ProcessHandlerMixin {} | {}'.format(cmd, msg))

    @property
    def timedOut(self):
        """True if the process has timed out for any reason."""
        return self.didTimeout

    @property
    def outputTimedOut(self):
        """True if the process has timed out for no output."""
        return self.didOutputTimeout

    @property
    def commandline(self):
        """the string value of the command line (command + args)"""
        return subprocess.list2cmdline([self.cmd] + self.args)

    def run(self, timeout=None, outputTimeout=None):
        """
        Starts the process.

        If timeout is not None, the process will be allowed to continue for
        that number of seconds before being killed. If the process is killed
        due to a timeout, the onTimeout handler will be called.

        If outputTimeout is not None, the process will be allowed to continue
        for that number of seconds without producing any output before
        being killed.
        """
        self.didTimeout = False
        self.didOutputTimeout = False
        args = dict(stdout=(subprocess.PIPE), stderr=(self._stderr),
          cwd=(self.cwd),
          env=(self.env),
          ignore_children=(self._ignore_children))
        args.update(self.keywordargs)
        self.proc = (self.Process)(([self.cmd] + self.args), **args)
        if isPosix:
            self.proc.pgid = self._getpgid(self.proc.pid)
            self.proc.detached_pid = None
        self.processOutput(timeout=timeout, outputTimeout=outputTimeout)

    def kill(self, sig=None):
        """
        Kills the managed process.

        If you created the process with 'ignore_children=False' (the
        default) then it will also also kill all child processes spawned by
        it. If you specified 'ignore_children=True' when creating the
        process, only the root process will be killed.

        Note that this does not manage any state, save any output etc,
        it immediately kills the process.

        :param sig: Signal used to kill the process, defaults to SIGKILL
                    (has no effect on Windows)
        """
        if not hasattr(self, 'proc'):
            raise RuntimeError("Process hasn't been started yet")
        self.proc.kill(sig=sig)
        rc = self.wait()
        if rc is None:
            self.debug('kill: wait failed -- process is still alive')
        return rc

    def poll(self):
        """Check if child process has terminated

        Returns the current returncode value:
        - None if the process hasn't terminated yet
        - A negative number if the process was killed by signal N (Unix only)
        - '0' if the process ended without failures

        """
        if not hasattr(self, 'proc'):
            raise RuntimeError("Process hasn't been started yet")
        else:
            if self.reader.is_alive():
                return
            if hasattr(self, 'returncode'):
                return self.returncode
            return self.proc.poll()

    def processOutput(self, timeout=None, outputTimeout=None):
        """
        Handle process output until the process terminates or times out.

        If timeout is not None, the process will be allowed to continue for
        that number of seconds before being killed.

        If outputTimeout is not None, the process will be allowed to continue
        for that number of seconds without producing any output before
        being killed.
        """
        if not hasattr(self, 'proc'):
            self.run(timeout=timeout, outputTimeout=outputTimeout)
            return
        if not self.reader.is_alive():
            self.reader.timeout = timeout
            self.reader.output_timeout = outputTimeout
            self.reader.start(self.proc)

    def wait(self, timeout=None):
        """
        Waits until all output has been read and the process is
        terminated.

        If timeout is not None, will return after timeout seconds.
        This timeout only causes the wait function to return and
        does not kill the process.

        Returns the process exit code value:
        - None if the process hasn't terminated yet
        - A negative number if the process was killed by signal N (Unix only)
        - '0' if the process ended without failures

        """
        if self.reader.thread:
            if self.reader.thread is not threading.current_thread():
                count = 0
                while self.reader.is_alive():
                    self.reader.join(timeout=1)
                    count += 1
                    if timeout is not None and count > timeout:
                        self.debug('wait timeout for reader thread')
                        return

        self.returncode = self.proc.wait()
        return self.returncode

    @property
    def pid(self):
        if not hasattr(self, 'proc'):
            raise RuntimeError("Process hasn't been started yet")
        return self.proc.pid

    @staticmethod
    def pid_exists(pid):
        if pid < 0:
            return False
            if isWin:
                try:
                    process = winprocess.OpenProcess(winprocess.PROCESS_QUERY_INFORMATION | winprocess.PROCESS_VM_READ, False, pid)
                    return winprocess.GetExitCodeProcess(process) == winprocess.STILL_ACTIVE
                except WindowsError as e:
                    try:
                        if e.winerror == winprocess.ERROR_INVALID_PARAMETER:
                            return False
                        if e.winerror == winprocess.ERROR_ACCESS_DENIED:
                            return True
                        raise
                    finally:
                        e = None
                        del e

        elif isPosix:
            try:
                os.kill(pid, 0)
            except OSError as e:
                try:
                    return e.errno == errno.EPERM
                finally:
                    e = None
                    del e

            else:
                return True

    @classmethod
    def _getpgid(cls, pid):
        try:
            return os.getpgid(pid)
        except OSError as e:
            try:
                if e.errno != errno.ESRCH:
                    raise
            finally:
                e = None
                del e

    def check_for_detached(self, new_pid):
        """Check if the current process has been detached and mark it appropriately.

        In case of application restarts the process can spawn itself into a new process group.
        From now on the process can no longer be tracked by mozprocess anymore and has to be
        marked as detached. If the consumer of mozprocess still knows the new process id it could
        check for the detached state.

        new_pid is the new process id of the child process.
        """
        if not hasattr(self, 'proc'):
            raise RuntimeError("Process hasn't been started yet")
        if isPosix:
            new_pgid = self._getpgid(new_pid)
            if new_pgid:
                if new_pgid != self.proc.pgid:
                    self.proc.detached_pid = new_pid
                    print(('Child process with id "%s" has been marked as detached because it is no longer in the managed process group. Keeping reference to the process id "%s" which is the new child process.' % (
                     self.pid, new_pid)),
                      file=(sys.stdout))


class CallableList(list):

    def __call__(self, *args, **kwargs):
        for e in self:
            e(*args, **kwargs)

    def __add__(self, lst):
        return CallableList(list.__add__(self, lst))


class ProcessReader(object):

    def __init__(self, stdout_callback=None, stderr_callback=None, finished_callback=None, timeout_callback=None, timeout=None, output_timeout=None):
        self.stdout_callback = stdout_callback or (lambda line: True)
        self.stderr_callback = stderr_callback or (lambda line: True)
        self.finished_callback = finished_callback or (lambda : True)
        self.timeout_callback = timeout_callback or (lambda : True)
        self.timeout = timeout
        self.output_timeout = output_timeout
        self.thread = None
        self.didOutputTimeout = False

    def debug(self, msg):
        if not MOZPROCESS_DEBUG:
            return
        print('DBG::MOZPROC ProcessReader | {}'.format(msg))

    def _create_stream_reader(self, name, stream, queue, callback):
        thread = threading.Thread(name=name, target=(self._read_stream),
          args=(
         stream, queue, callback))
        thread.daemon = True
        thread.start()
        return thread

    def _read_stream(self, stream, queue, callback):
        while True:
            line = stream.readline()
            if not line:
                break
            queue.put((line, callback))

        stream.close()

    def start(self, proc):
        queue = Queue()
        stdout_reader = None
        if proc.stdout:
            stdout_reader = self._create_stream_reader('ProcessReaderStdout', proc.stdout, queue, self.stdout_callback)
        stderr_reader = None
        if proc.stderr:
            if proc.stderr != proc.stdout:
                stderr_reader = self._create_stream_reader('ProcessReaderStderr', proc.stderr, queue, self.stderr_callback)
        self.thread = threading.Thread(name='ProcessReader', target=(self._read),
          args=(
         stdout_reader,
         stderr_reader,
         queue))
        self.thread.daemon = True
        self.thread.start()
        self.debug('ProcessReader started')

    def _read(self, stdout_reader, stderr_reader, queue):
        start_time = time.time()
        timed_out = False
        timeout = self.timeout
        if timeout is not None:
            timeout += start_time
        output_timeout = self.output_timeout
        if output_timeout is not None:
            output_timeout += start_time
        while not (stdout_reader and stdout_reader.is_alive()):
            if not stderr_reader or stderr_reader.is_alive():
                has_line = True
                try:
                    line, callback = queue.get(True, INTERVAL_PROCESS_ALIVE_CHECK)
                except Empty:
                    has_line = False

                now = time.time()
                if (has_line or output_timeout) is not None and now > output_timeout:
                    timed_out = True
                    self.didOutputTimeout = True
                    break
                else:
                    if output_timeout is not None:
                        output_timeout = now + self.output_timeout
                    callback(line.rstrip())
                if timeout is not None and now > timeout:
                    timed_out = True
                    break

        self.debug('_read loop exited')
        while not queue.empty():
            line, callback = queue.get(False)
            callback(line.rstrip())

        if timed_out:
            self.timeout_callback()
        if stdout_reader:
            stdout_reader.join()
        if stderr_reader:
            stderr_reader.join()
        if not timed_out:
            self.finished_callback()
        self.debug('_read exited')

    def is_alive(self):
        if self.thread:
            return self.thread.is_alive()
        return False

    def join(self, timeout=None):
        if self.thread:
            self.thread.join(timeout=timeout)


class StoreOutput(object):
    __doc__ = 'accumulate stdout'

    def __init__(self):
        self.output = []

    def __call__(self, line):
        self.output.append(line)


class StreamOutput(object):
    __doc__ = 'pass output to a stream and flush'

    def __init__(self, stream):
        self.stream = stream

    def __call__(self, line):
        try:
            self.stream.write(line + '\n'.encode('utf8'))
        except UnicodeDecodeError:
            self.stream.write(line.decode('iso8859-1') + '\n')

        self.stream.flush()


class LogOutput(StreamOutput):
    __doc__ = 'pass output to a file'

    def __init__(self, filename):
        self.file_obj = open(filename, 'a')
        StreamOutput.__init__(self, self.file_obj)

    def __del__(self):
        if self.file_obj is not None:
            self.file_obj.close()


class ProcessHandler(ProcessHandlerMixin):
    __doc__ = '\n    Convenience class for handling processes with default output handlers.\n\n    By default, all output is sent to stdout. This can be disabled by setting\n    the *stream* argument to None.\n\n    If processOutputLine keyword argument is specified the function or the\n    list of functions specified by this argument will be called for each line\n    of output; the output will not be written to stdout automatically then\n    if stream is True (the default).\n\n    If storeOutput==True, the output produced by the process will be saved\n    as self.output.\n\n    If logfile is not None, the output produced by the process will be\n    appended to the given file.\n    '

    def __init__(self, cmd, logfile=None, stream=True, storeOutput=True, **kwargs):
        kwargs.setdefault('processOutputLine', [])
        if callable(kwargs['processOutputLine']):
            kwargs['processOutputLine'] = [
             kwargs['processOutputLine']]
        elif logfile:
            logoutput = LogOutput(logfile)
            kwargs['processOutputLine'].append(logoutput)
        elif stream is True:
            kwargs['processOutputLine'] or kwargs['processOutputLine'].append(StreamOutput(sys.stdout))
        else:
            if stream:
                streamoutput = StreamOutput(stream)
                kwargs['processOutputLine'].append(streamoutput)
        self.output = None
        if storeOutput:
            storeoutput = StoreOutput()
            self.output = storeoutput.output
            kwargs['processOutputLine'].append(storeoutput)
        (ProcessHandlerMixin.__init__)(self, cmd, **kwargs)