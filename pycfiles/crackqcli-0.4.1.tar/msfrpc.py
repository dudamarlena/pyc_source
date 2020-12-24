# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/msfrpc.py
# Compiled at: 2016-12-29 01:49:52
import msgpack, logging, requests

class Msfrpc:

    class MsfError(Exception):

        def __init__(self, msg):
            self.msg = msg

        def __str__(self):
            return repr(self.msg)

    class MsfAuthError(MsfError):

        def __init__(self, msg):
            self.msg = msg

    def __init__(self, opts=[]):
        self.host = opts.get('host') or '127.0.0.1'
        self.port = opts.get('port') or '55552'
        self.uri = opts.get('uri') or '/api/'
        self.ssl = opts.get('ssl') or False
        self.token = None
        self.headers = {'Content-type': 'binary/message-pack'}
        return

    def encode(self, data):
        return msgpack.packb(data)

    def decode(self, data):
        return msgpack.unpackb(data)

    def call(self, method, opts=[]):
        if method != 'auth.login':
            if self.token == None:
                raise self.MsfAuthError('MsfRPC: Not Authenticated')
        if method != 'auth.login':
            opts.insert(0, self.token)
        if self.ssl == True:
            url = 'https://%s:%s%s' % (self.host, self.port, self.uri)
        else:
            url = 'http://%s:%s%s' % (self.host, self.port, self.uri)
        opts.insert(0, method)
        payload = self.encode(opts)
        r = requests.post(url, data=payload, headers=self.headers)
        opts[:] = []
        return self.decode(r.content)

    def login(self, user, password):
        auth = self.call('auth.login', [user, password])
        try:
            if auth['result'] == 'success':
                self.token = auth['token']
                return True
        except:
            raise self.MsfAuthError('MsfRPC: Authentication failed')