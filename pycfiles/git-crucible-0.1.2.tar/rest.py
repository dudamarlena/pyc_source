# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/joshbraegger/bc/git-crucible/crucible/rest.py
# Compiled at: 2012-03-23 23:13:39
import urllib2, base64

def request(url, method, body=None, username=None, password=None):
    headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}
    if username:
        headers['Authorization'] = 'Basic %s' % base64.encodestring('%s:%s' % (username, password))[:-1]
    req = urllib2.Request(url=url, data=body, headers=headers)
    return urllib2.urlopen(req)