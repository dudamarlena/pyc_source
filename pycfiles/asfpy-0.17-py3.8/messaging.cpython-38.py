# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asfpy/messaging.py
# Compiled at: 2020-04-19 18:58:17
# Size of source mod 2**32: 3328 bytes
"""
This is the standardized email library for sending emails.
It handles encoding options and required metadata,
as well as defaulting where bits are missing.

It also contains hipchat and stride integrations
"""
import email.utils, email.header, smtplib

def uniaddr(addr):
    """ Unicode-format an email address """
    bits = email.utils.parseaddr(addr)
    return email.utils.formataddr((email.header.Header(bits[0], 'utf-8').encode(), bits[1]))


def mail(host='mail.apache.org:2025', sender='Apache Infrastructure <users@infra.apache.org>', recipient=None, recipients=None, subject='No subject', message=None, messageid=None, headers=None):
    if not messageid:
        messageid = email.utils.make_msgid('asfpy')
    date = email.utils.formatdate()
    recipients = recipient or recipients
    if not recipients:
        raise Exception("No recipients specified for email, can't send!")
    if isinstance(recipients, str):
        recipients = [
         recipients]
    if isinstance(sender, bytes):
        sender = sender.decode('utf-8', errors='replace')
    if isinstance(message, bytes):
        message = message.decode('utf-8', errors='replace')
    for i, rec in enumerate(recipients):
        if isinstance(rec, bytes):
            rec = rec.decode('utf-8', errors='replace')
            recipients[i] = rec
        subject_encoded = email.header.Header(subject, 'utf-8').encode()
        sender_encoded = uniaddr(sender)
        recipient_encoded = ', '.join([uniaddr(x) for x in recipients])
        extra = ''
        if headers:
            for key, val in headers.items():
                extra += '%s: %s\n' % (key, val)

    else:
        extra += '\n'
        if not message:
            raise Exception('No message body provided!')
        msg = 'From: %s\nTo: %s\nSubject: %s\nMessage-ID: %s\nDate: %s\nContent-Type: text/plain; charset=utf-8\nContent-Transfer-Encoding: 8bit\n%s\n%s\n' % (
         sender_encoded, recipient_encoded, subject_encoded, messageid, date, extra, message)
        msg = msg.encode('utf-8', errors='replace')
        smtp_object = smtplib.SMTP(host)
        smtp_object.sendmail(sender, recipients, msg)