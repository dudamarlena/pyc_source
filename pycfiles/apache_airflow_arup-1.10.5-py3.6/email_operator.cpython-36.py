# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/email_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2803 bytes
from airflow.models import BaseOperator
from airflow.utils.email import send_email
from airflow.utils.decorators import apply_defaults

class EmailOperator(BaseOperator):
    __doc__ = '\n    Sends an email.\n\n    :param to: list of emails to send the email to. (templated)\n    :type to: list or string (comma or semicolon delimited)\n    :param subject: subject line for the email. (templated)\n    :type subject: str\n    :param html_content: content of the email, html markup\n        is allowed. (templated)\n    :type html_content: str\n    :param files: file names to attach in email\n    :type files: list\n    :param cc: list of recipients to be added in CC field\n    :type cc: list or string (comma or semicolon delimited)\n    :param bcc: list of recipients to be added in BCC field\n    :type bcc: list or string (comma or semicolon delimited)\n    :param mime_subtype: MIME sub content type\n    :type mime_subtype: str\n    :param mime_charset: character set parameter added to the Content-Type\n        header.\n    :type mime_charset: str\n    '
    template_fields = ('to', 'subject', 'html_content')
    template_ext = ('.html', )
    ui_color = '#e6faf9'

    @apply_defaults
    def __init__(self, to, subject, html_content, files=None, cc=None, bcc=None, mime_subtype='mixed', mime_charset='us_ascii', *args, **kwargs):
        (super(EmailOperator, self).__init__)(*args, **kwargs)
        self.to = to
        self.subject = subject
        self.html_content = html_content
        self.files = files or []
        self.cc = cc
        self.bcc = bcc
        self.mime_subtype = mime_subtype
        self.mime_charset = mime_charset

    def execute(self, context):
        send_email((self.to), (self.subject), (self.html_content), files=(self.files),
          cc=(self.cc),
          bcc=(self.bcc),
          mime_subtype=(self.mime_subtype),
          mime_charset=(self.mime_charset))