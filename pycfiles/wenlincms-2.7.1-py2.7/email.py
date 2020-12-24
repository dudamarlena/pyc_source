# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/utils/email.py
# Compiled at: 2016-05-20 23:41:38
from __future__ import unicode_literals
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template import loader, Context
from django.utils.http import int_to_base36
from future.builtins import bytes, str
from wenlincms.conf import settings
from wenlincms.conf.context_processors import settings as context_settings
from wenlincms.utils.urls import admin_url, next_url

def split_addresses(email_string_list):
    """
    Converts a string containing comma separated email addresses
    into a list of email addresses.
    """
    return [ f for f in [ s.strip() for s in email_string_list.split(b',') ] if f ]


def subject_template(template, context):
    """
    Loads and renders an email subject template, returning the
    subject string.
    """
    subject = loader.get_template(template).render(Context(context))
    return (b' ').join(subject.splitlines()).strip()


def send_mail_template(subject, template, addr_from, addr_to, context=None, attachments=None, fail_silently=None, addr_bcc=None, headers=None):
    """
    Send email rendering text and html versions for the specified
    template name using the context dictionary passed in.
    """
    if context is None:
        context = {}
    if attachments is None:
        attachments = []
    if fail_silently is None:
        fail_silently = settings.EMAIL_FAIL_SILENTLY
    context.update(context_settings())
    if isinstance(addr_to, str) or isinstance(addr_to, bytes):
        addr_to = [
         addr_to]
    if addr_bcc is not None and (isinstance(addr_bcc, str) or isinstance(addr_bcc, bytes)):
        addr_bcc = [
         addr_bcc]
    render = lambda type: loader.get_template(b'%s.%s' % (
     template, type)).render(Context(context))
    msg = EmailMultiAlternatives(subject, render(b'html'), addr_from, addr_to, addr_bcc, headers=headers)
    msg.attach_alternative(render(b'html'), b'text/html')
    for attachment in attachments:
        msg.attach(*attachment)

    msg.send(fail_silently=fail_silently)
    return


def send_verification_mail(request, user, verification_type, email_prefix=b''):
    """
    The ``verification_type`` arg is both the name of the urlpattern for
    the verification link, as well as the names of the email templates
    to use.
    """
    verify_url = reverse(verification_type, kwargs={b'uidb36': int_to_base36(user.id), b'token': default_token_generator.make_token(user)}) + b'?next=' + (next_url(request) or b'/')
    context = {b'request': request, 
       b'user': user, 
       b'verify_url': verify_url}
    subject_template_name = b'%semail/%s_subject.txt' % (email_prefix, verification_type)
    subject = subject_template(subject_template_name, context)
    send_mail_template(subject, b'%semail/%s' % (email_prefix, verification_type), settings.DEFAULT_FROM_EMAIL, user.email, context=context)


def send_approve_mail(request, user, email_prefix=b''):
    """
    Sends an email to staff, when a new user signs up
    """
    settings.use_editable()
    approval_emails = split_addresses(settings.ACCOUNTS_APPROVAL_EMAILS)
    if not approval_emails:
        return
    context = {b'request': request, b'user': user, 
       b'change_url': admin_url(user.__class__, b'change', user.id)}
    subject = subject_template(b'%semail/account_approve_subject.txt' % email_prefix, context)
    send_mail_template(subject, b'%semail/account_approve' % email_prefix, settings.DEFAULT_FROM_EMAIL, approval_emails, context=context)


def send_approved_mail(request, user, email_prefix=b''):
    """
    Sends an email to a user once their ``is_active`` status goes from
    ``False`` to ``True``
    """
    context = {b'request': request, b'user': user}
    subject = subject_template(b'%email/account_approved_subject.txt' % email_prefix, context)
    send_mail_template(subject, b'%email/account_approved' % email_prefix, settings.DEFAULT_FROM_EMAIL, user.email, context=context)