# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/wsgihatenaauth/__init__.py
# Compiled at: 2007-06-23 02:31:35
""" WSGI middleware for Hatena Auth
"""
import md5, base64, re, urllib, urllib2, simplejson
from Crypto.Cipher import AES
certUrl = 'http://auth.hatena.ne.jp/auth?api_key=%s&api_sig=%s'
authUrl = 'http://auth.hatena.ne.jp/api/auth.json?api_key=%s&cert=%s&api_sig=%s'

class HatenaAuthHandler(object):

    def __init__(self, apiKey, secret):
        self.app = None
        self.apiKey = apiKey
        self.secret = secret
        self.certedUrl = '/auth'
        self.authenvkey = 'REMOTE_USER'
        return

    def redirectToHatenaAuth(self, environment, start_response):
        start_response('302 Moved Temporarily', [
         (
          'Location', self.getLoginUrl())])
        return []

    def parseCookies(self, s):
        cookies = {}
        for x in [ t.strip() for t in s.replace(',', ':').split(':') ]:
            if x == '':
                continue
            (key, value) = x.split('=', 1)
            cookies[key] = value

        return cookies

    def __call__(self, app):
        self.app = app
        return self.handle

    def handle(self, environment, start_response):
        cookies = self.parseCookies(environment.get('HTTP_COOKIE', ''))
        if 'hatena_auth' not in cookies:
            if not self.isCerted(environment):
                return self.redirectToHatenaAuth(environment, start_response)
            cert = self.getCert(environment)
            auth = self.getCertedUser(cert)
            if auth['has_error']:
                start_response('500 Internal Error', [])
                return ['500 Internal Error',
                 'hatena auth errored',
                 auth['error']['message']]
            authname = 'hatena:%s' % auth['user']['name']
            environment[self.authenvkey] = auth
            serialized = self.serializeHatenaAuth(authname + ' ' * (32 - len(authname)))
            start_response('302 Moved Temporarily', [
             (
              'Set-Cookie',
              'hatena_auth=%s' % serialized),
             ('Location', '/')])
            return [
             simplejson.dumps(auth)]
        else:
            auth = self.deserializeHatenaAuth(cookies['hatena_auth'])
            environment[self.authenvkey] = auth
        return self.app(environment, start_response)

    def serializeHatenaAuth(self, auth):
        obj = AES.new('abcdefghijklmnop', AES.MODE_CBC)
        return base64.b64encode(obj.encrypt(auth + ' ' * (32 - len(auth))))

    def deserializeHatenaAuth(self, auth):
        obj = AES.new('abcdefghijklmnop', AES.MODE_CBC)
        return obj.decrypt(base64.b64decode(auth)).strip()

    def getCertedUser(self, cert):
        apiSig = self.createApiSignature(self.secret, {'api_key': self.apiKey, 'cert': cert})
        apiKey = self.apiKey
        url = authUrl % (apiKey, cert, apiSig)
        print url
        res = urllib2.urlopen(url)
        auth = simplejson.loads(res.read())
        return auth

    def createApiSignature(self, secret, params):
        paramKeys = params.keys()
        paramKeys.sort()
        paramStrs = []
        for key in paramKeys:
            paramStrs.append(key)
            paramStrs.append(params[key])

        print secret + ('').join(paramStrs)
        m = md5.new()
        m.update(secret + ('').join(paramStrs))
        sig = m.hexdigest()
        return sig

    def getLoginUrl(self):
        apiKey = self.apiKey
        secret = self.secret
        api_sig = self.createApiSignature(secret, {'api_key': apiKey})
        return certUrl % (apiKey, api_sig)

    def isCerted(self, environment):
        print environment['PATH_INFO']
        return environment['PATH_INFO'] == self.certedUrl and environment['QUERY_STRING'].startswith('cert=')

    def getCert(self, environment):
        r = re.compile('^cert=(?P<cert>\\w+)')
        m = r.match(environment['QUERY_STRING'])
        if m is None:
            return
        return m.group('cert')