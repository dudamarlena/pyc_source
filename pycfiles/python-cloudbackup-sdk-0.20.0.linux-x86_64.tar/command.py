# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/cloudbackup/common/command.py
# Compiled at: 2017-05-12 15:59:18
"""
Rackspace Cloud Backup Command API
"""

class Command(object):
    """
    Base class for defining HTTP REST API calls
    """

    def __init__(self, sslenabled, apihost, uripath):
        """
        Initialize the Command Object
          sslenabled - True if using HTTPS; otherwise False
          apihost - server to use for API calls
          uripath - HTTP(S) Path for the REST API being defined
        """
        self.body = {}
        self.headers = {}
        self.headers['X-RCBU-Integration-User-Agent'] = 'RCBU-Integration-Tests/1.0'
        self.headers['User-Agent'] = self.headers['X-RCBU-Integration-User-Agent']
        self.uri = ''
        self.apihost = apihost
        self.__ReInit(sslenabled, uripath)

    @property
    def ApiHost(self):
        """API Host"""
        return self.apihost

    @property
    def Body(self):
        """HTTP Message Body Data"""
        return self.body

    @property
    def Headers(self):
        """HTTP Message Header Data"""
        return self.headers

    @property
    def Uri(self):
        """HTTP URI"""
        return self.uri

    def ReInit(self, sslenabled, uripath):
        """
        Reinitialize the HTTP URI with the new specification
        Useful for objects that provide access to multiple HTTP REST API calls
        """
        self.body = None
        self.headers = {}
        self.headers['Content-Type'] = 'application/json; charset=utf-8'
        if sslenabled:
            self.uri = 'https://' + self.apihost + uripath
        else:
            self.uri = 'http://' + self.apihost + uripath
        return

    __ReInit = ReInit