# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\disk_test\lspci.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 14300 bytes
"""
Implements basic control over lspci utilities, so that we can identify and check the
status of PCIe devices on the host system
"""
import subprocess, platform, time, os, re, sys, ctypes, abc
ABC = abc.ABCMeta('ABC', (object,), {})
from quarchpy.disk_test import driveTestConfig
from quarchpy.user_interface import *

class abstractLSPCI(ABC):

    @abc.abstractmethod
    def getPcieDeviceList(self):
        pass

    @abc.abstractmethod
    def getPcieDeviceDetailedInfo(self, deviceInfo, devicesToScan):
        pass

    def sortList(self, err, out):
        pcieDevices = {}
        if err:
            raise ValueError('lspci error: ' + err.decode('utf-8'))
        out = out.decode('utf-8')
        blocks = out.split('\r\n\r\n')
        for desc in blocks:
            newDevice = {}
            for line in iter(desc.splitlines()):
                pos = line.find(':')
                if pos != -1:
                    if 'Summary of buses' in line:
                        break
                    newDevice[line[:pos].lower()] = line[pos + 1:].strip()

            if 'slot' in newDevice:
                pcieDevices[newDevice['slot']] = newDevice

        return pcieDevices

    @abc.abstractmethod
    def is_admin_mode(self):
        pass


