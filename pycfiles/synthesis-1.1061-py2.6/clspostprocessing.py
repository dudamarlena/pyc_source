# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/clspostprocessing.py
# Compiled at: 2010-12-12 22:28:56
from logger import Logger
import fileutils, os, ftplib
from clsexceptions import FTPUploadFailureError, VPNFailure
from conf import settings
import paramiko
from conf import outputConfiguration
from datetime import datetime

class ClsPostProcessing(FTPUploadFailureError, VPNFailure):

    def __init__(self, vendorID):
        self.settings = settings
        self.systemMode = settings.MODE
        debug = settings.DEBUG
        if debug == True:
            self.debug = True
        else:
            self.debug = False
        iniFile = 'logging.ini'
        self.debugMessages = Logger(iniFile)
        self.outputConfig = outputConfiguration.Configuration[vendorID]

    def processFile(self):
        pass

    def setINI(self, iniSettings):
        self.settings = iniSettings
        self.systemMode = iniSettings['options.systemmode']

    def processFileSFTP(self, filesToTransfer=[]):
        self.establishSFTP()
        self.transferSFTP(filesToTransfer)
        self.disconnectSFTP()

    def processFileVPN(self, pFiles):
        rc = self.establishVPN()
        if rc != 0:
            comm = self.settings[('%s_options.vpnconnect' % self.systemMode)]
            theError = (1095, 'VPN Process failed to connect with command: %s.  Return from command was: %s.  Stopping processing until this can be resolved.  In order to complete processing you can execute command python clspostprocessing.py which will upload the XML files for Bowman Processing.' % (comm, rc), 'processFile(self)')
            raise VPNFailure, theError
        rc = self.establishFTP(pFiles)
        rc = self.disconnectVPN()
        if rc != 0:
            comm = self.settings[('%s_options.vpndisconnect' % self.systemMode)]
            theError = (1096, 'VPN Process failed to disconnect with command: %s.  Return from command was: %s.  Stopping processing until this can be resolved.  In order to complete processing you can execute command %s' % (comm, rc, comm), 'processFile(self)')
            raise VPNFailure, theError
        print 'Processing completed'

    def establishSFTP(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.outputConfig['destinationURL'], username=self.outputConfig['username'], password=self.outputConfig['password'])
        except:
            pass

        self.ftp = self.ssh.open_sftp()

    def transferSFTP(self, filesToTransfer):
        destPath = self.outputConfig['outputpath']
        if destPath != '':
            self.ftp.chdir(destPath)
        for file in filesToTransfer:
            if self.debug:
                print 'writing file: %s to server: %s to dest file: %s' % (file, destPath, os.path.split(file)[1])
            destFile = os.path.split(file)[1]
            self.ftp.put(file, destFile)
            if self.outputConfig['owner'] != '':
                pass
            if self.outputConfig['chmod'] != '':
                self.ftp.chmod(destFile, self.outputConfig['chmod'])
            if self.outputConfig['group'] != '':
                pass
            print self.ftp.stat(destFile)

        self.ftp.chdir('..')
        print self.ftp.listdir(path=destPath)

    def disconnectSFTP(self):
        self.ftp.close()

    def establishVPN(self):
        command = self.settings[('%s_options.vpnconnect' % self.systemMode)]
        print 'Establishing VPN Connection using command: %s' % command
        rc = self.spawnProcess(command)
        return rc

    def establishFTP(self, pFiles):
        command = 'ftp baisix.servicept.com'
        print 'Connecting to FTP '
        self.ftp(pFiles)

    def disconnectVPN(self):
        print 'Disconnecting from VPN'
        command = self.settings[('%s_options.vpncdisconnect' % self.systemMode)]
        print 'Disconnecting from VPN Connection using command: %s' % command
        rc = self.spawnProcess(command)
        return rc

    def ftp(self, pFiles):
        outputDir = self.settings['filelocations.outputlocation']
        url = self.settings[('%s_options.ftpxmlupload' % self.systemMode)]
        uname = self.settings[('%s_options.ftpuname' % self.systemMode)]
        passwd = self.settings[('%s_options.ftppwd' % self.systemMode)]
        destdir = self.settings[('%s_options.ftpdestdir' % self.systemMode)]
        ftpsleep = self.settings['options.ftpsleep']
        ftpretries = self.settings['options.ftpretries']
        ftpinitialsleep = self.settings['options.ftpinitialsleep']
        if self.debug:
            self.debugMessages.log('url: %s\n' % url, 1)
            self.debugMessages.log('uname: %s\n' % uname, 1)
            self.debugMessages.log('passwd: %s\n' % passwd, 1)
            self.debugMessages.log('destdir: %s\n' % destdir, 1)
        attempt = 0
        ftpUploaded = False
        fileutils.sleep(int(ftpinitialsleep))
        while not ftpUploaded:
            print 'Connecting to: %s' % url
            attempt = +1
            print 'Attempting FTP Process: %s' % attempt
            if attempt > ftpretries:
                theError = (
                 1090, 'FTP Process failed to upload file: %s.  Process timeout parm: %s and sleep parm: %s.  Please check the VPN Connection or the FTP Server at: %s' % (str(pFiles), ftpretries, ftpsleep, url), 'ftp(self)')
                raise FTPUploadFailureError, theError
            try:
                f = ftplib.FTP(url, uname, passwd)
            except ftplib.all_errors:
                self.debugMessages.log('General FTP Error.  Possibly process is happening too quickly.  Sleeping for %s seconds and trying again.' % ftpsleep, 1)
                fileutils.sleep(int(ftpsleep))
                continue

            print 'Connected'
            print 'Changing Directories to: %s' % destdir
            print f.cwd(destdir)
            if len(pFiles) > 0:
                for file in pFiles:
                    print 'Uploading file: %s' % file
                    fo = open(file, 'r')
                    fname = os.path.basename(file)
                    rc = f.storlines('STOR ' + fname, fo)
                    if rc == '226 Transfer complete.':
                        self.renameFile(file, True)
                    else:
                        badFile = self.renameFile(file, False)
                        theError = (1080, 'FTP Error during upload of file: %s.  FTP Server returned: %s.  Stopping the upload process.  Please investigate and start the process again to complete the upload.  File was renamed to: %s' % (fname, rc, badFile), 'ftp(self)')
                        raise FTPUploadFailureError, rc
                        print 'Done uploading files'
                        fo.close()

            ftpUploaded = True
            break

        print f.close()
        print 'FTP Processing Completed, disconnected'
        return 0

    def renameFile(self, fileName, bSuccess=True):
        if bSuccess:
            renameExt = self.settings['filelocations.uploaded_file_extensions']
        else:
            renameExt = self.settings['filelocations.uploaded_failed_file_extensions']
        lsNowISO = datetime.now().isoformat()
        destFile = '%s.%s.%s' % (fileName, lsNowISO, renameExt)
        fileutils.renameFile(fileName, destFile)
        return destFile

    def spawnProcess(self, command):
        cmdParts = command.split(' ')
        rc = os.system(command)
        print 'Return Code is: %s' % rc
        return rc


if __name__ == '__main__':
    pprocess = ClsPostProcessing('5678')
    pprocess.processFile()