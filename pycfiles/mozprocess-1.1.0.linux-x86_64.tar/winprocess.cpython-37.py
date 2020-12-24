# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahal/.pyenv/versions/3.7.4/lib/python3.7/site-packages/mozprocess/winprocess.py
# Compiled at: 2019-12-02 09:22:55
# Size of source mod 2**32: 19443 bytes
from __future__ import absolute_import, unicode_literals, print_function
import subprocess, sys
from ctypes import cast, create_unicode_buffer, c_ulong, c_void_p, POINTER, sizeof, Structure, windll, WinError, WINFUNCTYPE
from ctypes.wintypes import BOOL, BYTE, DWORD, HANDLE, LPCWSTR, LPWSTR, UINT, WORD
from .qijo import QueryInformationJobObject
LPVOID = c_void_p
LPBYTE = POINTER(BYTE)
LPDWORD = POINTER(DWORD)
LPBOOL = POINTER(BOOL)
LPULONG = POINTER(c_ulong)

def ErrCheckBool(result, func, args):
    """errcheck function for Windows functions that return a BOOL True
    on success"""
    if not result:
        raise WinError()
    return args


class AutoHANDLE(HANDLE):
    __doc__ = 'Subclass of HANDLE which will call CloseHandle() on deletion.'
    CloseHandleProto = WINFUNCTYPE(BOOL, HANDLE)
    CloseHandle = CloseHandleProto(('CloseHandle', windll.kernel32))
    CloseHandle.errcheck = ErrCheckBool

    def Close(self):
        if self.value:
            if self.value != HANDLE(-1).value:
                self.CloseHandle(self)
                self.value = 0

    def __del__(self):
        self.Close()

    def __int__(self):
        return self.value


def ErrCheckHandle(result, func, args):
    """errcheck function for Windows functions that return a HANDLE."""
    if not result:
        raise WinError()
    return AutoHANDLE(result)


class PROCESS_INFORMATION(Structure):
    _fields_ = [
     (
      'hProcess', HANDLE),
     (
      'hThread', HANDLE),
     (
      'dwProcessID', DWORD),
     (
      'dwThreadID', DWORD)]

    def __init__(self):
        Structure.__init__(self)
        self.cb = sizeof(self)


LPPROCESS_INFORMATION = POINTER(PROCESS_INFORMATION)

class STARTUPINFO(Structure):
    _fields_ = [
     (
      'cb', DWORD),
     (
      'lpReserved', LPWSTR),
     (
      'lpDesktop', LPWSTR),
     (
      'lpTitle', LPWSTR),
     (
      'dwX', DWORD),
     (
      'dwY', DWORD),
     (
      'dwXSize', DWORD),
     (
      'dwYSize', DWORD),
     (
      'dwXCountChars', DWORD),
     (
      'dwYCountChars', DWORD),
     (
      'dwFillAttribute', DWORD),
     (
      'dwFlags', DWORD),
     (
      'wShowWindow', WORD),
     (
      'cbReserved2', WORD),
     (
      'lpReserved2', LPBYTE),
     (
      'hStdInput', HANDLE),
     (
      'hStdOutput', HANDLE),
     (
      'hStdError', HANDLE)]


LPSTARTUPINFO = POINTER(STARTUPINFO)
SW_HIDE = 0
STARTF_USESHOWWINDOW = 1
STARTF_USESIZE = 2
STARTF_USEPOSITION = 4
STARTF_USECOUNTCHARS = 8
STARTF_USEFILLATTRIBUTE = 16
STARTF_RUNFULLSCREEN = 32
STARTF_FORCEONFEEDBACK = 64
STARTF_FORCEOFFFEEDBACK = 128
STARTF_USESTDHANDLES = 256

