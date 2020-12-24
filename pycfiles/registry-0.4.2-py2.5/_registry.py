# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\_registry.py
# Compiled at: 2009-02-23 11:18:56
"""Lower-level API for handling registry
through ctypes.
"""
from ctypes import Structure
from ctypes import byref
from ctypes import c_ulong
from ctypes import c_wchar_p
from ctypes import create_string_buffer
from ctypes import create_unicode_buffer
from ctypes import sizeof
from ctypes import windll
import _winreg, struct, types
DWORD = c_ulong
HANDLE = DWORD
REG_DWORD = _winreg.REG_DWORD
REG_DWORD_BIG_ENDIAN = _winreg.REG_DWORD_BIG_ENDIAN
REG_EXPAND_SZ = _winreg.REG_EXPAND_SZ
REG_LINK = _winreg.REG_LINK
REG_SZ = _winreg.REG_SZ
REG_MULTI_SZ = _winreg.REG_MULTI_SZ
KEY_ALL_ACCESS = 983103
KEY_CREATE_LINK = 32
KEY_CREATE_SUB_KEY = 4
KEY_EXECUTE = 131097
KEY_READ = 131097
KEY_NOTIFY = 16
KEY_QUERY_VALUE = 1
KEY_SET_VALUE = 2
KEY_WOW64_32KEY = 512
KEY_WOW64_64KEY = 256
KEY_WRITE = 131078
MAX_KEYNAME_SIZE = 255

class FILETIME(Structure):
    """Sstructure used for getting last modified-time from registry key."""
    _fields_ = [
     (
      'dwLowDateTime', DWORD),
     (
      'dwHighDateTime', DWORD)]

    def __str__(self):
        text = 'dwLowDateTime: %s' % self.dwLowDateTime + 'dwHighDateTime: %s' % self.dwHighDateTime
        return text


def _win2unixtime(seconds):
    """Changes last-modified time from Windows registry time into mktime."""
    diff = 11644473600
    seconds = seconds / pow(10, 7)
    mktime = seconds - diff
    return mktime


def _python2wintype(data, regtype):
    """Changes data from Python type to format usable by Windows API."""
    if regtype in (REG_SZ, REG_EXPAND_SZ):
        buff = create_unicode_buffer(data)
    elif regtype == REG_MULTI_SZ:
        converted = ''
        for item in data:
            converted = ('').join((converted, item, '\x00'))

        buff = create_unicode_buffer(converted)
    elif regtype in (REG_DWORD, REG_DWORD_BIG_ENDIAN):
        buff = create_string_buffer(4)
        if regtype == REG_DWORD:
            buff.value = struct.pack('<l', int(data))
        else:
            buff.value = struct.pack('>l', int(data))
    elif regtype == 11:
        buff = create_string_buffer(8)
        buff.value = struct.pack('l2', int(data))
    elif regtype == REG_LINK:
        buff = create_string_buffer(len(data))
        buff.value = data
    else:
        buff = create_string_buffer(len(data))
        buff.value = data
    return buff


def _win2pythontype(name, data, regtype):
    """Changes data from Windows registry data to corresponding Python type."""
    if regtype in (REG_SZ, REG_EXPAND_SZ):
        if data[len(data) - 1:] != '\x00':
            data = data[:len(data)]
        else:
            data = data[:len(data) - 1]
    elif regtype == REG_MULTI_SZ:
        datalen = len(data[:len(data)].rstrip('\x00'))
        data = data[:datalen].split('\x00')
        if data == ['']:
            data = []
    elif regtype == REG_DWORD:
        data = struct.unpack('l', data[:4].ljust(4, '\x00'))[0]
    elif regtype == REG_DWORD_BIG_ENDIAN:
        data = struct.unpack('>l', data[:4].rjust(4, '\x00'))[0]
    elif regtype == 11:
        data = struct.unpack('ll', data[:8].ljust(8, '\x00'))[0]
    else:
        data = data[:len(data)]
    return (
     name, data, regtype)


def ConnectRegistry(key, computer=None):
    """Establishes a connection to a predefined registry key."""
    reg = HANDLE()
    if isinstance(key, types.StringTypes):
        key = getattr(_winreg, key)
    if computer is not None:
        computer = unicode(computer)
    feedback = windll.advapi32.RegConnectRegistryW(computer, key, byref(reg))
    if feedback != 0:
        raise WindowsError, feedback
    else:
        return reg.value
    return


def OpenKeyEx(reg, path, access=KEY_ALL_ACCESS):
    """Opens the specified registry key."""
    handle = HANDLE()
    windll.advapi32.RegOpenKeyExW(reg, c_wchar_p(path), 0, access, byref(handle))
    return handle.value


def CloseKey(handle):
    """Closes a handle to the specified registry key."""
    return windll.advapi32.RegCloseKey(handle)


