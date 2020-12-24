# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/house_arrest.py
# Compiled at: 2019-02-28 19:08:52
import os, logging
from pymobiledevice.lockdown import LockdownClient
from pymobiledevice.afc import AFCClient, AFCShell
from pprint import pprint
from optparse import OptionParser

class HouseArrestClient(AFCClient):

    def __init__(self, lockdown=None, serviceName='com.apple.mobile.house_arrest', service=None, udid=None, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.lockdown = lockdown if lockdown else LockdownClient(udid=udid)
        self.serviceName = serviceName
        self.service = service if service else self.lockdown.startService(self.serviceName)

    def stop_session(self):
        self.logger.info('Disconecting...')
        self.service.close()

    def send_command(self, applicationId, cmd='VendDocuments'):
        self.service.sendPlist({'Command': cmd, 'Identifier': applicationId})
        res = self.service.recvPlist()
        if res.get('Error'):
            self.logger.error('%s : %s', applicationId, res.get('Error'))
            return
        else:
            return res

    def shell(self, applicationId, cmd='VendDocuments'):
        res = self.send_command(applicationId, cmd='VendDocuments')
        if res:
            AFCShell(client=self.service).cmdloop()


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    parser = OptionParser(usage='%prog -a  applicationId')
    parser.add_option('-a', '--application', dest='applicationId', default=False, help='Application ID <com.apple.iBooks>', type='string')
    parser.add_option('-c', '--command', dest='cmd', default=False, help='House_Arrest commands: ', type='string')
    options, args = parser.parse_args()
    h = HouseArrestClient()
    if options.cmd:
        h.shell(options.applicationId, cmd=options.cmd)
    else:
        h.shell(options.applicationId)