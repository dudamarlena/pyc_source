# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mdipierro/make_web2py/web2py/gluon/contrib/pbkdf2_ctypes.py
# Compiled at: 2013-10-14 11:16:24
"""
    pbkdf2_ctypes
    ~~~~~~

    Fast pbkdf2.

    This module implements pbkdf2 for Python using crypto lib from
    openssl or commoncrypto.

    Note: This module is intended as a plugin replacement of pbkdf2.py
    by Armin Ronacher.

    Git repository: 
    $ git clone https://github.com/michele-comitini/pbkdf2_ctypes.git

    :copyright: Copyright (c) 2013: Michele Comitini <mcm@glisco.it>
    :license: LGPLv3

"""
import ctypes, ctypes.util, hashlib, platform, os.path, binascii, sys
__all__ = [
 'pkcs5_pbkdf2_hmac', 'pbkdf2_bin', 'pbkdf2_hex']
__version__ = '0.99.3'

def _commoncrypto_hashlib_to_crypto_map_get(hashfunc):
    hashlib_to_crypto_map = {hashlib.sha1: 1, hashlib.sha224: 2, 
       hashlib.sha256: 3, 
       hashlib.sha384: 4, 
       hashlib.sha512: 5}
    crypto_hashfunc = hashlib_to_crypto_map.get(hashfunc)
    if crypto_hashfunc is None:
        raise ValueError('Unkwnown digest %s' % hashfunc)
    return crypto_hashfunc


def _commoncrypto_pbkdf2(data, salt, iterations, digest, keylen):
    """Common Crypto compatibile wrapper
    """
    c_hashfunc = ctypes.c_uint32(_commoncrypto_hashlib_to_crypto_map_get(digest))
    c_pass = ctypes.c_char_p(data)
    c_passlen = ctypes.c_size_t(len(data))
    c_salt = ctypes.c_char_p(salt)
    c_saltlen = ctypes.c_size_t(len(salt))
    c_iter = ctypes.c_uint(iterations)
    c_keylen = ctypes.c_size_t(keylen)
    c_buff = ctypes.create_string_buffer(keylen)
    crypto.CCKeyDerivationPBKDF.restype = ctypes.c_int
    crypto.CCKeyDerivationPBKDF.argtypes = [ctypes.c_uint32,
     ctypes.c_char_p,
     ctypes.c_size_t,
     ctypes.c_char_p,
     ctypes.c_size_t,
     ctypes.c_uint32,
     ctypes.c_uint,
     ctypes.c_char_p,
     ctypes.c_size_t]
    ret = crypto.CCKeyDerivationPBKDF(2, c_pass, c_passlen, c_salt, c_saltlen, c_hashfunc, c_iter, c_buff, c_keylen)
    return (
     1 - ret, c_buff)


def _openssl_hashlib_to_crypto_map_get(hashfunc):
    hashlib_to_crypto_map = {hashlib.md5: crypto.EVP_md5, hashlib.sha1: crypto.EVP_sha1, 
       hashlib.sha256: crypto.EVP_sha256, 
       hashlib.sha224: crypto.EVP_sha224, 
       hashlib.sha384: crypto.EVP_sha384, 
       hashlib.sha512: crypto.EVP_sha512}
    crypto_hashfunc = hashlib_to_crypto_map.get(hashfunc)
    if crypto_hashfunc is None:
        raise ValueError('Unkwnown digest %s' % hashfunc)
    crypto_hashfunc.restype = ctypes.c_void_p
    return crypto_hashfunc()


def _openssl_pbkdf2(data, salt, iterations, digest, keylen):
    """OpenSSL compatibile wrapper
    """
    c_hashfunc = ctypes.c_void_p(_openssl_hashlib_to_crypto_map_get(digest))
    c_pass = ctypes.c_char_p(data)
    c_passlen = ctypes.c_int(len(data))
    c_salt = ctypes.c_char_p(salt)
    c_saltlen = ctypes.c_int(len(salt))
    c_iter = ctypes.c_int(iterations)
    c_keylen = ctypes.c_int(keylen)
    c_buff = ctypes.create_string_buffer(keylen)
    crypto.PKCS5_PBKDF2_HMAC.argtypes = [
     ctypes.c_char_p, ctypes.c_int,
     ctypes.c_char_p, ctypes.c_int,
     ctypes.c_int, ctypes.c_void_p,
     ctypes.c_int, ctypes.c_char_p]
    crypto.PKCS5_PBKDF2_HMAC.restype = ctypes.c_int
    err = crypto.PKCS5_PBKDF2_HMAC(c_pass, c_passlen, c_salt, c_saltlen, c_iter, c_hashfunc, c_keylen, c_buff)
    return (err, c_buff)


try:
    system = platform.system()
    if system == 'Windows':
        if platform.architecture()[0] == '64bit':
            libname = ctypes.util.find_library('libeay64')
            if not libname:
                raise OSError('Library not found')
            crypto = ctypes.CDLL(libname)
        else:
            libname = ctypes.util.find_library('libeay32')
            if not libname:
                raise OSError('Library libeay32 not found.')
            crypto = ctypes.CDLL(libname)
        _pbkdf2_hmac = _openssl_pbkdf2
        crypto.PKCS5_PBKDF2_HMAC
    elif system == 'Darwin':
        if [ int(x) for x in platform.mac_ver()[0].split('.') ] < [10, 7, 0]:
            raise OSError('OS X Version too old %s < 10.7.0' % platform.mac_ver()[0])
        libname = ctypes.util.find_library('System')
        if not libname:
            raise OSError('Library not found')
        crypto = ctypes.CDLL(os.path.basename(libname))
        _pbkdf2_hmac = _commoncrypto_pbkdf2
    else:
        libname = ctypes.util.find_library('crypto')
        if not libname:
            raise OSError('Library crypto not found.')
        crypto = ctypes.CDLL(os.path.basename(libname))
        _pbkdf2_hmac = _openssl_pbkdf2
        crypto.PKCS5_PBKDF2_HMAC
except (OSError, AttributeError):
    _, e, _ = sys.exc_info()
    raise ImportError('Cannot find a compatible cryptographic library on your system. %s' % e)

def pkcs5_pbkdf2_hmac(data, salt, iterations=1000, keylen=24, hashfunc=None):
    if hashfunc is None:
        hashfunc = hashlib.sha1
    err, c_buff = _pbkdf2_hmac(data, salt, iterations, hashfunc, keylen)
    if err == 0:
        raise ValueError('wrong parameters')
    return c_buff.raw[:keylen]


def pbkdf2_hex(data, salt, iterations=1000, keylen=24, hashfunc=None):
    return binascii.hexlify(pkcs5_pbkdf2_hmac(data, salt, iterations, keylen, hashfunc))


def pbkdf2_bin(data, salt, iterations=1000, keylen=24, hashfunc=None):
    return pkcs5_pbkdf2_hmac(data, salt, iterations, keylen, hashfunc)


if __name__ == '__main__':
    try:
        crypto.SSLeay_version.restype = ctypes.c_char_p
        print crypto.SSLeay_version(0)
    except:
        pass

    import platform
    if platform.python_version_tuple() < ('3', '0', '0'):

        def bytes(*args):
            return str(args[0])


    for h in [hashlib.sha1, hashlib.sha224, hashlib.sha256,
     hashlib.sha384, hashlib.sha512]:
        print binascii.hexlify(pkcs5_pbkdf2_hmac(bytes('secret', 'utf-8') * 11, bytes('salt', 'utf-8'), hashfunc=h))