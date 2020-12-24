# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pswinpy\api.py
# Compiled at: 2011-05-04 09:39:42
from pswinpy.request import Request
from pswinpy.http_sender import HttpSender

class API(object):

    def __init__(self, username, password):
        self.request = Request(username, password)

    def sendSms(self, to=None, text=None, sender='', TTL='', tariff='', serviceCode='', deliveryTime=''):
        if to and text:
            self.request.addMessage(to, text, sender, TTL, tariff, serviceCode, deliveryTime)
        sender = HttpSender()
        result = sender.send(self.request)
        return result