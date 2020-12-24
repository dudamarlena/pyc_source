# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/encryptor.py
# Compiled at: 2018-09-13 11:06:18
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import base64, sys

def encrypt(message, externKey, passphrase):
    publickey = open(externKey, 'r')
    rsa_key = RSA.importKey(publickey, passphrase=passphrase)
    encriptedData = rsa_key.encrypt(message, 0)
    print base64.b64encode(encriptedData[0])


if __name__ == '__main__':
    if len(sys.argv) == 4:
        encrypt(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print 'Usage: python encrypt.py password path/to/rsakey.pub passphrase'