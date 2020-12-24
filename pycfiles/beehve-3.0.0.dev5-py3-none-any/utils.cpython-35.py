# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/devel/cfm/beehve/beehve/apps/honey/utils.py
# Compiled at: 2016-08-07 13:07:33
# Size of source mod 2**32: 572 bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_email(request, recpts, subject, text_tmpl, context=None, html_tmpl=None):
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@beehve.io')
    text_content = render_to_string(text_tmpl, context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, recpts)
    if html_tmpl:
        html_content = render_to_string(html_tmpl)
        msg.attach_alternative(html_content, 'text/html')
    msg.send()