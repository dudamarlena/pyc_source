# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/maluki/blog/django_blog/blog_project/contact/emails.py
# Compiled at: 2019-07-25 09:20:18
# Size of source mod 2**32: 637 bytes
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_contact_email(email, message):
    c = {'email':email, 
     'message':message}
    email_subject = render_to_string('contact/email/contact_email_subject.txt', c).replace('\n', '')
    email_body = render_to_string('contact/email/contact_email_body.txt', c)
    email = EmailMessage(email_subject,
      email_body, email, [
     settings.DEFAULT_FROM_EMAIL],
      [], headers={'Reply-To': email})
    return email.send(fail_silently=False)