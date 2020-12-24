# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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