# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wmdlib\lowlevel\MediaDevMgrFactory.py
# Compiled at: 2007-09-09 20:06:25
import os, comtypes
_lcid = 0
from ctypes import *
from comtypes.client import GetModule
GetModule('stdole2.tlb')
import comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0
from comtypes import GUID
import wmdlib.lowlevel.mswmdm as mswmdm
from ctypes import HRESULT
from ctypes import WinError
from comtypes import helpstring
from comtypes import COMMETHOD
from comtypes import dispid
from comtypes import CoClass
from comtypes.client import CreateObject
from pkg_resources import ResourceManager

class IMediaDevMgrGetter(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    __module__ = __name__
    _case_insensitive_ = True
    _iid_ = GUID('{3DCEA998-6BB7-426A-A3BC-7D707578DA40}')
    _idlflags_ = ['nonextensible', 'dual', 'oleautomation']


IMediaDevMgrGetter._methods_ = [
 COMMETHOD([dispid(1), helpstring('Gibt DeviceManager Instanz zurück')], HRESULT, 'GetWMDeviceManager', (
  [
   'retval', 'out'], POINTER(POINTER(mswmdm.IWMDeviceManager)), 'ppDeviceManager'))]

class MediaDevMgrGetter(CoClass):
    """MediaDevMgrGetter Class"""
    __module__ = __name__
    _reg_clsid_ = GUID('{0311207F-5ED6-43B3-B7B1-5FCD422693C0}')
    _idlflags_ = []
    _reg_typelib_ = ('{BD3337B7-DFDF-4714-90EF-E76D6AD9A8F7}', 1, 0)


MediaDevMgrGetter._com_interfaces_ = [IMediaDevMgrGetter]

def GetWMDeviceManager():
    """Returns an Instance of IWMDeviceManager"""
    try:
        wmdmgrg = CreateObject(MediaDevMgrGetter, clsctx=comtypes.CLSCTX_ALL)
    except WindowsError:
        resman = ResourceManager()
        os.system('regsvr32 /s "%s"' % resman.resource_filename('wmdlib.lowlevel', 'WPD_noDRM_com.dll'))
        wmdmgrg = CreateObject(MediaDevMgrGetter, clsctx=comtypes.CLSCTX_ALL)

    return wmdmgrg.GetWMDeviceManager()


__all__ = [
 'GetWMDeviceManager']