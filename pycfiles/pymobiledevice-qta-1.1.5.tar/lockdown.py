# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/lockdown.py
# Compiled at: 2019-03-03 20:04:01
import os, plistlib, sys, uuid, platform, time, logging
from pymobiledevice.plist_service import PlistService
from pymobiledevice.ca import ca_do_everything
from pymobiledevice.util import readHomeFile, writeHomeFile, getHomePath
from pymobiledevice.usbmux import usbmux
from six import PY3
if PY3:
    plistlib.readPlistFromString = plistlib.loads
    plistlib.writePlistToString = plistlib.dumps
    plistlib.readPlist = plistlib.load

class NotTrustedError(Exception):
    pass


class PairingError(Exception):
    pass


class NotPairedError(Exception):
    pass


class CannotStopSessionError(Exception):
    pass


class StartServiceError(Exception):

    def __init__(self, message):
        print '[ERROR] %s' % message


class FatalPairingError(Exception):
    pass


HOMEFOLDER = '.pymobiledevice'
MAXTRIES = 20

def list_devices():
    mux = usbmux.USBMux()
    mux.process(1)
    return [ d.serial for d in mux.devices ]


class LockdownClient(object):

    def __init__(self, udid=None, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.paired = False
        self.SessionID = None
        self.c = PlistService(62078, udid)
        self.hostID = self.generate_hostID()
        self.SystemBUID = self.generate_hostID()
        self.paired = False
        self.label = 'pyMobileDevice'
        if not self.queryType() == 'com.apple.mobile.lockdown':
            raise AssertionError
            self.allValues = self.getValue()
            self.udid = self.allValues.get('UniqueDeviceID')
            self.UniqueChipID = self.allValues.get('UniqueChipID')
            self.DevicePublicKey = self.allValues.get('DevicePublicKey')
            self.ios_version = self.allValues.get('ProductVersion')
            self.identifier = self.udid
            if not self.identifier:
                if self.UniqueChipID:
                    self.identifier = '%x' % self.UniqueChipID
                else:
                    raise Exception('Could not get UDID or ECID, failing')
            self.validate_pairing() or self.pair()
            self.c = PlistService(62078, udid)
            if not self.validate_pairing():
                raise FatalPairingError
        self.paired = True
        return

    def queryType(self):
        self.c.sendPlist({'Request': 'QueryType'})
        res = self.c.recvPlist()
        return res.get('Type')

    def generate_hostID(self):
        hostname = platform.node()
        hostid = uuid.uuid3(uuid.NAMESPACE_DNS, hostname)
        return str(hostid).upper()

    def enter_recovery(self):
        self.c.sendPlist({'Request': 'EnterRecovery'})
        res = self.c.recvPlist()
        logger.debug(res)

    def stop_session(self):
        if self.SessionID and self.c:
            self.c.sendPlist({'Label': self.label, 'Request': 'StopSession', 'SessionID': self.SessionID})
            self.SessionID = None
            res = self.c.recvPlist()
            if not res or res.get('Result') != 'Success':
                raise CannotStopSessionError
            return res
        return

    def read_pair_record_from_file(self, path):
        pair_record = None
        try:
            with open(path, 'rb') as (fd):
                pair_record = plistlib.readPlist(fd)
        except IOError as e:
            self.logger.error(('I/O error({0}): {1}').format(e.errno, e.strerror))
            self.logger.error('Unable to read: %s', path)
        except:
            self.logger.error('Unable to read: %s', path)

        return pair_record

    def get_itunes_record_path(self):
        folder = None
        if sys.platform == 'win32':
            folder = os.environ['ALLUSERSPROFILE'] + '/Apple/Lockdown/'
        elif sys.platform == 'darwin':
            folder = '/var/db/lockdown/'
        elif len(sys.platform) >= 5:
            if sys.platform[0:5] == 'linux':
                folder = '/var/lib/lockdown/'
        return folder

    def get_pair_record(self):
        pair_record = None
        itune_records_folder_path = self.get_itunes_record_path()
        if itune_records_folder_path:
            path = itune_records_folder_path + '%s.plist' % self.identifier
            pair_record = self.read_pair_record_from_file(path)
            if pair_record:
                self.logger.info('Using iTunes pair record: %s.plist', self.identifier)
            else:
                self.logger.warning('No iTunes pairing record found for device %s', self.identifier)
        if pair_record == None:
            self.logger.warning('Looking for pymobiledevice pairing record...')
            path = getHomePath(HOMEFOLDER, '%s.plist' % self.identifier)
            pair_record = self.read_pair_record_from_file(path)
            if pair_record:
                self.logger.info('Found pymobiledevice pairing record for device %s', self.udid)
            else:
                self.logger.warning('No  pymobiledevice pairing record found for device %s', self.identifier)
        return pair_record

    def validate_pairing(self):
        pair_record = None
        certPem = None
        privateKeyPem = None
        pair_record = self.get_pair_record()
        if PY3:
            certPem = pair_record['HostCertificate']
            privateKeyPem = pair_record['HostPrivateKey']
        else:
            certPem = pair_record['HostCertificate'].data
            privateKeyPem = pair_record['HostPrivateKey'].data
        if int(self.ios_version.split('.')[0]) < 11:
            ValidatePair = {'Label': self.label, 'Request': 'ValidatePair', 'PairRecord': pair_record}
            self.c.sendPlist(ValidatePair)
            r = self.c.recvPlist()
            if not r or r.has_key('Error'):
                pair_record = None
                self.logger.error('ValidatePair fail: %s', ValidatePair)
                return False
        self.hostID = pair_record.get('HostID', self.hostID)
        self.SystemBUID = pair_record.get('SystemBUID', self.SystemBUID)
        d = {'Label': self.label, 'Request': 'StartSession', 'HostID': self.hostID, 'SystemBUID': self.SystemBUID}
        self.c.sendPlist(d)
        startsession = self.c.recvPlist()
        self.SessionID = startsession.get('SessionID')
        if startsession.get('EnableSessionSSL'):
            sslfile = self.identifier + '_ssl.txt'
            lf = '\n'
            if PY3:
                lf = '\n'
            sslfile = writeHomeFile(HOMEFOLDER, sslfile, certPem + lf + privateKeyPem)
            self.c.ssl_start(sslfile, sslfile)
        self.paired = True
        return True

    def pair(self):
        self.DevicePublicKey = self.getValue('', 'DevicePublicKey')
        if self.DevicePublicKey == '':
            self.logger.error('Unable to retreive DevicePublicKey')
            return False
        self.logger.info('Creating host key & certificate')
        certPem, privateKeyPem, DeviceCertificate = ca_do_everything(self.DevicePublicKey)
        pair_record = {'DevicePublicKey': plistlib.Data(self.DevicePublicKey), 'DeviceCertificate': plistlib.Data(DeviceCertificate), 
           'HostCertificate': plistlib.Data(certPem), 
           'HostID': self.hostID, 
           'RootCertificate': plistlib.Data(certPem), 
           'SystemBUID': '30142955-444094379208051516'}
        pair = {'Label': self.label, 'Request': 'Pair', 'PairRecord': pair_record}
        self.c.sendPlist(pair)
        pair = self.c.recvPlist()
        print pair
        if pair:
            if pair.get('Result') == 'Success' or pair.get('EscrowBag'):
                print 'kikou'
                pair_record['HostPrivateKey'] = plistlib.Data(privateKeyPem)
                pair_record['EscrowBag'] = pair.get('EscrowBag')
                writeHomeFile(HOMEFOLDER, '%s.plist' % self.identifier, plistlib.writePlistToString(pair_record))
                self.paired = True
                return True
            if pair.get('Error') == 'PasswordProtected':
                self.c.close()
                raise NotTrustedError
        else:
            self.logger.error(pair.get('Error'))
            self.c.close()
            raise PairingError

    def getValue(self, domain=None, key=None):
        if isinstance(key, str) and hasattr(self, 'record') and hasattr(self.record, key):
            return self.record[key]
        req = {'Request': 'GetValue', 'Label': self.label}
        if domain:
            req['Domain'] = domain
        if key:
            req['Key'] = key
        self.c.sendPlist(req)
        res = self.c.recvPlist()
        if res:
            r = res.get('Value')
            if hasattr(r, 'data'):
                return r.data
            return r

    def setValue(self, value, domain=None, key=None):
        req = {'Request': 'SetValue', 'Label': self.label}
        if domain:
            req['Domain'] = domain
        if key:
            req['Key'] = key
        req['Value'] = value
        self.c.sendPlist(req)
        res = self.c.recvPlist()
        self.logger.debug(res)
        return res

    def startService(self, name):
        if not self.paired:
            self.logger.info('NotPaired')
            raise NotPairedError
        self.c.sendPlist({'Label': self.label, 'Request': 'StartService', 'Service': name})
        StartService = self.c.recvPlist()
        if not StartService or StartService.get('Error'):
            raise StartServiceError(StartService.get('Error'))
        return PlistService(StartService.get('Port'), self.udid)

    def startServiceWithEscrowBag(self, name, escrowBag=None):
        if not self.paired:
            self.logger.info('NotPaired')
            raise NotPairedError
        if not escrowBag:
            escrowBag = self.record['EscrowBag']
        self.c.sendPlist({'Label': self.label, 'Request': 'StartService', 'Service': name, 'EscrowBag': escrowBag})
        StartService = self.c.recvPlist()
        if not StartService or StartService.get('Error'):
            if StartService.get('Error', '') == 'PasswordProtected':
                raise StartServiceError('your device is protected with password, please enter password in device and try again')
            raise StartServiceError(StartService.get('Error'))
        return PlistService(StartService.get('Port'), self.udid)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    l = LockdownClient()
    if l:
        n = writeHomeFile(HOMEFOLDER, '%s_infos.plist' % l.udid, plistlib.writePlistToString(l.allValues))
        logger.info('Wrote infos to %s', n)
    else:
        logger.error('Unable to connect to device')