# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./build/lib.linux-x86_64-2.7/serial/tools/list_ports_windows.py
# Compiled at: 2015-09-26 22:25:56
import re, ctypes
from ctypes.wintypes import BOOL
from ctypes.wintypes import HWND
from ctypes.wintypes import DWORD
from ctypes.wintypes import WORD
from ctypes.wintypes import LONG
from ctypes.wintypes import ULONG
from ctypes.wintypes import LPCSTR
from ctypes.wintypes import HKEY
from ctypes.wintypes import BYTE
import serial
from serial.win32 import ULONG_PTR
from serial.tools import list_ports_common

def ValidHandle(value, func, arguments):
    if value == 0:
        raise ctypes.WinError()
    return value


NULL = 0
HDEVINFO = ctypes.c_void_p
PCTSTR = ctypes.c_char_p
PTSTR = ctypes.c_void_p
CHAR = ctypes.c_char
LPDWORD = PDWORD = ctypes.POINTER(DWORD)
LPBYTE = PBYTE = ctypes.c_void_p
ACCESS_MASK = DWORD
REGSAM = ACCESS_MASK

def byte_buffer(length):
    """Get a buffer for a string"""
    return (BYTE * length)()


def string(buffer):
    s = []
    for c in buffer:
        if c == 0:
            break
        s.append(chr(c & 255))

    return ('').join(s)


class GUID(ctypes.Structure):
    _fields_ = [
     (
      'Data1', DWORD),
     (
      'Data2', WORD),
     (
      'Data3', WORD),
     (
      'Data4', BYTE * 8)]

    def __str__(self):
        return '{%08x-%04x-%04x-%s-%s}' % (
         self.Data1,
         self.Data2,
         self.Data3,
         ('').join([ '%02x' % d for d in self.Data4[:2] ]),
         ('').join([ '%02x' % d for d in self.Data4[2:] ]))


class SP_DEVINFO_DATA(ctypes.Structure):
    _fields_ = [
     (
      'cbSize', DWORD),
     (
      'ClassGuid', GUID),
     (
      'DevInst', DWORD),
     (
      'Reserved', ULONG_PTR)]

    def __str__(self):
        return 'ClassGuid:%s DevInst:%s' % (self.ClassGuid, self.DevInst)


PSP_DEVINFO_DATA = ctypes.POINTER(SP_DEVINFO_DATA)
PSP_DEVICE_INTERFACE_DETAIL_DATA = ctypes.c_void_p
setupapi = ctypes.windll.LoadLibrary('setupapi')
SetupDiDestroyDeviceInfoList = setupapi.SetupDiDestroyDeviceInfoList
SetupDiDestroyDeviceInfoList.argtypes = [HDEVINFO]
SetupDiDestroyDeviceInfoList.restype = BOOL
SetupDiClassGuidsFromName = setupapi.SetupDiClassGuidsFromNameA
SetupDiClassGuidsFromName.argtypes = [PCTSTR, ctypes.POINTER(GUID), DWORD, PDWORD]
SetupDiClassGuidsFromName.restype = BOOL
SetupDiEnumDeviceInfo = setupapi.SetupDiEnumDeviceInfo
SetupDiEnumDeviceInfo.argtypes = [HDEVINFO, DWORD, PSP_DEVINFO_DATA]
SetupDiEnumDeviceInfo.restype = BOOL
SetupDiGetClassDevs = setupapi.SetupDiGetClassDevsA
SetupDiGetClassDevs.argtypes = [ctypes.POINTER(GUID), PCTSTR, HWND, DWORD]
SetupDiGetClassDevs.restype = HDEVINFO
SetupDiGetClassDevs.errcheck = ValidHandle
SetupDiGetDeviceRegistryProperty = setupapi.SetupDiGetDeviceRegistryPropertyA
SetupDiGetDeviceRegistryProperty.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, DWORD, PDWORD, PBYTE, DWORD, PDWORD]
SetupDiGetDeviceRegistryProperty.restype = BOOL
SetupDiGetDeviceInstanceId = setupapi.SetupDiGetDeviceInstanceIdA
SetupDiGetDeviceInstanceId.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, PTSTR, DWORD, PDWORD]
SetupDiGetDeviceInstanceId.restype = BOOL
SetupDiOpenDevRegKey = setupapi.SetupDiOpenDevRegKey
SetupDiOpenDevRegKey.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, DWORD, DWORD, DWORD, REGSAM]
SetupDiOpenDevRegKey.restype = HKEY
advapi32 = ctypes.windll.LoadLibrary('Advapi32')
RegCloseKey = advapi32.RegCloseKey
RegCloseKey.argtypes = [HKEY]
RegCloseKey.restype = LONG
RegQueryValueEx = advapi32.RegQueryValueExA
RegQueryValueEx.argtypes = [HKEY, LPCSTR, LPDWORD, LPDWORD, LPBYTE, LPDWORD]
RegQueryValueEx.restype = LONG
DIGCF_PRESENT = 2
DIGCF_DEVICEINTERFACE = 16
INVALID_HANDLE_VALUE = 0
ERROR_INSUFFICIENT_BUFFER = 122
SPDRP_HARDWAREID = 1
SPDRP_FRIENDLYNAME = 12
SPDRP_LOCATION_PATHS = 35
DICS_FLAG_GLOBAL = 1
DIREG_DEV = 1
KEY_READ = 131097
Ports = serial.to_bytes([80, 111, 114, 116, 115])
PortName = serial.to_bytes([80, 111, 114, 116, 78, 97, 109, 101])

