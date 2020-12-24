# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/.venv/trade/lib/python3.6/site-packages/toolware/utils/email.py
# Compiled at: 2018-08-18 10:25:00
# Size of source mod 2**32: 1481 bytes
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL')

def prepare_email_subject(content):
    """ Email subject must be text and a single line """
    subject = ''.join(content.splitlines())
    return subject


def send_multi_alt_email(subject, text_content, to_emails, html_content=None, from_email=DEFAULT_FROM_EMAIL, fail_silently=True):
    """ 
    Send a message to one more email address(s).
    With text content as primary and html content as alternative.
    """
    messenger = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
    if html_content:
        messenger.attach_alternative(html_content, 'text/html')
    try:
        messenger.send()
    except Exception as e:
        if not fail_silently:
            raise


def send_html_email(subject, html_content, to_emails, from_email=DEFAULT_FROM_EMAIL, fail_silently=True):
    """ 
    Send a message to one more email address(s).
    With html content as primary.
    """
    messenger = EmailMessage(subject, html_content, from_email, to_emails)
    messenger.content_subtype = 'html'
    try:
        messenger.send()
    except Exception as e:
        if not fail_silently:
            raise