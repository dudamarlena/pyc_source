# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vm_automation/workstationVm.py
# Compiled at: 2018-04-06 12:02:43
import subprocess, os, time
vmrunExe = 'C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrun.exe'
vmPath = 'D:\\VMs'

class workstationServer:

    def __init__(self, vmRunExe, vmPath, logFile='default.log'):
        self.vmrunExe = vmRunExe
        self.vmPath = vmPath
        self.vmList = []
        return

    def __init__(self, configDictionary, logFile='default.log'):
        try:
            self.vmrunExe = configDictionary['VMRUN_PATH']
            self.vmPath = configDictionary['VM_PATH']
        except:
            return

        self.vmList = []
        return

    def enumerateVms(self, negFilter=None):
        for root, dirs, files in os.walk(vmPath):
            for file in files:
                if file.endswith('.vmx'):
                    if negFilter != None and negFilter.upper() in root.upper():
                        continue
                    else:
                        self.vmList.append(workstationVm(os.path.join(root, file)))

        return True

    def waitForVmsToBoot(self, vmList):
        readyVms = []
        ipAddressesSet = False
        while not ipAddressesSet:
            ipAddressesSet = True
            for i in vmList:
                if i not in readyVms:
                    if i.queryVmIp():
                        readyVms.append(i)
                    else:
                        ipAddressesSet = False
                time.sleep(1)

        return True


class workstationVm:

    def __init__(self, vmIdentifier):
        self.procList = []
        self.revertSnapshots = []
        self.snapshotList = []
        self.testVm = False
        self.vmIdentifier = vmIdentifier
        self.vmIp = ''
        self.vmName = vmIdentifier.split('\\')[(-1)][:-4]
        self.vmOS = self.vmName
        self.vmPassword = ''
        self.vmUsername = ''
        self.payloadList = []
        if 'x64' in self.vmName:
            self.arch = 'x64'
        elif 'x86' in self.vmName:
            self.arch = 'x86'
        else:
            self.arch = None
        return

    def runVmCommand(self, listCmd):
        vmRunCmd = [
         vmrunExe] + listCmd
        vmrunProc = subprocess.Popen(vmRunCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return vmrunProc.communicate()

    def runAuthenticatedVmCommand(self, listCmd):
        vmRunCmd = [
         vmrunExe] + ['-gu', self.vmUsername, '-gp', self.vmPassword] + listCmd
        vmrunProc = subprocess.Popen(vmRunCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return vmrunProc.communicate()

    def deleteSnapshot(self, snapshotName):
        return self.runVmCommand(['deleteSnapshot', self.vmIdentifier, snapshotName])

    def getArch(self):
        return self.arch

    def getFileFromGuest(self, srcPathName, dstPathName):
        return self.runAuthenticatedVmCommand(['CopyFileFromGuestToHost', self.vmIdentifier, srcPathName, dstPathName])

    def getSnapshots(self):
        self.snapshotList = self.runVmCommand(['listSnapshots', self.vmIdentifier])[0].split('\n')
        self.snapshotList = map(lambda s: s.strip(), self.snapshotList)
        return len(self.snapshotList)

    def getVmIp(self):
        return self.vmIp

    def getUsername(self):
        return self.vmUsername

    def isTestVm(self):
        return self.testVm

    def makeDirOnGuest(self, dirPath):
        return self.runAuthenticatedVmCommand(['createDirectoryInGuest', self.vmIdentifier, dirPath])

    def powerOn(self):
        self.runVmCommand(['start', self.vmIdentifier])

    def prepVm(self):
        self.getSnapshots()
        self.powerOn()

    def queryVmIp(self):
        tempIp = self.runVmCommand(['getGuestIPAddress', self.vmIdentifier])[0].strip()
        if 'error' in tempIp.lower():
            retVal = False
        else:
            self.vmIp = tempIp
            retVal = True
        return retVal

    def revertToSnapshot(self, snapshot):
        return self.runVmCommand(['revertToSnapshot', self.vmIdentifier, snapshot])[0]

    def revertDevVm(self):
        self.getSnapshots()
        for i in self.snapshotList:
            if 'TESTING-' in i:
                self.revertToSnapshot(i)
                self.deleteSnapshot(i)

    def revertToTestingBase(self):
        self.getSnapshots()
        for i in self.snapshotList:
            if 'testing_base' in i.lower():
                return self.revertToSnapshot(i)

        return 'NO SUCH SNAPSHOT'

    def runCmdOnGuest(self, argList):
        cmdRet = self.runAuthenticatedVmCommand(['runProgramInGuest', self.vmIdentifier] + argList)
        retVal = False
        if ('', '') == cmdRet:
            retVal = True
        return retVal

    def setPassword(self, vmPassword):
        self.vmPassword = vmPassword

    def setTestVm(self):
        self.testVm = True

    def setUsername(self, vmUsername):
        self.vmUsername = vmUsername

    def takeTempSnapshot(self):
        snapshotName = 'PAYLOAD_TESTING-' + str(time.time()).split('.')[0]
        self.runVmCommand(['snapshot', self.vmIdentifier, snapshotName])
        self.revertSnapshots.append(snapshotName)
        return snapshotName

    def updateProcList(self):
        self.procList = self.runAuthenticatedVmCommand(['listProcessesInGuest', self.vmIdentifier])[0].split('\n')
        return len(self.procList)

    def uploadFileToGuest(self, srcPathName, dstPathName):
        return self.runAuthenticatedVmCommand(['CopyFileFromHostToGuest', self.vmIdentifier, srcPathName, dstPathName])