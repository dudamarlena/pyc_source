# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/pastylegs/Dropbox/GitHub/python-parsnip/parsnip/operators/three.py
# Compiled at: 2012-05-02 05:37:21
from parsnip import BaseWebtexter, exceptions
import re, lxml.html
from lxml import etree
from urllib import urlencode
REGEX_1 = re.compile('if\\(\\(sendok\\)&&\\((.*?)==0\\)\\)')
REGEX_2 = re.compile('You can send  (.*?) more messages')

class Three(BaseWebtexter):
    NETWORK_NAME = 'Three'
    LOGIN_POST = 'http://webtext.three.ie/processLogin.jsp'
    LOGOUT_POST = 'http://webtext.three.ie/login'
    SEND_POST = 'http://webtext.three.ie/processSendMessage.jsp'
    SEND_PAGE = 'http://webtext.three.ie/send.jsp'
    MAX_LENGTH = 160

    @classmethod
    def is_operator(cls, n):
        return n == cls.NETWORK_NAME

    def login(self):
        response = self.connection.send(self.LOGIN_POST, data={'mobile': self.phone_number, 
           'pin': self.pin, 
           'serviceId': '19088', 
           'originCountryPrefix': '353'})
        html = lxml.html.fromstring(response)
        loginpage = html.find_class('LoginHeader')
        if len(loginpage) > 0:
            for s in html.find_class('leftdiv'):
                if 'Invalid login. Please try again.' in s.text_content():
                    raise exceptions.LoginError(msg='Invalid Login Username or Pin', webtexter=self)

            raise exceptions.LoginError('Unknown Login Error', webtexter=self)
        return True

    def _do_send(self, message_chunk, recipients_chunk):
        response = self.connection.send(self.SEND_PAGE)
        tree = lxml.html.fromstring(response)
        loginpage = tree.get_element_by_id('mobilenumber', None)
        if loginpage is not None:
            raise exceptions.LoginError('Tried to send webtext while not logged in', webtexter=self)
        response = None
        for recipient in recipients_chunk:
            response = self.connection.send(self.SEND_POST, data={'command': 'send', 
               'group': '', 
               'Msg1': message_chunk, 
               'grpSTR': '', 
               'ConSTR': '', 
               'country': '353', 
               'NumMessages': '', 
               'msisdn': recipient})

        if 'Message Sent!' in response:
            return True
        else:
            if 'This is a duplicate message ' in response:
                raise exceptions.MessageSendingError('Three requires that you wait 2 minutes between sending messages', webtexter=self)
            raise exceptions.MessageSendingError('Error After Message Sent', webtexter=self)
            return

    def get_remaining_webtexts(self):
        response = self.connection.send(self.SEND_PAGE)
        tree = lxml.html.fromstring(response)
        loginpage = tree.get_element_by_id('mobilenumber', None)
        if loginpage is not None:
            raise exceptions.LoginError('Tried to send webtext while not logged in', webtexter=self)
        match = REGEX_1.search(tree.text_content())
        return int(match.group(1))