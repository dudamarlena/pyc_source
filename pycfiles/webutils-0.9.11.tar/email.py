# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/pjs/python-modules/webutils/djtools/email.py
# Compiled at: 2017-04-07 14:12:41
from django.conf import settings
from django.core.mail import send_mail
from django.template import Template, loader

def send_simple_email(recip, subject, context, template, from_email=None, is_template_file=True, fail_silently=False):
    if is_template_file:
        msg_template = loader.get_template(template)
    else:
        msg_template = Template(template)
    msg_dict = {'from_email': from_email or settings.DEFAULT_FROM_EMAIL, 
       'message': msg_template.render(context), 
       'recipient_list': isinstance(recip, list) and recip or [recip], 
       'subject': subject}
    send_mail(fail_silently=fail_silently, **msg_dict)