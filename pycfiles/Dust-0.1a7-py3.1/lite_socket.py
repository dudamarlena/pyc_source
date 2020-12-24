# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/extensions/lite/lite_socket.py
# Compiled at: 2010-06-01 14:13:58
from dust.crypto.dust import hash
from dust.core.dust_socket import dust_socket
from dust.core.util import encodeAddress, xor

class lite_socket(dust_socket):

    def makeSession(self, address, tryInvite):
        addressKey = encodeAddress(address)
        if addressKey in self.sessionKeys:
            return self.sessionKeys[addressKey]
        h1 = hash(addressKey.encode('ascii'))
        h2 = hash(self.myAddressKey.encode('ascii'))
        sessionKey = xor(h1, h2)
        self.sessionKeys[addressKey] = sessionKey
        print('SessionKey:', len(self.sessionKeys[addressKey]))
        return sessionKey