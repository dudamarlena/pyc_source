# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/Utilities/RemoteOperations.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 20565 bytes
import logging, sys, os, os, datetime, getpass, shlex, shutil, tarfile, tempfile, time, hashlib
from HdlLib.Utilities import Timer
import getpass
try:
    import configparser
except:
    import ConfigParser as configparser

class RemoteOperations:

    def __init__(self, RemoteSubFolder='UnknownTool'):
        """
                Environment variables settings
                """
        self.RemoteHost = None
        self.UseOpenSSH = True

    def SetRemoteHost(self, RemoteHost, PromptID=False, Config=None):
        """
                Set Remote Mode to True/False.
                """
        self.RemoteHost = RemoteHost

    def Disconnect(self):
        """
                Configure connection parameters
                """
        try:
            disconnect_all()
        except:
            pass

    def SendPaths(self, DirList=[], FileDict={}):
        """
                Send a bunch of local path to remote host. Create, eventually, some host directories before.
                        DirList  : list of directories to be created on host.
                        FileDict : pair LocalPath:HostPath. Local paths to be sent to a Host path.
                """
        logging.debug('Send data to remote host.')
        for Directory in DirList:
            try:
                logging.debug("Create directory '{0}'.".format(Directory))
                if self.RemoteRun(Command='mkdir -p {0}'.format(Directory), ScriptsToSource=[], abort_on_prompts='True', warn_only=True) is False:
                    logging.error("Remote host configuration: unable to create directory '{0}'.".format(Directory))
                    return False
            except:
                logging.error("Remote host configuration: unable to create directory '{0}'.".format(Directory))
                return False

        TempPath = tempfile.mkdtemp(suffix='', prefix='tmp', dir=None)
        Archive = os.path.join(TempPath, 'Bundle.tar.gz')
        logging.debug("Create archive '{0}'".format(Archive))
        with tarfile.open(Archive, 'w:gz') as (TGZFile):
            for LocalPath, HostPath in FileDict.items():
                logging.debug("Move '{0}' to '{1}'.".format(LocalPath, HostPath))
                if os.path.exists(LocalPath):
                    LPath = os.path.abspath(os.path.normpath(os.path.expanduser(LocalPath)))
                    logging.debug("Add '{0}' to the archive.".format(LPath))
                    TGZFile.add(LPath, arcname=os.path.basename(LPath), recursive=True, exclude=None, filter=None)
                else:
                    logging.error("No such directory '{0}'".format(LocalPath))
                    return False

        if not os.path.isfile(Archive):
            logging.error("Unable to create tar.gz archive '{0}'.".format(Archive))
            return False
        if self.UploadToHost(LocalPath=Archive, HostPath=HostPath) is False:
            logging.error('Upload failure')
            return False
        os.remove(Archive)
        RemoteArchive = os.path.join(HostPath, os.path.basename(Archive))
        if self.RemoteRun(Command='tar -xzvf {1} --directory={0}'.format(HostPath, RemoteArchive), ScriptsToSource=[], abort_on_prompts='True', warn_only=True) is False:
            logging.error('Compression failure.')
            return False
        logging.info('Remote .tar.gz file successfully unpacked')
        logging.debug('Checksum operation.')
        LocalCheckSum = CheckSum(FilePath=LocalPath, Algo='md5')
        logging.debug("[LOCAL CHECKSUM] '{0}'  {1}".format(LocalCheckSum, LocalPath))
        ChecksumCmd = 'md5sum {0}'.format(RemoteArchive)
        Success = self.RemoteRun(Command=ChecksumCmd, ScriptsToSource=[], abort_on_prompts='True', warn_only=True)
        if self.RemoteRun(Command='rm {0}'.format(RemoteArchive), ScriptsToSource=[], abort_on_prompts='True', warn_only=True) is False:
            logging.error('Archive removal failure.')
            return False
        if Success is True:
            RemoteCheckSum = ChecksumCmd
            if RemoteCheckSum != ChecksumCmd:
                logging.error("File '{0}' checksum failed.".format(LocalPath))
                return False
        else:
            logging.error('Checksum command failed: {0}.'.format(ChecksumCmd))
            logging.error("Host file '{0}' checksum failed.".format(HostFilePath))
            return False
        return True

    def CreateHostDir(self, DirList=[]):
        """
                DirList  : list of directories to be created on host.
                """
        for Directory in DirList:
            try:
                Command = 'mkdir -p {0}'.format(Directory)
                logging.debug("Create directory '{0}'.".format(Directory))
                if self.RemoteRun(Command=Command, ScriptsToSource=[], abort_on_prompts='True', warn_only=True) is False:
                    logging.error("Remote host configuration: unable to create directory '{0}'.".format(Directory))
                    return False
            except:
                logging.error("Remote host configuration: unable to create directory '{0}'.".format(Directory))
                return False

        return True

    def SendPathsRelative(self, FileDict, HostAbsPath):
        """
                Send a bunch of local path to remote host. Create, eventually, some host directories before.
                        DirList  : list of directories to be created on host.
                        FileDict : pair LocalPath:HostRelPath. Local paths to be sent to a Host path.
                """
        logging.debug('Send data with relative path to remote host.')
        TempPath = tempfile.mkdtemp(suffix='', prefix='tmp', dir=None)
        Archive = os.path.join(TempPath, 'Bundle.tar.gz')
        logging.debug("Create archive '{0}'".format(Archive))
        with tarfile.open(Archive, 'w:gz') as (TGZFile):
            for LocalPath, HostRelPath in FileDict.items():
                logging.debug("Move '{0}' to '{1}' (relative:'{2}').".format(LocalPath, HostAbsPath, HostRelPath))
                if os.path.exists(LocalPath):
                    logging.debug("Add '{0}' to the archive.".format(os.path.basename(LocalPath)))
                    TGZFile.add(LocalPath, arcname=HostRelPath, recursive=True, exclude=None, filter=None)
                else:
                    logging.error("No such directory '{0}'".format(LocalPath))
                    return False

        if not os.path.isfile(Archive):
            logging.error("Unable to create tar.gz archive '{0}'.".format(Archive))
            return False
        if self.UploadToHost(LocalPath=Archive, HostPath=HostAbsPath) is False:
            logging.error('Upload failure')
            return False
        os.remove(Archive)
        RemoteArchive = os.path.join(HostAbsPath, os.path.basename(Archive))
        if self.RemoteRun(Command='tar -xzvf {1} --directory={0}'.format(HostAbsPath, RemoteArchive), ScriptsToSource=[], abort_on_prompts='True', warn_only=True) is False:
            logging.error('Compression failure.')
            return False
        logging.info('Remote .tar.gz file successfully unpacked')
        logging.debug('Checksum operation.')
        LocalCheckSum = CheckSum(FilePath=LocalPath, Algo='md5')
        logging.debug("[LOCAL CHECKSUM] '{0}'  {1}".format(LocalCheckSum, LocalPath))
        ChecksumCmd = 'md5sum {0}'.format(RemoteArchive)
        Success = self.RemoteRun(Command=ChecksumCmd, ScriptsToSource=[], abort_on_prompts='True', warn_only=True)
        if self.RemoteRun(Command='rm {0}'.format(RemoteArchive), ScriptsToSource=[], abort_on_prompts='True', warn_only=True) is False:
            logging.error('Archive removal failure.')
            return False
        if Success is True:
            RemoteCheckSum = ChecksumCmd
            if RemoteCheckSum != ChecksumCmd:
                logging.error("File '{0}' checksum failed.".format(LocalPath))
                return False
        else:
            logging.error('Checksum command failed: {0}.'.format(ChecksumCmd))
            logging.error("Host file '{0}' checksum failed.".format(HostFilePath))
            return False
        return True

    def UploadToHost(self, LocalPath, HostPath, **Settings):
        """
                Upload a local path to host.
                """
        time.sleep(0.1)
        if self.UseOpenSSH is True:
            Res = self.SSH_COPY_TO(SourcePath=LocalPath, TargetPath=HostPath)
            if Res == 0:
                return True
            else:
                return False
        else:
            with settings(**Settings):
                UploadedFiles = put(LocalPath, HostPath)
                if len(UploadedFiles) == 0:
                    return False
                else:
                    return True

    def DownloadFromHost(self, HostPath, LocalPath, **Settings):
        """
                Download a host path to local.
                """
        time.sleep(0.1)
        if self.UseOpenSSH is True:
            Res = self.SSH_COPY_FROM(SourcePath=HostPath, TargetPath=LocalPath)
            if Res == 0:
                return True
            else:
                return False
        else:
            logging.warning('fabric not supported.')

    def RemoteRun(self, Command, ScriptsToSource=[], FromDirectory=None, XForwarding=False, **Settings):
        """
                Run a command line on host bash console.
                """
        time.sleep(0.1)
        if self.UseOpenSSH is True:
            Res = self.SSH_RUN(Command=Command, ScriptsToSource=ScriptsToSource, FromDirectory=FromDirectory, XForwarding=XForwarding)
            if Res == 0:
                return True
            else:
                return False
        else:
            logging.warning('fabric not supported.')

    def SSH_RUN(self, Command, ScriptsToSource=[], FromDirectory=None, XForwarding=False):
        """
                Run a command line on host with openssh.
                """
        XOption = '-Y' if XForwarding is True else ''
        if FromDirectory is None:
            SSH_CMD = 'ssh {2} -t {0} bash -lic \\"{1}\\"'.format(self.RemoteHost, Command, XOption)
        else:
            SSH_CMD = 'ssh {3} -t {0} "cd {2};bash -lic \\"{1}\\""'.format(self.RemoteHost, Command, FromDirectory, XOption)
        logging.debug("SSH command: '{0}'".format(SSH_CMD))
        RetVal = os.system(SSH_CMD)
        return RetVal

    def SSH_COPY_TO(self, SourcePath, TargetPath):
        """
                Run a command line on host with openssh.
                """
        SSH_CMD = 'scp {SOURCE} {HOST}:{TARGET}'.format(SOURCE=SourcePath, TARGET=TargetPath, HOST=self.RemoteHost)
        logging.debug("SSH command: '{0}'".format(SSH_CMD))
        return os.system(SSH_CMD)

    def SSH_COPY_FROM(self, SourcePath, TargetPath):
        """
                Run a command line on host with openssh.
                """
        SSH_CMD = 'scp {HOST}:{SOURCE} {TARGET}'.format(SOURCE=SourcePath, TARGET=TargetPath, HOST=self.RemoteHost)
        logging.debug("SSH command: '{0}'".format(SSH_CMD))
        return os.system(SSH_CMD)

    def Hostcd(self, *argc, **argv):
        """
                Change current directory (context manager).
                """
        return cd(*argc, **argv)


def CheckSum(FilePath, Algo='md5'):
    """
        return check sum for specified "FilePath" calculated with algo "Algo".
        """
    BLOCKSIZE = 65536
    if Algo == 'md5':
        Hasher = hashlib.md5()
    else:
        if Algo == 'sha1':
            Hasher = hashlib.sha1()
        else:
            logging.error("[CheckSum] No such algorithm '{0}' defined for checksum.".format(Algo))
            return
    with open(FilePath, 'rb') as (FileChecked):
        Buf = FileChecked.read(BLOCKSIZE)
        while len(Buf) > 0:
            Hasher.update(Buf)
            Buf = FileChecked.read(BLOCKSIZE)

    return Hasher.hexdigest()