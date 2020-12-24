# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winpwn\win.py
# Compiled at: 2020-04-17 21:29:23
import os, sys, time
from ctypes import windll, byref, sizeof, wintypes, create_string_buffer, GetLastError, c_size_t
from ctypes.wintypes import HANDLE, LPVOID, LPSTR, DWORD, WORD, BOOL, BYTE
from ctypes import POINTER, Structure
from .context import context
from .misc import Latin1_encode, Latin1_decode, color, showbanner
HANDLE_FLAG_INHERIT = 1
STARTF_USESTDHANDLES = 256
STILL_ACTIVE = 259
CREATE_SUSPENDED = 4
PROCESS_VM_READ = 16
PROCESS_VM_WRITE = 32
PROCESS_VM_OPERATION = 8
PAGE_READWRITE = 4

class SECURITY_ATTRIBUTES(Structure):
    _fields_ = [
     (
      'nLength', DWORD),
     (
      'lpSecurityDescriptor', LPVOID),
     (
      'bInheritHandle', BOOL)]


class PROCESS_INFORMATION(Structure):
    _fields_ = [
     (
      'hProcess', HANDLE),
     (
      'hThread', HANDLE),
     (
      'dwProcessId', DWORD),
     (
      'dwThreadId', DWORD)]


class STARTUPINFO(Structure):
    _fields_ = [
     (
      'cb', DWORD),
     (
      'lpReserved', LPSTR),
     (
      'lpDesktop', LPSTR),
     (
      'lpTitle', LPSTR),
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
      'lpReserved2', POINTER(BYTE)),
     (
      'hStdInput', HANDLE),
     (
      'hStdOutput', HANDLE),
     (
      'hStdError', HANDLE)]


class winPipe:

    def __init__(self, bInheritHandle=1):
        self.timeout = context.timeout
        self.hReadPipe, self.hWritePipe, self.child_hReadPipe, self.child_hWritePipe = self.create(bInheritHandle=bInheritHandle)

    def create(self, bInheritHandle=1):
        attr = SECURITY_ATTRIBUTES()
        attr.lpSecurityDescriptor = 0
        attr.bInheritHandle = bInheritHandle
        attr.nLength = sizeof(attr)
        hReadPipe = wintypes.HANDLE()
        hWritePipe = wintypes.HANDLE()
        child_hReadPipe = wintypes.HANDLE()
        child_hWritePipe = wintypes.HANDLE()
        rs1 = windll.kernel32.CreatePipe(byref(hReadPipe), byref(child_hWritePipe), byref(attr), 0)
        rs2 = windll.kernel32.CreatePipe(byref(child_hReadPipe), byref(hWritePipe), byref(attr), 0)
        rs3 = windll.kernel32.SetHandleInformation(hReadPipe.value, HANDLE_FLAG_INHERIT, 0)
        rs4 = windll.kernel32.SetHandleInformation(hWritePipe.value, HANDLE_FLAG_INHERIT, 0)
        if rs1 and rs2 and rs3 and rs4:
            return (hReadPipe.value, hWritePipe.value, child_hReadPipe.value, child_hWritePipe.value)
        raise EOFError(color('[-]: Create Pipe error', 'red'))

    def read(self, n, timeout=None):

        def count():
            byteAvail = wintypes.DWORD()
            x = windll.kernel32.PeekNamedPipe(self.hReadPipe, 0, 0, 0, byref(byteAvail), 0)
            return byteAvail.value

        if timeout is None:
            if self.timeout:
                timeout = self.timeout
            else:
                timeout = context.timeout
        x_time = 0
        if count() < n:
            while x_time < timeout and count() < n:
                time.sleep(context.tick)
                x_time += context.tick

        cn = min(count(), n)
        beenRead = wintypes.DWORD()
        buf = create_string_buffer(cn)
        if cn > 0:
            windll.kernel32.ReadFile(self.hReadPipe, buf, cn, byref(beenRead), None)
        return Latin1_decode(buf.raw)

    def write(self, buf=''):
        buf = Latin1_encode(buf)
        length = len(buf)
        written = wintypes.DWORD()
        x = windll.kernel32.WriteFile(self.hWritePipe, buf, length, byref(written), None)
        if x == 0:
            raise EOFError()
        return written.value

    def getHandle(self):
        return (
         self.hReadPipe, self.hWritePipe, self.child_hReadPipe, self.child_hWritePipe)

    def close(self):
        windll.kernel32.CloseHandle(self.hReadPipe)
        windll.kernel32.CloseHandle(self.hWritePipe)


