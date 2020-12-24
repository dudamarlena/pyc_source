# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/jks/Root/Dev/python/jkspy/jokes/modules/hash.py
# Compiled at: 2015-10-27 15:18:59
# Size of source mod 2**32: 3834 bytes
""" Dependency: Crypto """
from Crypto import Random
from Crypto.Hash import MD5, SHA, SHA256, SHA512, HMAC
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
HASH_ALGORITHMS = {'MD5': MD5,  'SHA': SHA, 
 'SHA256': SHA256, 
 'SHA512': SHA512, 
 'HMAC': HMAC}

def get_hash(message, method='sha256', hex=True):
    if method.upper() in HASH_ALGORITHMS.keys():
        if type(message) == str:
            message = message.encode('utf-8')
        if hex:
            return HASH_ALGORITHMS[method.upper()].new(message).hexdigest()
        else:
            return HASH_ALGORITHMS[method.upper()].new(message).digest()
    else:
        raise AttributeError('Hash algorithm [' + method.upper() + '] is not supported')


def get_checksum(filepath, method='md5', hex=True):
    if method.upper() in HASH_ALGORITHMS.keys():
        h = HASH_ALGORITHMS[method.upper()].new()
        chunk_size = 8192
        with open(filepath, 'rb') as (f):
            while True:
                chunk = f.read(chunk_size)
                if len(chunk) == 0:
                    break
                h.update(chunk)

        if hex:
            return h.hexdigest()
        else:
            return h.digest()
    else:
        raise AttributeError('Hash algorithm [' + method.upper() + '] is not supported')


def add_padding(message, blocksize):
    return message + (blocksize - len(message) % blocksize) * chr(blocksize - len(message) % blocksize)


def remove_padding(message):
    return message[:-ord(message[len(message) - 1:])]


def b2hex(bytes):
    return ''.join([hex(c)[2:] for c in bytes]).upper()


def hex2b(hexstr):
    hexbytes = [hexstr[(2 * i)] + hexstr[(2 * i + 1)] for i in range(0, int(len(hexstr) / 2))]
    return bytes([int(c, 16) for c in hexbytes])


def make_key(key_size=16):
    return Random.new().read(key_size)


def sencrypt(passphrase, plaintext, mode='CFB'):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(get_hash(passphrase, 'sha256', False), getattr(AES, 'MODE_' + mode), iv)
    return iv + cipher.encrypt(add_padding(plaintext, len(get_hash(passphrase, 'md5'))))


def sdecrypt(passphrase, ciphertext, mode='CFB'):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(get_hash(passphrase, 'sha256', False), getattr(AES, 'MODE_' + mode), iv)
    return remove_padding(cipher.decrypt(ciphertext[AES.block_size:]))


KEYPAIR_ALGORITHMS = {'RSA': RSA}

def make_keypair(method='RSA'):
    if method.upper() in KEYPAIR_ALGORITHMS.keys():
        keypair = KEYPAIR_ALGORITHMS[method.upper()].generate(2048)
        return keypair
    raise AttributeError('Keygen algorithm [' + method.upper() + '] is not supported')


def encrypt(keypair, plaintext):
    return keypair.publickey().encrypt(plaintext.encode('utf-8'), 32)


def decrypt(keypair, ciphertext):
    return keypair.decrypt(ciphertext)


def sign(keypair, message):
    mhash = get_hash(message, 'sha256', False)
    print(mhash)
    return keypair.sign(mhash, '')


def test_rsa():
    print('\n\n>>> Testing RSA')
    keypair = make_keypair()
    ciphertext = encrypt(keypair, 'Hello World')
    print('CipherByte: ' + ciphertext.__str__())
    plaintext = decrypt(keypair, ciphertext)
    print('PlainByte: ' + plaintext.decode())
    signature = sign(keypair, plaintext)
    print('Signature: ' + signature.__str__())
    print('Verification successful') if keypair.publickey().verify(get_hash('Hello World', hex=False), signature) else print('Verification failure')
    print('>>> END RSA Test')


def main():
    ciphertext = sencrypt('password', 'Hello World')
    print('CipherHex: ' + b2hex(ciphertext).__str__())
    print('CipherByte: ' + hex2b(b2hex(ciphertext)).__str__())
    plaintext = sdecrypt('password', ciphertext)
    print('PlainHex: ' + b2hex(plaintext).__str__())
    print('PlainByte: ' + plaintext.__str__())
    test_rsa()
    print('>>> Routine End')