# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ipshaman/core/client.py
# Compiled at: 2020-03-11 19:26:58
# Size of source mod 2**32: 737 bytes
import requests

class Client:
    __doc__ = '\n    The ipshaman API client.\n\n    The client provides simplistic interaction with the ipshaman-server. It \n    can send requests to perform lookups on single IP addresses.\n    '

    def __init__(self, server=None):
        self.server = server or 'http://ipshaman.com/'
        self.session = requests.session()
        if not self.server.startswith('http'):
            self.server = 'http://' + self.server
        if not self.server.endswith('/'):
            self.server += '/'

    def __repr__(self):
        return f"<ipshaman {self.__class__.__name__}: {self.server}>"

    def lookup(self, ip):
        response = self.session.get(self.server + ip)
        return response.json()