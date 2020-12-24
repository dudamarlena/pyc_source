# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/columnclient/client.py
# Compiled at: 2017-08-21 17:07:37
import urlparse, requests
from columnclient import credentials
from columnclient import runs

class Client(object):

    def __init__(self, **kwargs):
        self.session = requests.session()
        protocol = kwargs.get('protocol', 'http')
        netloc = '%s:%d' % (kwargs.get('hostname', '127.0.0.1'),
         kwargs.get('port', 48620))
        self.base_url = urlparse.urlunparse((protocol, netloc, '', '', '', ''))
        self.credentials = credentials.CredentialsManager(self.session, self.base_url)
        self.runs = runs.RunManager(self.session, self.base_url)