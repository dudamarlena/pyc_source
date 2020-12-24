# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./build/lib.linux-x86_64-2.7/serial/win32.py
# Compiled at: 2015-08-29 23:20:15
from ctypes import *
from ctypes.wintypes import HANDLE
from ctypes.wintypes import BOOL
from ctypes.wintypes import LPCWSTR
from ctypes.wintypes import DWORD
from ctypes.wintypes import WORD
from ctypes.wintypes import BYTE
_stdcall_libraries = {}
_stdcall_libraries['kernel32'] = WinDLL('kernel32')
INVALID_HANDLE_VALUE = HANDLE(-1).value

def is_64bit():
    """Returns true when running on a 64 bit system"""
    return sizeof(c_ulong) != sizeof(c_void_p)


if is_64bit():
    ULONG_PTR = c_int64
else:
    ULONG_PTR = c_ulong

class _SECURITY_ATTRIBUTES(Structure):
    pass


LPSECURITY_ATTRIBUTES = POINTER(_SECURITY_ATTRIBUTES)
try:
    CreateEventW = _stdcall_libraries['kernel32'].CreateEventW
except AttributeError:
    from ctypes.wintypes import LPCSTR
    CreateEventA = _stdcall_libraries['kernel32'].CreateEventA
    CreateEventA.restype = HANDLE
    CreateEventA.argtypes = [LPSECURITY_ATTRIBUTES, BOOL, BOOL, LPCSTR]
    CreateEvent = CreateEventA
    CreateFileA = _stdcall_libraries['kernel32'].CreateFileA
    CreateFileA.restype = HANDLE
    CreateFileA.argtypes = [LPCSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE]
    CreateFile = CreateFileA
else:
    CreateEventW.restype = HANDLE
    CreateEventW.argtypes = [LPSECURITY_ATTRIBUTES, BOOL, BOOL, LPCWSTR]
    CreateEvent = CreateEventW
    CreateFileW = _stdcall_libraries['kernel32'].CreateFileW
    CreateFileW.restype = HANDLE
    CreateFileW.argtypes = [LPCWSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE]
    CreateFile = CreateFileW

class _OVERLAPPED(Structure):
    pass


OVERLAPPED = _OVERLAPPED

class _COMSTAT(Structure):
    pass


COMSTAT = _COMSTAT

class _DCB(Structure):
    pass


DCB = _DCB

class _COMMTIMEOUTS(Structure):
    pass


