# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/credentials/cryptocommon.py
# Compiled at: 2016-12-29 01:49:52
from struct import pack

class CryptoCommon:

    def transformKey(self, InputKey):
        OutputKey = []
        OutputKey.append(chr(ord(InputKey[0]) >> 1))
        OutputKey.append(chr((ord(InputKey[0]) & 1) << 6 | ord(InputKey[1]) >> 2))
        OutputKey.append(chr((ord(InputKey[1]) & 3) << 5 | ord(InputKey[2]) >> 3))
        OutputKey.append(chr((ord(InputKey[2]) & 7) << 4 | ord(InputKey[3]) >> 4))
        OutputKey.append(chr((ord(InputKey[3]) & 15) << 3 | ord(InputKey[4]) >> 5))
        OutputKey.append(chr((ord(InputKey[4]) & 31) << 2 | ord(InputKey[5]) >> 6))
        OutputKey.append(chr((ord(InputKey[5]) & 63) << 1 | ord(InputKey[6]) >> 7))
        OutputKey.append(chr(ord(InputKey[6]) & 127))
        for i in range(8):
            OutputKey[i] = chr(ord(OutputKey[i]) << 1 & 254)

        return ('').join(OutputKey)

    def deriveKey(self, baseKey):
        key = pack('<L', baseKey)
        key1 = key[0] + key[1] + key[2] + key[3] + key[0] + key[1] + key[2]
        key2 = key[3] + key[0] + key[1] + key[2] + key[3] + key[0] + key[1]
        return (self.transformKey(key1), self.transformKey(key2))