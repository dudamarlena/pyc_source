# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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