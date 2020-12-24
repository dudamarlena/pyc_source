# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/imap_attachment_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3024 bytes
from airflow.contrib.hooks.imap_hook import ImapHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class ImapAttachmentSensor(BaseSensorOperator):
    """ImapAttachmentSensor"""
    template_fields = ('attachment_name', )

    @apply_defaults
    def __init__(self, attachment_name, mail_folder='INBOX', check_regex=False, conn_id='imap_default', *args, **kwargs):
        (super(ImapAttachmentSensor, self).__init__)(*args, **kwargs)
        self.attachment_name = attachment_name
        self.mail_folder = mail_folder
        self.check_regex = check_regex
        self.conn_id = conn_id

    def poke(self, context):
        """
        Pokes for a mail attachment on the mail server.

        :param context: The context that is being provided when poking.
        :type context: dict
        :return: True if attachment with the given name is present and False if not.
        :rtype: bool
        """
        self.log.info('Poking for %s', self.attachment_name)
        with ImapHook(imap_conn_id=(self.conn_id)) as (imap_hook):
            return imap_hook.has_mail_attachment(name=(self.attachment_name),
              mail_folder=(self.mail_folder),
              check_regex=(self.check_regex))