class WindowsLSPCI(abstractLSPCI):

    def __init__(self):
        pass

    def is_admin_mode(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def getPcieDeviceList(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        lspciPath = os.path.join(dir_path, 'pciutils', 'lspci.exe')
        proc = subprocess.Popen([lspciPath, '-Mmmvvnn'], stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        out, err = proc.communicate()
        retValues = self.sortList(err, out)
        return retValues

    def getPcieDevices(self, mappingMode, filterDrives=False):
        pcieDevices = []
        dir_path = os.path.dirname(os.path.realpath(__file__))
        lspciPath = os.path.join(dir_path, 'pciutils', 'lspci.exe')
        if mappingMode == True:
            proc = subprocess.Popen([lspciPath, '-M'], stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        else:
            proc = subprocess.Popen([lspciPath], stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        out, err = proc.communicate()
        if err:
            printText('ERROR: ' + err.decode('utf-8'))
        out = out.decode('utf-8')
        for pciStr in iter(out.splitlines()):
            matchObj = re.match('[0-9a-fA-F]+:[0-9a-fA-F]+.[0-9a-fA-F]', pciStr)
            try:
                matchStr = matchObj.group(0)
            except:
                matchStr = ''

            if len(matchStr) > 0 and pciStr.find('##') == -1:
                if filterDrives == False:
                    pcieDevices.append(pciStr)
                else:
                    pcieDevices.append(pciStr)

        return pcieDevices

    def getPcieDeviceDetailedInfo(self, deviceInfo=None, devicesToScan='all'):
        if deviceInfo == None and devicesToScan == 'all':
            deviceInfo = self.getPcieDeviceInfo()
        else:
            if deviceInfo == None:
                deviceInfo = {}
                devicesToScan = devicesToScan[5:]
        dir_path = os.path.dirname(os.path.realpath(__file__))
        lspciPath = os.path.join(dir_path, 'pciutils', 'lspci.exe')
        proc = subprocess.Popen([lspciPath, '-vvvs', devicesToScan], stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        out, err = proc.communicate()
        retValue = self.sortDeviceInfo(err, out, deviceInfo, devicesToScan)
        return retValue

    def getPcieLinkStatus(self, deviceStr, mappingMode):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        lspciPath = os.path.join(dir_path, 'pciutils', 'lspci.exe')
        if str(deviceStr).lower().startswith('pcie:'):
            deviceStr = deviceStr[5:]
        elif mappingMode == False:
            proc = subprocess.Popen([lspciPath, '-vv', '-s ' + deviceStr], stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        else:
            proc = subprocess.Popen([lspciPath, '-M', '-vv', '-s ' + deviceStr], stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        out, err = proc.communicate()
        if err:
            printText('ERROR: ' + err.decode('utf-8'))
        out = out.decode('utf-8')
        strPos = out.find('LnkSta:')
        out = out[strPos:]
        try:
            matchObj = re.search('Speed (.*?),', out)
            linkSpeed = matchObj.group(0)
            matchObj = re.search('Width (.*?),', out)
            linkWidth = matchObj.group(0)
        except:
            linkSpeed = 'UNKNOWN'
            linkWidth = 'UNKNOWN'
            driveTestConfig.testCallbacks['TEST_LOG'](None, time.time(), 'error', 'Device does not report link speed/width', os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'textDetails': 'deviceName ' + deviceStr + ' is not suitable for link test'})

        return (linkSpeed, linkWidth)

    def getPcieDeviceInfo(self):
        pass


class LinuxLSPCI(abstractLSPCI):

    def __init__(self):
        pass

    def is_admin_mode(self):
        if os.getuid() == 0:
            return True
        return False

    def getPcieDeviceList(self):
        proc = subprocess.Popen(['lspci', '-mmvvvnn'], stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        out, err = proc.communicate()
        return self.sortList(err, bytes(out))

    def getPcieDevices(self, mappingMode, filterDrives=False):
        pcieDevices = []
        lspciPath = os.path.join(os.getcwd(), 'pciutils', 'lspci.exe')
        if mappingMode == True:
            proc = subprocess.Popen(['lspci', '-M'], stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        else:
            proc = subprocess.Popen(['lspci'], stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        out, err = proc.communicate()
        if err:
            printText('ERROR: ' + err.decode('utf-8'))
        out = out.decode('utf-8')
        for pciStr in iter(out.splitlines()):
            matchObj = re.match('[0-9a-fA-F]+:[0-9a-fA-F]+.[0-9a-fA-F]', pciStr)
            try:
                matchStr = matchObj.group(0)
            except:
                matchStr = ''

            if len(matchStr) > 0 and pciStr.find('##') == -1:
                if filterDrives == False:
                    pcieDevices.append(pciStr)
                else:
                    pcieDevices.append(pciStr)

        return pcieDevices

    def getPcieDeviceDetailedInfo(self, deviceInfo=None, devicesToScan='all'):
        if deviceInfo == None and devicesToScan == 'all':
            deviceInfo = self.getPcieDeviceInfo()
        else:
            if deviceInfo == None:
                deviceInfo = {}
                devicesToScan = devicesToScan[5:]
        proc = subprocess.Popen(['lspci', '-vvvs', devicesToScan], stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        out, err = proc.communicate()
        retValue = self.sortDeviceInfo(err, out, deviceInfo, devicesToScan)
        return retValue

    def getPcieLinkStatus(self, deviceStr, mappingMode):
        lspciPath = os.path.join(os.getcwd(), 'pciutils', 'lspci.exe')
        if str(deviceStr).startswith('pcie:'):
            deviceStr = deviceStr[5:]
        elif mappingMode == False:
            proc = subprocess.Popen(['lspci', '-vv', '-s', deviceStr], stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        else:
            proc = subprocess.Popen(['lspci', '-M', '-vv', '-s', deviceStr], stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        out, err = proc.communicate()
        if err:
            printText('ERROR: ' + err.decode('utf-8'))
        out = out.decode('utf-8')
        strPos = out.find('LnkSta:')
        out = out[strPos:]
        try:
            matchObj = re.search('Speed (.*?),', out)
            linkSpeed = matchObj.group(0)
            matchObj = re.search('Width (.*?),', out)
            linkWidth = matchObj.group(0)
        except:
            linkSpeed = 'UNKNOWN'
            linkWidth = 'UNKNOWN'
            driveTestConfig.testCallbacks['TEST_LOG'](None, time.time(), 'error', 'Device does not report link speed/width', os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'textDetails': 'deviceName ' + deviceStr + ' is not suitable for link test'})

        return (linkSpeed, linkWidth)

    def getPcieDeviceInfo(self):
        pass

    def sortList(self, err, out):
        pcieDevices = {}
        if err:
            raise ValueError('lspci error: ' + err.decode('utf-8'))
        out = out.decode('utf-8')
        blocks = out.split('\n\n')
        for desc in blocks:
            newDevice = {}
            for line in iter(desc.splitlines()):
                pos = line.find(':')
                if pos != -1:
                    if 'Summary of buses' in line:
                        break
                    newDevice[line[:pos].lower()] = line[pos + 1:].strip()

            if 'slot' in newDevice:
                pcieDevices[newDevice['slot']] = newDevice

        return pcieDevices