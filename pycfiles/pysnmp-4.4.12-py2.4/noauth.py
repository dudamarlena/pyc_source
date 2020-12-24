# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/secmod/rfc3414/auth/noauth.py
# Compiled at: 2019-08-18 17:24:05
from pysnmp.proto.secmod.rfc3414.auth import base
from pysnmp.proto import errind, error

class NoAuth(base.AbstractAuthenticationService):
    __module__ = __name__
    serviceID = (1, 3, 6, 1, 6, 3, 10, 1, 1, 1)

    def hashPassphrase(self, authKey):
        pass

    def localizeKey(self, authKey, snmpEngineID):
        pass

    def authenticateOutgoingMsg(self, authKey, wholeMsg):
        raise error.StatusInformation(errorIndication=errind.noAuthentication)

    def authenticateIncomingMsg(self, authKey, authParameters, wholeMsg):
        raise error.StatusInformation(errorIndication=errind.noAuthentication)