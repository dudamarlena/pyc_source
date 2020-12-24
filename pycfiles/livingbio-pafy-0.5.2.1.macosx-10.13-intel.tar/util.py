# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/davidchen/repos/django-video-composer/venv/lib/python2.7/site-packages/pafy/util.py
# Compiled at: 2017-12-12 20:44:10
import json, sys, os
if sys.version_info[:2] >= (3, 0):
    from urllib.error import HTTPError
    from urllib.parse import urlencode
else:
    from urllib2 import HTTPError
    from urllib import urlencode
from . import g
not_utf8_environment = False

class GdataError(Exception):
    """Gdata query failed."""
    pass


def call_gdata(api, qs):
    """Make a request to the youtube gdata api."""
    qs = dict(qs)
    qs['key'] = g.api_key
    url = g.urls['gdata'] + api + '?' + urlencode(qs)
    try:
        data = g.opener.open(url).read().decode('utf-8')
    except HTTPError as e:
        try:
            errdata = e.file.read().decode()
            error = json.loads(errdata)['error']['message']
            errmsg = 'Youtube Error %d: %s' % (e.getcode(), error)
        except:
            errmsg = str(e)

        raise GdataError(errmsg)

    return json.loads(data)


def utf8_replace(txt):
    """
    Replace unsupported characters in unicode string.

    :param txt: text to filter
    :type txt: str
    :returns: Unicode text without any characters unsupported by locale
    :rtype: str
    """
    sse = sys.stdout.encoding
    txt = txt.encode(sse, 'replace').decode(sse)
    return txt


def xenc(stuff):
    """ Replace unsupported characters. """
    if not_utf8_environment:
        return utf8_replace(stuff)
    return stuff