# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xix/utils/number.py
# Compiled at: 2007-01-21 19:00:11
"""Numerical functions.  Currently this module only contains a function
baserepr for building arbitrary base representation of a number.  More for
fun than any practicle application.
"""
__author__ = 'Drew Smathers'

def _pad(i, base):
    return '%s%i' % ((len('%d' % base) - len('%d' % i)) * ' ', i)


def baserepr(n, base, baser=None, prefix=None):
    prefix = prefix or ''
    baser = baser or (lambda i: _pad(i, base))
    buff = []
    modulus, rem = n % base, n / base
    buff.insert(0, baser(modulus))
    while rem >= base:
        modulus, rem = rem % base, rem / base
        buff.insert(0, baser(modulus))

    if rem:
        buff.insert(0, baser(rem))
    return prefix + ('').join(buff)


BASE64_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

def base64(n):
    baser = lambda i: BASE64_CHARS[i]
    return baserepr(n, 64, baser=baser)