COMMTIMEOUTS = _COMMTIMEOUTS
GetLastError = _stdcall_libraries['kernel32'].GetLastError
GetLastError.restype = DWORD
GetLastError.argtypes = []
LPOVERLAPPED = POINTER(_OVERLAPPED)
LPDWORD = POINTER(DWORD)
GetOverlappedResult = _stdcall_libraries['kernel32'].GetOverlappedResult
GetOverlappedResult.restype = BOOL
GetOverlappedResult.argtypes = [HANDLE, LPOVERLAPPED, LPDWORD, BOOL]
ResetEvent = _stdcall_libraries['kernel32'].ResetEvent
ResetEvent.restype = BOOL
ResetEvent.argtypes = [HANDLE]
LPCVOID = c_void_p
WriteFile = _stdcall_libraries['kernel32'].WriteFile
WriteFile.restype = BOOL
WriteFile.argtypes = [HANDLE, LPCVOID, DWORD, LPDWORD, LPOVERLAPPED]
LPVOID = c_void_p
ReadFile = _stdcall_libraries['kernel32'].ReadFile
ReadFile.restype = BOOL
ReadFile.argtypes = [HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED]
CloseHandle = _stdcall_libraries['kernel32'].CloseHandle
CloseHandle.restype = BOOL
CloseHandle.argtypes = [HANDLE]
ClearCommBreak = _stdcall_libraries['kernel32'].ClearCommBreak
ClearCommBreak.restype = BOOL
ClearCommBreak.argtypes = [HANDLE]
LPCOMSTAT = POINTER(_COMSTAT)
ClearCommError = _stdcall_libraries['kernel32'].ClearCommError
ClearCommError.restype = BOOL
ClearCommError.argtypes = [HANDLE, LPDWORD, LPCOMSTAT]
SetupComm = _stdcall_libraries['kernel32'].SetupComm
SetupComm.restype = BOOL
SetupComm.argtypes = [HANDLE, DWORD, DWORD]
EscapeCommFunction = _stdcall_libraries['kernel32'].EscapeCommFunction
EscapeCommFunction.restype = BOOL
EscapeCommFunction.argtypes = [HANDLE, DWORD]
GetCommModemStatus = _stdcall_libraries['kernel32'].GetCommModemStatus
GetCommModemStatus.restype = BOOL
GetCommModemStatus.argtypes = [HANDLE, LPDWORD]
LPDCB = POINTER(_DCB)
GetCommState = _stdcall_libraries['kernel32'].GetCommState
GetCommState.restype = BOOL
GetCommState.argtypes = [HANDLE, LPDCB]
LPCOMMTIMEOUTS = POINTER(_COMMTIMEOUTS)
GetCommTimeouts = _stdcall_libraries['kernel32'].GetCommTimeouts
GetCommTimeouts.restype = BOOL
GetCommTimeouts.argtypes = [HANDLE, LPCOMMTIMEOUTS]
PurgeComm = _stdcall_libraries['kernel32'].PurgeComm
PurgeComm.restype = BOOL
PurgeComm.argtypes = [HANDLE, DWORD]
SetCommBreak = _stdcall_libraries['kernel32'].SetCommBreak
SetCommBreak.restype = BOOL
SetCommBreak.argtypes = [HANDLE]
SetCommMask = _stdcall_libraries['kernel32'].SetCommMask
SetCommMask.restype = BOOL
SetCommMask.argtypes = [HANDLE, DWORD]
SetCommState = _stdcall_libraries['kernel32'].SetCommState
SetCommState.restype = BOOL
SetCommState.argtypes = [HANDLE, LPDCB]
SetCommTimeouts = _stdcall_libraries['kernel32'].SetCommTimeouts
SetCommTimeouts.restype = BOOL
SetCommTimeouts.argtypes = [HANDLE, LPCOMMTIMEOUTS]
WaitForSingleObject = _stdcall_libraries['kernel32'].WaitForSingleObject
WaitForSingleObject.restype = DWORD
WaitForSingleObject.argtypes = [HANDLE, DWORD]
ONESTOPBIT = 0
TWOSTOPBITS = 2
ONE5STOPBITS = 1
NOPARITY = 0
ODDPARITY = 1
EVENPARITY = 2
MARKPARITY = 3
SPACEPARITY = 4
RTS_CONTROL_HANDSHAKE = 2
RTS_CONTROL_DISABLE = 0
RTS_CONTROL_ENABLE = 1
RTS_CONTROL_TOGGLE = 3
SETRTS = 3
CLRRTS = 4
DTR_CONTROL_HANDSHAKE = 2
DTR_CONTROL_DISABLE = 0
DTR_CONTROL_ENABLE = 1
SETDTR = 5
CLRDTR = 6
MS_DSR_ON = 32
EV_RING = 256
EV_PERR = 512
EV_ERR = 128
SETXOFF = 1
EV_RXCHAR = 1
GENERIC_WRITE = 1073741824
PURGE_TXCLEAR = 4
FILE_FLAG_OVERLAPPED = 1073741824
EV_DSR = 16
MAXDWORD = 4294967295
EV_RLSD = 32
ERROR_IO_PENDING = 997
MS_CTS_ON = 16
EV_EVENT1 = 2048
EV_RX80FULL = 1024
PURGE_RXABORT = 2
FILE_ATTRIBUTE_NORMAL = 128
PURGE_TXABORT = 1
SETXON = 2
OPEN_EXISTING = 3
MS_RING_ON = 64
EV_TXEMPTY = 4
EV_RXFLAG = 2
MS_RLSD_ON = 128
GENERIC_READ = 2147483648
EV_EVENT2 = 4096
EV_CTS = 8
EV_BREAK = 64
PURGE_RXCLEAR = 8
INFINITE = 4294967295

class N11_OVERLAPPED4DOLLAR_48E(Union):
    pass


class N11_OVERLAPPED4DOLLAR_484DOLLAR_49E(Structure):
    pass


N11_OVERLAPPED4DOLLAR_484DOLLAR_49E._fields_ = [
 (
  'Offset', DWORD),
 (
  'OffsetHigh', DWORD)]
PVOID = c_void_p
N11_OVERLAPPED4DOLLAR_48E._anonymous_ = [
 '_0']
N11_OVERLAPPED4DOLLAR_48E._fields_ = [
 (
  '_0', N11_OVERLAPPED4DOLLAR_484DOLLAR_49E),
 (
  'Pointer', PVOID)]
_OVERLAPPED._anonymous_ = [
 '_0']
_OVERLAPPED._fields_ = [
 (
  'Internal', ULONG_PTR),
 (
  'InternalHigh', ULONG_PTR),
 (
  '_0', N11_OVERLAPPED4DOLLAR_48E),
 (
  'hEvent', HANDLE)]
_SECURITY_ATTRIBUTES._fields_ = [
 (
  'nLength', DWORD),
 (
  'lpSecurityDescriptor', LPVOID),
 (
  'bInheritHandle', BOOL)]
