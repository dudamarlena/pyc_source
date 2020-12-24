# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/python_grabber/yahoo.py
# Compiled at: 2009-12-05 18:42:15
from base import BaseGrabber, InvalidLogin

class YahooGrabber(BaseGrabber):
    LoginUrl = 'https://login.yahoo.com/config/login?'
    ExportUrl = 'http://address.yahoo.com/yab/us/Yahoo_ab.csv'

    def __init__(self, username, password):
        self.params = {'login': username, 'passwd': password}
        super(YahooGrabber, self).__init__()

    def grab(self):
        self.get_page(self.LoginUrl, self.params)
        html = self.get_page(self.ExportUrl)
        contacts = self.get_contacts(html)
        if 'free2rhyme@yahoo.com' in contacts:
            raise InvalidLogin, 'User or password incorrect'
        return contacts