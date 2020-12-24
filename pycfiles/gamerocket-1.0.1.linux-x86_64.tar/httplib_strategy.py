# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gamerocket/util/http_strategy/httplib_strategy.py
# Compiled at: 2013-08-09 04:06:51
import httplib

class HttplibStrategy(object):

    def __init__(self, config, environment):
        self.config = config
        self.environment = environment

    def http_do(self, http_verb, path, headers, request_body):
        if self.environment.is_ssl:
            conn = httplib.HTTPSConnection(self.environment.server, self.environment.port)
        else:
            conn = httplib.HTTPConnection(self.environment.server, self.environment.port)
        conn.request(http_verb, path, request_body, headers)
        response = conn.getresponse()
        status = response.status
        response_body = response.read()
        conn.close()
        return [status, response_body]