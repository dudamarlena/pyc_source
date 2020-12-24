# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/geofluent/geofluent.py
# Compiled at: 2017-04-18 03:37:30
import requests, time, calendar, jwt, base64, html
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

class GeoFluent(object):
    EXPIRATION_TIME = 8

    def __init__(self, key, secret, html_unescape=False, base='https://api.geofluent.com/Translation', version=3):
        self.key = key
        self.secret = secret
        self.html_unescape = html_unescape
        self.base = base
        self.version = version
        self._generate_token()

    def _generate_token(self):
        iat = calendar.timegm(time.gmtime())
        self.expiration = iat + 28800
        claims = {'sub': self.key, 
           'iat': iat, 
           'exp': self.expiration}
        self.token = jwt.encode(claims, base64.b64decode(self.secret), algorithm='HS256').decode('UTF-8')
        self.headers = {'User-Agent': 'GeoFluent Python Client', 
           'Content-Type': 'application/json', 
           'Accept': 'application/json', 
           'Authorization': 'Bearer %s' % self.token}

    def health_check(method):

        def check_expiration(self, *args):
            if calendar.timegm(time.gmtime()) > self.expiration:
                self._generate_token()
            return method(self, *args)

        return check_expiration

    def _get(self, endpoint, params={}):
        resource = '%s/v%d/%s' % (self.base, self.version, endpoint)
        if len(params) > 0:
            encoded_params = ('&').join('%s=%s' % (k, quote_plus(v)) for k, v in params.items())
            resource = '%s?%s' % (resource, encoded_params)
        return requests.get(resource, headers=self.headers)

    @health_check
    def languages(self):
        response = self._get('Languages')
        data = response.json()
        if response.status_code is not 200:
            msg = 'Request to %s responded with status code %d: %s' % (response.url, response.status_code, data['error'])
            raise RuntimeError(msg)
        else:
            return [ (r['source']['code'], r['target']['code']) for r in data['result'] ]

    @health_check
    def translate(self, text, source, target):
        response = self._get('Translate', params={'text': text, 'from': source, 'to': target})
        data = response.json()
        if response.status_code is not 200:
            msg = 'Request to %s responded with status code %d: %s' % (response.url, response.status_code, data['error'])
            raise RuntimeError(msg)
        else:
            text = data['result'][0]['text']
            if self.html_unescape:
                return html.unescape(text)
            return text

    @health_check
    def detect_language(self, text):
        response = self._get('Detect', params={'text': text})
        data = response.json()
        if response.status_code is not 200:
            msg = 'Request to %s responded with status code %d: %s' % (response.url, response.status_code, data['error'])
            raise RuntimeError(msg)
        else:
            return data['result']