class EnvironmentBlock:
    __doc__ = 'An object which can be passed as the lpEnv parameter of CreateProcess.\n    It is initialized with a dictionary.'

    def __init__(self, env):
        if not env:
            self._as_parameter_ = None
        else:
            values = []
            fs_encoding = sys.getfilesystemencoding() or 'mbcs'
            for k, v in env.items():
                if isinstance(k, bytes):
                    k = k.decode(fs_encoding, 'replace')
                if isinstance(v, bytes):
                    v = v.decode(fs_encoding, 'replace')
                values.append('{}={}'.format(k, v))

            values = create_unicode_buffer('\x00'.join(values) + '\x00')
            self._as_parameter_ = cast(values, LPCWSTR)


ERROR_ACCESS_DENIED = 5
ERROR_INVALID_PARAMETER = 87
ERROR_ABANDONED_WAIT_0 = 735
GetLastErrorProto = WINFUNCTYPE(DWORD)
GetLastErrorFlags = ()
GetLastError = GetLastErrorProto(('GetLastError', windll.kernel32), GetLastErrorFlags)
CreateProcessProto = WINFUNCTYPE(BOOL, LPCWSTR, LPWSTR, LPVOID, LPVOID, BOOL, DWORD, LPVOID, LPCWSTR, LPSTARTUPINFO, LPPROCESS_INFORMATION)
CreateProcessFlags = ((1, 'lpApplicationName', None), (1, 'lpCommandLine'), (1, 'lpProcessAttributes', None),
                      (1, 'lpThreadAttributes', None), (1, 'bInheritHandles', True),
                      (1, 'dwCreationFlags', 0), (1, 'lpEnvironment', None), (1, 'lpCurrentDirectory', None),
                      (1, 'lpStartupInfo'), (2, 'lpProcessInformation'))

def ErrCheckCreateProcess(result, func, args):
    ErrCheckBool(result, func, args)
    pi = args[9]
    return (AutoHANDLE(pi.hProcess), AutoHANDLE(pi.hThread), pi.dwProcessID, pi.dwThreadID)


CreateProcess = CreateProcessProto(('CreateProcessW', windll.kernel32), CreateProcessFlags)
CreateProcess.errcheck = ErrCheckCreateProcess
CREATE_BREAKAWAY_FROM_JOB = 16777216
CREATE_DEFAULT_ERROR_MODE = 67108864
CREATE_NEW_CONSOLE = 16
CREATE_NEW_PROCESS_GROUP = 512
CREATE_NO_WINDOW = 134217728
CREATE_SUSPENDED = 4
CREATE_UNICODE_ENVIRONMENT = 1024
INVALID_HANDLE_VALUE = HANDLE(-1)
COMPKEY_TERMINATE = c_ulong(0)
COMPKEY_JOBOBJECT = c_ulong(1)
JOB_OBJECT_LIMIT_BREAKAWAY_OK = 2048
JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK = 4096
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 8192
JOB_OBJECT_MSG_END_OF_JOB_TIME = 1
JOB_OBJECT_MSG_END_OF_PROCESS_TIME = 2
JOB_OBJECT_MSG_ACTIVE_PROCESS_LIMIT = 3
JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO = 4
JOB_OBJECT_MSG_NEW_PROCESS = 6
JOB_OBJECT_MSG_EXIT_PROCESS = 7
JOB_OBJECT_MSG_ABNORMAL_EXIT_PROCESS = 8
JOB_OBJECT_MSG_PROCESS_MEMORY_LIMIT = 9
JOB_OBJECT_MSG_JOB_MEMORY_LIMIT = 10
DEBUG_ONLY_THIS_PROCESS = 2
DEBUG_PROCESS = 1
DETACHED_PROCESS = 8
PROCESS_QUERY_INFORMATION = 1024
PROCESS_VM_READ = 16
OpenProcessProto = WINFUNCTYPE(HANDLE, DWORD, BOOL, DWORD)
OpenProcessFlags = ((1, 'dwDesiredAccess', 0), (1, 'bInheritHandle', False), (1, 'dwProcessId', 0))

