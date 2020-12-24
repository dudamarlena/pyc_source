# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/movister/env/src/django-email-html/email_html/mail.py
# Compiled at: 2015-10-13 09:05:53
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
import re
from .templatetags.email_html import html2text, extract_urllinks

def send_mail(subject, message=None, from_email=None, recipient_list=None, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None):
    """
    Replacement for monkey-patching Django's send_mail function for sending html email by default
    """
    if recipient_list is None:
        raise ValueError('You must specified recipient_list attribute')
    bcc_addrs = list(getattr(settings, 'EMAIL_BCC_ADDRESSES', []))
    admins = [ a[1] for a in settings.ADMINS ] if getattr(settings, 'EMAIL_ADMIN_DUPLICATE', False) else []
    bcc_addrs.extend(admins)
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    subject = settings.EMAIL_SUBJECT_PREFIX + subject.replace('\n', '')
    message = html_message or message
    if message.find('<html') != -1:
        message_plaintext = html2text(extract_urllinks(message))
        message_plaintext = re.sub('http://\\n', 'http://', message_plaintext)
        if 'mailer' in settings.INSTALLED_APPS:
            from mailer import send_html_mail
            return send_html_mail(subject=subject, message=message_plaintext, message_html=message, from_email=from_email, recipient_list=recipient_list, bcc=bcc_addrs, fail_silently=fail_silently, auth_user=auth_user, auth_password=auth_password)
        email = EmailMultiAlternatives(subject=subject, body=message_plaintext, from_email=from_email, to=recipient_list, bcc=bcc_addrs, connection=connection)
        email.attach_alternative(message, 'text/html')
        return email.send(fail_silently=fail_silently)
    else:
        email = EmailMessage(subject, message, from_email, recipient_list, bcc_addrs)
        email.send(fail_silently=fail_silently)
    return