# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-MsePIp/scf/tcfcli/cmds/native/common/runtime/python3.6/pstool/winps.py
# Compiled at: 2019-12-02 05:04:19
__all__ = [
 'win_peak_memory']
import ctypes
from ctypes import wintypes
GetCurrentProcess = ctypes.windll.kernel32.GetCurrentProcess
GetCurrentProcess.argtypes = []
GetCurrentProcess.restype = wintypes.HANDLE
SIZE_T = ctypes.c_size_t

class PROCESS_MEMORY_COUNTERS_EX(ctypes.Structure):
    _fields_ = [
     (
      'cb', wintypes.DWORD),
     (
      'PageFaultCount', wintypes.DWORD),
     (
      'PeakWorkingSetSize', SIZE_T),
     (
      'WorkingSetSize', SIZE_T),
     (
      'QuotaPeakPagedPoolUsage', SIZE_T),
     (
      'QuotaPagedPoolUsage', SIZE_T),
     (
      'QuotaPeakNonPagedPoolUsage', SIZE_T),
     (
      'QuotaNonPagedPoolUsage', SIZE_T),
     (
      'PagefileUsage', SIZE_T),
     (
      'PeakPagefileUsage', SIZE_T),
     (
      'PrivateUsage', SIZE_T)]


GetProcessMemoryInfo = ctypes.windll.psapi.GetProcessMemoryInfo
GetProcessMemoryInfo.argtypes = [
 wintypes.HANDLE,
 ctypes.POINTER(PROCESS_MEMORY_COUNTERS_EX),
 wintypes.DWORD]
GetProcessMemoryInfo.restype = wintypes.BOOL

def _get_current_process():
    """Return handle to current process."""
    return GetCurrentProcess()


def win_peak_memory(process=None):
    """Return Win32 process memory counters structure as a dict."""
    if process is None:
        process = _get_current_process()
    counters = PROCESS_MEMORY_COUNTERS_EX()
    ret = GetProcessMemoryInfo(process, ctypes.byref(counters), ctypes.sizeof(counters))
    if not ret:
        return 0
    else:
        info = dict((name, getattr(counters, name)) for name, _ in counters._fields_)
        return int(info['PeakWorkingSetSize'] / 1048576)