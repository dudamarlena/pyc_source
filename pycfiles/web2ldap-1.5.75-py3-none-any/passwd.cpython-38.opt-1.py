# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/ldaputil/passwd.py
# Compiled at: 2020-05-04 07:50:34
# Size of source mod 2**32: 2178 bytes
"""
ldaputil.passwd - client-side password setting

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import base64, hashlib, crypt, secrets
from ldap0.pw import random_string, PWD_UNIX_CRYPT_ALPHABET
AVAIL_USERPASSWORD_SCHEMES = {'crypt':'Unix crypt(3)', 
 'sha':'SHA-1', 
 'ssha':'salted SHA-1', 
 'md5':'MD5', 
 'smd5':'salted MD5', 
 'sha256':'SHA-256', 
 'ssha256':'salted SHA-256', 
 'sha384':'SHA-384', 
 'ssha384':'salted SHA-384', 
 'sha512':'SHA-512', 
 'ssha512':'salted SHA-512', 
 '':'plain text'}
SALTED_USERPASSWORD_SCHEMES = {
 'smd5',
 'ssha',
 'ssha256',
 'ssha384',
 'ssha512'}
SCHEME2HASHLIBFUNC = {'sha':hashlib.sha1, 
 'ssha':hashlib.sha1, 
 'md5':hashlib.md5, 
 'smd5':hashlib.md5, 
 'sha256':hashlib.sha256, 
 'ssha256':hashlib.sha256, 
 'sha384':hashlib.sha384, 
 'ssha384':hashlib.sha384, 
 'sha512':hashlib.sha512, 
 'ssha512':hashlib.sha512}

def user_password_hash(password, scheme, salt=None):
    """
    Return hashed password (including salt).
    """
    scheme = scheme.lower().strip()
    if not scheme:
        return password
    if scheme not in AVAIL_USERPASSWORD_SCHEMES.keys():
        raise ValueError('Hashing scheme %r not supported.' % scheme)
    elif scheme == 'crypt':
        encoded_pw = crypt.crypt(password.decode('utf-8'), random_string(PWD_UNIX_CRYPT_ALPHABET.decode('ascii'), 2)).encode('ascii')
    else:
        if scheme in SCHEME2HASHLIBFUNC:
            salt = secrets.token_bytes(12)
            encoded_pw = base64.encodebytes(SCHEME2HASHLIBFUNC[scheme](password + salt).digest() + salt).strip().replace(b'\n', b'')
        else:
            encoded_pw = password
    return b'{%s}%s' % (scheme.upper().encode('ascii'), encoded_pw)