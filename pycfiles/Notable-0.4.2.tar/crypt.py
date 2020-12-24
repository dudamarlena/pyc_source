# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmcfarlane/dev/personal/Notable/notable/crypt.py
# Compiled at: 2014-08-18 00:16:41
import base64, hashlib, random, sys

class NoEncryption(object):
    MODE_CBC = None


try:
    from Crypto.Cipher import AES
    from Crypto import Random
except (ImportError, NameError):
    AES = NoEncryption()

BLOCKS = 16
MODE = AES.MODE_CBC
PAD = chr(0)

def pad(string):
    _b32 = BLOCKS * 2
    return string + (_b32 - len(string) % _b32) * PAD


def encrypt(string, pwd):
    iv = Random.new().read(BLOCKS)
    cipher = iv + AES.new(key(pwd), MODE, iv).encrypt(pad(string))
    return base64.b64encode(cipher)


def key(pwd):
    return hashlib.sha256(pwd.encode('utf-8')).digest()


def decrypt(cipher, pwd):
    cipher = cipher.encode() if hasattr(cipher, 'encode') else cipher
    cipher = base64.b64decode(cipher)
    iv = cipher[:BLOCKS]
    decrypted = AES.new(key(pwd), MODE, iv).decrypt(cipher[BLOCKS:])
    if sys.version_info >= (3, 0):
        return decrypted.decode('utf-8', errors='ignore').rstrip(PAD)
    return decrypted.rstrip(PAD)


def main():
    pwd = 'my secret password'
    s = 'I love }apples{'
    encrypted = encrypt(s, pwd)
    print decrypt(encrypted, pwd)


if __name__ == '__main__':
    main()