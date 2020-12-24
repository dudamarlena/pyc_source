# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pswinpy\request.py
# Compiled at: 2011-05-04 08:09:08
from datetime import datetime

class Request(object):

    def __init__(self, username, password):
        self.user = username
        self.password = password
        self.messages = []

    def addMessage(self, to, text, sender='', TTL='', tariff='', serviceCode='', deliveryTime=''):
        self.messages.append({'receiver': to, 'text': text, 
           'sender': sender, 
           'TTL': TTL, 
           'tariff': tariff, 
           'serviceCode': serviceCode, 
           'deliveryTime': deliveryTime})

    def xml(self):
        return '<?xml version="1.0"?>\r\n' + '<SESSION><CLIENT>%s</CLIENT><PW>%s</PW><MSGLST>%s</MSGLST></SESSION>' % (
         self.user, self.password, self.messageListXml())

    def messageListXml(self):
        return reduce(lambda x, y: x + y, map(xmlForSingleMessage, self.messages), '')


def xmlForSingleMessage(message):
    return tag('MSG', tag('ID', '1') + tag('TEXT', message['text']) + tag('RCV', message['receiver']) + tag('SND', message['sender']) + tag('TTL', message['TTL']) + tag('TARIFF', message['tariff']) + tag('SERVICECODE', message['serviceCode']) + tag('DELIVERYTIME', message['deliveryTime']))


def tag(tagName, content):
    if isinstance(content, datetime):
        content = content.strftime('%Y%m%d%H%M')
    else:
        content = str(content)
    if content:
        return '<' + tagName + '>' + content + '</' + tagName + '>'
    return ''