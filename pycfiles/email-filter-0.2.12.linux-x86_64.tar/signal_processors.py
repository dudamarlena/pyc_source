# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/email_filter/signal_processors.py
# Compiled at: 2014-07-02 04:15:08
import smtplib
from django.conf import settings
from email_filter.models import EmailRedirect, get_name_from_email

def notify_unknown_user(sender, instance, original_msg, mail_sender_email, send_email, smtp_sendmail, **kwargs):
    smtp_server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    email_from = 'noreply%s' % EmailRedirect.get_server_email_domain()
    msg_format = 'To: {sender}\nFrom: {email_from}\nSubject: undelivered mail \n\nUser with username {username} not exists! \n\n'
    sender = sender_email or original_msg['From']
    username_to = get_name_from_email(instance.recipient)
    msg = msg_format.format(sender=sender, email_from=email_from, username=username_to)
    smtp_server.sendmail(email_from, sender, msg)
    smtp_server.quit()