# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/imap_attachment_to_s3_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3686 bytes
from airflow.contrib.hooks.imap_hook import ImapHook
from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class ImapAttachmentToS3Operator(BaseOperator):
    __doc__ = '\n    Transfers a mail attachment from a mail server into s3 bucket.\n\n    :param imap_attachment_name: The file name of the mail attachment that you want to transfer.\n    :type imap_attachment_name: str\n    :param s3_key: The destination file name in the s3 bucket for the attachment.\n    :type s3_key: str\n    :param imap_mail_folder: The folder on the mail server to look for the attachment.\n    :type imap_mail_folder: str\n    :param imap_check_regex: If set checks the `imap_attachment_name` for a regular expression.\n    :type imap_check_regex: bool\n    :param s3_overwrite: If set overwrites the s3 key if already exists.\n    :type s3_overwrite: bool\n    :param imap_conn_id: The reference to the connection details of the mail server.\n    :type imap_conn_id: str\n    :param s3_conn_id: The reference to the s3 connection details.\n    :type s3_conn_id: str\n    '
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