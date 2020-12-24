# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dalga/__init__.py
# Compiled at: 2013-10-04 05:43:27
import requests

class Client(object):

    def __init__(self, host='localhost', port=17500):
        self.host = host
        self.port = port
        self.session = requests.session()

    def schedule(self, routing_key, body, interval):
        url = 'http://%s:%i/schedule' % (self.host, self.port)
        data = {'routing_key': routing_key, 'body': body, 'interval': interval}
        response = self.session.post(url, data=data)
        assert response.ok

    def cancel(self, routing_key, body):
        url = 'http://%s:%i/cancel' % (self.host, self.port)
        data = {'routing_key': routing_key, 'body': body}
        response = self.session.post(url, data=data)
        assert response.ok