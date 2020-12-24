# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/shared/vnc/des.py
# Compiled at: 2016-11-12 07:38:04
import pyDes

class RFBDes(pyDes.des):

    def setKey(self, key):
        """RFB protocol for authentication requires client to encrypt
           challenge sent by server with password using DES method. However,
           bits in each byte of the password are put in reverse order before
           using it as encryption key."""
        newkey = []
        for ki in range(len(key)):
            bsrc = ord(key[ki])
            btgt = 0
            for i in range(8):
                if bsrc & 1 << i:
                    btgt |= 1 << 7 - i

            newkey.append(chr(btgt))

        super(RFBDes, self).setKey(newkey)