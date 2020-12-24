# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteScript-1.7.5-py2.6.egg/paste/script/util/secret.py
# Compiled at: 2012-02-27 07:41:53
"""
Create random secrets.
"""
import os, random

def random_bytes(length):
    """
    Return a string of the given length.  Uses ``os.urandom`` if it
    can, or just pseudo-random numbers otherwise.
    """
    try:
        return os.urandom(length)
    except AttributeError:
        return ('').join([ chr(random.randrange(256)) for i in xrange(length) ])


def secret_string(length=25):
    """
    Returns a random string of the given length.  The string
    is a base64-encoded version of a set of random bytes, truncated
    to the given length (and without any newlines).
    """
    s = random_bytes(length).encode('base64')
    for badchar in '\n\r=':
        s = s.replace(badchar, '')

    return s[:length]