# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/mail.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 5615 bytes
from __future__ import print_function, unicode_literals
import six, smtplib, sys
from mediagoblin import mg_globals, messages
from mediagoblin._compat import MIMEText
from mediagoblin.tools import common
EMAIL_TEST_INBOX = []
EMAIL_TEST_MBOX_INBOX = []

class FakeMhost(object):
    __doc__ = '\n    Just a fake mail host so we can capture and test messages\n    from send_email\n    '

    def login(self, *args, **kwargs):
        pass

    def sendmail(self, from_addr, to_addrs, message):
        global EMAIL_TEST_MBOX_INBOX
        EMAIL_TEST_MBOX_INBOX.append({'from': from_addr,  'to': to_addrs, 
         'message': message})

    def starttls(self):
        raise smtplib.SMTPException('No STARTTLS here')


def _clear_test_inboxes():
    global EMAIL_TEST_INBOX
    global EMAIL_TEST_MBOX_INBOX
    EMAIL_TEST_INBOX = []
    EMAIL_TEST_MBOX_INBOX = []


def send_email(from_addr, to_addrs, subject, message_body):
    """
    Simple email sending wrapper, use this so we can capture messages
    for unit testing purposes.

    Args:
     - from_addr: address you're sending the email from
     - to_addrs: list of recipient email addresses
     - subject: subject of the email
     - message_body: email body text
    """
    if common.TESTS_ENABLED or mg_globals.app_config['email_debug_mode']:
        mhost = FakeMhost()
    else:
        if not mg_globals.app_config['email_debug_mode']:
            if mg_globals.app_config['email_smtp_use_ssl']:
                smtp_init = smtplib.SMTP_SSL
            else:
                smtp_init = smtplib.SMTP
            mhost = smtp_init(mg_globals.app_config['email_smtp_host'], mg_globals.app_config['email_smtp_port'])
            if not mg_globals.app_config['email_smtp_host']:
                mhost.connect()
            try:
                mhost.starttls()
            except smtplib.SMTPException:
                if mg_globals.app_config['email_smtp_force_starttls']:
                    six.reraise(*sys.exc_info())

        if not common.TESTS_ENABLED:
            if mg_globals.app_config['email_smtp_user'] or mg_globals.app_config['email_smtp_pass']:
                mhost.login(mg_globals.app_config['email_smtp_user'], mg_globals.app_config['email_smtp_pass'])
        message = MIMEText(message_body.encode('utf-8'), 'plain', 'utf-8')
        message['Subject'] = subject
        message['From'] = from_addr
        message['To'] = ', '.join(to_addrs)
        if common.TESTS_ENABLED:
            EMAIL_TEST_INBOX.append(message)
        elif mg_globals.app_config['email_debug_mode']:
            print('===== Email =====')
            print('From address: %s' % message['From'])
            print('To addresses: %s' % message['To'])
            print('Subject: %s' % message['Subject'])
            print('-- Body: --')
            print(message_body)
    return mhost.sendmail(from_addr, to_addrs, message.as_string())


def normalize_email(email):
    """return case sensitive part, lower case domain name

    :returns: None in case of broken email addresses"""
    try:
        em_user, em_dom = email.split('@', 1)
    except ValueError:
        return

    email = '@'.join((em_user, em_dom.lower()))
    return email


def email_debug_message(request):
    """
    If the server is running in email debug mode (which is
    the current default), give a debug message to the user
    so that they have an idea where to find their email.
    """
    if mg_globals.app_config['email_debug_mode']:
        messages.add_message(request, messages.DEBUG, 'This instance is running in email debug mode. The email will be on the console of the server process.')