# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/pjs/python-modules/webutils/djtools/paypalipn.py
# Compiled at: 2016-05-17 14:52:55
"""
Class for accepting PayPal's Instant Payment Notification messages in a
Django application (or Django-on-App-Engine):

Original snippet found here:

http://www.djangosnippets.org/snippets/969/

I've altered it to fit my own personal needs.
"""
import urllib
from django.http import HttpResponse
from django.utils.encoding import smart_str

class Endpoint(object):
    default_response_text = 'Nothing to see here'
    verify_url = 'https://www.paypal.com/cgi-bin/webscr'

    def do_post(self, url, data):
        return urllib.urlopen(url, data).read()

    def verify(self, request):
        raw_post = request.body
        raw_post += '&cmd=_notify-validate'
        return self.do_post(self.verify_url, raw_post) == 'VERIFIED'

    def default_response(self):
        return HttpResponse(self.default_response_text)

    def __call__(self, request):
        r = None
        if request.method == 'POST':
            data = dict(request.POST.items())
            if self.verify(request):
                r = self.process(data)
            else:
                r = self.process_invalid(data)
        if r:
            return r
        else:
            return self.default_response()
            return

    def process(self, data):
        pass

    def process_invalid(self, data):
        pass