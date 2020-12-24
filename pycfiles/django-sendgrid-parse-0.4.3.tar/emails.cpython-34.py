# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/GitHub/django_sendgrid_repo/django_sendgrid_parse/emails.py
# Compiled at: 2016-08-30 19:07:21
# Size of source mod 2**32: 1952 bytes
from django.conf import settings
from django.utils import six
import sendgrid
try:
    import urllib.request
except ImportError:
    import urllib2 as urllib

class TransactionalEmail(object):

    def __init__(self, subject, template_id, body, from_email=None, to=None):
        if to:
            if isinstance(to, six.string_types):
                raise TypeError('"to" argument must be a list or tuple')
            self.to = list(to)
        if body:
            if not isinstance(body, dict):
                raise TypeError('"body" argument must be a dictionary')
            self.body = body
        self.from_email = from_email or settings.DEFAULT_FROM_EMAIL
        self.subject = subject
        self.template_id = template_id

    def recipients(self):
        return self.to

    def send(self):
        sg = sendgrid.SendGridAPIClient(apikey=settings.DJANGO_SENDGRID_PARSE_API)
        data = {'personalizations': [
                              {'to': [{'email': mail} for mail in self.to], 
                               'substitutions': self.body, 
                               'subject': self.subject}], 
         'from': {'email': self.from_email}, 
         'template_id': self.template_id}
        try:
            response = sg.client.mail.send.post(request_body=data)
        except urllib.HTTPError as e:
            print(e.read())