# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gamerocket/util/http_strategy/pycurl_strategy.py
# Compiled at: 2013-08-30 11:10:43
import StringIO
try:
    import pycurl
except ImportError:
    pass

class PycurlStrategy(object):

    def __init__(self, config, environment):
        self.config = config
        self.environment = environment

    def http_do(self, http_verb, path, headers, request_body):
        curl = pycurl.Curl()
        response = StringIO.StringIO()
        if self.environment.ssl_certificate:
            curl.setopt(pycurl.CAINFO, self.environment.ssl_certificate)
        curl.setopt(pycurl.SSL_VERIFYPEER, 1)
        curl.setopt(pycurl.SSL_VERIFYPEER, 2)
        curl.setopt(pycurl.URL, str(path))
        curl.setopt(pycurl.ENCODING, 'gzip')
        curl.setopt(pycurl.WRITEFUNCTION, response.write)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.HTTPHEADER, self._format_headers(headers))
        self._set_request_method_and_body(curl, http_verb, request_body)
        curl.perform()
        status = curl.getinfo(pycurl.HTTP_CODE)
        response = response.getvalue()
        return [status, response]

    def _set_request_method_and_body(self, curl, method, body):
        if method == 'GET':
            curl.setopt(pycurl.HTTPGET, 1)
        elif method == 'POST':
            curl.setopt(pycurl.POST, 1)
            curl.setopt(pycurl.POSTFIELDSIZE, len(body))
        elif method == 'PUT':
            curl.setopt(pycurl.PUT, 1)
            curl.setopt(pycurl.INFILESIZE, len(body))
        elif method == 'DELETE':
            curl.setopt(curl.CUSTOMREQUEST, 'DELETE')
        if body:
            curl.setopt(pycurl.READFUNCTION, StringIO.StringIO(body).read)

    def _format_headers(self, headers):
        return [ key + ': ' + value for key, value in headers.iteritems() ]