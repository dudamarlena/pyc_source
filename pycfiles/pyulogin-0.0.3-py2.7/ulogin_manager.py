# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyulogin/ulogin_manager.py
# Compiled at: 2014-03-05 20:44:28
"""
Copyright (c)2014 Gurov Dmitri 

See the file license.txt for copying permission.

This file contains class of UloginManager object,which return UloginUser with information about user
UloginManager execute query to ulogin service and processing data from service. 
   
"""
import json, urllib, urllib2
from user import UloginUser
import ulogin

class UloginManager:

    def __init__(self, request):
        server = request.environ['HTTP_HOST']
        token = request.form['token']
        self.ulogdata = {'token': token, 'host': server}
        self.setUserData()

    def setUserData(self):
        ulogdata = urllib.urlencode(self.ulogdata)
        self.ulogin = urllib2.urlopen(ulogin.url + '?' + ulogdata)
        self.ulogin = self.ulogin.read()
        decoder = json.JSONDecoder()
        self.ulogin = decoder.decode(self.ulogin)
        if 'error' in self.ulogin:
            if 'host is not' in ulogin['error']:
                raise ulogin.UloginError['host is not XXX']
            else:
                raise ulogin.UloginError[ulogin['error']]

    def getUser(self):
        return UloginUser(self.ulogin)