def comports():
    GUIDs = (GUID * 8)()
    guids_size = DWORD()
    if not SetupDiClassGuidsFromName(Ports, GUIDs, ctypes.sizeof(GUIDs), ctypes.byref(guids_size)):
        raise ctypes.WinError()
    for index in range(guids_size.value):
        g_hdi = SetupDiGetClassDevs(ctypes.byref(GUIDs[index]), None, NULL, DIGCF_PRESENT)
        devinfo = SP_DEVINFO_DATA()
        devinfo.cbSize = ctypes.sizeof(devinfo)
        index = 0
        while SetupDiEnumDeviceInfo(g_hdi, index, ctypes.byref(devinfo)):
            index += 1
            hkey = SetupDiOpenDevRegKey(g_hdi, ctypes.byref(devinfo), DICS_FLAG_GLOBAL, 0, DIREG_DEV, KEY_READ)
            port_name_buffer = byte_buffer(250)
            port_name_length = ULONG(ctypes.sizeof(port_name_buffer))
            RegQueryValueEx(hkey, PortName, None, None, ctypes.byref(port_name_buffer), ctypes.byref(port_name_length))
            RegCloseKey(hkey)
            if string(port_name_buffer).startswith('LPT'):
                continue
            szHardwareID = byte_buffer(250)
            if not SetupDiGetDeviceInstanceId(g_hdi, ctypes.byref(devinfo), ctypes.byref(szHardwareID), ctypes.sizeof(szHardwareID) - 1, None):
                if not SetupDiGetDeviceRegistryProperty(g_hdi, ctypes.byref(devinfo), SPDRP_HARDWAREID, None, ctypes.byref(szHardwareID), ctypes.sizeof(szHardwareID) - 1, None):
                    if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
                        raise ctypes.WinError()
            szHardwareID_str = string(szHardwareID)
            info = list_ports_common.ListPortInfo(string(port_name_buffer))
            if szHardwareID_str.startswith('USB'):
                m = re.search('VID_([0-9a-f]{4})&PID_([0-9a-f]{4})(\\\\(\\w+))?', szHardwareID_str, re.I)
                if m:
                    info.vid = int(m.group(1), 16)
                    info.pid = int(m.group(2), 16)
                    if m.group(4):
                        info.serial_number = m.group(4)
                loc_path_str = byte_buffer(250)
                if SetupDiGetDeviceRegistryProperty(g_hdi, ctypes.byref(devinfo), SPDRP_LOCATION_PATHS, None, ctypes.byref(loc_path_str), ctypes.sizeof(loc_path_str) - 1, None):
                    m = re.finditer('USBROOT\\((\\w+)\\)|#USB\\((\\w+)\\)', string(loc_path_str))
                    location = []
                    for g in m:
                        if g.group(1):
                            location.append('%d' % (int(g.group(1)) + 1))
                        else:
                            if len(location) > 1:
                                location.append('.')
                            else:
                                location.append('-')
                            location.append(g.group(2))

                    if location:
                        info.location = ('').join(location)
                info.hwid = info.usb_info()
            else:
                info.hwid = szHardwareID_str
            szFriendlyName = byte_buffer(250)
            if SetupDiGetDeviceRegistryProperty(g_hdi, ctypes.byref(devinfo), SPDRP_FRIENDLYNAME, None, ctypes.byref(szFriendlyName), ctypes.sizeof(szFriendlyName) - 1, None):
                info.description = string(szFriendlyName)
            yield info

        SetupDiDestroyDeviceInfoList(g_hdi)

    return


if __name__ == '__main__':
    for port, desc, hwid in sorted(comports()):
        print '%s: %s [%s]' % (port, desc, hwid)