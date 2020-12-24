# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\disk_test\sasFuncs.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 8232 bytes
"""
Implements basic SAS information parsing, so that we can identify and check the
status of SAS/SATA devices on the host
"""
import subprocess, platform, time, os, re, sys, ctypes, abc
ABC = abc.ABCMeta('ABC', (object,), {})
from quarchpy.user_interface import *

class abstractSASDet(ABC):

    @abc.abstractmethod
    def getSasDeviceList(self):
        pass

    @abc.abstractmethod
    def sortList(self, err, out):
        pass

    @abc.abstractmethod
    def is_admin_mode(self):
        pass

    def sortDeviceInfo(self, err, out, deviceInfo, devicesToScan):
        if err:
            raise ValueError('lspci error: ' + err.decode('utf-8'))
        out = out.decode('utf-8')
        blocks = out.split('\r\n\r\n')
        for desc in blocks:
            lnkStatSpeed = None
            lnkStatWidth = None
            lnkCapsSpeed = None
            lnkCapsWidth = None
            pos = desc.find(' ')
            currDevice = desc[:pos]
            try:
                strPos = desc.find('LnkSta:')
                statusText = desc[strPos:]
                matchObj = re.search('Speed (.*?),', statusText)
                lnkStatSpeed = matchObj.group(0)
            except:
                pass

            try:
                matchObj = re.search('Width (.*?),', statusText)
                lnkStatWidth = matchObj.group(0)
            except:
                pass

            try:
                strPos = desc.find('LnkCap:')
                statusText = desc[strPos:]
                matchObj = re.search('Speed (.*?),', statusText)
                lnkCapsSpeed = matchObj.group(0)
            except:
                pass

            try:
                matchObj = re.search('Width (.*?),', statusText)
                lnkCapsWidth = matchObj.group(0)
            except:
                pass

            if not devicesToScan == 'all':
                if currDevice in devicesToScan:
                    if currDevice not in deviceInfo:
                        deviceInfo[currDevice] = {}
                deviceInfo[currDevice]['link_status:speed'] = lnkStatSpeed
                deviceInfo[currDevice]['link_status:width'] = lnkStatWidth
                deviceInfo[currDevice]['link_capability:speed'] = lnkCapsSpeed
                deviceInfo[currDevice]['link_capability:width'] = lnkCapsWidth
                deviceInfo[currDevice]['present'] = 'true'

        if devicesToScan != 'all':
            blocks = devicesToScan.split('|')
            for currDevice in blocks:
                if currDevice not in deviceInfo:
                    deviceInfo[currDevice]['present'] = 'false'

        return deviceInfo


class WindowsSAS(abstractSASDet):

    def __init__(self):
        self.device_detection_command = 'wmic diskdrive list full'

    def return_device_det_cmd(self):
        return self.device_detection_command

    def is_admin_mode(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def getSasDeviceList(self):
        proc = subprocess.Popen(['wmic', 'diskdrive', 'list', 'full'], stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        out, err = proc.communicate()
        retValues = self.sortList(err, out)
        return retValues

    def sortList(self, err, out):
        SasDevices = {}
        unsorted = bytes(out).decode()
        deviceList = unsorted.split('\r\n\r\r')
        for dev in deviceList:
            if str(dev).strip() == '':
                continue
            newDevice = {}
            for line in iter(dev.splitlines()):
                pos = line.find('=')
                if pos != -1:
                    newDevice[line[:pos].lower()] = line[pos + 1:].strip()

            if 'name' in newDevice:
                SasDevices[newDevice['name']] = newDevice

        return SasDevices


class LinuxSAS(abstractSASDet):

    def __init__(self):
        self.device_detection_command = 'lsscsi -t -s -L'

    def return_device_det_cmd(self):
        return self.device_detection_command

    def is_admin_mode(self):
        if os.getuid() == 0:
            return True
        return False

    def getSasDeviceList(self):
        proc = subprocess.Popen(['lsscsi', '-t', '-s', '-L'], stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        out, err = proc.communicate()
        return self.sortList(err, bytes(out))

    def sortList(self, err, out):
        SasDevices = {}
        unsorted = bytes(out).decode()
        deviceList = re.split('\\[', unsorted)
        for dev in deviceList:
            if str(dev).strip() == '':
                continue
            dev = '[' + dev
            newDevice = {}
            for line in iter(dev.splitlines()):
                pos = line.find('=')
                if pos != -1:
                    newDevice[line[:pos].lower().strip()] = line[pos + 1:].strip()
                else:
                    details = re.split('\\s{2,}', dev.strip())
                    iterator = 0
                    for detailString in details:
                        newDevice[self.getDictKey(iterator)] = detailString.strip()
                        iterator = iterator + 1

            if 'sas' in newDevice['Conn_Type'].lower():
                SasDevices[newDevice['name']] = newDevice

        return SasDevices

    def getDictKey(self, iteratorValue):
        return {0:'Spec', 
         1:'Disk_Type', 
         2:'Conn_Type', 
         3:'name', 
         4:'size'}.get(iteratorValue, 'unknownDetail')