def ErrCheckOpenProcess(result, func, args):
    ErrCheckBool(result, func, args)
    return AutoHANDLE(result)


OpenProcess = OpenProcessProto(('OpenProcess', windll.kernel32), OpenProcessFlags)
OpenProcess.errcheck = ErrCheckOpenProcess
GetQueuedCompletionStatusProto = WINFUNCTYPE(BOOL, HANDLE, LPDWORD, LPULONG, LPULONG, DWORD)
GetQueuedCompletionStatusFlags = ((1, 'CompletionPort', INVALID_HANDLE_VALUE),
 (1, 'lpNumberOfBytes', None),
 (1, 'lpCompletionKey', None),
 (1, 'lpPID', None),
 (1, 'dwMilliseconds', 0))
GetQueuedCompletionStatus = GetQueuedCompletionStatusProto(('GetQueuedCompletionStatus',
 windll.kernel32), GetQueuedCompletionStatusFlags)
CreateIoCompletionPortProto = WINFUNCTYPE(HANDLE, HANDLE, HANDLE, c_ulong, DWORD)
CreateIoCompletionPortFlags = (
 (
  1, 'FileHandle', INVALID_HANDLE_VALUE),
 (1, 'ExistingCompletionPort', 0),
 (
  1, 'CompletionKey', c_ulong(0)),
 (1, 'NumberOfConcurrentThreads', 0))
CreateIoCompletionPort = CreateIoCompletionPortProto(('CreateIoCompletionPort',
 windll.kernel32), CreateIoCompletionPortFlags)
CreateIoCompletionPort.errcheck = ErrCheckHandle
SetInformationJobObjectProto = WINFUNCTYPE(BOOL, HANDLE, DWORD, LPVOID, DWORD)
SetInformationJobObjectProtoFlags = ((1, 'hJob', None), (1, 'JobObjectInfoClass', None),
                                     (1, 'lpJobObjectInfo', None), (1, 'cbJobObjectInfoLength', 0))
SetInformationJobObject = SetInformationJobObjectProto(('SetInformationJobObject',
 windll.kernel32), SetInformationJobObjectProtoFlags)
SetInformationJobObject.errcheck = ErrCheckBool
CreateJobObjectProto = WINFUNCTYPE(HANDLE, LPVOID, LPCWSTR)
CreateJobObjectFlags = ((1, 'lpJobAttributes', None), (1, 'lpName', None))
CreateJobObject = CreateJobObjectProto(('CreateJobObjectW', windll.kernel32), CreateJobObjectFlags)
CreateJobObject.errcheck = ErrCheckHandle
AssignProcessToJobObjectProto = WINFUNCTYPE(BOOL, HANDLE, HANDLE)
AssignProcessToJobObjectFlags = ((1, 'hJob'), (1, 'hProcess'))
AssignProcessToJobObject = AssignProcessToJobObjectProto((
 'AssignProcessToJobObject', windll.kernel32), AssignProcessToJobObjectFlags)
AssignProcessToJobObject.errcheck = ErrCheckBool
GetCurrentProcessProto = WINFUNCTYPE(HANDLE)
GetCurrentProcessFlags = ()
GetCurrentProcess = GetCurrentProcessProto((
 'GetCurrentProcess', windll.kernel32), GetCurrentProcessFlags)
GetCurrentProcess.errcheck = ErrCheckHandle
try:
    IsProcessInJobProto = WINFUNCTYPE(BOOL, HANDLE, HANDLE, LPBOOL)
    IsProcessInJobFlags = (
     (1, 'ProcessHandle'),
     (
      1, 'JobHandle', HANDLE(0)),
     (2, 'Result'))
    IsProcessInJob = IsProcessInJobProto((
     'IsProcessInJob', windll.kernel32), IsProcessInJobFlags)
    IsProcessInJob.errcheck = ErrCheckBool
