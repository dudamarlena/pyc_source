# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/datatable.py
# Compiled at: 2014-07-11 17:28:21
from bta.tools.flags import Flags, Enums

class UserAccountControl(Flags):
    _flags_ = {'script': 1, 
       'accountDisable': 2, 
       'homedirRequired': 8, 
       'lockout': 16, 
       'passwdNotrequired': 32, 
       'passwdCantChange': 64, 
       'encryptedTextPassAllowed': 128, 
       'tempDuplicateAccount': 256, 
       'normalAccount': 512, 
       'interdomainTrustAccount': 2048, 
       'workstationTrustAccount': 4096, 
       'serverTrustAccount': 8192, 
       'dontExpirePassword': 65536, 
       'mnsLogonAccount': 131072, 
       'smartcardRequired': 262144, 
       'trustedForDelegation': 524288, 
       'notDelegated': 1048576, 
       'useDESKeyOnly': 2097152, 
       'dontRequirePreAuth': 4194304, 
       'passwordExpired': 8388608, 
       'trustedToAuthForDelegation': 16777216, 
       'partialSecretsAccount': 67108864}


class TrustAttributes(Flags):
    _flags_ = {'NON_TRANSITIVE': 1, 
       'UPLEVEL_ONLY': 2, 
       'QUARANTINED_DOMAIN': 4, 
       'FOREST_TRANSITIVE': 8, 
       'CROSS_ORGANIZATION': 16, 
       'WITHIN_FOREST': 32, 
       'TREAT_AS_EXTERNAL': 64, 
       'USES_RC4_ENCRYPTION': 128}


class OIDPrefix(Enums):
    _enum_ = {'2.5.4.': 0, 
       '2.5.6.': 65536, 
       '1.2.840.113556.1.2.': 131072, 
       '1.2.840.113556.1.3.': 196608, 
       '2.5.5.': 524288, 
       '1.2.840.113556.1.4.': 589824, 
       '1.2.840.113556.1.5.': 655360, 
       '2.16.840.1.113730.3.': 1310720, 
       '0.9.2342.19200300.100.1.': 1376256, 
       '2.16.840.1.113730.3.1.': 1441792, 
       '1.2.840.113556.1.5.7000.': 1507328, 
       '2.5.21.': 1572864, 
       '2.5.18.': 1638400, 
       '2.5.20.': 1703936, 
       '1.3.6.1.4.1.1466.101.119.': 1769472, 
       '2.16.840.1.113730.3.2.': 1835008, 
       '1.3.6.1.4.1.250.1.': 1900544, 
       '1.2.840.113549.1.9.': 1966080, 
       '0.9.2342.19200300.100.4.': 2031616}


class TrustType(Enums):
    _enum_ = {'DOWNLEVEL': 1, 
       'UPLEVEL': 2, 
       'MIT': 3}


class TrustDirection(Enums):
    _enum_ = {'DISABLED': 0, 
       'INBOUND': 1, 
       'OUTBOUND': 2, 
       'BIDIRECTIONAL': 3}