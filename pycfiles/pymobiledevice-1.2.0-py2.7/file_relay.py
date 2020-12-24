# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/file_relay.py
# Compiled at: 2019-03-03 17:14:07
import os, zlib, gzip, logging
from pymobiledevice.lockdown import LockdownClient
from pymobiledevice.util.cpio import CpioArchive
from pymobiledevice.util import MultipleOption
from pprint import pprint
from tempfile import mkstemp
from optparse import OptionParser
from io import BytesIO
SRCFILES = 'Baseband\nCrashReporter\nMobileAsset\nVARFS\nHFSMeta\nLockdown\nMobileBackup\nMobileDelete\nMobileInstallation\nMobileNotes\nNetwork\nUserDatabases\nWiFi\nWirelessAutomation\nNANDDebugInfo\nSystemConfiguration\nUbiquity\ntmp\nWirelessAutomation'

class DeviceVersionNotSupported(Exception):
    pass


class FileRelay(object):

    def __init__(self, lockdown=None, serviceName='com.apple.mobile.file_relay', udid=None, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.lockdown = lockdown if lockdown else LockdownClient(udid=udid)
        ProductVersion = self.lockdown.getValue('', 'ProductVersion')
        if ProductVersion[0] >= '8':
            raise DeviceVersionNotSupported
        self.service = self.lockdown.startService(serviceName)
        self.packet_num = 0

    def stop_session(self):
        self.logger.info('Disconecting...')
        self.service.close()

    def request_sources(self, sources=[
 'UserDatabases']):
        self.service.sendPlist({'Sources': sources})
        while 1:
            res = self.service.recvPlist()
            if res:
                s = res.get('Status')
                if s == 'Acknowledged':
                    z = ''
                    while True:
                        x = self.service.recv()
                        if not x:
                            break
                        z += x

                    return z
                print res.get('Error')
                break

        return


if __name__ == '__main__':
    parser = OptionParser(option_class=MultipleOption, usage='%prog')
    parser.add_option('-s', '--sources', action='extend', dest='sources', metavar='SOURCES', choices=SRCFILES.split('\n'), help='comma separated list of file relay source to dump')
    parser.add_option('-e', '--extract', dest='extractpath', default=False, help='Extract archive to specified location', type='string')
    parser.add_option('-o', '--output', dest='outputfile', default=False, help='Output location', type='string')
    options, args = parser.parse_args()
    sources = []
    if options.sources:
        sources = options.sources
    else:
        sources = [
         'UserDatabases']
    print 'Downloading: %s' % ('').join([ str(item) + ' ' for item in sources ])
    fc = None
    try:
        fc = FileRelay()
    except:
        print 'Device with product vertion >= 8.0 does not allow access to fileRelay service'
        exit()

    data = fc.request_sources(sources)
    if data:
        if options.outputfile:
            path = options.outputfile
        else:
            _, path = mkstemp(prefix='fileRelay_dump_', suffix='.gz', dir='.')
        open(path, 'wb').write(data)
        self.logger.info('Data saved to:  %s ', path)
    if options.extractpath:
        with open(path, 'r') as (f):
            gz = gzip.GzipFile(mode='rb', fileobj=f)
            cpio = CpioArchive(fileobj=BytesIO(gz.read()))
            cpio.extract_files(files=None, outpath=options.extractpath)