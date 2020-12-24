# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johnny/workspaces/lazerball/src/python3.4env/lib/python3.4/site-packages/htdataredirector/publishers/httppublisher.py
# Compiled at: 2014-12-18 09:21:16
# Size of source mod 2**32: 624 bytes
from urllib.parse import urlencode
import httplib2, json

class HttpPublisher:

    def __init__(self, url):
        self.url = url
        self.headers = {'Content-Type': 'application/json', 
         'Accept': 'application/json;version=0.1'}

    def publish(self, data):
        h = httplib2.Http()
        resp, content = h.request(self.url, method='POST', body=json.dumps({'hit': data}), headers=self.headers)
        return content.decode('utf-8')