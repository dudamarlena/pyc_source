# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/email_filter/utils.py
# Compiled at: 2014-07-04 05:16:34
from email_filter.models import is_project_recipient

def is_outgoing(msg):
    recipients = [
     msg['To']]
    if recipients and ',' in recipients[0]:
        recipients = recipients[0].split(',')
    for recipient in recipients:
        if is_project_recipient(recipient.strip()):
            return False

    return True


def get_attachments(msg):
    """
    Return list of (filename, file_obj) tuples for attachments of msg.

    excepts ``msg`` to be instance of ``email.message.Message``

    """
    attaches = []
    for part in msg.walk():
        if part.get('Content-Disposition'):
            filename = part.get_filename()
            data = part.get_payload(decode=True)
            content_type = part.get_content_type()
            attaches.append((filename, data, content_type))

    return attaches