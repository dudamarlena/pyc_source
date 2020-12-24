# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/syscall/winapi.py
# Compiled at: 2017-03-22 02:19:40
# Size of source mod 2**32: 5758 bytes
"""Windows API function wrappers
"""
import os, ctypes, ctypes.wintypes
assert os.name == 'nt'

class MEMORYSTATUSEX(ctypes.Structure):
    __doc__ = 'Contains information about the current state of both\n    physical and virtual memory, including extended memory'
    _fields_ = [
     (
      'dwLength', ctypes.c_ulong),
     (
      'dwMemoryLoad', ctypes.c_ulong),
     (
      'ullTotalPhys', ctypes.c_ulonglong),
     (
      'ullAvailPhys', ctypes.c_ulonglong),
     (
      'ullTotalPageFile', ctypes.c_ulonglong),
     (
      'ullAvailPageFile', ctypes.c_ulonglong),
     (
      'ullTotalVirtual', ctypes.c_ulonglong),
     (
      'ullAvailVirtual', ctypes.c_ulonglong),
     (
      'sullAvailExtendedVirtual', ctypes.c_ulonglong)]

    def __init__(self):
        self.dwLength = ctypes.sizeof(self)
        super(MEMORYSTATUSEX, self).__init__()


class SID_IDENTIFIER_AUTHORITY(ctypes.Structure):
    __doc__ = 'The SID_IDENTIFIER_AUTHORITY structure represents the top-level\n    authority of a security identifier (SID).'
    _fields_ = [
     (
      'byte0', ctypes.c_byte),
     (
      'byte1', ctypes.c_byte),
     (
      'byte2', ctypes.c_byte),
     (
      'byte3', ctypes.c_byte),
     (
      'byte4', ctypes.c_byte),
     (
      'byte5', ctypes.c_byte)]

    def __init__(self, authority):
        self.byte5 = authority
        super(SID_IDENTIFIER_AUTHORITY, self).__init__()


def GetUserName():
    """Returns the current user name"""
    size = ctypes.pointer(ctypes.c_ulong(0))
    ctypes.windll.advapi32.GetUserNameA(None, size)
    user_buff = ctypes.create_string_buffer(size.contents.value)
    ctypes.windll.advapi32.GetUserNameA(user_buff, size)
    username = user_buff.value
    return username


def AllocateAndInitializeSid(pIdentifierAuthority, nSubAuthorityCount, dwSubAuthority0, dwSubAuthority1, dwSubAuthority2, dwSubAuthority3, dwSubAuthority4, dwSubAuthority5, dwSubAuthority6, dwSubAuthority7):
    """he AllocateAndInitializeSid function allocates and initializes
    a security identifier (SID) with up to eight subauthorities."""
    sid = ctypes.c_void_p()
    apiresult = ctypes.windll.advapi32.AllocateAndInitializeSid(ctypes.byref(pIdentifierAuthority), nSubAuthorityCount, dwSubAuthority0, dwSubAuthority1, dwSubAuthority2, dwSubAuthority3, dwSubAuthority4, dwSubAuthority5, dwSubAuthority6, dwSubAuthority7, ctypes.byref(sid))
    if apiresult == 0:
        raise Exception('AllocateAndInitializeSid failed')
    return sid


def CheckTokenMembership(TokenHandle, SidToCheck):
    """The CheckTokenMembership function determines whether a specified
    security identifier (SID) is enabled in an access token. """
    is_admin = ctypes.wintypes.BOOL()
    apiresult = ctypes.windll.advapi32.CheckTokenMembership(TokenHandle, SidToCheck, ctypes.byref(is_admin))
    if apiresult == 0:
        raise Exception('CheckTokenMembership failed')
    return is_admin.value != 0


def FreeSid(pSid):
    """The FreeSid function frees a security identifier (SID)
    previously allocated by using the AllocateAndInitializeSid function."""
    ctypes.windll.advapi32.FreeSid(pSid)


def is_user_admin():
    """Gets whether the current user has administrator rights on windows"""
    if GetUserName() == 'system':
        return True
    nt_authority = SID_IDENTIFIER_AUTHORITY(5)
    SECURITY_BUILTIN_DOMAIN_RID = 32
    DOMAIN_ALIAS_RID_ADMINS = 544
    sid = AllocateAndInitializeSid(nt_authority, 2, SECURITY_BUILTIN_DOMAIN_RID, DOMAIN_ALIAS_RID_ADMINS, 0, 0, 0, 0, 0, 0)
    try:
        return CheckTokenMembership(0, sid)
    finally:
        FreeSid(sid)


def GetDiskFreeSpaceExW(path):
    """Retrieves information about the amount of space that is available
    on a disk volume, which is the total amount of space, the total amount
    of free space, and the total amount of free space available to the user
    that is associated with the calling thread."""
    free = ctypes.c_ulonglong(0)
    total = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(path), None, ctypes.pointer(total), ctypes.pointer(free))
    return (total.value, free.value)


def GetTickCount64():
    """Retrieves the number of milliseconds that have elapsed
    since the system was started."""
    return ctypes.windll.kernel32.GetTickCount64()


def GlobalMemoryStatusEx():
    """Retrieves information about the system's current usage of
    both physical and virtual memory."""
    memory = MEMORYSTATUSEX()
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory))
    return memory