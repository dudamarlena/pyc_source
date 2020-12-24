# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/core/account.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 3106 bytes
"""
Created on Feb 8, 2018

@author: stelios
"""
import urllib, config, logging

class Account(object):
    __doc__ = '\n    classdocs\n    '

    def __init__(self, username=None, password=None, community=None, endpoint=config.endpoint):
        self.username = username
        self.password = password
        self.community = community
        self.logged_in = False
        self.endpoint = endpoint
        if self.username != None:
            self.login(username, password, community)

    @property
    def username(self):
        return self._Account__username

    @username.setter
    def username(self, username):
        self._Account__username = username

    @property
    def password(self):
        return self._Account__password

    @password.setter
    def password(self, password):
        self._Account__password = password

    @property
    def community(self):
        return self._Account__community

    @community.setter
    def community(self, community):
        self._Account__community = community

    @property
    def logged_in(self):
        return self._Account__logged_in

    @logged_in.setter
    def logged_in(self, logged_in):
        self._Account__logged_in = logged_in

    def login(self, username=None, password=None, community=None):
        try:
            req = urllib.request.Request((self.endpoint + config.system_info), headers=(self.get_identity_as_headers()))
            with urllib.request.urlopen(req) as (response):
                response.read().decode('utf-8')
                if response.getcode() == 200:
                    self.logged_in = True
                    self.username = username
                    self.password = password
                    self.community = community
        except Exception as e:
            logging.exception(e)

    def get_identity_as_headers(self):
        """
        Get a Dictionary of values representing a Identity, to be used for Firethorn Requests
        """
        if self.username != None:
            if self.password != None:
                if self.username != None:
                    if self.community != None:
                        return {'Accept':'application/json', 
                         'firethorn.auth.community':self.community,  'firethorn.auth.username':self.username,  'firethorn.auth.password':self.password}
            if self.community == None:
                return {'Accept':'application/json',  'firethorn.auth.username':self.username,  'firethorn.auth.password':self.password}
            else:
                if self.password == None:
                    return {'Accept':'application/json', 
                     'firethorn.auth.community':self.community,  'firethorn.auth.username':self.username}
                return {'Accept':'application/json',  'firethorn.auth.username':self.username}
        else:
            return {'Accept': 'application/json'}

    def __str__(self):
        """ Print User as string
        """
        return 'Username: %s ' % self.username