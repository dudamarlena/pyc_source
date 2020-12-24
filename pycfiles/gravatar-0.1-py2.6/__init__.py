# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gravatar/__init__.py
# Compiled at: 2010-02-06 12:55:57
"""Generates a Gravatar from an email. Calling...

    gravatar.make('jakevoytko@gmail.com')

returns the valid Gravatar image:

    http://gravatar.com/avatar/2145579130b5dd2aaa367501de04273c

Optional parameters:

 * rating:  One of 'g', 'pg','r', or 'x'. These carry the same meaning as
            their MPAA counterparts.
 * size:    A number satisfying 1<=number<=512.
 * default: Either a URL that returns a default image, or a 'special
            value'. Special values are one of 'identicon', 'monsterid',
            'wavatar', or '404'. This field is not checked for validity.

 'ValueError' or 'TypeError' will be raised when invalid parameters
 are detected, depending on the offense"""
import urllib, hashlib

def make(email, rating=None, size=None, default=None):
    """Generates a Gravatar image URI using 'email'. See the module
    documentation for usage information."""
    if not _PurposelyString(email):
        raise TypeError('Email type invalid: ' + type(email))
    baseUrl = 'http://gravatar.com/avatar/'
    emailHash = hashlib.md5(email.lower()).hexdigest()
    args = {}
    if rating is not None:
        if not _PurposelyString(rating):
            raise TypeError('Bad rating type: %s' % type(rating))
        rating = str(rating).lower()
        if rating not in ('g', 'pg', 'r', 'x'):
            raise ValueError('Invalid Gravatar rating: %s' % rating)
        args['r'] = rating
    if size is not None:
        size = int(size)
        if not 1 <= size <= 512:
            raise ValueError('Invalid Gravatar size: %s Must be 1<=size<=512' % size)
        args['s'] = size
    if default:
        args['d'] = str(default)
    ret = baseUrl + emailHash
    if len(args):
        ret += '?' + urllib.urlencode(args)
    return ret


def _PurposelyString(s):
    """Checks to see if 's' is either a str or a unicode object."""
    return isinstance(s, str) or isinstance(s, unicode)