def CreateKey(handle, valuename):
    """Creates the specified registry key."""
    new = DWORD()
    valuename = unicode(valuename)
    feedback = windll.advapi32.RegCreateKeyW(handle, c_wchar_p(valuename), byref(new))
    if feedback != 0:
        raise WindowsError, feedback
    return new.value


def DeleteKey(handle, keyname):
    """Deletes a subkey and its values."""
    return windll.advapi32.RegDeleteKeyW(handle, c_wchar_p(keyname))


def DeleteKeyEx(handle, keyname, sam=KEY_WOW64_32KEY):
    """Deletes a subkey and its values from the specified
platform-specific view of the registry."""
    return windll.advapi32.RegDeleteKeyExW(handle, c_wchar_p(keyname), sam, 0)


def EnumKeyEx(handle, index):
    """Enumerates the subkeys of the specified open registry key."""
    name = create_unicode_buffer(MAX_KEYNAME_SIZE + 1)
    feedback = windll.advapi32.RegEnumKeyExW(handle, DWORD(index), byref(name), byref(DWORD(sizeof(name))), None, None, None, None)
    if feedback != 0:
        raise WindowsError, feedback
    return name.value


def QueryInfoKey(handle):
    """Retrieves information about the specified registry key."""
    no_subkeys = DWORD()
    max_subkey_len = DWORD()
    max_class_len = DWORD()
    no_values = DWORD()
    max_valuename_len = DWORD()
    max_value_len = DWORD()
    security_descr = DWORD()
    last_write_time = FILETIME()
    feedback = windll.advapi32.RegQueryInfoKeyW(handle, None, None, None, byref(no_subkeys), byref(max_subkey_len), byref(max_class_len), byref(no_values), byref(max_valuename_len), byref(max_value_len), byref(security_descr), byref(last_write_time))
    if feedback != 0:
        raise WindowsError, feedback
    if not (last_write_time.dwHighDateTime == 0 and last_write_time.dwLowDateTime == 0):
        last_mod_date = _win2unixtime(last_write_time.dwHighDateTime * 4294967296 + last_write_time.dwLowDateTime)
    else:
        last_mod_date = 0
    return (
     no_subkeys.value,
     max_subkey_len.value,
     max_class_len.value,
     no_values.value,
     max_valuename_len.value,
     max_value_len.value,
     security_descr.value,
     last_mod_date)


def DeleteValue(handle, valuename):
    """Removes a named value from the specified registry key."""
    return windll.advapi32.RegDeleteValueW(handle, unicode(valuename))


def EnumValue(handle, index):
    """Enumerates the values for the specified open registry key."""
    max_valuename_len = QueryInfoKey(handle)[4]
    name = create_unicode_buffer(max_valuename_len + 1)
    regtype, size = DWORD(), DWORD()
    feedback = windll.advapi32.RegEnumValueW(handle, DWORD(index), byref(name), byref(DWORD(sizeof(name))), None, byref(regtype), None, byref(size))
    if feedback != 0:
        raise WindowsError, feedback
    if regtype.value in (REG_SZ,
     REG_MULTI_SZ,
     REG_EXPAND_SZ):
        data = create_unicode_buffer(size.value / 2)
    else:
        data = create_string_buffer(size.value)
    feedback = windll.advapi32.RegEnumValueW(handle, DWORD(index), byref(name), byref(DWORD(sizeof(name))), None, byref(regtype), byref(data), byref(DWORD(sizeof(data))))
    if feedback != 0:
        raise WindowsError, feedback
    return _win2pythontype(name.value, data, regtype.value)


def QueryValueEx(handle, valuename):
    """Used to retrieve a value of a registry key.
Handle must be a handle to an open registry key."""
    regtype, size = DWORD(), DWORD()
    name = unicode(valuename)
    feedback = windll.advapi32.RegQueryValueExW(handle, name, None, byref(regtype), None, byref(size))
    if feedback != 0:
        raise WindowsError, feedback
    if regtype.value in (REG_SZ, REG_MULTI_SZ, REG_EXPAND_SZ):
        data = create_unicode_buffer(size.value / 2)
    else:
        data = create_string_buffer(size.value)
    feedback = windll.advapi32.RegQueryValueExW(handle, name, None, byref(regtype), data, byref(DWORD(sizeof(data))))
    if feedback != 0:
        raise WindowsError, feedback
    return _win2pythontype(name, data, regtype.value)[1:]


def SetValueEx(handle, valuename, regtype, data):
    """Sets the data and type of a specified value under a registry key."""
    valuename = unicode(valuename)
    if isinstance(regtype, types.StringTypes):
        regtype = getattr(_winreg, regtype)
    buff = _python2wintype(data, regtype)
    return windll.advapi32.RegSetValueExW(handle, valuename, 0, regtype, buff, sizeof(buff))