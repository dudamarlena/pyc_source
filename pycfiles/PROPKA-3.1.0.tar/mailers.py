# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/propjockey/mailers.py
# Compiled at: 2017-11-22 16:02:35
import abc, requests

class Mailer(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, config):
        pass

    @abc.abstractmethod
    def send(self, message):
        pass


class NullMailer(Mailer):

    def __init__(self, config):
        pass

    def send(self, message):
        to = message['to']
        to = to if isinstance(to, list) else [to]
        if message.get('use_bcc') is True:
            to_for_bcc = message.get('to_for_bcc', message['from'])
            to, bcc = [to_for_bcc], to
        else:
            to, bcc = to, []
        return {'text': message['text'], 
           'from': message['from'], 
           'to': to, 
           'subject': message['subject'], 
           'bcc': bcc}


class Mailgun(Mailer):

    def __init__(self, config):
        self.API_KEY = config['API_KEY']
        self.BASE_URL = config['BASE_URL']

    def send(self, message):
        to = message['to']
        to = to if isinstance(to, list) else [to]
        if message.get('use_bcc') is True:
            to_for_bcc = message.get('to_for_bcc', message['from'])
            to, bcc = [to_for_bcc], to
        else:
            to, bcc = to, []
        return requests.post(self.BASE_URL + '/messages', auth=(
         'api', self.API_KEY), data={'text': message['text'], 
           'from': message['from'], 
           'to': to, 
           'subject': message['subject'], 
           'bcc': bcc})


MAILERS = {'null': NullMailer, 
   'mailgun': Mailgun}