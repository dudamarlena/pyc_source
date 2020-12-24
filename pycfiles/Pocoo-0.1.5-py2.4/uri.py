# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/utils/uri.py
# Compiled at: 2006-12-26 17:18:07
"""
    pocoo.utils.uri
    ~~~~~~~~~~~~~~~

    URI processing utilities.

    :copyright: 2006 by Armin Ronacher.
    :license: GNU GPL, see LICENSE for more details.
"""
import urllib

def urlencode(*args, **kwargs):
    """
    Like urllib.urlencode but takes also unicode objects
    which are automatically encoded in utf-8.
    The returned object is an ascii encoded unicode object.

    If the first argument is a string or unicode, it
    will be used to urlencode the first part of the url,
    right before the question mark.
    """
    if args and isinstance(args[0], basestring):
        root, args = args[0], args[1:]
        url = unicode(urllib.quote(root.encode('utf-8')))
    else:
        url = ''
    tmp = {}
    for (key, value) in dict(*args, **kwargs).iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        elif isinstance(value, unicode):
            value = value.encode('utf-8')
        tmp[key] = value

    return (tmp and url + '?' or url) + urllib.urlencode(tmp)