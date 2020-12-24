# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\disk_test\hostInformation.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 16332 bytes
"""
Implements a cross platform system for scanning and querying system resources.

########### VERSION HISTORY ###########

06/05/2019 - Andy Norrie    - First version

####################################
"""
import subprocess, platform, time, os, re, sys, ctypes, logging
from quarchpy.user_interface import *
from quarchpy.disk_test import driveTestConfig
import quarchpy.disk_test.dtsGlobals as dtsGlobals
from quarchpy.disk_test.dtsComms import DTSCommms
if hasattr(__builtins__, 'raw_input'):
    input = raw_input
elif platform.system() == 'Windows':
    import quarchpy.disk_test.lspci as lspci
    import quarchpy.disk_test.sasFuncs as sasDET
else:
    import quarchpy.disk_test.lspci as lspci
    import quarchpy.disk_test.sasFuncs as sasDET

class HostInformation:
    _HostInformation__mylspci = lspci()
    _HostInformation__mySAS = sasDET()
    internalResults = {}

    def _init_(self):
        pass

    def list_physical_drives(self, drive_type, search_params=None):
        filter_drives = True
        if search_params is not None:
            if 'filter_drives' in search_params:
                filter_drives = search_params['filter_drives']
        user_devices = {}
        if drive_type.lower() == 'pcie':
            pcie_scan_data = self._HostInformation__mylspci.getPcieDeviceList()
            for pcie_name, pcie_device in pcie_scan_data.items():
                if '[01' in pcie_device['class']:
                    user_devices['pcie:' + pcie_device['slot']] = pcie_device

            return user_devices
        if drive_type.lower() == 'sas':
            sas_scan_data = self._HostInformation__mySAS.getSasDeviceList()
            for sas_name, sas_device in sas_scan_data.items():
                if 'description' in sas_device:
                    if 'Disk drive' in sas_device['description']:
                        user_devices['SAS:' + sas_device['name']] = sas_device
                    elif 'type' in sas_device:
                        if 'disk' in sas_device['type'].lower():
                            user_devices['SAS:/dev/' + sas_device['name']] = sas_device
                    elif 'Disk_Type' in sas_device and 'disk' in sas_device['Disk_Type'].lower():
                        user_devices['SAS:' + sas_device['name']] = sas_device

            return user_devices

    def get_device_status(self, device_id):
        if device_id.find('pcie') == 0:
            return self._HostInformation__mylspci.getPcieDeviceDetailedInfo(devicesToScan=device_id)
        return self._HostInformation__mySAS.getSasDeviceDetailedInfo(devicesToScan=device_id)

    def verifyDriveStats(self, uniqueID, driveId, mappingMode):
        if 'pcie' in str(driveId).lower():
            expectedSpeed = self.internalResults[(driveId + '_linkSpeed')]
            expectedWidth = self.internalResults[(driveId + '_linkWidth')]
            linkSpeed, linkWidth = self._HostInformation__mylspci.getPcieLinkStatus(driveId, mappingMode)
            if linkSpeed == expectedSpeed:
                if linkWidth == expectedWidth:
                    driveTestConfig.testCallbacks['TEST_LOG'](uniqueID, time.time(), 'testResult', 'Drive link speed/width was maintained ' + driveId, os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'testResult': True})
                    return True
            changeDetails = 'Was: ' + expectedSpeed + '/' + expectedWidth + ' Now: ' + linkSpeed + '/' + linkWidth
            driveTestConfig.testCallbacks['TEST_LOG'](uniqueID, time.time(), 'testResult', 'Drive link speed/width was NOT maintained for: ' + driveId, os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'testResult':False, 
             'textDetails':changeDetails})
            return False
        else:
            driveTestConfig.testCallbacks['TEST_LOG'](uniqueID, time.time(), 'testResult', "Drive still ID'd - No record of speeds for : " + driveId, os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'testResult':True, 
             'textDetails':'No change'})
            return True

    def isDevicePresent(self, deviceStr, mappingMode, driveType):
        cwd = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        if 'pcie' in str(driveType).lower():
            deviceList = self._HostInformation__mylspci.getPcieDevices(mappingMode)
            if str(deviceStr).startswith('pcie'):
                deviceStr = deviceStr[5:]
        elif 'sas' in str(driveType).lower():
            deviceList = self._HostInformation__mySAS.getSasDeviceList()
            if not str(deviceStr).startswith('sas'):
                deviceStr = 'SAS:' + deviceStr
            if '\\' in deviceStr:
                if '.' in deviceStr:
                    deviceStr = deviceStr.replace('\\', '').replace('.', '').replace('SAS:', '')
        os.chdir(cwd)
        for devStr in deviceList:
            if platform.system() == 'Windows':
                if str(deviceStr).strip() in str(devStr).strip():
                    return True
                elif 'sas' in deviceStr.lower():
                    if str(devStr).strip() in str(deviceStr).strip():
                        return True
                elif str(deviceStr).strip() in str(devStr).strip():
                    return True

        return False

    def storeInitialDriveStats(self, driveId, linkSpeed, linkWidth):
        self.internalResults[driveId + '_linkSpeed'] = linkSpeed
        self.internalResults[driveId + '_linkWidth'] = linkWidth

    def getDriveList(self, mappingMode):
        cwd = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        deviceList = self._HostInformation__mylspci.getPcieDevices(mappingMode)
        deviceList += self._HostInformation__mySAS.getSasDeviceList()
        os.chdir(cwd)
        return deviceList

    def devicePresentInList(self, deviceList, deviceStr):
        for pciStr in deviceList:
            if deviceStr in pciStr:
                return True

        return False

    def get_sas_drive_det_cmd(self):
        return sasDET.return_device_det_cmd()

    def pickPcieTarget(self, resourceName, drive_type):
        comms = DTSCommms()
        dtsGlobals.choiceResponse = None
        mappingMode = driveTestConfig.testCallbacks['TEST_GETRESOURCE']('pcieMappingMode')
        if mappingMode == None:
            mappingMode = False
        else:
            deviceStr = 'NO_DEVICE_STRING'
            comms.sendMsgToGUI('QuarchDTS::header<DRIVE>::Choose a Drive to test', None)
            if 'all' in drive_type:
                deviceDictSas = self.list_physical_drives('sas')
                deviceDictPcie = self.list_physical_drives('pcie')
                if not deviceDictSas:
                    if not deviceDictPcie:
                        printText('ERROR - No devices found to display')
                self.sendChoiceObjects(comms, deviceDictSas, 'sas')
                self.sendChoiceObjects(comms, deviceDictPcie, 'pcie')
            else:
                deviceDict = self.list_physical_drives(drive_type)
                if not deviceDict:
                    printText('ERROR - No devices found to display')
                self.sendChoiceObjects(comms, deviceDict, drive_type)
            comms.sendMsgToGUI('QuarchDTS::end-of-data', None)
            while dtsGlobals.choiceResponse is None and dtsGlobals.continueTest is True:
                time.sleep(0.25)

            if dtsGlobals.choiceResponse is None:
                return 0
            choice = bytes.decode(dtsGlobals.choiceResponse)
            if 'all' in drive_type:
                if 'sas' in choice.lower():
                    deviceDict = deviceDictSas
                if 'pcie' in choice.lower():
                    deviceDict = deviceDictPcie
            selection = choice.split('::')
            selection = selection[1]
            if 'rescan' not in selection:
                printText(('Response from drive selection was : ' + selection.replace('\n', '').replace('\r', '')), fillLine=True, terminalWidth=80)
            logging.debug('Response from drive selection was : ' + choice)
            if 'choice-abort' in selection or dtsGlobals.continueTest is False:
                printText('No item selected, test aborted. Waiting for new test start..\n')
                return 0
            if 'rescan' in selection:
                return self.pickPcieTarget(resourceName, drive_type)
            found = False
            for key, value in deviceDict.items():
                if selection.strip() == key:
                    deviceStr = key
                    found = True
                    break

            return found or 0
        if selection.lower().find('pcie') == 0:
            linkSpeed, linkWidth = self._HostInformation__mylspci.getPcieLinkStatus(deviceStr, mappingMode)
            self.storeInitialDriveStats(deviceStr, linkSpeed, linkWidth)
            driveTestConfig.testCallbacks['TEST_LOG'](None, time.time(), 'debug', 'Device Selected: PCIE:' + deviceStr + ' - Speed:' + linkSpeed + ', Width:' + linkWidth, os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name)
            driveTestConfig.testCallbacks['TEST_SETRESOURCE'](resourceName, 'PCIE:' + deviceStr)
        if selection.find('SAS') == 0:
            driveTestConfig.testCallbacks['TEST_LOG'](None, time.time(), 'debug', 'Device Selected: ' + deviceStr, os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name)
            driveTestConfig.testCallbacks['TEST_SETRESOURCE'](resourceName, deviceStr)

    def checkAdmin(self):
        if self._HostInformation__mylspci.is_admin_mode() == False:
            logging.critical('Not in Admin mode\nExiting Program')
            quit()

    def sendChoiceObjects(self, comms, deviceDict, drive_type):
        for key, value in deviceDict.items():
            try:
                comms.newNotifyChoiceOption('drive', key, value, drive_type)
            except Exception as e:
                try:
                    printText(e)
                finally:
                    e = None
                    del e

    def getPcieLinkStatus(self, deviceStr, mappingMode):
        return self._HostInformation__mylspci.getPcieLinkStatus(deviceStr, mappingMode)