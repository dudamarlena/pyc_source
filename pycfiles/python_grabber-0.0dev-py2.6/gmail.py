# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/python_grabber/gmail.py
# Compiled at: 2010-01-22 19:28:16
from base import BaseGrabber, InvalidLogin, iphone_request
from lxml.html import fromstring
from pyquery import PyQuery as pq
import csv

class GmailGrabber(BaseGrabber):
    LoginUrl = 'https://www.google.com/accounts/ServiceLoginAuth'
    ExportUrl = 'https://mail.google.com/mail/contacts/data/export?exportType=ALL&groupToExport=&out=GMAIL_CSV'

    def __init__(self, username, password):
        self.params = {'Email': username, 'Passwd': password, 'PersistentCookie': 'yes', 'signIn': 'Sign in'}
        super(GmailGrabber, self).__init__()

    def grab(self):
        html = self.get_page(self.LoginUrl)
        doc = fromstring(html)
        d = pq(doc)
        inputs = d('input')
        self.params['dsh'] = inputs[0].attrib['value']
        self.params['rmShown'] = inputs[5].attrib['value']
        self.params['GALX'] = inputs[1].attrib['value']
        a = self.get_page(self.LoginUrl, self.params)
        x = self.get_page(self.ExportUrl).decode('utf-16')
        return self.get_contacts(x)