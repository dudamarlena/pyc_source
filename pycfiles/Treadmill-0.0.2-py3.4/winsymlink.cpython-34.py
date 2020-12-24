# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/syscall/winsymlink.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 7093 bytes
"""Module for handlinkg symlinks on windows"""
import ctypes.wintypes, errno, os, struct
FSCTL_GET_REPARSE_POINT = 589992
FILE_ATTRIBUTE_REPARSE_POINT = 1024
GENERIC_READ = 2147483648
OPEN_EXISTING = 3
INVALID_HANDLE_VALUE = ctypes.wintypes.HANDLE(-1).value
INVALID_FILE_ATTRIBUTES = 4294967295
FILE_FLAG_REPARSE_BACKUP = 35651584

def _errcheck_link(value, func, args):
    """Checks CreateSymbolicLinkW and CreateHardLinkW result"""
    if value != 0:
        return
    last_error = ctypes.windll.kernel32.GetLastError()
    if last_error == 0 or last_error == 2:
        return
    if last_error == 183:
        raise OSError(errno.EEXIST, 'Cannot create a file when that file already exists', args[0])


DeviceIoControl = ctypes.windll.kernel32.DeviceIoControl
DeviceIoControl.argtypes = [
 ctypes.wintypes.HANDLE,
 ctypes.wintypes.DWORD,
 ctypes.wintypes.LPVOID,
 ctypes.wintypes.DWORD,
 ctypes.wintypes.LPVOID,
 ctypes.wintypes.DWORD,
 ctypes.POINTER(ctypes.wintypes.DWORD),
 ctypes.wintypes.LPVOID]
DeviceIoControl.restype = ctypes.wintypes.BOOL
CreateSymbolicLinkW = ctypes.windll.kernel32.CreateSymbolicLinkW
CreateSymbolicLinkW.argtypes = [
 ctypes.c_wchar_p,
 ctypes.c_wchar_p,
 ctypes.c_uint32]
CreateSymbolicLinkW.restype = ctypes.wintypes.BOOLEAN
CreateSymbolicLinkW.errcheck = _errcheck_link
CreateHardLinkW = ctypes.windll.kernel32.CreateHardLinkW
CreateHardLinkW.argtypes = [
 ctypes.c_wchar_p,
 ctypes.c_wchar_p,
 ctypes.c_void_p]
CreateHardLinkW.restype = ctypes.wintypes.BOOL
CreateHardLinkW.errcheck = _errcheck_link

def _islink(path):
    """Gets whether the specified path is symlink"""
    if not os.path.isdir(path):
        return False
    if not isinstance(path, str):
        path = str(path)
    attributes = ctypes.windll.kernel32.GetFileAttributesW(path)
    if attributes == INVALID_FILE_ATTRIBUTES:
        return False
    return attributes & FILE_ATTRIBUTE_REPARSE_POINT > 0


def device_io_control(hDevice, ioControlCode, input_buffer, output_buffer):
    """Sends a control code directly to a specified device driver,
    causing the corresponding device to perform the corresponding operation"""
    if input_buffer:
        input_size = len(input_buffer)
    else:
        input_size = 0
    if isinstance(output_buffer, int):
        output_buffer = ctypes.create_string_buffer(output_buffer)
    output_size = len(output_buffer)
    assert isinstance(output_buffer, ctypes.Array)
    bytesReturned = ctypes.wintypes.DWORD()
    status = DeviceIoControl(hDevice, ioControlCode, input_buffer, input_size, output_buffer, output_size, bytesReturned, None)
    if status != 0:
        return output_buffer[:bytesReturned.value]
    else:
        return


def _readlink(path):
    """ Windows readlink implementation. """
    is_unicode = isinstance(path, str)
    if not is_unicode:
        path = str(path)
    if not _islink(path):
        raise OSError(errno.EINVAL, 'Invalid argument', path)
    hfile = ctypes.windll.kernel32.CreateFileW(path, GENERIC_READ, 0, None, OPEN_EXISTING, FILE_FLAG_REPARSE_BACKUP, None)
    if hfile == INVALID_HANDLE_VALUE:
        raise OSError(errno.ENOENT, 'No such file or directory', path)
    data_buffer = device_io_control(hfile, FSCTL_GET_REPARSE_POINT, None, 16384)
    ctypes.windll.kernel32.CloseHandle(hfile)
    if not data_buffer or len(data_buffer) < 9:
        raise OSError(errno.ENOENT, 'No such file or directory', path)
    SymbolicLinkReparseFormat = 'LHHHHHHL'
    SymbolicLinkReparseSize = struct.calcsize(SymbolicLinkReparseFormat)
    tag, dataLength, reserver, SubstituteNameOffset, SubstituteNameLength, PrintNameOffset, PrintNameLength, Flags = struct.unpack(SymbolicLinkReparseFormat, data_buffer[:SymbolicLinkReparseSize])
    start = SubstituteNameOffset + SymbolicLinkReparseSize
    actualPath = data_buffer[start:start + SubstituteNameLength].decode('utf-16')
    index = actualPath.find('\x00')
    if index > 0:
        actualPath = actualPath[:index]
    if actualPath.startswith('\\??'):
        actualPath = actualPath[4:]
    if not is_unicode:
        return str(actualPath)
    return actualPath


def _link(filename, existing_filename):
    """symlink(source, link_name)
        Creates a symbolic link pointing to source named link_name"""
    CreateHardLinkW(filename, existing_filename, 0)


def _symlink(source, link_name):
    """symlink(source, link_name)
        Creates a symbolic link pointing to source named link_name"""
    flags = 0
    if source is not None:
        if os.path.isdir(source):
            flags = 1
    CreateSymbolicLinkW(link_name, source, flags)


def _unlink(path):
    """Remove (delete) the file path."""
    if os.path.isdir(path):
        os.rmdir(path)
    else:
        os.remove(path)


os.symlink = _symlink
os.link = _link
os.readlink = _readlink
os.path.islink = _islink
os.unlink = _unlink