except AttributeError:

    def IsProcessInJob(process):
        return False


def ErrCheckResumeThread(result, func, args):
    if result == -1:
        raise WinError()
    return args


ResumeThreadProto = WINFUNCTYPE(DWORD, HANDLE)
ResumeThreadFlags = ((1, 'hThread'), )
ResumeThread = ResumeThreadProto(('ResumeThread', windll.kernel32), ResumeThreadFlags)
ResumeThread.errcheck = ErrCheckResumeThread
TerminateProcessProto = WINFUNCTYPE(BOOL, HANDLE, UINT)
TerminateProcessFlags = ((1, 'hProcess'), (1, 'uExitCode', 127))
TerminateProcess = TerminateProcessProto((
 'TerminateProcess', windll.kernel32), TerminateProcessFlags)
TerminateProcess.errcheck = ErrCheckBool
TerminateJobObjectProto = WINFUNCTYPE(BOOL, HANDLE, UINT)
TerminateJobObjectFlags = ((1, 'hJob'), (1, 'uExitCode', 127))
TerminateJobObject = TerminateJobObjectProto((
 'TerminateJobObject', windll.kernel32), TerminateJobObjectFlags)
TerminateJobObject.errcheck = ErrCheckBool
WaitForSingleObjectProto = WINFUNCTYPE(DWORD, HANDLE, DWORD)
WaitForSingleObjectFlags = ((1, 'hHandle'), (1, 'dwMilliseconds', -1))
WaitForSingleObject = WaitForSingleObjectProto((
 'WaitForSingleObject', windll.kernel32), WaitForSingleObjectFlags)
INFINITE = -1
WAIT_TIMEOUT = 258
WAIT_OBJECT_0 = 0
WAIT_ABANDONED = 128
STILL_ACTIVE = 259
ERROR_CONTROL_C_EXIT = 572
GetExitCodeProcessProto = WINFUNCTYPE(BOOL, HANDLE, LPDWORD)
GetExitCodeProcessFlags = ((1, 'hProcess'), (2, 'lpExitCode'))
GetExitCodeProcess = GetExitCodeProcessProto((
 'GetExitCodeProcess', windll.kernel32), GetExitCodeProcessFlags)
GetExitCodeProcess.errcheck = ErrCheckBool

def CanCreateJobObject():
    currentProc = GetCurrentProcess()
    if IsProcessInJob(currentProc):
        jobinfo = QueryInformationJobObject(HANDLE(0), 'JobObjectExtendedLimitInformation')
        limitflags = jobinfo['BasicLimitInformation']['LimitFlags']
        return bool(limitflags & JOB_OBJECT_LIMIT_BREAKAWAY_OK) or bool(limitflags & JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK)
    return True


def parent():
    print('Starting parent')
    currentProc = GetCurrentProcess()
    if IsProcessInJob(currentProc):
        print('You should not be in a job object to test', file=(sys.stderr))
        sys.exit(1)
    assert CanCreateJobObject()
    print('File: %s' % __file__)
    command = [sys.executable, __file__, '-child']
    print('Running command: %s' % command)
    process = subprocess.Popen(command)
    process.kill()
    code = process.returncode
    print('Child code: %s' % code)
    assert code == 127


def child():
    print('Starting child')
    currentProc = GetCurrentProcess()
    injob = IsProcessInJob(currentProc)
    print('Is in a job?: %s' % injob)
    can_create = CanCreateJobObject()
    print('Can create job?: %s' % can_create)
    process = subprocess.Popen('c:\\windows\\notepad.exe')
    assert process._job
    jobinfo = QueryInformationJobObject(process._job, 'JobObjectExtendedLimitInformation')
    print('Job info: %s' % jobinfo)
    limitflags = jobinfo['BasicLimitInformation']['LimitFlags']
    print('LimitFlags: %s' % limitflags)
    process.kill()