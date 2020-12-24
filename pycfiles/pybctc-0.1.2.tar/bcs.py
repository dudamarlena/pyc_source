# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\yanglin\test/..\pybcs\bcs.py
# Compiled at: 2012-03-18 20:38:22
import urllib, re, sys, os, time, hmac, base64, hashlib, commands, logging
try:
    import json
except:
    import simplejson as json

import common
from bucket import Bucket
from httpc import *

class BCS:

    def __init__(self, host, ak, sk, httpclient_class):
        if host.endswith('/'):
            host = host[:-1]
        self.host = host
        self.ak = ak
        self.sk = sk
        if not httpclient_class:
            httpclient_class = select_best_httpc()
        self.c = httpclient_class()
        self.get_url = self.sign('GET', '', '/')

    @network
    def list_buckets(self):
        rst = self.c.get(self.get_url)
        text = rst['body']
        j = json.loads(text)
        return [ self.bucket(b['bucket_name']) for b in j ]

    def bucket(self, bucket_name):
        b = Bucket(self, bucket_name)
        return b

    def sign(self, M, B, O, T=None, I=None, S=None):
        flag = ''
        s = ''
        if M:
            flag += 'M'
            s += 'Method=%s\n' % M
        if B:
            flag += 'B'
            s += 'Bucket=%s\n' % B
        if O:
            flag += 'O'
            s += 'Object=%s\n' % O
        if T:
            flag += 'T'
            s += 'Time=%s\n' % T
        if I:
            flag += 'I'
            s += 'Ip=%s\n' % I
        if S:
            flag += 'S'
            s += 'Size=%s\n' % S
        s = ('\n').join([flag, s])

        def h(sk, body):
            digest = hmac.new(sk, body, hashlib.sha1).digest()
            t = base64.encodestring(digest)
            return urllib.quote(t.strip())

        sign = h(self.sk, s)
        return '%s/%s%s?sign=%s:%s:%s' % (
         self.host, B, O, flag, self.ak, sign)