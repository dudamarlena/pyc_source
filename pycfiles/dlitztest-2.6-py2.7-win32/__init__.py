# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\__init__.py
# Compiled at: 2013-03-13 13:15:35
"""Python Cryptography Toolkit

A collection of cryptographic modules implementing various algorithms
and protocols.

Subpackages:

Crypto.Cipher
 Secret-key (AES, DES, ARC4) and public-key encryption (RSA PKCS#1) algorithms
Crypto.Hash
 Hashing algorithms (MD5, SHA, HMAC)
Crypto.Protocol
 Cryptographic protocols (Chaffing, all-or-nothing transform, key derivation
 functions). This package does not contain any network protocols.
Crypto.PublicKey
 Public-key encryption and signature algorithms (RSA, DSA)
Crypto.Signature
 Public-key signature algorithms (RSA PKCS#1) 
Crypto.Util
 Various useful modules and functions (long-to-string conversion, random number
 generation, number theoretic functions)
"""
__all__ = [
 'Cipher', 'Hash', 'Protocol', 'PublicKey', 'Util', 'Signature']
__version__ = '2.6'
__revision__ = '$Id$'
version_info = (2, 6, 0, 'final', 0)