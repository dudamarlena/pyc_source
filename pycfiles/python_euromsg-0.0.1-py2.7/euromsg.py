# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/euromsg/euromsg.py
# Compiled at: 2017-07-23 13:16:03
import zeep

class EuromsgMailer(object):
    """"""
    AUTHORIZATION_URL = 'https://ws.euromsg.com/live/auth.asmx?wsdl'
    POST_URL = 'https://ws.euromsg.com/live/post.asmx?wsdl'
    username = ''
    password = ''

    def __init__(self, _username, _password, _authurl=None, _posturl=None):
        self.username = _username
        self.password = _password
        if _authurl:
            self.AUTHORIZATION_URL = _authurl
        if _posturl:
            self.POST_URL = _posturl

    def send_mail(self, from_name, from_address, replyto_address, to_name, to_address, subject, message, encoding='UTF-8'):
        client = zeep.Client(wsdl=self.AUTHORIZATION_URL)
        resp = client.service.Login(self.username, self.password)
        try:
            ticket = resp['ServiceTicket']
        except KeyError:
            raise Exception('There was an error with authentication!')

        client = zeep.Client(wsdl=self.POST_URL)
        post_resp = client.service.PostHtml(ticket, from_name, from_address, replyto_address, subject, message, encoding, to_name, to_address, None)
        if post_resp['Code'] == '00':
            return post_resp['PostID']
        else:
            raise Exception(('{}: {}').format(post_resp['Code'], post_resp['Message']))
            return