# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\utils\hashed.py
# Compiled at: 2020-02-23 02:04:03
"""
"""
from .. import HASHED_NONE, HASHED_MD5, HASHED_SALTED_MD5, HASHED_SALTED_SHA, HASHED_SALTED_SHA256, HASHED_SALTED_SHA384, HASHED_SALTED_SHA512, HASHED_SHA, HASHED_SHA256, HASHED_SHA384, HASHED_SHA512
import hashlib
from os import urandom
from base64 import b64encode
from ..core.exceptions import LDAPInvalidHashAlgorithmError
algorithms_table = {HASHED_MD5: ('md5', 'MD5'), 
   HASHED_SHA: ('sha', 'SHA1'), 
   HASHED_SHA256: ('sha256', 'SHA256'), 
   HASHED_SHA384: ('sha384', 'SHA384'), 
   HASHED_SHA512: ('sha512', 'SHA512')}
salted_table = {HASHED_SALTED_MD5: (
                     'smd5', HASHED_MD5), 
   HASHED_SALTED_SHA: (
                     'ssha', HASHED_SHA), 
   HASHED_SALTED_SHA256: (
                        'ssha256', HASHED_SHA256), 
   HASHED_SALTED_SHA384: (
                        'ssha384', HASHED_SHA384), 
   HASHED_SALTED_SHA512: (
                        'ssha512', HASHED_SHA512)}

def hashed(algorithm, value, salt=None, raw=False, encoding='utf-8'):
    if str is not bytes and not isinstance(value, bytes):
        value = value.encode(encoding)
    if algorithm is None or algorithm == HASHED_NONE:
        return value
    else:
        if algorithm in algorithms_table:
            try:
                digest = hashlib.new(algorithms_table[algorithm][1], value).digest()
            except ValueError:
                raise LDAPInvalidHashAlgorithmError('Hash algorithm ' + str(algorithm) + ' not available')

            if raw:
                return digest
            return '{%s}' % algorithms_table[algorithm][0] + b64encode(digest).decode('ascii')
        else:
            if algorithm in salted_table:
                if not salt:
                    salt = urandom(8)
                digest = hashed(salted_table[algorithm][1], value + salt, raw=True) + salt
                if raw:
                    return digest
                return '{%s}' % salted_table[algorithm][0] + b64encode(digest).decode('ascii')
            try:
                if not salt:
                    digest = hashlib.new(algorithm, value).digest()
                else:
                    digest = hashlib.new(algorithm, value + salt).digest() + salt
            except ValueError:
                raise LDAPInvalidHashAlgorithmError('Hash algorithm ' + str(algorithm) + ' not available')

            if raw:
                return digest
            return '{%s}' % algorithm + b64encode(digest).decode('ascii')
        return