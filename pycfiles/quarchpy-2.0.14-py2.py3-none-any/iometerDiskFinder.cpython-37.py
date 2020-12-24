# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\disk_test\iometerDiskFinder.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 6765 bytes
import re, time, sys
wmi = None
from sys import platform
from subprocess import check_output
import quarchpy.disk_test.AbsDiskFinder as AbsDiskFinder
from quarchpy.user_interface import *

class iometerDiskFinder(AbsDiskFinder):

    def __init__(self):
        global wmi
        if platform == 'win32':
            try:
                import wmi as newImport
                wmi = newImport
            except ImportError:
                raise ImportError("'wmi' module required, please install this")

            try:
                import win32file, win32api
            except ImportError:
                raise ImportError("'pywin32' module required, please install this")

    def returnDisk(self):
        deviceList = self.findDevices()
        myDeviceID = self.formatList(deviceList)
        return myDeviceID

    def findDevices(self):
        diskList = self.getAvailableDisks('OS')
        driveList = self.getAvailableDrives()
        deviceList = driveList + diskList
        return deviceList

    def formatList(self, deviceList):
        printText('\n\n ########## STEP 2 = Select a target drive. ##########\n')
        printText(' ------------------------------------------------------------------')
        printText(' |  {:^5}  |  {:^10}  |  {:^35}  |'.format('INDEX', 'VOLUME', 'DESCRIPTION'))
        printText(' ------------------------------------------------------------------')
        templ = ' |  %5s  |  %10s  |  %35s  |'
        for idx, i in enumerate(deviceList):
            printText(templ % (str(idx + 1), i.get('DRIVE'), i.get('NAME')))
            printText(' ------------------------------------------------------------------')

        try:
            drive_index = int(raw_input('\n>>> Enter the index of the target device: ')) - 1
        except NameError:
            drive_index = int(input('\n>>> Enter the index of the target device: ')) - 1

        if drive_index > -1:
            myDeviceID = deviceList[drive_index]
        else:
            myDeviceID = None
        return myDeviceID

    def getAvailableDisks(self, hostDrive):
        driveList = []
        diskNum = 0
        diskScan = wmi.WMI()
        for disk in diskScan.Win32_diskdrive(['Caption', 'DeviceID', 'FirmwareRevision']):
            driveInfo = {'NAME':None, 
             'DRIVE':None, 
             'FW_REV':None}
            DiskInfo = str(disk)
            DiskInfo.strip()
            a = re.search('Caption = "(.+?)";', DiskInfo)
            if a:
                diskName = a.group(1)
            b = re.search('DRIVE(.+?)";', DiskInfo)
            if b:
                if b == '':
                    b = '""'
                diskId = b.group(1)
            diskFw = None
            c = re.search('FirmwareRevision = "(.+?)";', DiskInfo)
            if c:
                diskFw = c.group(1)
            if diskName != hostDrive:
                driveInfo.update(dict(zip(['NAME', 'DRIVE', 'FW_REV'], [diskName, diskId, diskFw])))
                driveList.append(driveInfo)

        return driveList

    def getAvailableDrives(self):
        RList = check_output('wmic logicaldisk get caption, Description')
        if sys.version_info.major == 3:
            RList = str(RList, 'utf-8')
        RList_Lines = RList.split('\n')
        RList_MinusNetwork = []
        for item in RList_Lines:
            if 'Network Connection' not in item and len(item) > 0:
                RList_MinusNetwork.append(item[0:item.find('  ')])

        del RList_MinusNetwork[0]
        RList_MinusNetwork = self.remove_values_from_list(RList_MinusNetwork, '\r')
        RL_DrivesAndVolumeInfo = []
        for i in RList_MinusNetwork:
            i.replace(':', '://')
            try:
                RL_DrivesAndVolumeInfo.append(win32api.GetVolumeInformation(i)[0])
                RL_DrivesAndVolumeInfo.append(i)
                time.sleep(0.1)
            except:
                continue

        driveList = []
        try:
            for i in xrange(0, len(RL_DrivesAndVolumeInfo), 2):
                driveInfo = {'NAME':None, 
                 'DRIVE':None, 
                 'FW_REV':None}
                driveInfo.update(dict(zip(['NAME', 'DRIVE', 'FW_REV'], [RL_DrivesAndVolumeInfo[i], RL_DrivesAndVolumeInfo[(i + 1)], ''])))
                driveList.append(driveInfo)

        except:
            for i in range(0, len(RL_DrivesAndVolumeInfo), 2):
                driveInfo = {'NAME':None, 
                 'DRIVE':None, 
                 'FW_REV':None}
                driveInfo.update(dict(zip(['NAME', 'DRIVE', 'FW_REV'], [RL_DrivesAndVolumeInfo[i], RL_DrivesAndVolumeInfo[(i + 1)], ''])))
                driveList.append(driveInfo)

        return driveList

    def remove_values_from_list(self, the_list, val):
        return [value for value in the_list if value != val]