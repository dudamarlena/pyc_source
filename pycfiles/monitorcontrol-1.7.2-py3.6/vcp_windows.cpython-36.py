# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/monitorcontrol/vcp/vcp_windows.py
# Compiled at: 2020-02-29 14:57:33
# Size of source mod 2**32: 6447 bytes
from typing import List, Tuple
import sys, ctypes
from .vcp_abc import VCP, VCPError
if sys.platform == 'win32':
    from ctypes.wintypes import DWORD, RECT, BOOL, HMONITOR, HDC, LPARAM, HANDLE, BYTE, WCHAR

    class PhysicalMonitor(ctypes.Structure):
        _fields_ = [
         (
          'handle', HANDLE), ('description', WCHAR * 128)]


    class WindowsVCP(VCP):
        __doc__ = "\n        Windows API access to a monitor's virtual control panel.\n\n        References:\n            https://stackoverflow.com/questions/16588133/\n        "

        def __init__(self, hmonitor: HMONITOR):
            """
            Args:
                hmonitor: logical monitor handle
            """
            self.hmonitor = hmonitor

        def __enter__(self):
            self.open()

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.close()

        def open(self):
            """
            Opens the connection to the monitor.

            Raises:
                VCPError: unable to open monitor
            """
            num_physical = DWORD()
            try:
                ctypes.windll.dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(self.hmonitor, ctypes.byref(num_physical))
            except ctypes.WinError as e:
                raise VCPError('Windows API call failed') from e

            if num_physical.value == 0:
                raise VCPError('no physical monitor found')
            else:
                if num_physical.value > 1:
                    raise VCPError('more than one physical monitor per hmonitor')
            physical_monitors = PhysicalMonitor * num_physical.value()
            try:
                ctypes.windll.dxva2.GetPhysicalMonitorsFromHMONITOR(self.hmonitor, num_physical.value, physical_monitors)
            except ctypes.WinError as e:
                raise VCPError('failed to open physical monitor handle') from e

            self.handle = physical_monitors[0].handle

        def close(self):
            """
            Closes the connection to the monitor.

            Raises:
                VCPError: unable to open monitor
            """
            try:
                ctypes.windll.dxva2.DestroyPhysicalMonitor(self.handle)
            except ctypes.WinError as e:
                raise VCPError('failed to close handle') from e

        def set_vcp_feature(self, code: int, value: int):
            """
            Sets the value of a feature on the virtual control panel.

            Args:
                code: feature code
                value: feature value

            Raises:
                VCPError: failed to set VCP feature
            """
            try:
                ctypes.windll.dxva2.SetVCPFeature(HANDLE(self.handle), BYTE(code), DWORD(value))
            except ctypes.WinError as e:
                raise VCPError('failed to close handle') from e

        def get_vcp_feature(self, code: int) -> Tuple[(int, int)]:
            """
            Gets the value of a feature from the virtual control panel.

            Args:
                code: feature code

            Returns:
                current feature value, maximum feature value

            Raises:
                VCPError: failed to get VCP feature
            """
            feature_current = DWORD()
            feature_max = DWORD()
            try:
                ctypes.windll.dxva2.GetVCPFeatureAndVCPFeatureReply(HANDLE(self.handle), BYTE(code), None, ctypes.byref(feature_current), ctypes.byref(feature_max))
            except ctypes.WinError as e:
                raise VCPError('failed to get VCP feature') from e

            return (
             feature_current.value, feature_max.value)


    def get_vcps() -> List[WindowsVCP]:
        """
        Opens handles to all physical VCPs.

        Returns:
            List of all VCPs detected.

        Raises:
            VCPError: failed to enumerate VCPs
        """
        vcps = []
        hmonitors = []
        try:

            def _callback(hmonitor, hdc, lprect, lparam):
                hmonitors.append(HMONITOR(hmonitor))
                del hmonitor
                del hdc
                del lprect
                del lparam
                return True

            MONITORENUMPROC = ctypes.WINFUNCTYPE(BOOL, HMONITOR, HDC, ctypes.POINTER(RECT), LPARAM)
            callback = MONITORENUMPROC(_callback)
            ctypes.windll.user32.EnumDisplayMonitors(0, 0, callback, 0)
        except ctypes.WinError as e:
            raise VCPError('failed to enumerate VCPs') from e

        for logical in hmonitors:
            vcps.append(WindowsVCP(logical))

        return vcps