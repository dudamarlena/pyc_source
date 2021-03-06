# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ed_crypt.py
# Compiled at: 2008-04-16 23:51:24
"""
This module provides utilities for encrypting and decrypting data. It is mostly
used for saving passwords and other sensitive data in config files. The code in
this file uses a fairly simple string transformation algorithm combined with a 
random salt for the encryption/decryption, and I also threw in a little code 
obfustication just for fun ;-).

USAGE:

Encrypt:
  1. Get the password string to encrypt
  2. Generate a new random salt with os.urandom() or some other randomly 
     generated string for each password to use as an encryption key
  3. Encrypt the password by calling Encrypt(password, salt)
  4. Save the salt somewhere else
  5. Write out the encrypted password to your config file

Decrypt:
  1. Get the encrypted password string
  2. Get the associated salt
  3. Decrypt and get the orignal password by calling 
     Decrypt(encrypted_passwd, salt)

EXAMPLE:

  >>> salt = os.urandom(8)
  >>> passwd = "HelloWorld"
  >>> encrypted_passwd = Encrypt(passwd, salt)
  >>> print encrypted_passwd
  eNoNysERADAIArCVUAFx/8XauzyTqTEtdKEXoQIWCbCZjaM74qhPlhK4f+BVPKTTyQP7JQ5i
  >>> decrypted_passwd = Decrypt(passwd, salt)
  >>> print decrypted_passwd
  HelloWorld

Finally:
This message will self destruct in 5 seconds ...

@summary: Cryptographic routines for encrypting/decrypting text

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: ed_crypt.py 52855 2008-03-27 14:53:06Z CJP $'
__revision__ = '$Revision: 52855 $'
__all__ = [
 'Encrypt', 'Decrypt']
import os, zlib, random, base64

def _Encode(text):
    g = lambda y: (y != '\\' and [y] or [str(8 + random.randint(0, 100) % 2)])[0]
    return ('').join([ g(y) for y in ('').join([ '\\%o' % ord(x) for x in text ]) ])


def _Decode(text):
    exec 's="' + text.replace('8', '\\').replace('9', '\\') + '"'
    return s


def Encrypt(passwd, salt):
    """Encrypt the given password string using the supplied salt as the 
    cryptographic key. If either the passwd or salt strings are empty the 
    return value will be the same as the passwd parameter.
    @param passwd: String to encrypt
    @param salt: key to encrypt string with

    """
    if not len(passwd.strip()) or not len(salt.strip()):
        return passwd
    else:
        return base64.b64encode(zlib.compress(str(long(_Encode(passwd)) * long(_Encode(salt).replace('8', '9'))), 9))


def Decrypt(passwd, salt):
    """Decrypt the given password string using the supplied salt as a key
    If either the passwd or salt strings are empty the return value will be
    the same as the passwd parameter.
    @param passwd: a non empty string
    @param salt: a non empty string

    """
    if not len(passwd.strip()) or not len(salt.strip()):
        return passwd
    else:
        return _Decode(str(long(zlib.decompress(base64.b64decode(passwd))) / long(str.replace(_Encode(salt), '8', '9'))))


if __name__ == '__main__':
    TEST_FILE = 'TEST_passwd.crypt'
    PASSWD = 'HelloWorld'
    salt = os.urandom(8)
    print 'PASSWORD STR: ', PASSWD
    es = Encrypt(PASSWD, salt)
    print 'ENCRYPTED STR: ', es
    print 'DECRYPTED STR: ', Decrypt(es, salt)
    print 'Empty String Test'
    salt2 = os.urandom(8)
    es = Encrypt('', salt2)
    print 'Encrypted String', es
    print 'Decrypted String', Decrypt(es, salt)