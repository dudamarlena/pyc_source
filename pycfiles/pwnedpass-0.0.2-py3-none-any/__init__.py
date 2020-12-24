# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pwnedcheck/__init__.py
# Compiled at: 2014-01-02 10:05:39
__author__ = 'Casey Dunham'
__version__ = '0.1.3'
import urllib, urllib2, json
PWNED_API_URL = 'https://haveibeenpwned.com/api/breachedaccount/%s'

class InvalidEmail(Exception):
    pass


def check(email):
    req = urllib2.Request(PWNED_API_URL % urllib.quote(email))
    try:
        resp = urllib2.urlopen(req)
        return json.loads(resp.read())
    except urllib2.HTTPError as e:
        if e.code == 400:
            raise InvalidEmail('Email address does not appear to be a valid email')
        return []