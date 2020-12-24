# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Documents/LibraryApp/LibAppDjango/feedback/emails.py
# Compiled at: 2019-07-26 09:44:51
# Size of source mod 2**32: 1124 bytes
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_feedback_email(email, message):
    c = {'email':email, 
     'message':message}
    email_subject = render_to_string('feedback/email/feedback_email_subject.html', c).replace('\n', '')
    email_body = render_to_string('feedback/email/feedback_email_body.html', c)
    email = EmailMessage(email_subject,
      email_body, email, [
     settings.DEFAULT_FROM_EMAIL],
      [], headers={'Reply-To': email})
    return email.send(fail_silently=False)


def send_periodic_email():
    send_mail('Did you get this subject',
      'message: did you?.',
      'kevin@example.com',
      [
     'she@example.com'],
      fail_silently=False)