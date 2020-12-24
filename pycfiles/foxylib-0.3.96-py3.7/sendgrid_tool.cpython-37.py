# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/sendgrid/sendgrid_tool.py
# Compiled at: 2020-01-08 12:53:55
# Size of source mod 2**32: 834 bytes
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class MailConfig:

    class Field:
        FROM_EMAIL = 'from_email'
        TO_EMAILS = 'to_emails'
        SUBJECT = 'subject'
        PLAIN_TEXT_CONTENT = 'plain_text_content'
        HTML_CONTENT = 'html_content'

    F = Field


class MailTool:

    @classmethod
    def j_config2mail(cls, j_config):
        return Mail(**j_config)

    @classmethod
    def j_config2send(cls, client, j_config):
        mail = cls.j_config2mail(j_config)
        response = client.send(mail)
        return response