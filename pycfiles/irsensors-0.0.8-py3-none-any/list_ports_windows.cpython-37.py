# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ISEN\AppData\Local\Temp\pip-install-57ghrzot\pyserial\serial\tools\list_ports_windows.py
# Compiled at: 2019-09-23 21:15:07
# Size of source mod 2**32: 11336 bytes
import re, ctypes
from ctypes.wintypes import BOOL
from ctypes.wintypes import HWND
from ctypes.wintypes import DWORD
from ctypes.wintypes import WORD
from ctypes.wintypes import LONG
from ctypes.wintypes import ULONG
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
LPCTSTR = ctypes.c_wchar_p
PCTSTR = ctypes.c_wchar_p
PTSTR = ctypes.c_wchar_p
LPDWORD = PDWORD = ctypes.POINTER(DWORD)
LPBYTE = PBYTE = ctypes.c_void_p
ACCESS_MASK = DWORD
REGSAM = ACCESS_MASK

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
        return '{{{:08x}-{:04x}-{:04x}-{}-{}}}'.format(self.Data1, self.Data2, self.Data3, ''.join(['{:02x}'.format(d) for d in self.Data4[:2]]), ''.join(['{:02x}'.format(d) for d in self.Data4[2:]]))


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
        return 'ClassGuid:{} DevInst:{}'.format(self.ClassGuid, self.DevInst)


PSP_DEVINFO_DATA = ctypes.POINTER(SP_DEVINFO_DATA)
PSP_DEVICE_INTERFACE_DETAIL_DATA = ctypes.c_void_p
setupapi = ctypes.windll.LoadLibrary('setupapi')
SetupDiDestroyDeviceInfoList = setupapi.SetupDiDestroyDeviceInfoList
SetupDiDestroyDeviceInfoList.argtypes = [HDEVINFO]
SetupDiDestroyDeviceInfoList.restype = BOOL
SetupDiClassGuidsFromName = setupapi.SetupDiClassGuidsFromNameW
SetupDiClassGuidsFromName.argtypes = [PCTSTR, ctypes.POINTER(GUID), DWORD, PDWORD]
SetupDiClassGuidsFromName.restype = BOOL
SetupDiEnumDeviceInfo = setupapi.SetupDiEnumDeviceInfo
SetupDiEnumDeviceInfo.argtypes = [HDEVINFO, DWORD, PSP_DEVINFO_DATA]
SetupDiEnumDeviceInfo.restype = BOOL
SetupDiGetClassDevs = setupapi.SetupDiGetClassDevsW
SetupDiGetClassDevs.argtypes = [ctypes.POINTER(GUID), PCTSTR, HWND, DWORD]
SetupDiGetClassDevs.restype = HDEVINFO
SetupDiGetClassDevs.errcheck = ValidHandle
SetupDiGetDeviceRegistryProperty = setupapi.SetupDiGetDeviceRegistryPropertyW
SetupDiGetDeviceRegistryProperty.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, DWORD, PDWORD, PBYTE, DWORD, PDWORD]
SetupDiGetDeviceRegistryProperty.restype = BOOL
SetupDiGetDeviceInstanceId = setupapi.SetupDiGetDeviceInstanceIdW
SetupDiGetDeviceInstanceId.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, PTSTR, DWORD, PDWORD]
SetupDiGetDeviceInstanceId.restype = BOOL
SetupDiOpenDevRegKey = setupapi.SetupDiOpenDevRegKey
SetupDiOpenDevRegKey.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, DWORD, DWORD, DWORD, REGSAM]
SetupDiOpenDevRegKey.restype = HKEY
advapi32 = ctypes.windll.LoadLibrary('Advapi32')
RegCloseKey = advapi32.RegCloseKey
RegCloseKey.argtypes = [HKEY]
RegCloseKey.restype = LONG
RegQueryValueEx = advapi32.RegQueryValueExW
RegQueryValueEx.argtypes = [HKEY, LPCTSTR, LPDWORD, LPDWORD, LPBYTE, LPDWORD]
RegQueryValueEx.restype = LONG
DIGCF_PRESENT = 2
DIGCF_DEVICEINTERFACE = 16
INVALID_HANDLE_VALUE = 0
ERROR_INSUFFICIENT_BUFFER = 122
SPDRP_HARDWAREID = 1
SPDRP_FRIENDLYNAME = 12
SPDRP_LOCATION_PATHS = 35
SPDRP_MFG = 11
DICS_FLAG_GLOBAL = 1
DIREG_DEV = 1
KEY_READ = 131097

