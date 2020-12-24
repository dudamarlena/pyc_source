# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/inviteme/utils.py
# Compiled at: 2012-05-28 15:48:21
import Queue, threading
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
mail_sent_queue = Queue.Queue()

class EmailThread(threading.Thread):

    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list)
        if self.html:
            msg.attach_alternative(self.html, 'text/html')
        msg.send(self.fail_silently)
        mail_sent_queue.put(True)


def send_mail(subject, body, from_email, recipient_list, fail_silently=False, html=None):
    EmailThread(subject, body, from_email, recipient_list, fail_silently, html).start()