_COMSTAT._fields_ = [
 (
  'fCtsHold', DWORD, 1),
 (
  'fDsrHold', DWORD, 1),
 (
  'fRlsdHold', DWORD, 1),
 (
  'fXoffHold', DWORD, 1),
 (
  'fXoffSent', DWORD, 1),
 (
  'fEof', DWORD, 1),
 (
  'fTxim', DWORD, 1),
 (
  'fReserved', DWORD, 25),
 (
  'cbInQue', DWORD),
 (
  'cbOutQue', DWORD)]
_DCB._fields_ = [
 (
  'DCBlength', DWORD),
 (
  'BaudRate', DWORD),
 (
  'fBinary', DWORD, 1),
 (
  'fParity', DWORD, 1),
 (
  'fOutxCtsFlow', DWORD, 1),
 (
  'fOutxDsrFlow', DWORD, 1),
 (
  'fDtrControl', DWORD, 2),
 (
  'fDsrSensitivity', DWORD, 1),
 (
  'fTXContinueOnXoff', DWORD, 1),
 (
  'fOutX', DWORD, 1),
 (
  'fInX', DWORD, 1),
 (
  'fErrorChar', DWORD, 1),
 (
  'fNull', DWORD, 1),
 (
  'fRtsControl', DWORD, 2),
 (
  'fAbortOnError', DWORD, 1),
 (
  'fDummy2', DWORD, 17),
 (
  'wReserved', WORD),
 (
  'XonLim', WORD),
 (
  'XoffLim', WORD),
 (
  'ByteSize', BYTE),
 (
  'Parity', BYTE),
 (
  'StopBits', BYTE),
 (
  'XonChar', c_char),
 (
  'XoffChar', c_char),
 (
  'ErrorChar', c_char),
 (
  'EofChar', c_char),
 (
  'EvtChar', c_char),
 (
  'wReserved1', WORD)]
_COMMTIMEOUTS._fields_ = [
 (
  'ReadIntervalTimeout', DWORD),
 (
  'ReadTotalTimeoutMultiplier', DWORD),
 (
  'ReadTotalTimeoutConstant', DWORD),
 (
  'WriteTotalTimeoutMultiplier', DWORD),
 (
  'WriteTotalTimeoutConstant', DWORD)]
__all__ = [
 'GetLastError', 'MS_CTS_ON', 'FILE_ATTRIBUTE_NORMAL',
 'DTR_CONTROL_ENABLE', '_COMSTAT', 'MS_RLSD_ON',
 'GetOverlappedResult', 'SETXON', 'PURGE_TXABORT',
 'PurgeComm', 'N11_OVERLAPPED4DOLLAR_48E', 'EV_RING',
 'ONESTOPBIT', 'SETXOFF', 'PURGE_RXABORT', 'GetCommState',
 'RTS_CONTROL_ENABLE', '_DCB', 'CreateEvent',
 '_COMMTIMEOUTS', '_SECURITY_ATTRIBUTES', 'EV_DSR',
 'EV_PERR', 'EV_RXFLAG', 'OPEN_EXISTING', 'DCB',
 'FILE_FLAG_OVERLAPPED', 'EV_CTS', 'SetupComm',
 'LPOVERLAPPED', 'EV_TXEMPTY', 'ClearCommBreak',
 'LPSECURITY_ATTRIBUTES', 'SetCommBreak', 'SetCommTimeouts',
 'COMMTIMEOUTS', 'ODDPARITY', 'EV_RLSD',
 'GetCommModemStatus', 'EV_EVENT2', 'PURGE_TXCLEAR',
 'EV_BREAK', 'EVENPARITY', 'LPCVOID', 'COMSTAT', 'ReadFile',
 'PVOID', '_OVERLAPPED', 'WriteFile', 'GetCommTimeouts',
 'ResetEvent', 'EV_RXCHAR', 'LPCOMSTAT', 'ClearCommError',
 'ERROR_IO_PENDING', 'EscapeCommFunction', 'GENERIC_READ',
 'RTS_CONTROL_HANDSHAKE', 'OVERLAPPED',
 'DTR_CONTROL_HANDSHAKE', 'PURGE_RXCLEAR', 'GENERIC_WRITE',
 'LPDCB', 'CreateEventW', 'SetCommMask', 'EV_EVENT1',
 'SetCommState', 'LPVOID', 'CreateFileW', 'LPDWORD',
 'EV_RX80FULL', 'TWOSTOPBITS', 'LPCOMMTIMEOUTS', 'MAXDWORD',
 'MS_DSR_ON', 'MS_RING_ON',
 'N11_OVERLAPPED4DOLLAR_484DOLLAR_49E', 'EV_ERR',
 'ULONG_PTR', 'CreateFile', 'NOPARITY', 'CloseHandle']