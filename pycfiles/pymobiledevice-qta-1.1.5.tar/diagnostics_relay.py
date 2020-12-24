# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/diagnostics_relay.py
# Compiled at: 2019-03-03 16:57:38
from pymobiledevice.lockdown import LockdownClient
from pprint import pprint
import plistlib
from optparse import OptionParser
Requests = 'Goodbye\nAll\nGasGauge\nWiFi\nShutdown\nRestart\nMobileGestalt\nSleep\nNAND\nIORegistry\nObliterate\n'
MobileGestaltKeys = 'DieId\nSerialNumber\nUniqueChipID\nWifiAddress\nCPUArchitecture\nBluetoothAddress\nEthernetMacAddress\nFirmwareVersion\nMLBSerialNumber\nModelNumber\nRegionInfo\nRegionCode\nDeviceClass\nProductType\nDeviceName\nUserAssignedDeviceName\nHWModelStr\nSigningFuse\nSoftwareBehavior\nSupportedKeyboards\nBuildVersion\nProductVersion\nReleaseType\nInternalBuild\nCarrierInstallCapability\nIsUIBuild\nInternationalMobileEquipmentIdentity\nMobileEquipmentIdentifier\nDeviceColor\nHasBaseband\nSupportedDeviceFamilies\nSoftwareBundleVersion\nSDIOManufacturerTuple\nSDIOProductInfo\nUniqueDeviceID\nInverseDeviceID\nChipID\nPartitionType\nProximitySensorCalibration\nCompassCalibration\nWirelessBoardSnum\nBasebandBoardSnum\nHardwarePlatform\nRequiredBatteryLevelForSoftwareUpdate\nIsThereEnoughBatteryLevelForSoftwareUpdate\nBasebandRegionSKU\nencrypted-data-partition\nSysCfg\nDiagData\nSIMTrayStatus\nCarrierBundleInfoArray\nAllDeviceCapabilities\nwi-fi\nSBAllowSensitiveUI\ngreen-tea\nnot-green-tea\nAllowYouTube\nAllowYouTubePlugin\nSBCanForceDebuggingInfo\nAppleInternalInstallCapability\nHasAllFeaturesCapability\nScreenDimensions\nIsSimulator\nBasebandSerialNumber\nBasebandChipId\nBasebandCertId\nBasebandSkeyId\nBasebandFirmwareVersion\ncellular-data\ncontains-cellular-radio\nRegionalBehaviorGoogleMail\nRegionalBehaviorVolumeLimit\nRegionalBehaviorShutterClick\nRegionalBehaviorNTSC\nRegionalBehaviorNoWiFi\nRegionalBehaviorChinaBrick\nRegionalBehaviorNoVOIP\nRegionalBehaviorAll\nApNonce'

class DIAGClient(object):

    def __init__(self, lockdown=None, serviceName='com.apple.mobile.diagnostics_relay'):
        if lockdown:
            self.lockdown = lockdown
        else:
            self.lockdown = LockdownClient()
        self.service = self.lockdown.startService(serviceName)
        self.packet_num = 0

    def stop_session(self):
        print 'Disconecting...'
        self.service.close()

    def query_mobilegestalt(self, MobileGestalt=MobileGestaltKeys.split('\n')):
        self.service.sendPlist({'Request': 'MobileGestalt', 'MobileGestaltKeys': MobileGestalt})
        res = self.service.recvPlist()
        d = res.get('Diagnostics')
        if d:
            return d.get('MobileGestalt')
        else:
            return

    def action(self, action='Shutdown', flags=None):
        self.service.sendPlist({'Request': action})
        res = self.service.recvPlist()
        return res.get('Diagnostics')

    def restart(self):
        return self.action('Restart')

    def shutdown(self):
        return self.action('Shutdown')

    def diagnostics(self, diagType='All'):
        self.service.sendPlist({'Request': diagType})
        res = self.service.recvPlist()
        if res:
            return res.get('Diagnostics')
        else:
            return

    def ioregistry_entry(self, name=None, ioclass=None):
        d = {}
        if name:
            d['EntryName'] = name
        if ioclass:
            d['EntryClass'] = ioclass
        d['Request'] = 'IORegistry'
        self.service.sendPlist(d)
        res = self.service.recvPlist()
        pprint(res)
        if res:
            return res.get('Diagnostics')
        else:
            return

    def ioregistry_plane(self, plane=''):
        d = {}
        if plane:
            d['CurrentPlane'] = plane
        else:
            d['CurrentPlane'] = ''
        d['Request'] = 'IORegistry'
        self.service.sendPlist(d)
        res = self.service.recvPlist()
        dd = res.get('Diagnostics')
        if dd:
            return dd.get('IORegistry')
        else:
            return


if __name__ == '__main__':
    parser = OptionParser(usage='%prog')
    parser.add_option('-c', '--cmd', dest='cmd', default=False, help='Launch diagnostic command', type='string')
    parser.add_option('-m', '--mobilegestalt', dest='mobilegestalt_key', default=False, help='Request mobilegestalt key', type='string')
    parser.add_option('-i', '--ioclass', dest='ioclass', default=False, help='Request ioclass', type='string')
    parser.add_option('-n', '--ioname', dest='ioname', default=False, help='Request ionqme', type='string')
    options, args = parser.parse_args()
    diag = DIAGClient()
    if not options.cmd:
        res = diag.diagnostics()
    elif options.cmd == 'IORegistry':
        res = diag.ioregistry_plane()
    elif options.cmd == 'MobileGestalt':
        if not options.mobilegestalt_key or options.mobilegestalt_key not in MobileGestaltKeys.split('\n'):
            res = diag.query_mobilegestalt()
        else:
            res = diag.query_mobilegestalt([options.mobilegestalt_key])
    else:
        res = diag.action(options.cmd)
    if res:
        for k in res.keys():
            print ' %s \t: %s' % (k, res[k])