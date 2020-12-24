# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/imap_attachment_to_s3_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3686 bytes
from airflow.contrib.hooks.imap_hook import ImapHook
from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class ImapAttachmentToS3Operator(BaseOperator):
    """ImapAttachmentToS3Operator"""
    template_fields = ('imap_attachment_name', 's3_key')

    @apply_defaults
    def __init__(self, imap_attachment_name, s3_key, imap_mail_folder='INBOX', imap_check_regex=False, s3_overwrite=False, imap_conn_id='imap_default', s3_conn_id='aws_default', *args, **kwargs):
        (super(ImapAttachmentToS3Operator, self).__init__)(*args, **kwargs)
        self.imap_attachment_name = imap_attachment_name
        self.s3_key = s3_key
        self.imap_mail_folder = imap_mail_folder
        self.imap_check_regex = imap_check_regex
        self.s3_overwrite = s3_overwrite
        self.imap_conn_id = imap_conn_id
        self.s3_conn_id = s3_conn_id

    def execute(self, context):
        """
        This function executes the transfer from the email server (via imap) into s3.

        :param context: The context while executing.
        :type context: dict
        """
        self.log.info('Transferring mail attachment %s from mail server via imap to s3 key %s...', self.imap_attachment_name, self.s3_key)
        with ImapHook(imap_conn_id=(self.imap_conn_id)) as (imap_hook):
            imap_mail_attachments = imap_hook.retrieve_mail_attachments(name=(self.imap_attachment_name),
              mail_folder=(self.imap_mail_folder),
              check_regex=(self.imap_check_regex),
              latest_only=True)
        s3_hook = S3Hook(aws_conn_id=(self.s3_conn_id))
        s3_hook.load_bytes(bytes_data=(imap_mail_attachments[0][1]), key=(self.s3_key),
          replace=(self.s3_overwrite))