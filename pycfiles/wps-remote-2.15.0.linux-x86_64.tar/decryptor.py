# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/decryptor.py
# Compiled at: 2018-09-13 11:06:18
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import base64, sys

def decrypt(message, externKey, passphrase):
    privatekey = open(externKey, 'r')
    rsa_key = RSA.importKey(privatekey, passphrase=passphrase)
    decriptedData = rsa_key.decrypt(base64.b64decode(message))
    print decriptedData


if __name__ == '__main__':
    if len(sys.argv) == 4:
        decrypt(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print 'Usage: python decrypt.py password path/to/rsakey.pem passphrase'