def iterate_comports():
    """Return a generator that yields descriptions for serial ports"""
    GUIDs = (GUID * 8)()
    guids_size = DWORD()
    if not SetupDiClassGuidsFromName('Ports', GUIDs, ctypes.sizeof(GUIDs), ctypes.byref(guids_size)):
        raise ctypes.WinError()
    for index in range(guids_size.value):
        bInterfaceNumber = None
        g_hdi = SetupDiGetClassDevs(ctypes.byref(GUIDs[index]), None, NULL, DIGCF_PRESENT)
        devinfo = SP_DEVINFO_DATA()
        devinfo.cbSize = ctypes.sizeof(devinfo)
        index = 0
        while SetupDiEnumDeviceInfo(g_hdi, index, ctypes.byref(devinfo)):
            index += 1
            hkey = SetupDiOpenDevRegKey(g_hdi, ctypes.byref(devinfo), DICS_FLAG_GLOBAL, 0, DIREG_DEV, KEY_READ)
            port_name_buffer = ctypes.create_unicode_buffer(250)
            port_name_length = ULONG(ctypes.sizeof(port_name_buffer))
            RegQueryValueEx(hkey, 'PortName', None, None, ctypes.byref(port_name_buffer), ctypes.byref(port_name_length))
            RegCloseKey(hkey)
            if port_name_buffer.value.startswith('LPT'):
                continue
            else:
                szHardwareID = ctypes.create_unicode_buffer(250)
                if not SetupDiGetDeviceInstanceId(g_hdi, ctypes.byref(devinfo), szHardwareID, ctypes.sizeof(szHardwareID) - 1, None):
                    if not SetupDiGetDeviceRegistryProperty(g_hdi, ctypes.byref(devinfo), SPDRP_HARDWAREID, None, ctypes.byref(szHardwareID), ctypes.sizeof(szHardwareID) - 1, None):
                        if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
                            raise ctypes.WinError()
                szHardwareID_str = szHardwareID.value
                info = list_ports_common.ListPortInfo(port_name_buffer.value)
                if szHardwareID_str.startswith('USB'):
                    m = re.search('VID_([0-9a-f]{4})(&PID_([0-9a-f]{4}))?(&MI_(\\d{2}))?(\\\\(\\w+))?', szHardwareID_str, re.I)
                    if m:
                        info.vid = int(m.group(1), 16)
                        if m.group(3):
                            info.pid = int(m.group(3), 16)
                        if m.group(5):
                            bInterfaceNumber = int(m.group(5))
                        if m.group(7):
                            info.serial_number = m.group(7)
                    loc_path_str = ctypes.create_unicode_buffer(250)
                    if SetupDiGetDeviceRegistryProperty(g_hdi, ctypes.byref(devinfo), SPDRP_LOCATION_PATHS, None, ctypes.byref(loc_path_str), ctypes.sizeof(loc_path_str) - 1, None):
                        m = re.finditer('USBROOT\\((\\w+)\\)|#USB\\((\\w+)\\)', loc_path_str.value)
                        location = []
                        for g in m:
                            if g.group(1):
                                location.append('{:d}'.format(int(g.group(1)) + 1))
                            else:
                                if len(location) > 1:
                                    location.append('.')
                                else:
                                    location.append('-')
                                location.append(g.group(2))

                        if bInterfaceNumber is not None:
                            location.append(':{}.{}'.format('x', bInterfaceNumber))
                        if location:
                            info.location = ''.join(location)
                    info.hwid = info.usb_info()
                else:
                    if szHardwareID_str.startswith('FTDIBUS'):
                        m = re.search('VID_([0-9a-f]{4})\\+PID_([0-9a-f]{4})(\\+(\\w+))?', szHardwareID_str, re.I)
                        if m:
                            info.vid = int(m.group(1), 16)
                            info.pid = int(m.group(2), 16)
                            if m.group(4):
                                info.serial_number = m.group(4)
                        info.hwid = info.usb_info()
                    else:
                        info.hwid = szHardwareID_str
            szFriendlyName = ctypes.create_unicode_buffer(250)
            if SetupDiGetDeviceRegistryProperty(g_hdi, ctypes.byref(devinfo), SPDRP_FRIENDLYNAME, None, ctypes.byref(szFriendlyName), ctypes.sizeof(szFriendlyName) - 1, None):
                info.description = szFriendlyName.value
            szManufacturer = ctypes.create_unicode_buffer(250)
            if SetupDiGetDeviceRegistryProperty(g_hdi, ctypes.byref(devinfo), SPDRP_MFG, None, ctypes.byref(szManufacturer), ctypes.sizeof(szManufacturer) - 1, None):
                info.manufacturer = szManufacturer.value
            yield info

        SetupDiDestroyDeviceInfoList(g_hdi)


def comports(include_links=False):
    """Return a list of info objects about serial ports"""
    return list(iterate_comports())


if __name__ == '__main__':
    for port, desc, hwid in sorted(comports()):
        print('{}: {} [{}]'.format(port, desc, hwid))