class winProcess(object):

    def __init__(self, argv, cwd=None, flags=0):
        self.pipe = winPipe()
        self.hReadPipe, self.hWritePipe, self.child_hReadPipe, self.child_hWritePipe = self.pipe.getHandle()
        self.pid = 0
        self.phandle = 0
        self.tid = 0
        self.thandle = 0
        self.create(argv, cwd, flags)

    def create(self, argv, cwd=None, flags=None):
        lpCurrentDirectory = cwd
        lpEnvironment = None
        dwCreationFlags = flags
        bInheritHandles = True
        lpProcessAttributes = None
        lpThreadAttributes = None
        lpProcessInformation = PROCESS_INFORMATION()
        StartupInfo = STARTUPINFO()
        StartupInfo.cb = sizeof(StartupInfo)
        StartupInfo.dwFlags = STARTF_USESTDHANDLES
        StartupInfo.hStdInput = self.child_hReadPipe
        StartupInfo.hStdOutput = self.child_hWritePipe
        StartupInfo.hStdError = self.child_hWritePipe
        lpStartupInfo = byref(StartupInfo)
        lpCommandLine = None
        lpApplicationName = None
        if not isinstance(argv, list):
            lpApplicationName = Latin1_encode(argv)
        else:
            lpCommandLine = Latin1_encode((' ').join([ str(a) for a in argv ]))
        try:
            bs = windll.kernel32.CreateProcessA(lpApplicationName, lpCommandLine, lpProcessAttributes, lpThreadAttributes, bInheritHandles, dwCreationFlags, lpEnvironment, lpCurrentDirectory, byref(StartupInfo), byref(lpProcessInformation))
            self.pid = lpProcessInformation.dwProcessId
            self.phandle = lpProcessInformation.hProcess
            self.tid = lpProcessInformation.dwThreadId
            self.thandle = lpProcessInformation.hThread
            showbanner(('Create process success #pid 0x{:x}').format(self.pid))
        except:
            raise EOFError(color('[-]: Create process error', 'red'))

        return

    def read(self, n, timeout=None):
        return self.pipe.read(n, timeout=timeout)

    def write(self, buf):
        return self.pipe.write(buf)

    def is_exit(self):
        x = wintypes.DWORD()
        n = windll.kernel32.GetExitCodeProcess(self.phandle, byref(x))
        if n != 0 and x.value == STILL_ACTIVE:
            return False
        return True

    def close(self):
        self.pipe.close()
        windll.kernel32.TerminateProcess(self.phandle, 1)

    def readm(self, addr, n):
        addr = c_size_t(addr)
        handle = windll.kernel32.OpenProcess(PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION, 0, self.pid)
        oldprotect = wintypes.DWORD()
        x = windll.kernel32.VirtualProtectEx(handle, addr, n, PAGE_READWRITE, byref(oldprotect))
        buf = create_string_buffer(n)
        x = windll.kernel32.ReadProcessMemory(handle, addr, buf, n, 0)
        if x == 0:
            raise MemoryError
        windll.kernel32.VirtualProtectEx(handle, addr, n, oldprotect.value, 0)
        windll.kernel32.CloseHandle(handle)
        return Latin1_decode(buf.raw)

    def writem(self, addr, buf):
        buf = Latin1_encode(buf)
        addr = c_size_t(addr)
        n = len(buf)
        handle = windll.kernel32.OpenProcess(PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION, 0, self.pid)
        oldprotect = wintypes.DWORD()
        x = windll.kernel32.VirtualProtectEx(handle, addr, n, PAGE_READWRITE, byref(oldprotect))
        written = c_size_t(0)
        x = windll.kernel32.WriteProcessMemory(handle, addr, buf, n, byref(written))
        if x == 0:
            raise MemoryError
        windll.kernel32.VirtualProtectEx(handle, addr, n, oldprotect.value, 0)
        windll.kernel32.CloseHandle(handle)
        return written.value