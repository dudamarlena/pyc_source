# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_support_page/handlers/mail_handler.py
# Compiled at: 2018-06-05 20:58:24
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

def mail_handler(subject, body, from_name, from_email, data, files, fail_silently, request):
    send_to = getattr(settings, 'DJANGO_SUPPORT_EMAIL_TO', None)
    if not send_to:
        raise Exception('Please add DJANGO_SUPPORT_EMAIL_TO to your settings.py,\n                 It should contain a list of email addresses to send support\n                 email to.')
    textemail = get_template('django_support_page/emails/email.txt')
    htmlemail = get_template('django_support_page/emails/email_html.txt')
    data = [ (k, data[k]) for k in sorted(data.keys()) ]
    context = Context(dict(data=data, body=body, from_name=from_name, from_email=from_email))
    text_content = textemail.render(context)
    html_content = htmlemail.render(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, send_to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    return