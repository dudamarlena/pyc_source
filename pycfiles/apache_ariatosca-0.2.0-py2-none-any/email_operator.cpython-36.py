# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/email_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2803 bytes
from airflow.models import BaseOperator
from airflow.utils.email import send_email
from airflow.utils.decorators import apply_defaults

class EmailOperator(BaseOperator):
    """EmailOperator"""
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